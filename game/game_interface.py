from abc import ABC, abstractmethod
from typing import List

class GameInterface(ABC):
    @abstractmethod
    def allowed_moves(self) -> List[str]:
        """Return a list of allowed next states as strings."""
        pass

    @abstractmethod
    def make_move(self, next_state: str) -> None:
        """Make a move to the given next state."""
        pass

    @abstractmethod
    def playable(self) -> bool:
        """Return True if the game is still playable."""
        pass

    @abstractmethod
    def predict_winner(self, state: List[str]) -> str:
        """Predict the winner based on the given state."""
        pass

    # @abstractmethod
    # def print_board(self) -> None:
    #     """Print the current board state."""
    #     pass

    @property
    @abstractmethod
    def state(self):
        """The current state of the game."""
        pass

    @property
    @abstractmethod
    def player(self):
        """The current player."""
        pass

    @property
    @abstractmethod
    def winner(self):
        """The winner of the game, if any."""
        pass