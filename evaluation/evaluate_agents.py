import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from agents.qlearning_agent import QLearningAgent
from game.tsoro_yematatu import TsoroYematatuGame

# - Loads the trained Q-learning agent (qlearning_table.pkl).
# - Plays num_games matches where Random is always X and Q-learning is O.
# - Tracks wins and draws, then prints a summary.

def evaluate(num_games=100, q_table_path="qlearning_table.pkl"):
    # Load trained agent
    q_agent = QLearningAgent(TsoroYematatuGame)
    q_agent.load(q_table_path)

    q_wins, random_wins, draws = 0, 0, 0

    for i in range(num_games):
        game = TsoroYematatuGame()
        while game.playable():
            if game.player == 'X':  # Random plays as X
                allowed_moves = game.allowed_moves()
                if not allowed_moves:
                    break
                move = random.choice(allowed_moves)
                game.make_move(move)
            else:  # Q-learning plays as O
                move = q_agent.play_select_move(game)
                if move:
                    game.make_move(move)

        if game.winner == 'X':
            random_wins += 1
        elif game.winner == 'O':
            q_wins += 1
        else:
            draws += 1

    print(f"Results over {num_games} games:")
    print(f"Random wins: {random_wins}")
    print(f"Q-learning wins: {q_wins}")
    print(f"Draws: {draws}")

if __name__ == "__main__":
    evaluate(100)