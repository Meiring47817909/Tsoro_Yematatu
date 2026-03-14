import torch
from agents.dqn_agent import DQNAgent
from game.tsoro_yematatu import TsoroYematatuGame

def encode_state(game):
    return [1 if c == 'X' else -1 if c == 'O' else 0 for c in game.state]

def agent_reward(game):
    if game.winner == 'X': return 1.0
    if game.winner == 'O': return -1.0
    return 0.0

def train_dqn(num_episodes=5000, target_update_freq=100):
    # Detect device (GPU if available, else CPU)
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("GPU:", torch.cuda.get_device_name(0))
    elif torch.backends.mps.is_available():
        device = torch.device("mps")  # Apple Silicon
        print("Apple Silicon GPU (MPS) detected")
    else:
        device = torch.device("cpu")
        import platform
        print("CPU:", platform.processor() or "Generic CPU")

    print("Training on:", device)

    # Initialize agent on chosen device
    agent = DQNAgent(state_dim=7, action_dim=7, device=device)

    for episode in range(num_episodes):
        game = TsoroYematatuGame()
        state = encode_state(game)
        done = False

        while not done:
            allowed_moves = game.allowed_moves()
            action_index = agent.select_action(state, allowed_moves)
            next_state_str = allowed_moves[action_index]

            game.make_move(next_state_str)
            reward = agent_reward(game)
            next_state = encode_state(game)
            done = not game.playable()

            agent.replay_buffer.push(state, action_index, reward, next_state, done)
            agent.update()
            state = next_state

        agent.decay_epsilon()
        if episode % target_update_freq == 0:
            agent.update_target_network()

        if (episode + 1) % 500 == 0:
            print(f"Episode {episode+1}, Epsilon: {agent.epsilon:.2f}")

    agent.save_model("dqn_tsoro.pth")
    print("Training complete, model saved.")
    return agent

if __name__ == "__main__":
    train_dqn(5000)