class Logger(object):
	_instance = None

	@classmethod
	def __new__(cls):
		if cls._instance is None:
			print('Creating the object')
			cls._instance = super(Logger, cls).__new__(cls)
			# Put any initialization here.
		return cls._instance
	
class Ehe(Logger):

	@classmethod
	def __new__(cls, fuck):
		return super().__new__()

class ThisIsStupid(Ehe):

	@classmethod
	def __new__(cls, shit):
		print(shit)
		return super().__new__(cls)

a = ThisIsStupid()