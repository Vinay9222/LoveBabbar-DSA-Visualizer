import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches
import matplotlib as mpl

# ===============================
# Global UI Theme (Dark)
# ===============================
mpl.rcParams['figure.facecolor'] = '#111'
mpl.rcParams['axes.facecolor'] = '#111'
mpl.rcParams['text.color'] = 'white'
mpl.rcParams['font.weight'] = 'bold'


# ===============================
# Factorial Logic With Steps
# ===============================
def factorial_steps(n):
    steps = []
    result = [1]

    steps.append({
        "status": "start",
        "result": result.copy(),
        "carry": 0,
        "digit": None,
        "multiplier": None,
        "expression": "",
        "message": f"Starting computation of {n}! Initial value: 1"
    })

    for mul in range(2, n + 1):
        carry = 0

        steps.append({
            "status": "multiplying",
            "result": result.copy(),
            "carry": carry,
            "digit": None,
            "multiplier": mul,
            "expression": "",
            "message": f"Multiplying stored result by {mul}"
        })

        for i in range(len(result)):
            product = result[i] * mul + carry
            expression = f"{result[i]} × {mul} + {carry} = {product}"

            steps.append({
                "status": "digit-update",
                "result": result.copy(),
                "carry": carry,
                "digit": i,
                "multiplier": mul,
                "expression": expression,
                "message": f"Updating digit index {i}"
            })

            result[i] = product % 10
            carry = product // 10

            steps.append({
                "status": "carry-process",
                "result": result.copy(),
                "carry": carry,
                "digit": i,
                "multiplier": mul,
                "expression": f"Digit updated → {result[i]}, new carry → {carry}",
                "message": "Processing carry"
            })

        while carry:
            steps.append({
                "status": "carry-append",
                "result": result.copy(),
                "carry": carry,
                "digit": None,
                "multiplier": mul,
                "expression": f"Appending carry digit: {carry % 10}",
                "message": "Appending leftover carry to result"
            })

            result.append(carry % 10)
            carry //= 10

        steps.append({
            "status": "cycle-complete",
            "result": result.copy(),
            "carry": 0,
            "digit": None,
            "multiplier": mul,
            "expression": "",
            "message": f"Completed step with {mul}"
        })

    steps.append({
        "status": "done",
        "result": result.copy(),
        "carry": 0,
        "digit": None,
        "multiplier": None,
        "expression": "",
        "message": f"Final Result Ready"
    })

    return steps


# ===============================
# Visualization Controller
# ===============================
class FactorialVisualizer:
    def __init__(self, n):
        self.steps = factorial_steps(n)
        self.idx = 0

        self.fig, self.ax = plt.subplots(figsize=(14, 7))
        self.fig.subplots_adjust(bottom=0.22)

        # Buttons
        self.ax_prev = plt.axes([0.32, 0.05, 0.15, 0.09], facecolor="#333")
        self.ax_next = plt.axes([0.53, 0.05, 0.15, 0.09], facecolor="#444")

        self.btn_prev = Button(self.ax_prev, "⬅ Previous", color="#1B263B", hovercolor="#415A77")
        self.btn_next = Button(self.ax_next, "Next ➡", color="#1B263B", hovercolor="#415A77")

        self.btn_prev.on_clicked(self.prev)
        self.btn_next.on_clicked(self.next)

        # Keyboard event
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

        self.draw()

    # ==========================
    # Step Navigation
    # ==========================
    def next(self, event=None):
        if self.idx < len(self.steps) - 1:
            self.idx += 1
            self.draw()

    def prev(self, event=None):
        if self.idx > 0:
            self.idx -= 1
            self.draw()

    def on_key(self, event):
        if event.key == "right":
            self.next()
        elif event.key == "left":
            self.prev()

    # ==========================
    # Rendering Logic
    # ==========================
    def draw(self):
        self.ax.clear()
        step = self.steps[self.idx]

        # Header
        # self.ax.text(0.5, 1.05, f"STEP {self.idx + 1}/{len(self.steps)} - {step['status'].upper()}",
        #              ha='center', fontsize=18, fontweight='bold', transform=self.ax.transAxes)

        self.ax.text(0.5, 0.93, step["message"], ha="center", fontsize=14,
                     color="#00E5FF", transform=self.ax.transAxes)

        # Expression (human multiplication style)
        if step["expression"]:
            self.ax.text(0.5, 0.87, f"🧠 Operation: {step['expression']}",
                         ha="center", fontsize=16, color="#98FB98", transform=self.ax.transAxes)

        # Current Multiplier
        if step["multiplier"]:
            self.ax.text(0.5, 0.80, f"Multiplier: {step['multiplier']}",
                         fontsize=14, ha="center", color="yellow", transform=self.ax.transAxes)

        # Carry
        self.ax.text(0.5, 0.75, f"Carry: {step['carry']}",
                     fontsize=14, ha="center", color="#FFD369", transform=self.ax.transAxes)

        # Draw result digits
        digits = step["result"]
        start_x = 0.05
        spacing = 0.065

        for i, d in enumerate(digits):
            x = start_x + i * spacing
            box_color = "#007F5F" if step["digit"] == i else "#393E46"

            rect = patches.Rectangle((x, 0.45), 0.055, 0.10, edgecolor="white",
                                     facecolor=box_color, linewidth=2)
            self.ax.add_patch(rect)

            self.ax.text(x + 0.027, 0.495, str(d), ha="center", fontsize=16, color="white")

            # Index with spacing improvement ⬇
            self.ax.text(x + 0.027, 0.42, f"[{i}]", fontsize=9, ha="center", color="#999")

        # Final display
        if step["status"] == "done":
            final = ''.join(map(str, digits[::-1]))
            self.ax.text(0.5, 0.20, f"🎉 Final Result:\n{final}",
                         ha="center", fontsize=22, color="#00FF88")

        self.ax.axis("off")
        self.fig.canvas.draw_idle()


# ===============================
# RUN PROGRAM
# ===============================
if __name__ == "__main__":
    FactorialVisualizer(6)  # change here for bigger factorial
    plt.show()
