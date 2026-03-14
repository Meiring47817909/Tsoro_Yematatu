import argparse
from game.tsoro_yematatu import TsoroYematatuGame
from game.board_gui import BoardGUI
from agents.gui_agent import GUIAgent
from agents.qlearning_agent import QLearningAgent
from agents.dqn_agent import DQNAgent

def run_game(mode="random", computer_player="X"):
    game = TsoroYematatuGame()
    gui = BoardGUI(game)

    rl_agent = None
    if mode == "qlearning":
        rl_agent = QLearningAgent(TsoroYematatuGame)
        rl_agent.load("qlearning_table.pkl")
    elif mode == "dqn":
        rl_agent = DQNAgent(state_dim=7, action_dim=7)
        rl_agent.load_model("dqn_tsoro.pth")

    agent = GUIAgent(game, gui=gui, mode=mode, rl_agent=rl_agent)
    agent.interactive_game(computer_player=computer_player)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Tsoro Yematatu")
    parser.add_argument("--mode", choices=["random", "qlearning", "dqn"], default="random",
                        help="Choose opponent type")
    parser.add_argument("--player", choices=["X", "O"], default="X",
                        help="Choose computer player side")
    args = parser.parse_args()

    run_game(mode=args.mode, computer_player=args.player)

# - Random opponent → mode="random" (computer picks random moves).
# - Q‑learning opponent → mode="qlearning" (loads saved Q‑table).
# - DQN opponent → mode="dqn" (loads saved neural network weights).
# - computer_player="X" lets you decide which side the computer plays.

# 🚀 Workflow
# - Train Q‑learning agent with training/train_qlearning.py → saves qlearning_table.pkl.
# - Train DQN agent with training/train_dqn.py → saves dqn_tsoro.pth.
# - Run main.py and set mode to "random", "qlearning", or "dqn" depending on which opponent you want.