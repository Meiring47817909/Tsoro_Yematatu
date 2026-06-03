# Renamed for clarity. Added save/load methods so you can persist the Q‑table.

import random
import pickle

class QLearningAgent:
    def __init__(self, game_class, epsilon=0.1, alpha=0.5, value_player='X'):
        self.V = dict()              # state-value table
        self.NewGame = game_class    # reference to game class
        self.epsilon = epsilon       # exploration rate
        self.alpha = alpha           # learning rate
        self.value_player = value_player

    def learn_game(self, num_episodes):
        for _ in range(num_episodes):
            self.learn_from_episode()

    def learn_from_episode(self):
        game = self.NewGame()
        _, move = self.learn_select_move(game)
        while move:
            move = self.learn_from_move(game, move)
            if game.alternate >= 50: # Cap at 50 turns
                break

    def learn_select_move(self, game):
        allowed_state_values = self.__state_values(game.allowed_moves())
        if game.player == self.value_player:
            best_move = self.__argmax_V(allowed_state_values)
        else:
            best_move = self.__argmin_V(allowed_state_values)

        selected_move = best_move
        if random.random() < self.epsilon:
            selected_move = self.__random_V(allowed_state_values)
        return (best_move, selected_move)

    def __state_values(self, game_states):
        return {state: self.state_value(state) for state in game_states}

    def state_value(self, game_state):
        return self.V.get(game_state, 0.0)

    def __argmax_V(self, state_values):
        max_V = max(state_values.values())
        return random.choice([s for s, v in state_values.items() if v == max_V])

    def __argmin_V(self, state_values):
        min_V = min(state_values.values())
        return random.choice([s for s, v in state_values.items() if v == min_V])

    def __random_V(self, state_values):
        return random.choice(list(state_values.keys()))

    def learn_from_move(self, game, move):
        game.make_move(move)
        r = self.__reward(game)

        next_state_value = 0.0
        selected_next_move = None

        if game.playable():
            best_next_move, selected_next_move = self.learn_select_move(game)
            next_state_value = self.state_value(best_next_move)

        current_state_value = self.state_value(move)
        td_target = r + next_state_value

        self.V[move] = current_state_value + self.alpha * (td_target - current_state_value)
        return selected_next_move

    def play_select_move(self, game):
        allowed_state_values = self.__state_values(game.allowed_moves())
        if game.player == self.value_player:
            return self.__argmax_V(allowed_state_values)
        else:
            return self.__argmin_V(allowed_state_values)
    
    def __reward(self, game):
        if game.winner == self.value_player: 
            return 1.0 - (game.alternate * 0.01)
        elif game.winner: 
            return -1.0 + (game.alternate * 0.01)
        return 0.0

    def save(self, filepath="qlearning_table.pkl"):
        with open(filepath, "wb") as f:
            pickle.dump(self.V, f)
        print(f"Q-table saved to {filepath}")

    def load(self, filepath="qlearning_table.pkl"):
        with open(filepath, "rb") as f:
            self.V = pickle.load(f)
        print(f"Q-table loaded from {filepath}")