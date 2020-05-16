# def sum(integers):
# 	x = 0
# 	for i in integers:
# 		x += i
# 	return x
#
# list = [1,2,3]
# a = sum(list)
# print(a)

# def sum(*args):
# 	result = 0
# 	for i in args:
# 		result = result + i
# 	return result
# print(sum(1,2,3,4,5,6))

# def concantinate(**kwargs):
# 	result = ""
# 	for i in kwargs.values():
# 		result = result + " brother of " + i
# 	return result
# print(concantinate(a="ruth",b="sahana"))

def test(a, b, *args, **kwargs):
	sum = a + b
	result = 0
	for i in args:
		result = result + i
	totalvalue = result + sum
	
	word = ""
	for x in kwargs.values():
		word = word + x
	
	return print("{} and its sum is {}".format(totalvalue,word))

a = test(1,2,3,4,5,p="ruth",q="bhar")

	

