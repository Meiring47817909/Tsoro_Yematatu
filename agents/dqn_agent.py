import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque

# --- Q-network ---
class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=64):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)  # Q-values for each possible move index


# --- Replay Buffer ---
class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action_index, reward, next_state, done):
        self.buffer.append((state, action_index, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (np.array(states),
                np.array(actions),
                np.array(rewards),
                np.array(next_states),
                np.array(dones))

    def __len__(self):
        return len(self.buffer)

# --- DQN Agent ---
class DQNAgent:
    def __init__(self, state_dim, action_dim, device=None,
                 epsilon=1.0, epsilon_min=0.01,
                 epsilon_decay=0.995, gamma=0.99,
                 lr=0.001, batch_size=64):

        self.state_dim = state_dim
        self.action_dim = action_dim
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.gamma = gamma
        self.batch_size = batch_size

        # Default device detection if none provided
        if device is None:
            if torch.cuda.is_available():
                device = torch.device("cuda")
            elif torch.backends.mps.is_available():
                device = torch.device("mps")
            else:
                device = torch.device("cpu")

        # 🔧 Store device properly
        self.device = device

        # Networks on device
        self.q_net = QNetwork(state_dim, action_dim).to(self.device)
        self.target_net = QNetwork(state_dim, action_dim).to(self.device)
        self.target_net.load_state_dict(self.q_net.state_dict())  # sync initially

        self.optimizer = optim.Adam(self.q_net.parameters(), lr=lr)
        self.replay_buffer = ReplayBuffer()

    def select_action(self, state, allowed_moves):
        """Select an action index corresponding to one of the allowed moves."""
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device) # Execute on device
        q_values = self.q_net(state_tensor).squeeze(0)

        valid_q_values = q_values[:len(allowed_moves)]

        if random.random() < self.epsilon:
            return random.randrange(len(allowed_moves))
        else:
            return torch.argmax(valid_q_values).item()

    def update(self):
        if len(self.replay_buffer) < self.batch_size:
            return  # not enough samples yet

        states, actions, rewards, next_states, dones = self.replay_buffer.sample(self.batch_size)

        states = torch.tensor(states, dtype=torch.float32).to(self.device) # Execute on device
        actions = torch.tensor(actions, dtype=torch.int64).to(self.device) # Execute on device
        rewards = torch.tensor(rewards, dtype=torch.float32).to(self.device) # Execute on device
        next_states = torch.tensor(next_states, dtype=torch.float32).to(self.device) # Execute on device
        dones = torch.tensor(dones, dtype=torch.float32).to(self.device) # Execute on device

        # Current Q-values
        q_values = self.q_net(states).gather(1, actions.unsqueeze(1)).squeeze(1)

        # Target Q-values
        with torch.no_grad():
            next_q_values = self.target_net(next_states).max(1)[0]
            targets = rewards + self.gamma * next_q_values * (1 - dones)

        # Loss and update
        loss = nn.MSELoss()(q_values, targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_target_network(self):
        self.target_net.load_state_dict(self.q_net.state_dict())

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    # --- Save and Load ---
    def save_model(self, filepath="dqn_model.pth"):
        torch.save(self.q_net.state_dict(), filepath)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath="dqn_model.pth"):
        self.q_net.load_state_dict(torch.load(filepath, map_location=self.device))
        self.target_net.load_state_dict(self.q_net.state_dict())
        print(f"Model loaded from {filepath}")
