# main.py
from agent import Agent
from tsoro_yematatu import TsoroYematatuGame
from board_gui import TsoroYematatuGUI

game = TsoroYematatuGame()
gui = TsoroYematatuGUI(game)

agent = Agent(game, gui)   # pass the *instance*, not the class
agent.interactive_game()