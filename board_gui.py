import tkinter as tk

class TsoroYematatuGUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Tsoro Yematatu Board")
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(expand=True, fill="both")
        self.canvas.bind("<Configure>", self.on_resize)

        self.move_done = tk.BooleanVar(value=False)  # signal for Agent loop
        self.dragging_piece = None
        self.drag_start_label = None
        self.node_ovals = {}
        self.node_texts = {}

    def on_resize(self, event):
        self.draw_board(event.width, event.height)

    def draw_board(self, width=None, height=None):
        self.canvas.delete("all")
        if width is None: width = self.canvas.winfo_width()
        if height is None: height = self.canvas.winfo_height()

        # Scaled positions
        self.positions = {
            "C1": (width/2, height*0.15),
            "M1": (width*0.25, height*0.4),
            "I":  (width/2, height*0.4),
            "M2": (width*0.75, height*0.4),
            "C2": (width*0.15, height*0.7),
            "M3": (width/2, height*0.7),
            "C3": (width*0.85, height*0.7),
        }

        connectors = [
            ("C1","M1"), ("C1","I"), ("C1","M2"),
            ("M1","C2"), ("M1","I"),
            ("M2","C3"), ("M2","I"),
            ("C2","M3"), ("M3","C3"),
            ("I","M3")
        ]
        for a,b in connectors:
            x1,y1 = self.positions[a]; x2,y2 = self.positions[b]
            self.canvas.create_line(x1,y1,x2,y2,width=2)

        radius = min(width,height)*0.05
        for label,(x,y) in self.positions.items():
            val = self.game.state[self.game.board[label]]

            # Decide display text and color
            if val == "X":
                display = "X"
                fill_color = "blue"
            elif val == "O":
                display = "O"
                fill_color = "red"
            else:
                display = label
                fill_color = "lightgray"

            # Always start with lightgray fill
            oval_id = self.canvas.create_oval(
                x-radius, y-radius, x+radius, y+radius,
                fill=fill_color, outline="black"
            )
            self.node_ovals[label] = oval_id

            # Text shows either X, O, or label
            text_id = self.canvas.create_text(
                x, y, text=display,
                font=("Arial", int(radius/2), "bold")
            )
            self.node_texts[label] = text_id

            if self.game.state.count("_") > 1:
                # Placement phase: clicks only
                self.canvas.tag_bind(oval_id,"<Button-1>",lambda e,l=label:self.on_click(l))
                self.canvas.tag_bind(text_id,"<Button-1>",lambda e,l=label:self.on_click(l))
            else:
                # Movement phase: drag only
                self.canvas.tag_bind(oval_id,"<ButtonPress-1>",lambda e,l=label:self.start_drag(l))
                self.canvas.tag_bind(oval_id,"<ButtonRelease-1>",lambda e,l=label:self.end_drag(l))

            # Hover highlight always active
            self.canvas.tag_bind(
                oval_id, "<Enter>",
                lambda e,i=oval_id,l=label: self.highlight_node(i, True, l)
            )
            self.canvas.tag_bind(
                oval_id, "<Leave>",
                lambda e,i=oval_id,l=label: self.highlight_node(i, False, l)
            )


    def highlight_node(self, item_id, active, label=None):
        """Change oval color on hover only if node is empty."""
        idx = self.game.board[label]
        val = self.game.state[idx]

        if val == "X":
            base_color = "blue"
        elif val == "O":
            base_color = "red"
        else:
            base_color = "lightgray"

        if val == "_":  # only highlight empty nodes
            color = "yellow" if active else base_color
        else:
            color = base_color  # occupied nodes keep their color

        self.canvas.itemconfig(item_id, fill=color)

    def on_click(self,label):
        if self.game.state.count("_") > 1:
            idx = self.game.board[label]
            if self.game.state[idx] == "_":
                new_state = list(self.game.state)
                new_state[idx] = self.game.player
                candidate = "".join(new_state)
                if candidate in self.game.allowed_moves():
                    self.game.make_move(candidate)
                    self.move_done.set(True)
                    # Update text immediately
                    self.canvas.itemconfig(self.node_texts[label], text=self.game.player)
                    # Animate oval from gray to player color
                    color = "blue" if self.game.player == "X" else "red"
                    self.animate_fill(self.node_ovals[label], "lightgray", color)

    def start_drag(self,label):
        if self.game.state.count("_") <= 1:
            idx = self.game.board[label]
            if self.game.state[idx] == self.game.player:
                print("Start drag:", label)
                self.dragging_piece = label
                self.drag_start_label = label
                # Bind motion
                self.canvas.bind("<Motion>", self.drag_motion)

    def drag_motion(self, event):
        if self.dragging_piece:
            # Show a temporary circle following the mouse
            if hasattr(self, "drag_preview"):
                self.canvas.delete(self.drag_preview)
            r = 20
            self.drag_preview = self.canvas.create_oval(
                event.x-r, event.y-r, event.x+r, event.y+r,
                fill="lightblue", outline="blue"
            )

    def end_drag(self, label=None):
        if self.dragging_piece and self.game.state.count("_") <= 1:
            # Find nearest node to mouse release
            x, y = self.root.winfo_pointerx() - self.root.winfo_rootx(), \
                self.root.winfo_pointery() - self.root.winfo_rooty()
            nearest = min(self.positions.items(),
                        key=lambda kv: (kv[1][0]-x)**2 + (kv[1][1]-y)**2)[0]

            vacant_idx = self.game.board[nearest]
            if self.game.state[vacant_idx] == "_":
                new_state = list(self.game.state)
                new_state[self.game.board[self.drag_start_label]] = "_"
                new_state[vacant_idx] = self.game.player
                candidate = "".join(new_state)
                if candidate in self.game.allowed_moves():
                    self.game.make_move(candidate)
                    self.move_done.set(True)
                    # Update texts
                    self.canvas.itemconfig(self.node_texts[self.drag_start_label], text=self.drag_start_label)
                    self.canvas.itemconfig(self.node_texts[nearest], text=self.game.player)
                    # Animate fade out at start node
                    self.animate_fill(self.node_ovals[self.drag_start_label],
                                    "blue" if self.game.player=="X" else "red",
                                    "lightgray")
                    # Animate fill at target node
                    color = "blue" if self.game.player == "X" else "red"
                    self.animate_fill(self.node_ovals[nearest], "lightgray", color)
                else:
                    print("Invalid move rejected:", candidate)
        self.dragging_piece = None
        self.drag_start_label = None
        self.canvas.unbind("<Motion>")
        if hasattr(self, "drag_preview"):
            self.canvas.delete(self.drag_preview)
            del self.drag_preview

    def animate_fill(self, item_id, start_color, end_color, steps=20, delay=15):
        sr, sg, sb = self.canvas.winfo_rgb(start_color)
        er, eg, eb = self.canvas.winfo_rgb(end_color)

        def step(i=0):
            if i > steps: return
            r = int(sr + (er - sr) * i / steps) // 256
            g = int(sg + (eg - sg) * i / steps) // 256
            b = int(sb + (eb - sb) * i / steps) // 256
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.itemconfig(item_id, fill=hex_color)
            self.root.after(delay, lambda: step(i+1))

        step()

    def run(self):
        self.draw_board()
        self.root.mainloop()