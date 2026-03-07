'''
   Copyright 2017 Neil Slater
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
   The original code as been modified for educational purposes.
'''

from game_interface import GameInterface

class TsoroYematatuGame(GameInterface):
    def __init__(self):
        self.board = {
            "C1": 0,
            "M1": 1,
            "I": 2,
            "M2": 3,
            "C2": 4,
            "M3": 5,
            "C3": 6,
        }      
        self._state = ["_"] * 7  # a string of length 7 that encodes the state of the board 
        self._player = 'X'
        self.alternate = 0
        self._winner = None

    @property
    def state(self):
        return self._state

    @property
    def player(self):
        return self._player

    @property
    def winner(self):
        return self._winner

    # State space of available moves
    def allowed_moves(self):
        states = [] # Store all possible next states

        # First both players place all 3 their pieces on the board on any vacant points
        if self.alternate < 6:
            for i in range(len(self._state)):
                if self._state[i] == "_":  # if the point is vacant
                    new_state = list(self._state)   # copy current state
                    new_state[i] = self._player     # place piece
                    states.append("".join(new_state))  # store as string snapshot

        # After all pieces have been placed they can be moved
        else:
            # Find the vacant point
            # Example board is: "XXO_OOX"
            vacant_point_index = [i for i, val in enumerate(self._state) if val == "_"][0] # Example: 3
            vacant_point_key = [key for key, value in self.board.items() if value == vacant_point_index][0] # Example: m2

            # Get indexes where current player's pieces are located
            player_piece_indexes = [i for i, val in enumerate(self._state) if val == self._player] # Example: [0, 1, 6]

            # Convert indexes to board keys
            keys_for_values = []
            for player_piece_index in player_piece_indexes:
                for key, value in self.board.items():
                    if value == player_piece_index:
                        keys_for_values.append(key)
                        break
            # Example: [c1, m1, c3]

            # Move type 1: Move one space
            # adjacency map: Identify all adjacent points a piece can move to.
            adjacency = {
                "C1": ["M1", "M2", "I"],
                "C2": ["M1", "M3"],
                "C3": ["M2", "M3"],
                "M1": ["C1", "C2", "I"],
                "M2": ["C1", "C3", "I"],
                "M3": ["C2", "C3", "I"],
                "I":  ["M1", "M2", "M3", "C1"],
            }

            for key in keys_for_values:  # each piece the current player owns
                if vacant_point_key in adjacency[key]:  # check if vacant spot is adjacent
                    # build new state string with piece moved
                    new_state = list(self._state)  # convert to list for mutability
                    new_state[self.board[key]] = "_"  # clear old position
                    new_state[self.board[vacant_point_key]] = self._player  # place piece at vacant spot
                    states.append("".join(new_state))

            # Move type 2: Jump over an adjacent piece
            # jump rules map: Identify all landing points a piece can jump to over an intermediate piece.
            jump_rules = { # Each starting point maps to (landing, intermediate)
                "C1": [("C2", "M1"), ("C3", "M2"), ("M3", "I")],
                "C2": [("C1", "M1"), ("C3", "M3")],
                "C3": [("C1", "M2"), ("C2", "M3")],
                "M1": [("M2", "I")],
                "M2": [("M1", "I")],
                "M3": [("C1", "I")],
            }

            for key in keys_for_values: # each piece the current player owns
                if key in jump_rules:
                    for landing, intermediate in jump_rules[key]:
                        # Check if landing spot is the vacant point
                        if vacant_point_key == landing:
                            # Landing must be empty, intermediate must be occupied
                            if (self._state[self.board[landing]] == "_" and self._state[self.board[intermediate]] in ["X", "O"]):                           
                                new_state = list(self._state) # Build new state string with piece jumped
                                new_state[self.board[key]] = "_" # clear old position
                                new_state[self.board[landing]] = self._player # place piece at landing
                                states.append("".join(new_state))
        return states
    
    # Make move
    def make_move(self, next_state):
        if self._winner:
            raise(Exception("Game already completed, cannot make another move!"))
        if not self.__valid_move(next_state):
            raise(Exception("Cannot make move {} to {} for player {}".format(
                    self._state, next_state, self._player)))

        self._state = list(next_state)
        self.alternate += 1
        
        self._winner = self.predict_winner(self._state)
        if self._winner:
            self._player = None
        elif self._player == 'X':
            self._player = 'O'
        else:
            self._player = 'X'

    def __valid_move(self, next_state):
        allowed_moves = self.allowed_moves()  #get all possible next states
        if any(state == next_state for state in allowed_moves): #check if the input next_state is in 
            return True
        return False
    
    def playable(self):
        return ( (not self._winner) and any(self.allowed_moves()) )

    def predict_winner(self, state):
        # Create win line indexes:
        winLines = [
            ["C1", "M1", "C2"],
            ["C1", "I", "M3"], 
            ["C1", "M2", "C3"], 
            ["M1", "I", "M2"], 
            ["C2", "M3", "C3"]
        ]
    
        # indexWinLines = [[0, 1, 4], [0, 2, 5], [0, 3, 6], [1, 2, 3], [4, 5, 6]]
        indexWinLines = [[self.board[k] for k in line] for line in winLines]

        winner = None
        for line in indexWinLines:
            line_state = state[line[0]] + state[line[1]] + state[line[2]]
            if line_state == 'XXX':
                winner = 'X'
            elif line_state == 'OOO':
                winner = 'O'
        return winner