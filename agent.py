import random
from game_interface import GameInterface

class Agent:
    def __init__(self, game: GameInterface, gui=None):
        self.game = game
        self.gui = gui

    def play_random_move(self, game: GameInterface) -> str:
        return random.choice(game.allowed_moves())

    def request_human_move(self, game: GameInterface) -> str:
        allowed_moves = game.allowed_moves()
        phase = "placement" if game.state.count(" ") > 1 else "movement"

        print(f"Allowed {phase} moves for {game.player}:")
        for idx, move in enumerate(allowed_moves):
            diffs = [i for i, (old, new) in enumerate(zip("".join(game.state), move)) if old != new]

            if phase == "placement":
                point = [k for k, v in game.board.items() if v == diffs[0]][0]
                print(f"{idx}: {point}")
            else:
                removed_index = next(i for i in diffs if game.state[i] == game.player and move[i] == " ")
                added_index   = next(i for i in diffs if game.state[i] == " " and move[i] == game.player)

                from_pt = [k for k, v in game.board.items() if v == removed_index][0]
                to_pt   = [k for k, v in game.board.items() if v == added_index][0]

                print(f"{idx}: move piece at {from_pt} to {to_pt}")

        while True:
            try:
                idx = int(input("Enter move index: "))
                if 0 <= idx < len(allowed_moves):
                    return allowed_moves[idx]
                print("Invalid index, try again.")
            except ValueError:
                print("Please enter a valid number.")

    def interactive_game(self, computer_player='X'):
        turn = 0

        if self.gui:
            self.gui.draw_board()

        while self.game.playable():
            turn += 1
            print(f"\nTurn {turn}")

            if self.game.player == computer_player:
                move = self.play_random_move(self.game)
                self.game.make_move(move)
                print(f"Computer ({computer_player}) made a move.")
            else:
                move = self.request_human_move(self.game)
                self.game.make_move(move)

            if self.gui:
                self.gui.draw_board()
            else:
                self.game.print_board()

        print(f"\nFinal Turn {turn}")
        if self.gui:
            self.gui.draw_board()
        else:
            self.game.print_board()

        print(f"\n{'The winner is ' + self.game.winner if self.game.winner else 'It\'s a draw!'}")
        return self.game.winner or '-'