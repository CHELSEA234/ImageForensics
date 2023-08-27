
template = {
			"DDPM": ["Diffusion Models with Denoising Score Matching (DDPM) is an advanced technique in the field of generative modeling. \
				It combines the concepts of diffusion processes and denoising score matching to create a powerful framework \
				for generating realistic and high-quality images. "],

			"DDIM": ["DDIM (Deep Diffusion Image Model) is a generative model that employs a diffusion process and deep neural networks \
				to generate high-quality images. It builds upon DDPM (Diffusion Models with Denoising Score Matching), \
				enhancing image generation capabilities and offering improvements in training stability and efficiency."], 

			"GLIDE": ["GLIDE (Generative Latent-Informed Discovery and Exploration) Diffusion is a type of generative model that \
				leverages diffusion processes to generate images. It enhances the flexibility and control over the \
				generative process by utilizing latent variables to guide the image synthesis. "], 

			"LDM": ["Latent diffusion is a generative modeling technique that employs a diffusion process to generate images \
				from a given set of latent variables. In this approach, the generative process is guided by \
				latent variables that control various aspects of image generation"],

			"style2": ["StyleGAN2, a specialized version of the StyleGAN architecture, is particularly renowned for its ability to \
				generate highly realistic and diverse images. It introduces innovations like adaptive instance \
				normalization and style mixing"],

			"style3": ["StyleGAN3 generates state of the art results for un-aligned datasets and looks much more natural in motion, \
				it uses Use of fourier features, filtering, 1x1 convolution kernels and other modifications make the \
				generator equivariant to translation and rotation"],

			"starGANv2": ["StarGAN (Star Generative Adversarial Network) is a machine learning architecture used \
				for image-to-image translation tasks. \
				It allows a single model to transform images from one domain to another, \
				like changing hair color or facial expression."],

			"HiSD": ["Hierarchical Style Disentanglement (HiSD) to address the issue of uncontrolled manipulations, \
			 	to the translation results"],

			'STGAN': ["STGAN is for arbitrary attribute editing, which has a encoder-decoder and generative adversarial networks."],

			'deepfakes': ["Deepfake face images refer to manipulated images in which the face of a person is \
				digitally replaced or superimposed onto \
				another person's face in a way that appears convincingly realistic."],

			'inpainting': ["Inpainting image forgery is a form of digital image manipulation where certain portions of an image \
				are removed or obscured and then replaced with new content. \
				This is typically done to conceal or remove unwanted objects, text, or areas from the original image."],

			'splicing': ["Splicing image forgery is a type of digital image manipulation where different parts from multiple images are \
				 combined to create a deceptive or misleading representation. \
				 This technique involves taking elements from one image and placing them into another to create a new composition."],

			"copy-move": ["Copy-move image forgery is a type of digital image manipulation \
				where a portion of an image is copied and then pasted onto \
				another part of the same image. This technique is often used to conceal or duplicate objects within an image, \
				creating a deceptive appearance."],
			}

template_hier = {
					'level_0': ['fully synthesis', "partial_manipulated"], 
					'level_1': ["diffusion", "GAN", "CNN-based", "Image Editing"],
					'level_2': ['uncondition', 'conditional', 'uncondition', 'conditional', "CNN-based", "Image Editing"],
					'level_3': ['DDPM', "DDIM", "GLIDE", "LDM", "style2", "style3", "starGANv2", "HiSD",
									'deepfakes', 'STGAN', 'inpainting', 'splicing', 'copy-move']
				}