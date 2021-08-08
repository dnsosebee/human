# human.py is a command line interface that instructs humans by interpreting the human programming language. by Daniel Sosebee

import argparse
import sys
import os
from human_interpreter import HumanInterpreter

def create_arg_parser():
	parser = argparse.ArgumentParser(description='A simple computer program to facilitate natural-language human-self-programming')
	parser.add_argument('input_file', help="<Required> Path to the file containing the human language program you'd like to follow.")
	parser.add_argument('--values', '-v', nargs='+', help='')
	return parser

if __name__ == "__main__":
	args = create_arg_parser().parse_args(sys.argv[1:])
	input_file = args.input_file
	values = args.values
	if os.path.exists(input_file):
		path = os.path.abspath(input_file)
		interpreter = HumanInterpreter(path, values)
		interpreter.interpret()
	else:
		raise FileNotFoundError(f"could not find file {input_file}")