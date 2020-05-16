import re

samples = []

with open('text') as myfile:
    for line in myfile.readlines():
	    z = re.match("(arn\w+)", line):\
		    samples.append(line)

print(samples)