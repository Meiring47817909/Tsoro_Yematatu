from tsoro_yematatu import print_select_board
import random
from game_interface import GameInterface

class Agent:
    def __init__(self, game_class: type[GameInterface]):
        self.board = {
            "C1": 0,
            "M1": 1,
            "I": 2,
            "M2": 3,
            "C2": 4,
            "M3": 5,
            "C3": 6,
        }
        self.NewGame = game_class

    def play_random_move(self, game: GameInterface) -> str:
        """Computer selects a random allowed move."""
        allowed_moves = game.allowed_moves()
        return random.choice(allowed_moves)

    def request_human_move(self, game: GameInterface) -> str:
        """Ask the human to select a move."""
        allowed_moves = game.allowed_moves()

        # Placement phase: more than one empty spot means pieces are still being placed
        if game.state.count(" ") > 1:
            print(f"Allowed placement moves for {game.player}:")

            for idx, move in enumerate(allowed_moves):
                # find index of the newly placed piece in the candidate move string
                playable_point_index = [
                    i for i, (old, new) in enumerate(zip("".join(game.state), move))
                    if old != new and new == game.player
                ][0]

                # convert that index to the board key name (e.g. "M2")
                playable_point = [
                    key for key, value in game.board.items() if value == playable_point_index
                ][0]

                print(f"{idx}: {playable_point}")
        else:
            print(f"Allowed pieces to be moved for {game.player}:")
            for idx, move in enumerate(allowed_moves):
                # find index of piece to be moved
                moveable_point_index = move.index(" ")
                # find point of piece to be moved
                moveable_point = [key for key, value in game.board.items() if value == moveable_point_index][0]

                # find index of the newly placed piece in the candidate move string
                playable_point_index = [
                    i for i, (old, new) in enumerate(zip("".join(game.state), move))
                    if old != new and new == game.player
                ][0]
                # convert that index to the board key name (e.g. "M2")
                playable_point = [
                    key for key, value in game.board.items() if value == playable_point_index
                ][0]

                print(f"{idx}: move piece at {moveable_point} to {playable_point}")
                print(f"{move}")

        choice = None
        while choice is None:
            try:
                idx = int(input("Enter the index of your chosen move: "))
                if 0 <= idx < len(allowed_moves):
                    choice = allowed_moves[idx]
                else:
                    print("Invalid index, try again.")
            except ValueError:
                print("Please enter a valid number.")
        return choice

    def interactive_game(self, computer_player='X'):
        """Run a full interactive game between human and computer."""
        print_select_board()
        game = self.NewGame()
        turn = 0

        while game.playable():
            print(f"\nTurn {turn}")
            game.print_board()

            if game.player == computer_player:
                move = self.play_random_move(game)

                if game.state.count(" ") > 1:
                    # Placement phase
                    playable_point_index = [
                        i for i, (old, new) in enumerate(zip("".join(game.state), move))
                        if old != new and new == game.player
                    ][0]
                    playable_point = [key for key, value in game.board.items()
                                    if value == playable_point_index][0]
                    print(f"Computer ({game.player}) chooses placement move: {playable_point}")
                else:
                    # Movement phase
                    # find index of piece moved (became " ")
                    moveable_point_index = [
                        i for i, (old, new) in enumerate(zip("".join(game.state), move))
                        if old == game.player and new == " "
                    ][0]
                    moveable_point = [key for key, value in game.board.items()
                                    if value == moveable_point_index][0]

                    # find index of new piece location
                    playable_point_index = [
                        i for i, (old, new) in enumerate(zip("".join(game.state), move))
                        if old != new and new == game.player
                    ][0]
                    playable_point = [key for key, value in game.board.items()
                                    if value == playable_point_index][0]

                    print(f"Computer ({game.player}) chooses piece move: {moveable_point} => {playable_point}")

                game.make_move(move)
            else:
                move = self.request_human_move(game)
                game.make_move(move)

            turn += 1

        print(f"\nFinal Turn {turn}")
        game.print_board()

        if game.winner:
            print(f"\n{game.winner} is the winner!")
            return game.winner
        else:
            print("\nIt's a draw!")
            return '-'