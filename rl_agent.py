# rl_agent.py
import random

class Agent:
    def __init__(self, game_class, epsilon=0.1, alpha=0.5, value_player='X'):
        # Dictionary to store estimated values of states (V[state] = value)
        self.V = dict()
        # Reference to the game class (used to create new game instances)
        self.NewGame = game_class
        # Exploration rate for epsilon-greedy strategy
        self.epsilon = epsilon
        # Learning rate for temporal difference updates
        self.alpha = alpha
        # The player this agent is learning values for (e.g., 'X')
        self.value_player = value_player

    def learn_game(self, num_episodes=1000):
        # Run multiple episodes to train the agent
        for episode in range(num_episodes):
            self.learn_from_episode()

    def learn_from_episode(self):
        # Start a new game
        game = self.NewGame()
        # Select the first move
        _, move = self.learn_select_move(game)
        # Continue learning until no moves are left
        while move:
            move = self.learn_from_move(game, move)

    def learn_select_move(self, game):
        # Get values for all allowed moves from current state
        allowed_state_values = self.__state_values(game.allowed_moves())
        
        # If it's the agent's turn, pick the move with max value
        if game.player == self.value_player:
            best_move = self.__argmax_V(allowed_state_values)
        else:
            # If it's the opponent's turn, assume they minimize the agent's value
            best_move = self.__argmin_V(allowed_state_values)

        # Default to best move, but with probability epsilon explore randomly
        selected_move = best_move
        if random.random() < self.epsilon:  # epsilon-greedy exploration
            selected_move = self.__random_V(allowed_state_values)

        return (best_move, selected_move)
    
    # --- Helper methods ---
    def __state_values(self, game_states):
        # Return dictionary of {state: value} for each possible game state
        return dict((state, self.state_value(state)) for state in game_states)
    
    def state_value(self, game_state):
        # Look up value of a state, default to 0.0 if unseen
        return self.V.get(game_state, 0.0)
    
    def __argmax_V(self, state_values):
        # Choose state(s) with maximum value, break ties randomly
        max_V = max(state_values.values())
        chosen_state = random.choice([state for state, v in state_values.items() if v == max_V])
        return chosen_state

    def __argmin_V(self, state_values):
        # Choose state(s) with minimum value, break ties randomly
        min_V = min(state_values.values())
        chosen_state = random.choice([state for state, v in state_values.items() if v == min_V])
        return chosen_state
    
    def __random_V(self, state_values):
        # Pick a random state from the available ones
        return random.choice(list(state_values.keys()))
    
    def learn_from_move(self, game, move):
        # Apply the move to the game
        game.make_move(move)
        # Get immediate reward from the resulting state
        r = self.__reward(game)
        
        # Initialize TD target
        td_target = r
        next_state_value = 0.0
        selected_next_move = None
        
        # If game is still playable, look ahead to next move
        if game.playable():
            best_next_move, selected_next_move = self.learn_select_move(game)
            next_state_value = self.state_value(best_next_move)
        
        # Current value estimate
        current_state_value = self.state_value(move)
        
        # TD target = reward + value of best next state
        td_target = r + next_state_value
        
        # Update rule: V(s) ← V(s) + α [TD_target - V(s)]
        self.V[move] = current_state_value + self.alpha * (td_target - current_state_value)
        
        # Return the next move to continue learning
        return selected_next_move

    def play_select_move(self, game):
        # When playing (not learning), select moves based on learned values
        allowed_state_values = self.__state_values(game.allowed_moves())
        if game.player == self.value_player:
            # Agent plays optimally (greedy)
            return self.__argmax_V(allowed_state_values)
        else:
            # Opponent plays randomly (could be changed to minimizer)
            return self.__random_V(allowed_state_values)

    def __reward(self, game):
        # Reward function:
        # +1 if agent wins, -1 if opponent wins, 0 otherwise
        if game.winner == self.value_player:
            return 1.0
        elif game.winner:
            return -1.0
        else:
            return 0.0

    def round_V(self):
        # Round values to one decimal place to stabilize action selection
        for k in self.V.keys():
            self.V[k] = round(self.V[k], 1)