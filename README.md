# Tsoro Yematatu Reinforcement Learning Project

This project implements the traditional African board game **Tsoro Yematatu** and explores reinforcement learning approaches (tabular Q‑learning and Deep Q‑Networks) to train agents that can play the game. It also includes a Tkinter GUI for interactive play.

---

## 📂 Project Structure   
    tsoro_yematatu/
    │
    ├── game/
    │   ├── game_interface.py       # Abstract interface for games
    │   ├── tsoro_yematatu.py       # Tsoro Yematatu game rules & logic
    │   ├── board_gui.py            # Tkinter GUI for human play
    │
    ├── agents/
    │   ├── gui_agent.py            # GUI wrapper for human vs computer
    │   ├── qlearning_agent.py      # Tabular Q-learning agent
    │
    ├── training/
    │   ├── train_qlearning.py      # Train tabular Q-learning agent
    │
    ├── evaluation/
    │   ├── evaluate_agents.py      # Pit agents against each other
    │
    ├── main.py                     # Entry point for GUI play
    
## 🚀 Workflow

### 1. Train Agents
- **Q-learning (tabular):**
  ```bash
  python training/train_qlearning.py
  ```
Saves qlearning_table.pkl

### 2. Evaluate Agents
- **Run head‑to‑head matches between trained agents:**
  ```bash
  python evaluation/evaluate_agents.py
  ```
Outputs win/draw statistics.

### 3. Play GUI
- **Play interactively against computer opponents:**
  ```bash
  python main.py --mode qlearning --player O
  
### Options
- `--mode random` → computer plays random moves  
- `--mode qlearning` → computer uses trained Q‑learning agent  
- `--player X|O` → choose which side the computer plays  

### ✨ Features
Game logic fully encapsulated in TsoroYematatuGame.
Agents with consistent interfaces (select_action or play_select_move).
Training scripts separated from evaluation.
GUI with drag‑and‑drop and placement phases.
Save/load functionality for Q‑learning agent.
### 🔧 Requirements
Python 3.9+
Tkinter (usually included with Python)
### 📌 Notes
Q‑learning converges quickly to play Tsoro Yematatu.
GUI is for human play and visualization, not training.
