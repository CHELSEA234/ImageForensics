import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn as nn

from torch import linalg as LA
from torchvision.models import resnet18, ResNet18_Weights
from torchvision.models import resnet50, ResNet50_Weights
from copy import deepcopy

from .LaPlacianMs import LaPlacianMs

def rgb2gray(rgb):
    b, g, r = rgb[:, 0, :, :], rgb[:, 1, :, :], rgb[:, 2, :, :]
    gray = 0.2989*r + 0.5870*g + 0.1140*b
    gray = torch.unsqueeze(gray, 1)
    return gray

class BayarConv2d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=5, stride=1, padding=0):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.minus1 = (torch.ones(self.in_channels, self.out_channels, 1) * -1.000)

        super(BayarConv2d, self).__init__()
        # only (kernel_size ** 2 - 1) trainable params as the center element is always -1
        self.kernel = nn.Parameter(torch.rand(self.in_channels, self.out_channels, kernel_size ** 2 - 1),
                                   requires_grad=True)


    def bayarConstraint(self):
        self.kernel.data = self.kernel.permute(2, 0, 1)
        self.kernel.data = torch.div(self.kernel.data, self.kernel.data.sum(0))
        self.kernel.data = self.kernel.permute(1, 2, 0)
        ctr = self.kernel_size ** 2 // 2
        real_kernel = torch.cat((self.kernel[:, :, :ctr], self.minus1.to(self.kernel.device), self.kernel[:, :, ctr:]), dim=2)
        real_kernel = real_kernel.reshape((self.out_channels, self.in_channels, self.kernel_size, self.kernel_size))
        return real_kernel

    def forward(self, x):
        x = F.conv2d(x, self.bayarConstraint(), stride=self.stride, padding=self.padding)
        return x

class GCN_frequency(nn.Module):
	def __init__(self,
				layer_num=2,
				in_dim=64,
				feat_dim=64,
				output_dim=64,
				alpha=0.2,
				attn=True,
				self_attn=False,
				matching_matrix_list=None,
				matrix_scale=1000,
				):
		super(GCN_frequency, self).__init__()
		self.in_dim = in_dim
		self.feat_dim = feat_dim
		self.gcn_drop = nn.Dropout(0.2)
		self.W = nn.ModuleList()
		self.corr_list = nn.ModuleList()
		self.match_lst = nn.ModuleList()
		self.layer_num = layer_num
		self.output_dim = output_dim
		self.alpha = alpha
		self.attn  = attn
		self.self_attn = self_attn

		for layer in range(layer_num*3):
			input_dim = self.in_dim if layer == 0 else self.feat_dim
			self.W.append(nn.Linear(input_dim, self.feat_dim))

		self.output_mlp = nn.Linear(feat_dim, output_dim)
		self.a = nn.Parameter(torch.empty(size=(2*output_dim, 1)))
		self.attn_fuc = self._prepare_attentional_mechanism_input
		nn.init.xavier_uniform_(self.a.data, gain=1.414)
		self.leakyrelu = nn.LeakyReLU(self.alpha)
		self.activ_out = nn.Tanh()

		## GX: graph pooling layer:
		## GX: three size values: 12, 18, 43
		self.SCALE = matrix_scale
		self.corr_list.append(nn.Linear(self.feat_dim, 18))
		self.corr_list.append(nn.Linear(self.feat_dim, 43))
		self.match_lst.append(nn.Linear(self.feat_dim, 18))
		self.match_lst.append(nn.Linear(self.feat_dim, 43))
		self.corre_activ = nn.Sigmoid()
		self.match_activ = nn.Softmax(dim=1)

	def _prepare_attentional_mechanism_input(self, Wh, dot=True):
		mul_a = self.a[:self.output_dim, :]
		mul_a = torch.unsqueeze(mul_a, 0)
		mul_a = torch.cat([mul_a]*Wh.size()[0], axis=0)
		Wh1 = Wh.bmm(mul_a)

		mul_b = self.a[self.output_dim:, :]
		mul_b = torch.unsqueeze(mul_b, 0)
		mul_b = torch.cat([mul_b]*Wh.size()[0], axis=0)
		Wh2 = Wh.bmm(mul_b)            
		Wh2 = torch.permute(Wh2, (0,2,1))
		e = Wh1 + Wh2
		return e, -9e15*torch.ones_like(e)

	def _GCN_loop(self, x, adj, idx):
		'''
			the standard GCN operation for the AXW with the self-loop.
			attention is optional.
		'''
		if self.attn:
			e, zero_vec = self._prepare_attentional_mechanism_input(x)
			adj_ab = torch.where(adj > 0, e, zero_vec)
			adj    = F.softmax(adj_ab, dim=2)
		
		denom = adj.sum(2).unsqueeze(2) + 1 
		for l in range(self.layer_num):
			Ax = adj.bmm(x)
			AxW = self.W[l+idx*2](Ax)
			B   = self.W[l+idx*2](x)
			AxW = AxW + B       # self loop
			AxW = AxW / denom
			gAxW = F.relu(AxW)
			x = self.gcn_drop(gAxW) if l < self.layer_num - 1 else gAxW

		return x

	def _matching_gen(self, x, adj, idx):
		'''
		generate matching matrix, which is a soft assignment of each node at this layer to the next layer.
		generate the adjcency matrix in the next level.
		'''
		match_matrix = self.match_lst[idx](x)
		match_matrix = self.match_activ(match_matrix)
		# print(match_matrix.size())
		match_matrix = torch.permute(match_matrix, (0,2,1))
		x_coarse = match_matrix.bmm(x)
		# print(torch.sum(match_matrix[0,0,:]))	# tensor(1., device='cuda:0', grad_fn=<SumBackward0>)
		# print(match_matrix.size())			# torch.Size([32, 14, 31])
		# print(x.size())						# torch.Size([32, 31, 128])
		# import sys;sys.exit(0)

		## M^T*A*M
		## GX: you are trying to use x to estimate the correlation.
		## GX: some images will have zero correlation graphs.
		## GX: you can add some pseudo-label for the supervision first.
		## GX: in fact, to enhance the training, you can decrease the self.SCALE.
		corr_graph = self.corr_list[idx](x)
		corr_graph = self.corre_activ(self.SCALE*corr_graph)
		# print(m.size())		# torch.Size([128, 31, 14])
		tmp = adj.bmm(corr_graph)
		# print(tmp.size())		# torch.Size([128, 31, 14])
		# import sys;sys.exit(0)
		corr_graph = torch.permute(corr_graph, (0,2,1))
		# print(m.size())		# torch.Size([128, 14, 31])
		# import sys;sys.exit(0)
		adj_pred   = corr_graph.bmm(tmp)
		# print(adj_pred.size())
		# import sys;sys.exit(0)
		zero_vec = -9e15*torch.ones_like(adj_pred)
		ones_vec = torch.ones_like(adj_pred)
		adj      = torch.where(adj_pred > 0.1, ones_vec, zero_vec)

		return x_coarse, adj, match_matrix, corr_graph

	def forward(self, x, adj_0):
		x_0 = self._GCN_loop(x, adj_0, idx=0)
		
		x_1, adj_1, mm_1, cg_1 = self._matching_gen(x_0, adj_0, idx=0)
		x_1 = self._GCN_loop(x_1, adj_1, idx=1)

		x_2, adj_2, mm_2, cg_2 = self._matching_gen(x_1, adj_1, idx=1)
		x_2 = self._GCN_loop(x_2, adj_2, idx=2)

		output = self.output_mlp(x_2+x_0)
		output = self.activ_out(output)
		output_intermediate = x_1
		return output, output_intermediate, [mm_1, mm_2, cg_1, cg_2], [adj_0, adj_1, adj_2]

class CatDepth(nn.Module):
	def __init__(self):
		super(CatDepth, self).__init__()

	def forward(self, x, y):
		return torch.cat([x,y],dim=1)

class ResNetBackbone3(nn.Module):
	def __init__(self, 
				class_num, 
				task_num, 
				feat_dim=512, 
				output_dim=128,
				gcn_layer=2,
				gcn_feat_dim=128,
				matching_matrix_list=None
				):
		super(ResNetBackbone3, self).__init__()
		weights = ResNet18_Weights.DEFAULT
		resNet = resnet18(weights=weights, progress=True)
		self.lp_0 = LaPlacianMs(in_c=64,gauss_ker_size=3,scale=[2,4,8])
		self.rgb_branch = nn.Sequential(
										resNet.conv1,
										resNet.bn1,
										resNet.relu,
										resNet.maxpool
										)

		resNet_lp = resnet18(weights=weights, progress=True)
		self.lp_0 = LaPlacianMs(in_c=64,gauss_ker_size=3,scale=[2,4,8])
		self.hif_branch = nn.Sequential(
										resNet_lp.conv1,
										resNet_lp.bn1,
										resNet_lp.relu,
										self.lp_0,
										resNet_lp.maxpool
										)

		self.constrain_conv = BayarConv2d(in_channels=1, out_channels=3, padding=2)
		resNet_noise = resnet18(weights=weights, progress=True)
		self.noise_branch = nn.Sequential(
										self.constrain_conv,
										resNet_noise.conv1,
										resNet_noise.bn1,
										resNet_noise.relu,
										resNet_noise.maxpool
										)

		self.out_branch = nn.Sequential(
										resNet.layer1,
										resNet.layer2,
										resNet.layer3,
										resNet.layer4,
										resNet.avgpool,
										)
		self.concat_depth = CatDepth()
		self.pool = nn.AdaptiveAvgPool2d((1, 1))
		self.conv_1x1_merge = nn.Sequential(nn.Conv2d(128, 64,
												  kernel_size=1, stride=1,
												  bias=False,groups=2),
										nn.BatchNorm2d(64),
										nn.ReLU(inplace=True),
										nn.Dropout(p=0.2)
									   )

		# self.laplacian  = LaPlacianMs(in_c=64,gauss_ker_size=3,scale=[2,4,8])
		self.feat_dim   = feat_dim
		self.output_dim = output_dim
		self.task_num   = task_num

		# print("matching matrix list is: ", len(matching_matrix_list))
		# import sys;sys.exit(0)
		self.GCN_refine = GCN_frequency(
										layer_num=gcn_layer,
										in_dim=gcn_feat_dim,
										feat_dim=gcn_feat_dim,
										output_dim=gcn_feat_dim,
										matching_matrix_list=matching_matrix_list
										)
		for i in range(task_num):
			name = f'head_{(i+1):d}'
			setattr(self, 
					name, 
					self._make_pred_head()
					)
		self.classifier = self._make_classifier(input_dim=output_dim)
		self.classifier_real_fake = self._make_classifier(input_dim=(512+128))

	def _make_pred_head(self):
		# GX: used for the pesudo center area.
		# GX: what if two pesudo centers are close to each other?
		return nn.Sequential(
							nn.Linear(self.feat_dim, self.feat_dim),
							nn.ReLU(inplace=True),
							nn.Linear(self.feat_dim, self.output_dim)
							)

	def _make_classifier(self, input_dim, output_num=2):
		return nn.Sequential(
							nn.Linear(input_dim, input_dim),
							nn.ReLU(inplace=True),
							nn.Linear(input_dim, output_num),
							)

	def forward(self, x, adj, tsne=False):
		x_rbg = self.rgb_branch(x)
		x_hif = self.hif_branch(x)
		x_noise = self.noise_branch(rgb2gray(x))
		## GX: the hyper-parameters need to be consistent with the generation model.
		x = x_rbg + 0.0001*x_hif + 0.0001*x_noise
		x = self.out_branch(x)
		x = self.pool(x)
		output_feat = torch.flatten(x, 1)

		res_list = []
		for i in range(self.task_num):
			name = f'head_{(i+1):d}'
			x = getattr(self, name)(output_feat)
			x = F.normalize(x, dim=1)
			res_list.append(torch.unsqueeze(x, 1))

		gcn_inputs = torch.cat(res_list, dim=1)
		gcn_out, gcn_middle, [mm_1, mm_2, cg_1, cg_2], [adj_0, adj_1, adj_2] = self.GCN_refine(gcn_inputs, adj)

		# zero_vec = 0.*torch.ones_like(adj_2)
		# ones_vec = torch.ones_like(adj_2)
		# adj_2    = torch.where(adj_2 > 0.1, ones_vec, zero_vec)
		# print(torch.sum(adj_2))
		# # print("==============")
		# # print(mm_1.size())
		# # print(mm_2.size())
		# # print(cg_1.size())
		# # print(cg_2.size())
		# # print(adj_0.size())
		# # print(adj_1.size())
		# # print(adj_2.size())
		# print(output_feat.size())
		# print(output_feat.size())
		# print(gcn_middle.size())
		gcn_middle = torch.mean(gcn_middle, axis=1)
		# print(gcn_middle.size())

		feature_real_fake = torch.cat([gcn_middle, output_feat], axis=-1)
		# print(feature_real_fake.size())
		# import sys;sys.exit(0)
		pred_real_fake = self.classifier_real_fake(feature_real_fake)
		# print(pred_real_fake.size())
		# import sys;sys.exit(0)
		ce_pred = self.classifier(gcn_out)
		if not tsne:
			return pred_real_fake, ce_pred, gcn_out, [mm_1, mm_2, cg_1, cg_2]
		else:
			return pred_real_fake, ce_pred, [adj_0, adj_1, adj_2], [mm_1, mm_2, cg_1, cg_2]


if __name__ == "__main__":
	print("...coming here...")