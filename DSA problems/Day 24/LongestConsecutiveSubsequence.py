import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button
import matplotlib as mpl

# ---------------------------
# Helper: Create step states
# ---------------------------


def build_steps(arr):
    steps = []
    nums = set(arr)  # hashing-based approach uses set lookup
    global_best = 0
    global_best_chain = []

    # We'll iterate through the array in its original order for pedagogy (visual mapping to boxes)
    step_counter = 0
    for idx, num in enumerate(arr):
        # Checking step
        steps.append(
            {
                "step": step_counter,
                "index": idx,
                "number": num,
                "is_start": None,
                "chain": [],
                "local_len": 0,
                "global_best": global_best,
                "global_best_chain": global_best_chain.copy(),
                "status": "checking",
                "note": f"Checking {num} (arr index {idx})",
            }
        )
        step_counter += 1

        # Determine whether this number is a possible sequence start
        if (num - 1) in nums:
            # Not a start — quick explanation step
            steps.append(
                {
                    "step": step_counter,
                    "index": idx,
                    "number": num,
                    "is_start": False,
                    "chain": [],
                    "local_len": 0,
                    "global_best": global_best,
                    "global_best_chain": global_best_chain.copy(),
                    "status": "not-sequence-start",
                    "note": f"{num} - 1 exists → not a sequence start",
                }
            )
            step_counter += 1
            continue

        # Valid start — begin building sequence
        steps.append(
            {
                "step": step_counter,
                "index": idx,
                "number": num,
                "is_start": True,
                "chain": [],
                "local_len": 0,
                "global_best": global_best,
                "global_best_chain": global_best_chain.copy(),
                "status": "building-sequence",
                "note": f"{num} is a sequence start → expanding forward",
            }
        )
        step_counter += 1

        # Expand forward from num as long as num+k in set
        chain = []
        cur = num
        while cur in nums:
            chain.append(cur)
            # Add a step for adding this element into the chain
            steps.append(
                {
                    "step": step_counter,
                    "index": idx,
                    "number": num,
                    "is_start": True,
                    "chain": chain.copy(),
                    "local_len": len(chain),
                    "global_best": global_best,
                    "global_best_chain": global_best_chain.copy(),
                    "status": "building-sequence",
                    "note": f"Found {cur} in set → chain grows: {chain}",
                }
            )
            step_counter += 1
            cur += 1

        # After building sequence, maybe update global best
        local_len = len(chain)
        if local_len > global_best:
            global_best = local_len
            global_best_chain = chain.copy()
            steps.append(
                {
                    "step": step_counter,
                    "index": idx,
                    "number": num,
                    "is_start": True,
                    "chain": chain.copy(),
                    "local_len": local_len,
                    "global_best": global_best,
                    "global_best_chain": global_best_chain.copy(),
                    "status": "update-global",
                    "note": f"New global best → length {global_best}, chain {global_best_chain}",
                }
            )
            step_counter += 1
        else:
            # No update needed; record a finalizing step for this number
            steps.append(
                {
                    "step": step_counter,
                    "index": idx,
                    "number": num,
                    "is_start": True,
                    "chain": chain.copy(),
                    "local_len": local_len,
                    "global_best": global_best,
                    "global_best_chain": global_best_chain.copy(),
                    "status": "building-sequence",
                    "note": f"Sequence built (length {local_len}), global best remains {global_best}",
                }
            )
            step_counter += 1

    # Final step
    steps.append(
        {
            "step": step_counter,
            "index": None,
            "number": None,
            "is_start": None,
            "chain": global_best_chain.copy(),
            "local_len": len(global_best_chain),
            "global_best": global_best,
            "global_best_chain": global_best_chain.copy(),
            "status": "final",
            "note": f"Finished → longest consecutive subsequence length = {global_best}",
        }
    )
    return steps


# ---------------------------
# Visualization: Box drawing
# ---------------------------


class LongestConsecutiveViz:
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        self.steps = build_steps(arr)
        self.current_step_idx = 0

        # Color palette (hex)
        self.bg_color = "#111111"
        self.text_color = "#FFFFFF"
        self.box_edge = "#AAAAAA"
        self.active_cyan = "#00ffff"  # active element
        self.not_start_orange = "#FF8C00"  # not a start
        self.chain_green = "#00FF7F"  # building chain
        self.best_gold = "#FFD700"  # global best chain highlight
        self.box_fill = "#1e1e1e"  # default box fill

        # Fonts
        mpl.rcParams["font.family"] = "DejaVu Sans"
        mpl.rcParams["font.weight"] = "bold"

        # Build figure
        self.fig = plt.figure(figsize=(12, 6), facecolor=self.bg_color)
        self.ax = self.fig.add_axes([0.03, 0.18, 0.94, 0.72], facecolor=self.bg_color)
        self.ax.set_xlim(0, max(10, self.n))
        self.ax.set_ylim(0, 10)
        self.ax.axis("off")

        # UI text axes (top and bottom)
        self.top_text_ax = self.fig.add_axes([0.03, 0.92, 0.94, 0.06], facecolor=self.bg_color)
        self.top_text_ax.axis("off")
        self.bottom_text_ax = self.fig.add_axes([0.03, 0.02, 0.94, 0.14], facecolor=self.bg_color)
        self.bottom_text_ax.axis("off")

        # Buttons axes
        axprev = self.fig.add_axes([0.25, 0.1, 0.2, 0.09])
        axnext = self.fig.add_axes([0.50, 0.1, 0.2, 0.09])
        axprev.patch.set_facecolor(self.bg_color)
        axnext.patch.set_facecolor(self.bg_color)

        # Create Buttons
        self.btn_prev = Button(axprev, "Previous", color="#222222", hovercolor="#333333")
        self.btn_next = Button(axnext, "Next", color="#222222", hovercolor="#333333")
        self.btn_prev.on_clicked(self.on_prev)
        self.btn_next.on_clicked(self.on_next)

        # Draw initial state
        self._draw_static_layout()
        self.update_visual()

    def _draw_static_layout(self):
        # Draw boxes area (we will update rectangles text each step)
        self.boxes = []
        self.box_texts = []
        self.index_texts = []

        # Box layout parameters
        box_w = 0.9
        spacing = 0.1
        total_width = self.n * (box_w + spacing)
        start_x = max(0,(10 - total_width) / 2)

        self.box_positions = []
        for i, val in enumerate(self.arr):
            x = start_x + i * (box_w + spacing)
            y = 6  # vertical placement
            rect = Rectangle((x, y), box_w, 1.6, linewidth=2, edgecolor=self.box_edge, facecolor=self.box_fill)
            self.ax.add_patch(rect)
            self.boxes.append(rect)
            self.box_positions.append((x, y, box_w, 1.6))
            # Character text
            t = self.ax.text(
                x + box_w / 2,
                y + 0.9,
                str(val),
                ha="center",
                va="center",
                color=self.text_color,
                fontsize=16,
                fontweight="bold",
            )
            self.box_texts.append(t)
            # Index below
            it = self.ax.text(
                x + box_w / 2,
                y - 0.3,
                str(i),
                ha="center",
                va="center",
                color="#BBBBBB",
                fontsize=10,
            )
            self.index_texts.append(it)

        # Explanations placeholders
        self.top_msg = self.top_text_ax.text(
            0.5,
            0.5,
            "",
            ha="center",
            va="center",
            color=self.text_color,
            fontsize=14,
            fontweight="bold",
        )

        # Bottom info: current chain, local & global values
        self.bottom_msg = self.bottom_text_ax.text(
            0.3,
            3,
            "",
            ha="left",
            va="top",
            color=self.text_color,
            fontsize=12,
            fontweight="bold",
        )

        # Right-side summary block
        # self.summary_ax = self.fig.add_axes([0.75, 0.12, 0.22, 0.2], facecolor=self.bg_color)
        # self.summary_ax.axis("off")
        # self.summary_text = self.summary_ax.text(
        #     0.5,
        #     1.25,
        #     "",
        #     ha="center",
        #     va="center",
        #     color=self.text_color,
        #     fontsize=12,
        #     fontweight="bold",
        # )

    def _clear_highlights(self):
        # Reset rectangles to default
        for rect in self.boxes:
            rect.set_edgecolor(self.box_edge)
            rect.set_facecolor(self.box_fill)
            rect.set_linewidth(2)

    def update_visual(self):
        """
        Update the entire visualization based on self.current_step_idx
        """
        state = self.steps[self.current_step_idx]
        status = state["status"]

        # Clear highlights first
        self._clear_highlights()

        # Update top message
        top_message = state.get("note", "")
        self.top_msg.set_text(top_message)

        # Visual highlighting rules:
        # - Active element: cyan border
        # - If not a start: orange fill
        # - Elements in currently building chain: green fill
        # - Global best chain elements: gold edge (and slightly thicker)
        # Note: mapping from chain numbers to indexes uses original arr positions for visual clarity
        current_idx = state["index"]

        # Mark active box (if index exists)
        if current_idx is not None:
            active_rect = self.boxes[current_idx]
            active_rect.set_edgecolor(self.active_cyan)
            active_rect.set_linewidth(3)

        # Map values to indices so we can highlight chain elements
        value_to_indices = {}
        for i, v in enumerate(self.arr):
            value_to_indices.setdefault(v, []).append(i)

        # Highlight building chain
        chain_vals = state.get("chain", []) or []
        for val in chain_vals:
            # highlight all positions with this value
            for idx in value_to_indices.get(val, []):
                rect = self.boxes[idx]
                rect.set_facecolor(self.chain_green)
                rect.set_edgecolor(self.box_edge)
                rect.set_linewidth(2)

        # If not a sequence start, highlight the active box in orange
        if state.get("is_start") is False and current_idx is not None:
            rect = self.boxes[current_idx]
            rect.set_facecolor(self.not_start_orange)

        # Highlight global best chain (if any)
        best_chain = state.get("global_best_chain", []) or []
        for val in best_chain:
            for idx in value_to_indices.get(val, []):
                rect = self.boxes[idx]
                # gold edge to indicate global best
                rect.set_edgecolor(self.best_gold)
                rect.set_linewidth(3)

        # Compose bottom message (live counters and current discovered chain)
        bottom_lines = []
        bottom_lines.append(f"Status: {status.upper()}")
        if current_idx is not None:
            bottom_lines.append(f"Evaluating arr[{current_idx}] = {state['number']}")
        bottom_lines.append(f"Current chain (building): {' → '.join(map(str, chain_vals)) if chain_vals else '—'}")
        bottom_lines.append(f"Local chain length: {state.get('local_len', 0)}")
        bottom_lines.append(f"Global best length: {state.get('global_best', 0)}")
        bottom_lines.append(f"Global best chain: {' → '.join(map(str, best_chain)) if best_chain else '—'}")
        # Final note
        if status == "final":
            bottom_lines.append(f"FINAL ANSWER → Length of longest consecutive subsequence = {state['global_best']}")
            bottom_lines.append(f"Sequence: {' → '.join(map(str, state['global_best_chain'])) if state['global_best_chain'] else '—'}")

        self.bottom_msg.set_text("\n".join(bottom_lines))

        # Update right summary (compact)
        # summary = f"Step {self.current_step_idx + 1} / {len(self.steps)}\n\n"
        # summary += f"Status: {status}\n"
        # summary += f"Global best: {state.get('global_best', 0)}\n"
        # if state.get("global_best_chain"):
        #     summary += "Best chain: " + ", ".join(map(str, state["global_best_chain"])) + "\n"
        # else:
        #     summary += "Best chain: —\n"

        # self.summary_text.set_text(summary)

        # Refresh canvas
        self.fig.canvas.draw_idle()

    # Button callbacks
    def on_next(self, event):
        if self.current_step_idx < len(self.steps) - 1:
            self.current_step_idx += 1
            self.update_visual()

    def on_prev(self, event):
        if self.current_step_idx > 0:
            self.current_step_idx -= 1
            self.update_visual()


# ---------------------------
# Example usage
# ---------------------------


def main():
    # Example arrays you can test with:
    examples = [
        [100, 4, 200, 1, 3, 2],
        [9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6],
        [0, 0, 1, 2, 3, 4, 2],
        [10, 5, 12, 3, 55, 30, 4, 11, 2, 1],
    ]

    # Choose one input array (uncomment or modify)
    arr = examples[0]

    # Create the visualization UI
    viz = LongestConsecutiveViz(arr)

    # Display instructions in console
    print("Interactive Longest Consecutive Subsequence Visualization")
    print(" - Use the Next / Previous buttons on the figure to step through the algorithm.")
    print(" - Close the figure window to exit.")
    plt.show()


if __name__ == "__main__":
    main()
