import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.qlearning_agent import QLearningAgent
from game.tsoro_yematatu import TsoroYematatuGame

def train_qlearning(num_episodes=1000):
    # Create Q-learning agent
    agent = QLearningAgent(TsoroYematatuGame)

    # Train the agent
    agent.learn_game(num_episodes)

    # Optionally save learned Q-table
    agent.save(f"qlearning_table_{num_episodes}.pkl")

    print(f"Training complete after {num_episodes} episodes.")
    return agent

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Train Q-Learning Agent")
    parser.add_argument("--episodes", type=int, default=1000, help="Number of episodes to train")
    args = parser.parse_args()

    trained_agent = train_qlearning(args.episodes)

# train with train_qlearning.py, save the Q‑table, and then load it inside your GUI (GUIAgent) to play against a trained agent.
