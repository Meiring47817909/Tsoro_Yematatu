import sys
import os
import csv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.qlearning_agent import QLearningAgent
from game.tsoro_yematatu import TsoroYematatuGame

def evaluate_agents(agent1, agent2, num_games=100):
    agent1.value_player = 'X'
    agent2.value_player = 'X'
    
    wins = 0
    draws = 0
    losses = 0
    total_turns = 0
    
    e1, e2 = agent1.epsilon, agent2.epsilon
    agent1.epsilon, agent2.epsilon = 0.0, 0.0
    
    for _ in range(num_games):
        game = TsoroYematatuGame()
        while game.playable():
            if game.alternate >= 50:
                break
                
            if game.player == 'X':
                move = agent1.learn_select_move(game)[1]
            else:
                move = agent2.learn_select_move(game)[1]
                
            game.make_move(move)
            
        total_turns += game.alternate
        if game.winner == 'X':
            wins += 1
        elif game.winner == 'O':
            losses += 1
        else:
            draws += 1
            
    agent1.epsilon, agent2.epsilon = e1, e2
    agent1.value_player = 'X'
    agent2.value_player = 'X'
    
    return wins, draws, losses, total_turns / num_games

def main():
    print("Loading Master Agent (1000 Episodes)...")
    master = QLearningAgent(TsoroYematatuGame)
    master.load("qlearning_table1000.pkl")
    
    results = []
    
    for i in range(100, 1100, 100):
        print(f"Loading Opponent Agent ({i} Episodes)...")
        opponent = QLearningAgent(TsoroYematatuGame)
        opponent.load(f"qlearning_table{i}.pkl")
        
        # Master as 'X' vs Opponent as 'O'
        w1, d1, l1, avg1 = evaluate_agents(master, opponent, 100)
        
        # Master as 'O' vs Opponent as 'X'
        # In evaluate_agents, agent1 is 'X' and agent2 is 'O'.
        # We pass opponent as agent1 and master as agent2.
        w2, d2, l2, avg2 = evaluate_agents(opponent, master, 100)
        
        # We want the results from Master's perspective.
        # w2 is Opponent win, l2 is Opponent loss (Master win)
        master_w2 = l2
        master_l2 = w2
        master_d2 = d2
        
        total_w = w1 + master_w2
        total_d = d1 + master_d2
        total_l = l1 + master_l2
        avg_turns = (avg1 + avg2) / 2
        
        results.append((i, total_w, total_d, total_l, avg_turns))
        
    csv_file = "master_evaluation.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Opponent_Episodes", "Master_Wins", "Draws", "Master_Losses", "Avg_Turns"])
        for r in results:
            writer.writerow(r)

    md = "## Master Agent (1000) vs Historical Checkpoints (200 games per opponent)\n\n"
    md += "The 1000-episode Master agent played 100 games as 'X' and 100 games as 'O' against each of its historical checkpoints.\n\n"
    md += "| Opponent | Master Wins | Draws | Master Losses | Avg Turns |\n"
    md += "|---|---|---|---|---|\n"
    for ep, w, d, l, avg_len in results:
        md += f"| Checkpoint {ep} | {w} | {d} | {l} | {avg_len:.2f} |\n"
    md += "\n"
        
    with open("walkthrough_master_eval.md", "w") as f:
        f.write(md)
        
    print(f"Evaluation complete! Markdown saved to walkthrough_master_eval.md and data exported to {csv_file}")

if __name__ == "__main__":
    main()
