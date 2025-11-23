import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button

# ---------------------------
# USER CONFIGURABLE INPUT
# ---------------------------
# Change this array to visualize other examples.
ARRAY = [-2, 6, -3, -10, 0, 2]  # Example with positives, negatives and zero.
# ---------------------------

# ---------- Algorithm: compute steps and store detailed records ----------
def compute_max_product_steps(arr):
    steps = []
    n = len(arr)
    if n == 0:
        return steps

    # Initialization for index 0
    cur_max = arr[0]
    cur_min = arr[0]
    global_max = arr[0]

    explanation = f"Start → index 0 value = {arr[0]} → initialize cur_max, cur_min, global_max"
    step0 = {
        "index": 0,
        "value": arr[0],
        "cur_max": cur_max,
        "cur_min": cur_min,
        "global_max": global_max,
        "swap": False,
        "reset": (arr[0] == 0),
        "flags": ["processing"] if n > 1 else ["final"],
        "explanation": explanation,
        "global_update": True  # initial sets global
    }
    steps.append(step0)

    # Process remaining elements
    for i in range(1, n):
        val = arr[i]
        swap = False
        reset = False
        flags = ["processing"]

        prev_cur_max = cur_max
        prev_cur_min = cur_min
        prev_global = global_max

        explanation_parts = [f"Index {i} → value = {val}"]

        if val == 0:
            # Zero encountered: it's a reset point for subarray products.
            reset = True
            # After zero, the best we can have up to this index is 0.
            cur_max = 0
            cur_min = 0
            explanation_parts.append("Zero encountered → reset cur_max and cur_min to 0")
        else:
            # If val is negative, swapping cur_max and cur_min before multiplication
            if val < 0:
                swap = True
                # swap logically for the multiplication effect
                temp_max = prev_cur_min
                temp_min = prev_cur_max
                explanation_parts.append("Negative detected → swap prev cur_max and cur_min (before multiply)")
            else:
                temp_max = prev_cur_max
                temp_min = prev_cur_min

            # compute candidates
            # Three possibilities: val alone, val * temp_max, val * temp_min
            candidate1 = val
            candidate2 = val * temp_max
            candidate3 = val * temp_min

            cur_max = max(candidate1, candidate2, candidate3)
            cur_min = min(candidate1, candidate2, candidate3)

            explanation_parts.append(
                f"Computed candidates → [{candidate1}, {candidate2}, {candidate3}] → "
                f"cur_max = {cur_max}, cur_min = {cur_min}"
            )

        # update global
        global_update = False
        if cur_max > global_max:
            global_update = True
            explanation_parts.append(f"Updated global max from {global_max} → {cur_max}")
            global_max = cur_max

        # Compose flags
        if swap:
            flags.append("swap-triggered")
        if reset:
            flags.append("reset")
        if global_update:
            flags.append("global-update")

        # If this was the final array element, add final flag
        if i == n - 1:
            flags.append("final")
            explanation_parts.append("Final step reached.")

        step = {
            "index": i,
            "value": val,
            "cur_max": cur_max,
            "cur_min": cur_min,
            "global_max": global_max,
            "swap": swap,
            "reset": reset,
            "flags": flags,
            "explanation": " → ".join(explanation_parts),
            "global_update": global_update
        }

        steps.append(step)

    return steps


# ---------- Visualization: matplotlib interactive UI ----------
class MaxProductVisualizer:
    def __init__(self, arr, steps):
        self.arr = arr
        self.steps = steps
        self.n = len(arr)
        self.idx = 0  # current step index
        # Create figure and axes
        self.fig = plt.figure(figsize=(14, 6), facecolor="#111111")
        # main axis for drawing boxes
        self.ax = self.fig.add_axes([0.05, 0.20, 0.90, 0.65], facecolor="#111111")
        self.ax.set_xlim(0, max(10, self.n))
        self.ax.set_ylim(0, 10)
        self.ax.axis("off")

        # Message area (top explanation)
        self.info_ax = self.fig.add_axes([0.05, 0.8, 0.90, 0.10], facecolor="#111111")
        self.info_ax.axis("off")

        # Bottom status area
        self.status_ax = self.fig.add_axes([0.05, 0.02, 0.90, 0.16], facecolor="#111111")
        self.status_ax.axis("off")

        # Buttons
        axprev = self.fig.add_axes([0.33, 0.09, 0.12, 0.06])
        axnext = self.fig.add_axes([0.55, 0.09, 0.12, 0.06])

        # Button styling: create Buttons and attach callbacks
        self.bprev = Button(axprev, "⬅️ Previous")
        self.bnext = Button(axnext, "Next ➡️")
        # Set button facecolors in a subtle way, but we can't set color palettes across backends consistently.
        # We'll set the button text properties and use the button's color attributes where supported.
        try:
            axprev.set_facecolor("#222222")
            axnext.set_facecolor("#222222")
        except Exception:
            pass

        self.bprev.on_clicked(self.on_prev)
        self.bnext.on_clicked(self.on_next)

        # Title / header
        self.fig.suptitle("Maximum Product Subarray",
                          color="white", fontsize=18, fontweight="bold", y=0.97)

        # Initial draw
        self.draw_step(self.idx)

    def draw_boxes(self, active_idx, step):
        self.ax.clear()
        self.ax.set_xlim(0, max(10, self.n))
        self.ax.set_ylim(0, 10)
        self.ax.axis("off")

        # box geometry
        total_width = max(0.8 * self.n, 8)
        box_w = max(0.8, total_width / (self.n + 1))
        spacing = box_w * 0.2
        start_x = 1.0

        # draw each box
        for i, val in enumerate(self.arr):
            x = start_x + i * (box_w + spacing)
            y = 5.0
            # default style
            facecolor = "#222222"
            edgecolor = "#555555"
            linewidth = 1.0

            # highlight logic for the active index
            if i == active_idx:
                edgecolor = "cyan"
                linewidth = 3.0

                # Swap event
                if step["swap"]:
                    facecolor = "#6b5700"  # a yellowish tone
                # Reset
                if step["reset"]:
                    facecolor = "#7a0b0b"  # red tone
                # Global update
                if step["global_update"]:
                    facecolor = "#044d13"  # green tone

            # Additionally, if the global_max equals the value at this index (rare),
            # we won't attempt to find subarray; we only color the active index as required.
            rect = Rectangle((x, y), box_w, 1.6, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth, zorder=2)
            self.ax.add_patch(rect)
            # Value text: big and bold
            self.ax.text(x + box_w / 2, y + 0.8, str(val),
                         color="white", fontsize=14, fontweight="bold",
                         ha="center", va="center", zorder=3)

            # index label below the box
            self.ax.text(x + box_w / 2, y - 0.2, f"idx {i}",
                         color="#bbbbbb", fontsize=10, ha="center", va="top")

            # if this step updated global and it's the active index, mark global value bubble
            if i == active_idx and step["global_update"]:
                gm = step["global_max"]
                self.ax.text(x + box_w / 2, y + 2.0, f"GLOBAL → {gm}",
                             color="#8bff9b", fontsize=11, fontweight="bold", ha="center")

        # small legend / cue boxes on the side
        # legend_x = start_x + (self.n + 0.2) * (box_w + spacing)
        # ly = 6.8
        # legend_items = [
        #     ("Active index", "cyan"),
        #     ("Swap event", "#e6c85b"),
        #     ("Zero reset", "#e57373"),
        #     ("Global update", "#6ed58f")
        # ]
        # for k, (label, color) in enumerate(legend_items):
        #     self.ax.add_patch(Rectangle((legend_x, ly - k * 0.6), 0.6, 0.35, facecolor=color, edgecolor="#444444"))
        #     self.ax.text(legend_x + 0.7, ly - k * 0.6 + 0.17, label, color="white", fontsize=10, va="center")

    def draw_info(self, step):
        """
        Top explanation message area.
        """
        self.info_ax.clear()
        self.info_ax.axis("off")

        explanation = step["explanation"]
        # wrap short if too long — simple split for this UI
        self.info_ax.text(0.01, 0.55, f"Step {step['index'] + 1}/{len(self.steps)}",
                          color="#cccccc", fontsize=12, fontweight="bold", va="center")
        self.info_ax.text(0.20, 0.5, explanation,
                          color="white", fontsize=12, fontweight="bold", va="center")

    def draw_status(self, step):
        """
        Bottom status showing cur_max, cur_min, global, flags and final result if final.
        """
        self.status_ax.clear()
        self.status_ax.axis("off")

        # left side: running values
        left_x = 0.02
        top_y = 2.5
        line_h = 0.28

        self.status_ax.text(left_x, top_y, f"Index pointer → {step['index']}",
                            color="#ffffff", fontsize=12, fontweight="bold")
        self.status_ax.text(left_x, top_y - line_h, f"Current max product (cur_max): {step['cur_max']}",
                            color="#d1ffd8" if step['cur_max'] >= 0 else "#ffb3b3", fontsize=12, fontweight="bold")
        self.status_ax.text(left_x, top_y - 2 * line_h, f"Current min product (cur_min): {step['cur_min']}",
                            color="#ffd9a6" if step['cur_min'] <= 0 else "#d1ffd8", fontsize=12, fontweight="bold")
        self.status_ax.text(left_x, top_y - 3 * line_h, f"Global max product: {step['global_max']}",
                            color="#8bff9b", fontsize=13, fontweight="bold")

        # right side: flags and outcome
        right_x = 0.55
        self.status_ax.text(right_x, top_y, "Flags:", color="#cccccc", fontsize=12, fontweight="bold")
        flags_display = ", ".join(step["flags"])
        self.status_ax.text(right_x, top_y - line_h, flags_display, color="white", fontsize=12, fontweight="bold")

        # swap/reset indicators
        swap_text = "Yes" if step["swap"] else "No"
        reset_text = "Yes" if step["reset"] else "No"
        self.status_ax.text(right_x, top_y - 2 * line_h, f"Swap occurred: {swap_text}", color="#ffd86b", fontsize=12, fontweight="bold")
        self.status_ax.text(right_x, top_y - 3 * line_h, f"Zero reset: {reset_text}", color="#ff7b7b", fontsize=12, fontweight="bold")

        # final result prominent if final
        if "final" in step["flags"]:
            res_x = 0.82
            res_y = 1.25
            self.status_ax.text(res_x, res_y, "FINAL RESULT", color="#ffffff", fontsize=12, fontweight="bold", ha="center")
            self.status_ax.text(res_x, res_y - 0.18, f"Maximum Product Subarray = {step['global_max']}",
                                color="#8bff9b", fontsize=16, fontweight="bold", ha="center")

    def draw_step(self, step_idx):
        """
        Draw everything for the requested step index.
        """
        step = self.steps[step_idx]
        active_idx = step["index"]

        # draw array boxes and highlights
        self.draw_boxes(active_idx, step)

        # explanation text area
        self.draw_info(step)

        # bottom status
        self.draw_status(step)

        # ensure redraw
        self.fig.canvas.draw_idle()

    # Button callbacks
    def on_next(self, event):
        if self.idx < len(self.steps) - 1:
            self.idx += 1
            self.draw_step(self.idx)

    def on_prev(self, event):
        if self.idx > 0:
            self.idx -= 1
            self.draw_step(self.idx)


# ---------- Main run ----------
def main():
    arr = ARRAY[:]
    if len(arr) == 0:
        print("Array is empty. Please set ARRAY to a non-empty list.")
        return

    steps = compute_max_product_steps(arr)

    # Safety: ensure at least one final step exists; algorithm already tags final on last step.
    if len(steps) == 0:
        print("No steps computed.")
        return

    vis = MaxProductVisualizer(arr, steps)
    plt.show()


if __name__ == "__main__":
    main()
