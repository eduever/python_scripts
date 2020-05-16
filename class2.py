class family:
	'''this is doc string'''
	def __init__(self,father,mother,son,daughter):
		self.father = father
		self.mother = mother
		self.son = son
		self.daughter = daughter
	def familydesc(self):
		print('{0} his spouse is {1} and son is  {2} and daughter is  {3}:'.format(self.father,self.mother,self.son,self.daughter))

f = family('ramu','hari','ruth','sahana')
f.familydesc()

class employee:
	def __init__(self,emp,salary,title):
		self.emp = emp
		self.salary = salary
		self.title = title
	def employeedetails(self):
		print("his name is {} and role is  {} and wage={}".format(self.emp, self.salary, self.title))
a = employee("ruth",3000,"devops")
a.employeedetails()

