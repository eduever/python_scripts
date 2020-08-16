"""def fucn_lines(fname, lines):
	from itertools import islice
	with open(fname) as f:
		for line in islice(f,lines):
			print(line)
fucn_lines('text.txt',2)
----
def append_line(fname, lines):
	with open(fname,'w') as f:
		f.writelines(lines)
		f.close()
		print(open(fname).read())
L= ["rutwik \n", "bharadwaj"]
append_line('text.txt',L)
----
with open('text.txt','a') as f:
	f.write("hello rutwik")
print(open('text.txt').read())


"""



