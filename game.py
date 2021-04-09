# Program to Show how to create a switch
# import kivy module	
import kivy
	
# base Class of your App inherits from the App class.	
# app:always refers to the instance of your application
from kivy.app import App
from kivy.uix.gridlayout import GridLayout	
from kivy.logger import Logger
# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require('1.9.0')

# Builder is used when .kv file is
# to be used in .py file
from kivy.lang import Builder

# The screen manager is a widget
# dedicated to managing multiple screens for your application.
from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition,
SlideTransition, CardTransition, SwapTransition,
FadeTransition, WipeTransition, FallOutTransition, RiseInTransition)
from components.board import Board, UnwriteableSquareError, InvalidSquareValueError

# You can create your kv code in the Python file
Builder.load_file('gui/gui.kv')

# Create a class for all screens in which you can include
# helpful methods specific to that screen
class SplashScreen(Screen):
	def sayhi(self):
		Logger.critical("Hi!")

	def saybye(self):
		Logger.critical("Bye!")

class NewGame(Screen):
	def __init__(self, **kwargs):
		super(Screen,self).__init__(**kwargs)
		self.new_board = Board(board_data=None)
		self.initialize_board()

	def initialize_board(self):
		"""
		Sets the hardcoded values to the board upon loading
		"""
		for screen in self.walk():
			for text_input in screen.walk():
				if isinstance(text_input, kivy.uix.textinput.TextInput):
					value = self.new_board.get_value(text_input.board_row, text_input.board_col)
					text_input.text = str(value)

	def set_value(self, instance):
		try:
			value = int(instance.text)
			self.new_board.change_square(instance.board_row, instance.board_col, value)
		except UnwriteableSquareError as e:
			# Handles when a person tries to over write a hardcoded value, write back old value
			old_value = self.new_board.get_value(instance.board_row, instance.board_col)
			instance.text = str(old_value)
		except InvalidSquareValueError as e:
			# Handles values < 1 or > 9 
			# DECIDE - should this write a blank or the old value back
			Logger.error(f"InvalidSquareValueError: {e}")
		except ValueError as e:
			# Handles non-integer inputs - clear square/don't allow
			instance.text = ''
		finally:
			self.check_win()
	
	def check_win(self):
		"""
		After every move, good or bad, just check the win 
		"""
		if self.new_board.won:
			Logger.info("You won!")

class Options(Screen):
	pass

class ScreenFour(Screen):
	pass


# The ScreenManager controls moving between screens
# You can change the transitions accorsingly
screen_manager = ScreenManager()

# Add the screens to the manager and then supply a name
# that is used to switch screens
screen_manager.add_widget(SplashScreen(name ="Splash Screen"))
screen_manager.add_widget(NewGame(name ="New Game"))
screen_manager.add_widget(Options(name ="Options"))
screen_manager.add_widget(ScreenFour(name ="Screen 4"))

# Create the App class
class ScreenApp(App):
	def build(self):
		return screen_manager

# run the app
if __name__ == "__main__":
    sample_app = ScreenApp()
    sample_app.run()