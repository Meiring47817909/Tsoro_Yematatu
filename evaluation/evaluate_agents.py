from agents.qlearning_agent import QLearningAgent
from agents.dqn_agent import DQNAgent
from game.tsoro_yematatu import TsoroYematatuGame

def encode_state(game):
    return [1 if c == 'X' else -1 if c == 'O' else 0 for c in game.state]

# - Loads the trained Q-learning agent (qlearning_table.pkl) and the trained DQN agent (dqn_tsoro.pth).
# - Plays num_games matches where DQN is always X and Q-learning is O.
# - Tracks wins and draws, then prints a summary.

def evaluate(num_games=100, dqn_model_path="dqn_tsoro.pth", q_table_path="qlearning_table.pkl"):
    # Load trained agents
    q_agent = QLearningAgent(TsoroYematatuGame)
    q_agent.load(q_table_path)

    dqn_agent = DQNAgent(state_dim=7, action_dim=7)
    dqn_agent.load_model(dqn_model_path)

    q_wins, dqn_wins, draws = 0, 0, 0

    for i in range(num_games):
        game = TsoroYematatuGame()
        while game.playable():
            if game.player == 'X':  # DQN plays as X
                state = encode_state(game)
                allowed_moves = game.allowed_moves()
                action_index = dqn_agent.select_action(state, allowed_moves)
                next_state_str = allowed_moves[action_index]
                game.make_move(next_state_str)
            else:  # Q-learning plays as O
                move = q_agent.play_select_move(game)
                game.make_move(move)

        if game.winner == 'X':
            dqn_wins += 1
        elif game.winner == 'O':
            q_wins += 1
        else:
            draws += 1

    print(f"Results over {num_games} games:")
    print(f"DQN wins: {dqn_wins}")
    print(f"Q-learning wins: {q_wins}")
    print(f"Draws: {draws}")

if __name__ == "__main__":
    evaluate(100)