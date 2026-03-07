# main.py
from agent import GUIAgent
from tsoro_yematatu import TsoroYematatuGame
from board_gui import TsoroYematatuGUI
from rl_agent import Agent as RLAgent   # import RL agent

game = TsoroYematatuGame()
gui = TsoroYematatuGUI(game)

# --- Option 1: Random agent ---
# agent = GUIAgent(game, gui, mode="random")
# agent.interactive_game(computer_player='X')

# --- Option 2: RL agent ---
rl_agent = RLAgent(game_class=TsoroYematatuGame, epsilon=0.1, alpha=0.5, value_player='X')
print("Training RL agent...")
rl_agent.learn_game(num_episodes=10000)   # train for 10000 episodes
rl_agent.round_V()
print("Training complete.")

agent = GUIAgent(game, gui, mode="rl", rl_agent=rl_agent)

agent.interactive_game(computer_player='X')
