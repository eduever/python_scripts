#!/usr/bin/python

"""
## read last N lines

def read_lastNline(fname, N):
	with open(fname) as file:
		for lines in (file.readlines() [-N:]):
			print(lines, end='')

read_lastNline('text.txt',3)

if __name__ == '__main__':
	filename = 'text.txt'
	number = 3
	try:
		read_lastNline(filename,number)
	except:
		print('file NOT found')

--------
## add lines to a list

def append_linestoList(fname,list):
	with open(fname,"r") as f:
		for line in (f.readlines()):
			list.append(line)
	print(list,end='')
append_linestoList('text.txt',[1,2])

------
## return MAX lenght word

def max_word(fname):
	with open(fname) as f:
		words = f.read().split()
		maxlen_word = max(words, key=len)
	return [print(maxlen_word)]

max_word('text.txt')

-------

## find no of lines in a file

def findnolines(fname):
	with open(fname) as f:
		print("returntype", type(f))
		for i, l in enumerate(f,1):
			pass
	return print(i)

findnolines('text.txt')

-------
## find no of words

from collections import Counter
def nowords(fname):
	with open(fname) as f:
		return print("no of words:",Counter(f.read().split()))
nowords('text.txt')

------
## copy file
def copy(source,destination):
	import shutil
	try:
		shutil.copyfile(source,destination)
		print("files copied success")
	except shutil.SameFileError:
		print("both same files")
	except IsADirectoryError:
		print("something is a dir")
	except PermissionError:
		print("permission error")
	except:
		print("something wrong")

copy('text.txt','copy.txt')
-----------
## write list to a file

def listtofile(fname,list):
	with open(fname,"w") as f:
		for element in list:
			f.write("%s\n" % element)
	return print(open(fname).read())

listtofile('abc.txt',['hello','ruth'])

--------

"""

