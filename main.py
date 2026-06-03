import argparse
from game.tsoro_yematatu import TsoroYematatuGame
from game.board_gui import BoardGUI
from agents.gui_agent import GUIAgent
from agents.qlearning_agent import QLearningAgent

def run_game(mode="random", computer_player="X", model_path="qlearning_table.pkl"):
    game = TsoroYematatuGame()
    gui = BoardGUI(game)

    rl_agent = None
    if mode == "qlearning":
        rl_agent = QLearningAgent(TsoroYematatuGame)
        rl_agent.load(model_path)

    agent = GUIAgent(game, gui=gui, mode=mode, rl_agent=rl_agent)
    agent.interactive_game(computer_player=computer_player)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Tsoro Yematatu")
    parser.add_argument("--mode", choices=["random", "qlearning"], default="random",
                        help="Choose opponent type")
    parser.add_argument("--player", choices=["X", "O"], default="X",
                        help="Choose computer player side")
    parser.add_argument("--model", type=str, default="qlearning_table.pkl",
                        help="Path to the trained Q-table file to load")
    args = parser.parse_args()

    run_game(mode=args.mode, computer_player=args.player, model_path=args.model)

# - Random opponent → mode="random" (computer picks random moves).
# - Q‑learning opponent → mode="qlearning" (loads saved Q‑table).
# - computer_player="X" lets you decide which side the computer plays.

# 🚀 Workflow
# - Train Q‑learning agent with training/train_qlearning.py → saves qlearning_table.pkl.
# - Run main.py and set mode to "random" or "qlearning" depending on which opponent you want.