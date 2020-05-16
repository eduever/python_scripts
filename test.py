# x = range(10)
# for n in x:
# 	print(n)

'''
python test.py 1 2 3

import sys
n = len(sys.argv)
add = 0
print(n)
for i in range(1,n):
	add = add + int(sys.argv[i])
print(add)
'''


a = [1,2,3,4,[2,3,4],3,6,[6,7]]

new_list = []
for i in a:
	if type(i) == list:
		new_list.extend(i)
	else:
		new_list.append(i)

new_list.sort()
print(new_list)
