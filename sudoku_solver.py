"""
Been playing a lot of sudoku recently.  Developed an algorithm for solving it.  Want to try to code
it to as optimally as possible.  Here is attempt number 1.  Lets goooo.

Design Decisions:
	How to represent the board?  A list of lists seems natural, if a little crass.  But easy to
	get started with at least.
	Creating an insruction stack
	Creating a second "Board" that keeps track of possible values per square

Algorithm:
	I'm calling it the slightly greedy algorithm as it has aspects where it wants to be
	greedy but other parts where it just does what comes naturally.
"""

class Square():
	"""
	Represents a singular square on the sudoku board.  Make this so we can easily change value to the right coordinate and have it display
	"""
	row = None
	column = None
	value = None
	group = None
	erasable = True
	def __init__(self, row, column, value, initial_setup=False):
		self.row = row
		self.column = column
		self.value = value
		# Want to track and make sure that the numbers which are make up the board initially are not erasable
		if initial_setup:
			self.erasable = False
		self.calculate_group()

	def calculate_group(self):
		first_row = self.row >= 0 and self.row < 3
		second_row = self.row >= 3 and self.row < 6
		third_row = self.row >= 6 and self.row <= 8
		first_column = self.column >= 0 and self.column < 3
		second_column = self.column >=3 and self.column < 6
		third_column = self.column >=6 and self.column <= 8
		if first_row and first_column:
			self.group = 1
		elif first_row and second_column:
			self.group = 2
		elif first_row and third_column:
			self.group = 3
		elif second_row and first_column:
			self.group = 4
		elif second_row and second_column:
			self.group = 5
		elif second_row and third_column:
			self.group = 6
		elif third_row and first_column:
			self.group = 7
		elif third_row and second_column:
			self.group = 8
		elif third_row and third_column:
			self.group = 9

	def change_value(self, value):
		if self.erasable:
			if value is None or (isinstance(value, int) and 1 <= value <= 9):
				self.value = value
			else:
				raise ValueError("Square must be an integer between 1 and 9")
		else:
			raise ValueError("You cannot change a value that is hardcoded to the board")

class Board():
	"""
	Represents the full Sudoku board.  Allows entering of values into None, as long as it is currently valid.
	Also allows erasing of inputted values.  Cannot erase values that were given by the board.
	"""
	raw_board_data = None
	board_data = None
	won = False
	def __init__(self, board_data):
		self.raw_board_data = board_data
		self.initialize_board()
		self.parse_board_data()

	def initialize_board(self):
		self.board_data = [[],[],[],[],[],[],[],[],[]]
		for i in range(0, 9):
			self.board_data[i] = [None, None, None, None, None, None, None, None, None]

	def parse_board_data(self):
		for row_ind, row in enumerate(self.raw_board_data):
			for col_ind, value in enumerate(row):
				initial_setup = value is not None
				self.board_data[row_ind][col_ind] = Square(row_ind, col_ind, value, initial_setup=initial_setup)
	
	def print_value(self, square):
		"""
		Last part of pretty print, decide how to print each number.
		  Args:
			square: Square class either an int or None
		  Returns:
			None
		"""
		if square.value is not None:
			print(f" {square.value} ", end='')
		else:
			print("   ", end='')

	def print_row(self, row):
		"""
		Pretty prints a single row of the board
		  Args:
			row: list of 9 numbers or Nones
		  Returns:
			None
		"""
		for index, square in enumerate(row, start=0):
			if index == 0:
				print("|", end='')
				self.print_value(square)
			elif index == 2 or index == 5:
				self.print_value(square)
				print("|", end='')
			elif index == 8:
				self.print_value(square)
				print("|", end='\n')
			else:
				self.print_value(square)

	def print_board(self):
		"""
		Pretty prints current board.
		  Arg: 
			Board
		  Returns:
			None
		"""
		border = "-------------------------------"
		print(border, end='\n')
		for index, row in enumerate(self.board_data):
			self.print_row(row)
			if index == 2 or index == 5:
				print(border, end='\n')
		print(border, end='\n')

	def change_square(self, row, col, value):
		"""
		Used to change value of underlying square class
		"""
		try:
			if value == 0:
				self.board_data[row][col].change_value(None)
			else:
#				Maybe make this an option thing that may or may not be turned on for newbies.
#				self.is_valid_move(row, col, value)
				self.board_data[row][col].change_value(value)
				self.check_win()
		except ValueError as e:
			print(e)
		except IndexError:
			print("Column or row is too large.  Remember to use 0 through 8.")

	def check_win(self):
		row_win = self.check_row_win()
		col_win = self.check_col_win()
		group_win = self.check_group_win()
		print(f"Row win: {row_win}, Col win: {col_win}, Group win: {group_win}")
		if row_win and col_win and group_win:
			self.won = True

	def check_row_win(self):
		correct_answer = {1, 2, 3, 4, 5, 6, 7, 8, 9}
		all_true = True
		for row_ind, row in enumerate(self.board_data):
			row_values = set([value.value for value in row])
			equals = correct_answer.issubset(row_values) and row_values.issubset(correct_answer)
			if not equals:
				all_true = False
				print(f"Row is not right for row number {row_ind}")
				break
		return all_true
	
	def check_col_win(self):
		correct_answer = {1, 2, 3, 4, 5, 6, 7, 8, 9}
		all_true = True
		for col_ind in range(0, 9):
			col_values = set([row[col_ind].value for row in self.board_data])
			equals = correct_answer.issubset(col_values) and col_values.issubset(correct_answer)
			if not equals:
				all_true = False
				print(f"Col is not right for col number {col_ind}")
				break
		return all_true

	def check_group_win(self):
		correct_answer = {1, 2, 3, 4, 5, 6, 7, 8, 9}
		all_true = True
		for group_num in range(1,10):
			# turns a 2d list into a set
			group_values = set.union(*map(set,self.get_group(group_num)))
			equals = correct_answer.issubset(group_values) and group_values.issubset(correct_answer)
			if not equals:
				all_true = False
				print(f"Group is not right for group num {group_num}")
				break
		return all_true

	def get_group(self, group_num):
		"""
		Gets all values for a group.  Group 1 being the block of 9 numbers in the top left,
		group 2 being the 9 numbers in the top middle, 3 top 9 numbers top right, and so on.
		  Args:
		    group_num: int, between 1 and 9
		    board:  test_board, an infed board, or the answer board
		  Returns:
		    list of values in that group
		"""
		if group_num in (1,2,3):
			first_row = 0
			last_row = 3
		elif group_num in (4,5,6):
			first_row = 3
			last_row = 6
		elif group_num in (7,8,9):
			first_row = 6
			last_row = 9
		else:
			raise ValueError("Group number is invalid")

		if group_num in (1,4, 7):
			first_col = 0
			last_col = 3
		elif group_num in (2, 5, 8):
			first_col = 3
			last_col = 6
		elif group_num  in (3, 6, 9):
			first_col = 6
			last_col = 9

		return [[x.value for x in row[first_col:last_col]] for row in self.board_data[first_row:last_row]]

class SudokuSolver(Board):
	possible_answers = None
	def __init__(self,board_data):
		super().__init__(board_data)
		self.initialize_possible_answers()

	def initialize_possible_answers():
		pass

	def is_valid_move(self, row, col, value):
		"""
		Checks all three vectors to see if a move is possible.
		"""
		self.check_if_valid_row_value(row, col, value)
		self.check_if_valid_col_value(row, col, value)
		self.check_if_valid_group_value(row, col, value)

	def check_if_valid_row_value(self, row, col, value):
		"""
		Checks if the entered value is allowed in the row
		"""
		pass
	
	def check_if_valid_col_value(self, row, col, value):
		"""
		Check if entered value is allowed in the col
		"""
		pass

	def check_if_valid_group_value(self, row, col, value):
		"""
		Ceck if entered value is allowed in the group
		"""
		pass

	def get_group(group_num, board):
		"""
		Gets all values for a group.  Group 1 being the block of 9 numbers in the top left,
		group 2 being the 9 numbers in the top middle, 3 top 9 numbers top right, and so on.
		  Args:
		    group_num: int, between 1 and 9
		    board:  test_board, an infed board, or the answer board
		  Returns:
		    list of values in that group
		"""
		if group_num in (1,2,3):
			first_row = 0
			last_row = 3
		elif group_num in (4,5,6):
			first_row = 3
			last_row = 6
		elif group_num in (7,8,9):
			first_row = 6
			last_row = 9
		else:
			raise ValueError("Group number is invalid")

		if group_num in (1,4, 7):
			first_col = 0
			last_col = 3
		elif group_num in (2, 5, 8):
			first_col = 3
			last_col = 6
		elif group_num  in (3, 6, 9):
			first_col = 6
			last_col = 9

		return [(row[first_col:last_col],) for row in test_board[first_row:last_row]]

	def initialize_possible_answers():
		"""
		Set sets possible answers at first so 1-9 is a possible answer for each square
		"""
		for row in possible_answers:
			for num in range(1,10):
				row.append({1,2,3,4,5,6,7,8,9})

	def first_pass_possible_answers(board):
		"""
		Takes an existing board and then, for each blank space, calculates the possible answers for
		that square.
		  Args:
		    board
		  Returns:
		    modifies possible_answers variable
		"""
		# First, for all given values, reduce their sets to the actual value
		for row_index, row in enumerate(board):
			for col_index, value in enumerate(row):
				if value is not None:
					possible_answers[row_index][col_index] = possible_answers[row_index][col_index].intersection({value})
		# Now, group by group for 1-9, go through, find any solved/given answers, and remove that from the other possible ansewrs in the group
		# row by row - reduce by solved/given answers
		# column by column - reduce by solved answers

test_board = [
		[None, 6, None, None, 4, None, 7, None, None,],
		[None, 2, None, 1, None, None, None, None, None],
		[8, None, 5, 2, None, 6, None, 9, 4],
		[None, None, 1, None, 9, 3, None, None, 7],
		[4, 3, None, 5, None, 8, None, 2, 9],
		[5, None, None, 4, 7, None, 8, None, None],
		[6, 5, None, 7, None, 4, 3, None, 8],
		[None, None, None, None, None, 9, None, 4, None],
		[None, None, 2, None, 5, None, None, 7, None]
	     ]

if __name__ == "__main__":
	game = Board(test_board)
	game.print_board()
	while True:
		try:
			row = int(input("Choose a row"))
			col = int(input("Choose a column"))
			value = int(input("Choose a value, 0 if you want to erase"))
			game.change_square(row, col, value)
			if game.won:
				print("Congrats you win!")
				game.print_board()
				break
		except ValueError:
			print("Please enter an integer")		
		game.print_board()