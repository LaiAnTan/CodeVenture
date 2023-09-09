class	test:
	a = 0
	_instance = None

	@classmethod
	def	__new__(cls, val: int):
		cls.a = val

	@classmethod
	def	instance(cls, val: int):
		if cls._instance == None:
			cls._instance = cls.__new__(val)
		return (cls._instance)
	
	@classmethod
	def	print_val(cls):
		print(cls.a)

	@classmethod
	def change(cls):
		cls.a += 1

class	inherittest(test):
	@classmethod
	def instance(cls, val: int):
		return super().instance(val)

	@classmethod
	def change(cls):
		cls.a -= 1

class	inherit2test(test):
	@classmethod
	def instance(cls, val: int):
		return super().instance(val)

	@classmethod
	def change(cls):
		cls.a *= 2


if __name__ == "__main__":
	print("base:")
	test.instance(1)
	test.print_val()
	test.change()
	test.print_val()
	print()

	print("inherited")
	inherittest.instance(5)
	inherittest.print_val()
	inherittest.change()
	inherittest.print_val()
	print()
	print("base value")
	test.print_val()
	print()

	print("2nd inherited")
	inherit2test.instance(6)
	inherit2test.print_val()
	inherit2test.change()
	inherit2test.print_val()
	print()

	print("final")
	test.print_val()
	inherittest.print_val()
	inherit2test.print_val()
	print()