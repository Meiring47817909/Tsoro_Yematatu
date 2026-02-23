import tkinter as tk

class TsoroYematatuGUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Tsoro Yematatu Board")
        # Make canvas expand with window
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(expand=True, fill="both")

        # Bind resize event
        self.canvas.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Redraw board whenever window is resized."""
        self.draw_board(event.width, event.height)

    def draw_board(self, width=None, height=None):
        self.canvas.delete("all")

        # Use current canvas size if not provided
        if width is None: width = self.canvas.winfo_width()
        if height is None: height = self.canvas.winfo_height()

        # Positions scaled relative to canvas size
        positions = {
            "C1": (width/2, height*0.15),
            "M1": (width*0.25, height*0.4),
            "I":  (width/2, height*0.4),
            "M2": (width*0.75, height*0.4),
            "C2": (width*0.15, height*0.7),
            "M3": (width/2, height*0.7),
            "C3": (width*0.85, height*0.7),
        }

        # Connectors (adjacency lines)
        connectors = [
            ("C1","M1"), ("C1","I"), ("C1","M2"),
            ("M1","C2"), ("M1","I"),
            ("M2","C3"), ("M2","I"),
            ("C2","M3"), ("M3","C3"),
            ("I","M3")
        ]
        for a, b in connectors:
            x1, y1 = positions[a]
            x2, y2 = positions[b]
            self.canvas.create_line(x1, y1, x2, y2, width=2)

        # Draw nodes (scaled size)
        radius = min(width, height) * 0.05
        for label, (x, y) in positions.items():
            val = self.game.state[self.game.board[label]]
            display = val if val != " " else label
            self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="lightgray")
            self.canvas.create_text(x, y, text=display, font=("Arial", int(radius/2), "bold"))

    def run(self):
        self.draw_board()
        self.root.mainloop()