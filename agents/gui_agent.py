import random

class GUIAgent:
    def __init__(self, game, gui=None, mode="random", rl_agent=None):
        self.game = game
        self.gui = gui
        self.turn = 0
        self.computer_player = 'X'
        self.mode = mode          # "random", or "qlearning"
        self.rl_agent = rl_agent  # trained agent if mode="qlearning"

    def play_computer_move(self):
        if self.mode == "qlearning" and self.rl_agent:
            return self.rl_agent.play_select_move(self.game)
        else:
            return random.choice(self.game.allowed_moves())

    def next_turn(self):
        if not self.game.playable():
            print(f"\nFinal Turn {self.turn}")
            self.gui.draw_board()
            print(f"\n{'The winner is ' + self.game.winner if self.game.winner else 'It\'s a draw!'}")
            return

        self.turn += 1
        print(f"\nTurn {self.turn}")

        if self.game.player == self.computer_player:
            move = self.play_computer_move()
            self.game.make_move(move)
            print(f"Computer ({self.computer_player}) made a move.")
            self.gui.draw_board()
            self.gui.root.after(500, self.next_turn)
        else:
            self.gui.move_done.set(False)
            self.check_human_move()

    def check_human_move(self):
        if self.gui.move_done.get():
            self.gui.draw_board()
            self.gui.root.after(500, self.next_turn)
        else:
            self.gui.root.after(100, self.check_human_move)

    def interactive_game(self, computer_player='X'):
        self.computer_player = computer_player
        self.gui.draw_board()
        self.gui.root.after(500, self.next_turn)
        self.gui.run()