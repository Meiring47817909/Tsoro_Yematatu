from tsoro_yematatu import print_select_board
import random
from game_interface import GameInterface

class Agent:
    def __init__(self, game_class: type[GameInterface]):
        self.NewGame = game_class

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

    # Play against the AI
    def interactive_game(self, computer_player='X'):
        print_select_board()
        game = self.NewGame()
        turn = 0

        while game.playable():
            turn += 1
            print(f"\nTurn {turn}")

            if game.player == computer_player:
                move = self.play_random_move(game)
                if game.state.count(" ") > 1:
                    # Placement phase
                    playable_point_index = [
                        i for i, (old, new) in enumerate(zip("".join(game.state), move))
                        if old != new and new == game.player
                    ][0]
                    playable_point = [k for k, v in game.board.items() if v == playable_point_index][0]
                    print(f"Computer ({game.player}) chooses placement move: {playable_point}")
                else:
                    # Movement phase
                    diffs = [i for i, (old, new) in enumerate(zip("".join(game.state), move)) if old != new]

                    removed_index = next(i for i in diffs if game.state[i] == game.player and move[i] == " ")
                    added_index   = next(i for i in diffs if game.state[i] == " " and move[i] == game.player)

                    from_pt = [k for k, v in game.board.items() if v == removed_index][0]
                    to_pt   = [k for k, v in game.board.items() if v == added_index][0]

                    print(f"Computer ({game.player}) chooses piece move: {from_pt} => {to_pt}")

                game.make_move(move)
                game.print_board()   # <-- print immediately after move
            else:
                move = self.request_human_move(game)
                game.make_move(move)
                game.print_board()   # <-- print immediately after move

        print(f"\nFinal Turn {turn}")
        game.print_board()
        print(f"\n{"The winner is " + game.winner if game.winner else 'It\'s a draw!'}")
        return game.winner or '-'