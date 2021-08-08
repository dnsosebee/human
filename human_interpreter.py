# human_interpreter.py -- an interpreter of the human programming language. By Daniel Sosebee

import os
from re import split as re_split
from errors import InvalidGoalException, WrongNumberOfVariablesException, NoInstructionsException

class HumanInterpreter:
	BEGINNING_OF_GOAL_STRING = "HOW TO " # all .human files must start with "HOW TO "
	BEGINNING_OF_CALL_STRING = "FOLLOWING " # this is the string that indicates that a line should call a different file
	INSTRUCTION_PROMPT = "DO THIS: " # printed before the current instruction
	INPUTS_TO_VIEW_STACK = ["g", "goals"] # input either of these to see the whole goals stack
	PRINT_BEFORE_LEVEL = "LEVEL " # printed before the level in the stack
	PRINT_BEFORE_GOAL = " GOAL: To " # printed before the goal in the stack
	USAGE_MESSAGE = "Then, press enter here to continue. (input 'g' to view current goals) " # printed to let the user know their input options

	# @param path: 			the path to the .human file that we'd like to execute now
	# @param variable_vals: a list of values corresponding to the variables in the goal of the .human file
	# @param parent: 		the HumanInterpreter that created this HumanInterpreter, if relevant
	def __init__(self, path, variable_vals, parent=None):
		self.path = path
		self.human_file = open(path, 'r')
		self.variable_vals = []
		if variable_vals:
			self.variable_vals = variable_vals
		self.variable_map = {} # a map from variable name to value
		self.parent = parent
		self.goal = "" # the goal stored in the first line of the program, hydrated with variable values

	# @Story: This method is the only real public method: It interprets the file self.human_file,
	# giving the human instructions to complete.
	def interpret(self):
		self.interpret_goal()
		self.interpret_instructions()

	# @Story: The first relevant line of a file is the goal, (format: "HOW TO do something with {variable}")
	# This method reads that line and uses it to create self.variables_map and self.goal
	# This lets us create a map of variables to values (self.variables_map), and fill in self.goal
	def interpret_goal(self):
		self.goal = ""
		line = self.get_line()
		if line and line[ : len(self.BEGINNING_OF_GOAL_STRING)] == self.BEGINNING_OF_GOAL_STRING:
			raw_goal = line[len(self.BEGINNING_OF_GOAL_STRING) : ]
			if len(raw_goal) > 1:
				variable_count = 0
				while True:
					variable_indices = self.find_first_variable_indices(raw_goal)
					if (variable_indices):
						variable_count += 1
						if variable_count > len(self.variable_vals):
							raise WrongNumberOfVariablesException()
						variable_name_before = raw_goal[variable_indices[0] + 1 : variable_indices[1]]
						variable_name_after = self.variable_vals[variable_count - 1]
						self.variable_map[variable_name_before] = variable_name_after
						self.goal += raw_goal[ : variable_indices[0]] + variable_name_after
						raw_goal = raw_goal[variable_indices[1] + 1 : ]
					else:
						self.goal += raw_goal
						break
				if variable_count != len(self.variable_vals):
					raise WrongNumberOfVariablesException()
		else:
			raise InvalidGoalException()
	
	# return the indices of the first curly-braced variable in the string (indices returned are the braces)
	def find_first_variable_indices(self, string):
		return self.find_indices_of_first_enclosure(string, '{', '}')

	# return the indices of the first bracketted value in the string (indices returned are the brackets)
	def find_first_value_indices(self, string):
		return self.find_indices_of_first_enclosure(string, '[', ']')

	# return the indices of the first value enclosed by l to the left and r to the right
	def find_indices_of_first_enclosure(self, string, l, r):
		l_index = string.find(l)
		if l_index > -1:
			r_index = string[l_index : ].find(r) + l_index
			if r_index > -1:
				return (l_index, r_index)
		return False

	# @Story: We need to read lines from the self.human_file, but some of them have comments, and some are empty.
	# this function gets rid of comments and returns the first non-empty line.
	def get_line(self):
		for line in self.human_file:
			line = line.strip()
			# check for comments '#'
			line_split = line.split('#')
			line = line_split[0]
			# check if any of the comments are escaped by a backspace: '\#'
			for i in range(len(line_split) - 1):
				if line_split[i] == "":
					break
				if line_split[i][-1] == '\\':
					line = line[ : -1] + '#' + line_split[i + 1]
				else:
					break
			if len(line) < 1:
				continue
			return line
		return False

	# @Story: After reading the goal line, we need to read the instruction lines.
	# These lines might be printed to the user, or might lead to calling a new .human file.
	def interpret_instructions(self):
		line = self.get_line()
		if not line:
			raise NoInstructionsException()
		while (line):
			while True:
				variable_indices = self.find_first_variable_indices(line)
				if (variable_indices):
					variable_name_before = line[variable_indices[0] + 1 : variable_indices[1]]
					variable_name_after = self.variable_map[variable_name_before]
					line = line[ : variable_indices[0]] + variable_name_after + line[variable_indices[1] + 1 : ]
				else:
					break
			if line[ : len(self.BEGINNING_OF_CALL_STRING)] == self.BEGINNING_OF_CALL_STRING:
				self.interpret_new_program(line)
			else:
				self.print_instruction_and_wait(line)
			line = self.get_line()

	# @Story: If a file has a line like 'FOLLOWING ./program.human, brush [your brother's] teeth',
	# Then we want to interpret that program, showing those instructions to the user.
	# This is much like adding a new stack frame. 
	def interpret_new_program(self, line):
		line = line[len(self.BEGINNING_OF_CALL_STRING) :]
		line_split = re_split('(:| |,)', line, 1)
		relative_path_to_program = line_split[0]
		program = line_split[2]
		dir_path = os.path.dirname(self.path)
		os.chdir(dir_path)
		new_program_path = os.path.abspath(relative_path_to_program)
		vals = []
		# collect all values found between brackets '[val]'
		while True:
			val_indices = self.find_first_value_indices(program)
			if (val_indices):
				vals.append(program[val_indices[0] + 1 : val_indices[1]])
				program = program[val_indices[1] + 1 : ]
			else:
				break
		interpreter = HumanInterpreter(new_program_path, vals, self)
		interpreter.interpret()

	# @Story: For each instruction line, we want to show the user the instruction,
	# prompting them to do it.
	def print_instruction_and_wait(self, line, view_stack=False):
		print(chr(27) + "[2J")
		if view_stack:
			self.print_goal_stack()
		print(f"{self.INSTRUCTION_PROMPT}{line}\n")
		response = input(self.USAGE_MESSAGE)
		if response in self.INPUTS_TO_VIEW_STACK:
			self.print_instruction_and_wait(line, True)
	
	# @Story: If a user wants to, they can see the whole stack of goals leading up to their current instruction.
	# this method prints that stack
	def print_goal_stack(self):
		ancestry_goals = self.get_ancestry_goals()
		for i in range(len(ancestry_goals)):
			goal = ancestry_goals[i]
			level = len(ancestry_goals) - i
			print(f"{self.PRINT_BEFORE_LEVEL}{level}{self.PRINT_BEFORE_GOAL}{goal}")

	# @Story: We want to see 'the call stack' of human program goals so that the human can see what they're working on
	# so, we need to traverse upwards in the family tree of interpreters to find each parent's goal.
	# @return a list of strings representing the goals of all parents, and this interpreter.r
	def get_ancestry_goals(self):
		goals = []
		if self.parent:
			goals = self.parent.get_ancestry_goals()
		goals.append(self.goal)
		return goals

	def __del__(self):
		self.human_file.close()
