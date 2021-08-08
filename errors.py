# errors.py -- errors for the human interpreter. By Daniel Sosebee

class InvalidGoalException(Exception):
	def __init__(self):
		self.message = "The first line of the file must start with 'HOW TO '..."
		super().__init__(self.message)

class WrongNumberOfVariablesException(Exception):
	def __init__(self):
		self.message = "The number of values provided does not match the number of variables in the program description."
		super().__init__(self.message)

class NoInstructionsException(Exception):
	def __init__(self):
		self.message = "The .human file didn't have any instructions."
		super().__init__(self.message)

