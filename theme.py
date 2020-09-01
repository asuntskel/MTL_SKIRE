class Theme():
	def __init__(self, choice):
		self.choice = choice;

		if choice == "dark":
			self.bg = "#17252A"
			self.font = "#def2f1"
		elif choice == "clear":
			self.bg = "#dbd9d2"
			self.font = "#ffffff"