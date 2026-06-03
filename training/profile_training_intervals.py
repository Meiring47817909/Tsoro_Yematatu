import sys
import os
import csv
import types

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.qlearning_agent import QLearningAgent
from game.tsoro_yematatu import TsoroYematatuGame

def main():
    agent = QLearningAgent(TsoroYematatuGame, epsilon=0.1)
    
    interval_game_lengths = []
    
    # We monkey-patch learn_from_episode to track game lengths
    def profiled_learn_from_episode(self):
        game = self.NewGame()
        _, move = self.learn_select_move(game)
        while move:
            move = self.learn_from_move(game, move)
            if game.alternate >= 50: # Hard cap at 50 turns
                break
        interval_game_lengths.append(game.alternate)
        
    agent.learn_from_episode = types.MethodType(profiled_learn_from_episode, agent)
    
    results = []
    
    print("Profiling training game lengths over 100-episode intervals...")
    for i in range(100, 1100, 100):
        # Clear the tracker for the new bucket
        interval_game_lengths.clear()
        
        # Train for 100 episodes
        agent.learn_game(100)
        
        # Calculate the average for THIS specific interval
        avg_turns = sum(interval_game_lengths) / len(interval_game_lengths)
        results.append((i, avg_turns))
        print(f"Interval {i-99} to {i}: Average Turns = {avg_turns:.2f}")

    csv_file = "training_intervals_profile.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Interval_End_Episode", "Avg_Turns"])
        for r in results:
            writer.writerow(r)
            
    print(f"\nData exported to {csv_file}")
    
    md = "\n## Live Training Profile (100-Episode Intervals)\n\n"
    md += "This tracks the average length of games *during* the training phase (with epsilon=0.1 active).\n\n"
    md += "| Interval (Episodes) | Avg Turns |\n"
    md += "|---|---|\n"
    for ep, avg in results:
        md += f"| {ep-99} to {ep} | {avg:.2f} |\n"
    md += "\n"
    
    with open("walkthrough_training_intervals.md", "w") as f:
        f.write(md)

if __name__ == "__main__":
    main()
