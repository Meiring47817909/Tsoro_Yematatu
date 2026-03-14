from agents.qlearning_agent import QLearningAgent
from game.tsoro_yematatu import TsoroYematatuGame

def train_qlearning(num_episodes=5000):
    # Create Q-learning agent
    agent = QLearningAgent(TsoroYematatuGame)

    # Train the agent
    agent.learn_game(num_episodes)

    # Optionally save learned Q-table
    agent.save("qlearning_table.pkl")

    print(f"Training complete after {num_episodes} episodes.")
    return agent

if __name__ == "__main__":
    trained_agent = train_qlearning(5000)

# train with train_qlearning.py, save the Q‑table, and then load it inside your GUI (GUIAgent) to play against a trained agent.
