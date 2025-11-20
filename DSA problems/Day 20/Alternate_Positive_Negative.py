"""
Simplified Dark‑Mode Tkinter Visualization
Alternate Positive / Negative Arrangement (Option A – Keep Order)
Clean, simple, readable code (no complex ternary, no nested logic)
Run in VS Code with:  python app.py
"""

import tkinter as tk
from tkinter import font

# --------------------------------------------------
# STEP GENERATOR (simple and clean)
# --------------------------------------------------
def generate_steps(arr):
    pos = [x for x in arr if x >= 0]
    neg = [x for x in arr if x < 0]

    result = [None] * len(arr)
    steps = []

    i = j = k = 0

    steps.append({
        "arr": arr.copy(),
        "pos": pos.copy(),
        "neg": neg.copy(),
        "result": result.copy(),
        "i": i, "j": j, "k": k,
        "action": "Initialization complete"
    })

    while k < len(arr):
        if k % 2 == 0 and i < len(pos):
            result[k] = pos[i]
            steps.append({
                "arr": arr.copy(), "pos": pos.copy(), "neg": neg.copy(),
                "result": result.copy(),
                "i": i, "j": j, "k": k,
                "action": f"Placed POS {pos[i]} at index {k}"
            })
            i += 1

        elif k % 2 == 1 and j < len(neg):
            result[k] = neg[j]
            steps.append({
                "arr": arr.copy(), "pos": pos.copy(), "neg": neg.copy(),
                "result": result.copy(),
                "i": i, "j": j, "k": k,
                "action": f"Placed NEG {neg[j]} at index {k}"
            })
            j += 1

        k += 1

    steps.append({
        "arr": arr.copy(), "pos": pos.copy(), "neg": neg.copy(),
        "result": result.copy(),
        "i": i, "j": j, "k": k,
        "action": "Final result completed"
    })

    return steps


# --------------------------------------------------
# GUI APPLICATION (simple, no complex conditions)
# --------------------------------------------------
class VisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alternate Positive-Negative Visualizer — Simple Clean Version")
        self.root.configure(bg="#111111")

        # default array
        self.arr = [1, -3, 5, -2, 7, -8, 9, -6]
        self.steps = generate_steps(self.arr)
        self.index = 0

        # fonts
        self.title_font = font.Font(family="Arial", size=14, weight="bold")
        self.text_font = font.Font(family="Arial", size=12)
        self.small_font = font.Font(family="Arial", size=10)

        # canvas
        self.canvas = tk.Canvas(root, width=1100, height=700, bg="#111111", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        # bottom panel
        self.build_controls()

        # draw initial
        self.draw_step()

    # --------------------------------------------------
    # load user array
    # --------------------------------------------------
    def load_array(self):
        raw = self.entry.get().strip()
        try:
            arr = eval(raw, {"__builtins__": None}, {})
            if not isinstance(arr, list):
                raise ValueError

            clean = []
            for v in arr:
                clean.append(int(v))  # SIMPLE SAFE CONVERSION

            self.arr = clean
            self.steps = generate_steps(self.arr)
            self.index = 0
            self.draw_step()

        except:
            self.flash("Invalid array. Example: [1, -2, 3, -4]")

    # --------------------------------------------------
    def reset(self):
        self.arr = [1, -3, 5, -2, 7, -8, 9, -6]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(self.arr))
        self.steps = generate_steps(self.arr)
        self.index = 0
        self.draw_step()

    # --------------------------------------------------
    def build_controls(self):
        frame = tk.Frame(self.root, bg="#111111")
        frame.pack(pady=(0, 10))

        self.prev_btn = tk.Button(frame, text="◀ Previous", width=15, height=2,
                                  command=self.prev_step, bg="#222222", fg="white")
        self.prev_btn.pack(side="left", padx=10)

        self.next_btn = tk.Button(frame, text="Next ▶", width=15, height=2,
                                  command=self.next_step, bg="#00875A", fg="white")
        self.next_btn.pack(side="left", padx=10)

        tk.Label(frame, text="Array:", bg="#111111", fg="white", font=self.text_font).pack(side="left", padx=10)

        self.entry = tk.Entry(frame, width=30, bg="#1e1e1e", fg="white")
        self.entry.insert(0, str(self.arr))
        self.entry.pack(side="left")

        tk.Button(frame, text="Load", command=self.load_array, bg="#333", fg="white").pack(side="left", padx=6)
        tk.Button(frame, text="Reset", command=self.reset, bg="#333", fg="white").pack(side="left", padx=6)

    # --------------------------------------------------
    def flash(self, msg):
        t = self.canvas.create_text(30, 680, anchor="w", text=msg,
                                    font=self.small_font, fill="red")
        self.root.after(2000, lambda: self.canvas.delete(t))

    # --------------------------------------------------
    def next_step(self):
        if self.index < len(self.steps) - 1:
            self.index += 1
            self.draw_step()

    def prev_step(self):
        if self.index > 0:
            self.index -= 1
            self.draw_step()

    # --------------------------------------------------
    # DRAW ROW OF BOXES
    # --------------------------------------------------
    def draw_row(self, title, arr, y, ptr=None, label=None):
        self.canvas.create_text(40, y + 25, anchor="w", text=title,
                                font=self.text_font, fill="white")

        box_w = 70
        start_x = 200
        gap = 10

        for i, val in enumerate(arr):
            x1 = start_x + i * (box_w + gap)
            x2 = x1 + box_w
            y1 = y
            y2 = y + 50

            self.canvas.create_rectangle(x1, y1, x2, y2, outline="white", width=2)
            txt = "_" if val is None else str(val)
            self.canvas.create_text((x1 + x2) // 2, y1 + 25, text=txt,
                                    font=self.text_font, fill="#00FFFF")

            if ptr == i:
                self.canvas.create_text((x1 + x2) // 2, y2 + 15, text=label,
                                        font=self.small_font, fill="#FFFF00")

    # --------------------------------------------------
    def draw_step(self):
        self.canvas.delete("all")

        step = self.steps[self.index]

        # header
        self.canvas.create_text(550, 20, text="Alternate Positive-Negative ",
                                font=self.title_font, fill="white")

        # draw arrays
        self.draw_row("ORIGINAL", step["arr"], 70)
        self.draw_row("POSITIVE", step["pos"], 170,
                      ptr=step["i"] if step["i"] < len(step["pos"]) else None,
                      label="i → pos")
        self.draw_row("NEGATIVE", step["neg"], 280,
                      ptr=step["j"] if step["j"] < len(step["neg"]) else None,
                      label="j → neg")
        self.draw_row("RESULT", step["result"], 390,
                      ptr=step["k"] if step["k"] < len(step["result"]) else None,
                      label="k → result")

        # action box
        self.canvas.create_rectangle(180, 520, 1000, 580,
                                     outline="#FF9900", width=2)
        self.canvas.create_text(190, 550, anchor="w",
                                text=f"Step: {step['action']}",
                                font=self.text_font, fill="#FFA500")

        # footer (step number)
        self.canvas.create_text(900, 550,
                                text=f"{self.index + 1} / {len(self.steps)}",
                                font=self.text_font, fill="white")


# --------------------------------------------------
# RUN APP
# --------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    VisualizerApp(root)
    root.resizable(False, False)
    root.mainloop()
