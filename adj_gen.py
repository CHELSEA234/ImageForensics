import numpy as np

import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from operator import add
THRESHOLD = 0.2

def viz_func(input_list):
	array = input_list
	total_length = len(input_list)
	df_cm = pd.DataFrame(
						array, 
						index = [i for i in range(total_length)],
	                  	columns = [i for i in range(total_length)]
	                  	)
	plt.figure(figsize = (10,7))
	sn.heatmap(df_cm, annot=True, cmap="crest")
	plt.show()

## loading the architecture parameters.
archi_fun_list = 'copy_list_archi.txt'
f = open(archi_fun_list, "r")
lines = f.readlines()
label_archi_list = []
for idx, _ in enumerate(lines):
	cur_list = []
	line = _.strip()
	par_lst = line.split(' ')
	for par in par_lst:
		if par.isdigit(): ## GX: in case STARGAN 2, STYLEGAN 2
			par_val = int(par)
			cur_list.append(par_val)
	label_archi_list.append(cur_list)
f.close()

## refine the architecture parameters.
## GX: do not have F2-F5, divide others into 3 blocks.
refine_archi_list = []
max_value_list = [97,8365,9,16,94008488]
for cur_list in label_archi_list:
	refine_cur_list = []
	cur_list = cur_list[-15:]
	for idx, ele in enumerate(cur_list):
		if idx in [1,2,3,4]:
			# refine_archi_list.append()
			continue
		elif idx == 0:
			if ele < 30:
				# tmp = [float(ele/30),0,0]
				tmp = [1,0,0]
			elif 30 <= ele and ele < 60:
				# tmp = [0,float((ele-30)/30),0]
				tmp = [0,1,0]
			else:
				# tmp = [0,0,float((ele-60)/(97-60))]
				tmp = [0,0,1]
		elif idx == 5: # num of filter
			if ele < 3000:
				# tmp = [float(ele/3000),0,0]
				tmp = [1,0,0]
			elif 3000 <= ele and ele < 6000:
				# tmp = [0,float((ele-3000)/3000),0]
				tmp = [0,1,0]
			else:
				# tmp = [0,0,float((ele-6000)/(8365-6000))]
				tmp = [0,0,1]
		elif idx == 6:	# num of block
			if ele < 3:
				# tmp = [float(ele/3),0,0]
				tmp = [1,0,0]
			elif 3 <= ele and ele < 6:
				# tmp = [0,float((ele-3)/3),0]
				tmp = [0,1,0]
			else:
				# tmp = [0,0,float((ele-6)/3)]
				tmp = [0,0,1]
		elif idx == 7:	# layer per block
			if ele < 5:
				# tmp = [float(ele/5),0,0]
				tmp = [1,0,0]
			elif 5 <= ele and ele < 10:
				# tmp = [0,float((ele-5)/5),0]
				tmp = [0,1,0]
			else:
				# tmp = [0,0,float((ele-5)/6)]
				tmp = [0,0,1]
		elif idx == 8:	# para. num.
			if ele < 10000000:
				# tmp = [float(ele/10000000),0,0]
				tmp = [1,0,0]
			elif 10000000 <= ele and ele < 60000000:
				# tmp = [0,float((ele-10000000)/50000000),0]
				tmp = [0,1,0]
			else:
				# tmp = [0,0,float((ele-50000000)/94008488-50000000)]
				tmp = [0,0,1]
		else:
			if ele == 0:
				tmp = [0]
			else:
				tmp = [1]
		refine_cur_list.extend(tmp)
	refine_archi_list.append(refine_cur_list)

## loading the objective functions.
object_fun_list = "copy_list.txt"
f = open(object_fun_list, "r")
lines = f.readlines()
label_obj_list = []
for idx, _ in enumerate(lines):
	cur_list = []
	line = _.strip()
	line = line.replace(" ", "")
	for char in line:
		cur_list.append(int(char))
	label_obj_list.append(cur_list)
f.close()

nor_correlation = []
adj_correlation = []
total_length = len(refine_archi_list[0]) + len(label_obj_list[0])
list2 = [[] for _ in range(total_length)]
for target_idx in range(total_length):
	list1 = [0 for _ in range(total_length)]
	for idx, _ in enumerate(refine_archi_list):
		list2 = label_obj_list[idx] + refine_archi_list[idx]
		if list2[target_idx] == 1:
			list1 = list(map(add, list1, list2))
	nor_list = [x / list1[target_idx] for x in list1]
	adj_list = []
	for nor_unit in nor_list:
		if nor_unit >= THRESHOLD:
			adj_list.append(1)
		else:
			adj_list.append(0)
	nor_correlation.append(nor_list)
	adj_correlation.append(adj_list)

adj_array = np.asarray(adj_correlation)
print(np.sum(adj_array))
np.save('adj_matrix.npy', adj_array)
viz_func(nor_correlation)
viz_func(adj_correlation)