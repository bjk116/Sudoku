from queue import LifoQueue
import sys
sys.path.append('..')
from components.board import Board

class BrianSolver():
	"""
	This class inherits the Sudoku board class and implements a stack of instructions for soling it, that grows/
	dynamically changes as numbers are found.
	Properties:
		possible_answers: 2D list of sets with possible answers.  sets of size are the correct answer
	"""
	possible_answers = None

	def __init__(self, board):
		self.board = board
		self.instruction_stack = LifoQueue()
		self.initialize_possible_answers()

	def round_robin_group(self, group):
		"""
		Takes a row and column, and then gets the set of of numbers already existing in that group, and removes
		from the square based on that.
		"""
		print(f"doing group {group}")
#		group_values = self.get_group_set(row, col)
#		self.possible_answers[row][col] = self.possible_answers[row][col].difference(group_values)


	def initialize_possible_answers(self):
		"""
		Before creating any instructions, we first determine possible values for each empty square.
		We do this on initialization in case we want this information to be used in determining our first
		instruction.

		While this does work and runs fine and could potentially solve many puzzles, its' not using the stack
		structure like I want.
		"""
		self.possible_answers = [[],[],[],[],[],[],[],[],[]]
		for i in range(0, 9):
			self.possible_answers[i] = [None, None, None, None, None, None, None, None, None]
		for row_num, row in enumerate(self.board.board_data):
			row_values = self.get_row_set(row_num)
			for col_num, square in enumerate(row):
				col_values = self.get_col_set(col_num)
				group_values = self.get_group_set(row_num, col_num)
				if square.value is not None:
					self.possible_answers[row_num][col_num] = set([square.value])
				else:
					full_values = set([1,2,3,4,5,6,7,8,9])
					self.possible_answers[row_num][col_num] = full_values
#					This function should be purely to initalize for usage, not start solving.  We want to do all solving
#					via our stack structure
#					sets_to_subtract = [row_values, col_values, group_values]
#					self.possible_answers[row_num][col_num] = full_values.difference(*sets_to_subtract)
		self.print_possible_answers()

	def print_possible_answers(self):
		"""
		Prints out current possible answers per square.
		"""
		print(f"poss answers {self.possible_answers}")
		for row_num, row in enumerate(self.possible_answers):
			for col_num, set_values in enumerate(row):
				only_one_answer_left_and_not_on_board_and_not_erasable = len(set_values) == 1 and self.board.board_data[row_num][col_num].value is None and self.board.board_data[row_num][col_num].erasable
				if  only_one_answer_left_and_not_on_board_and_not_erasable:
					print(f"Found new answer {set_values} for {row_num},{col_num}")


	def get_row_set(self, row):
		"""
		Returns a set of all numbers that appear in the row
		"""
		return set([x.value for x in self.board.board_data[row]])		

	def get_col_set(self, col):
		"""
		Returns set of all numbers that appear in the column
		"""
		return  set([row[col].value for row in self.board.board_data])

	def get_group_set(self, row, col):
		"""
		Get set of values in group
		"""
		group_num = self.board.board_data[row][col].group
		return self.board.get_group_value_set(group_num)

	def do_next_step(self):
		"""
		Creates, and then does, next step into stack.
		"""
		if self.instruction_stack.empty():
			self.instruction_stack.put((self.round_robin_group,(9,),{}))
			self.instruction_stack.put((self.round_robin_group,(8,),{}))
			self.instruction_stack.put((self.round_robin_group,(7,),{}))
			self.instruction_stack.put((self.round_robin_group,(6,),{}))
			self.instruction_stack.put((self.round_robin_group,(5,),{}))
			self.instruction_stack.put((self.round_robin_group,(4,),{}))
			self.instruction_stack.put((self.round_robin_group,(3,),{}))
			self.instruction_stack.put((self.round_robin_group,(2,),{}))
			self.instruction_stack.put((self.round_robin_group,(1,),{}))
		func, params, keyword_params = self.instruction_stack.get()
		func(*params, **keyword_params)

if __name__ == "__main__":
	new_game = Board()
	my_solver = BrianSolver(new_game)