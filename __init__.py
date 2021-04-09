from board import Board
from sample_boards import test_board_1

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