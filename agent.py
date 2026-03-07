import random
from game_interface import GameInterface

class Agent:
    def __init__(self, game, gui=None):
        self.game = game
        self.gui = gui
        self.turn = 0
        self.computer_player = 'X'

    def play_random_move(self):
        return random.choice(self.game.allowed_moves())

    def next_turn(self):
        # If game is no longer playable, show result and stop
        if not self.game.playable():
            print(f"\nFinal Turn {self.turn}")
            self.gui.draw_board()
            print(f"\n{'The winner is ' + self.game.winner if self.game.winner else 'It\'s a draw!'}")
            return

        self.turn += 1
        print(f"\nTurn {self.turn}")

        if self.game.player == self.computer_player:
            move = self.play_random_move()
            self.game.make_move(move)
            print(f"Computer ({self.computer_player}) made a move.")
            self.gui.draw_board()
            # Schedule next turn
            self.gui.root.after(500, self.next_turn)
        else:
            # Human move: wait until GUI sets move_done
            self.gui.move_done.set(False)
            # Poll until move_done is True
            self.check_human_move()

    def check_human_move(self):
        if self.gui.move_done.get():
            self.gui.draw_board()
            self.gui.root.after(500, self.next_turn)
        else:
            # Check again after 100ms
            self.gui.root.after(100, self.check_human_move)

    def interactive_game(self, computer_player='X'):
        self.computer_player = computer_player
        self.gui.draw_board()
        self.gui.root.after(500, self.next_turn)
        self.gui.run()

    