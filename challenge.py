import activity as ac

class Challange(ac.Activity):

	def __init__(self, filename: str) -> None:
		super().__init__(filename, ac.Activity.AType["Challenge"])
		self.read_mf_read()

	def __str__(self):
		return super().__str__()
	
	def RunActivity(self):
		print("Challange Activity is Running~")

if __name__ == "__main__":
	test = Challange("CH0000")
	print(test)