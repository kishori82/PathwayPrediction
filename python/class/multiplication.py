class Multiplication(object):

	first=None
	second=None
	result=None

	def firstNo(self):
		self.first=input("enter the first number: ")
		pass

	def secondNo(self):
		self.second=input("enter the second number: ")

	def result(self):

		self.firstNo()
		self.secondNo()
		result= self.first * self.second
		print "result of multiplication is: %f" %(result)

if __name__=="__main__":

	init=Multiplication()

	init.result()


