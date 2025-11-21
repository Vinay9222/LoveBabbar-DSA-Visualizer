import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def visualize_zero_sum_subarray(arr):
    steps = []
    prefix_sum = 0
    hashmap = {}
    found = False
    result_range = None

    # ---- Collect Algorithm Steps ----
    for idx, num in enumerate(arr):
        prefix_sum += num
        explanation = f"Index {idx}: Add {num} → Prefix Sum = {prefix_sum}"

        if prefix_sum == 0:
            found = True
            result_range = (0, idx)
            explanation += "\n🟢 Prefix sum became 0 → Zero-sum subarray found!"
        elif prefix_sum in hashmap:
            found = True
            prev_idx = hashmap[prefix_sum]
            result_range = (prev_idx + 1, idx)
            explanation += f"\n🟢 Prefix sum repeated (previous seen at {prev_idx}) → Subarray exists!"
        else:
            explanation += "\nStored prefix sum into hashmap."

        snapshot = dict(hashmap)
        snapshot[prefix_sum] = idx

        steps.append((arr[:], snapshot, idx, prefix_sum, explanation, result_range))

        if found:
            break

        hashmap[prefix_sum] = idx

    if not found:
        steps.append((arr[:], hashmap.copy(), -1, prefix_sum, "❌ No Zero-Sum Subarray Exists.", None))


    # ---- Visualization ----
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(13, 5))
    plt.subplots_adjust(bottom=0.23)
    current = {'index': 0}

    # Colors
    ACTIVE_COLOR = "#FFD166"     # Amber
    FOUND_COLOR = "#06D6A0"      # Teal
    NORMAL_COLOR = "#118AB2"     # Soft Blue


    def draw(step_index):
        ax.clear()
        arr_vals, map_vals, idx, p_sum, text, rrange = steps[step_index]

        ax.set_title("🔍 Detecting Subarray With Zero Sum", fontsize=16, pad=20, color="white")

        # Draw Array
        for i, val in enumerate(arr_vals):
            if rrange and rrange[0] <= i <= rrange[1]:
                color = FOUND_COLOR
            elif i == idx:
                color = ACTIVE_COLOR
            else:
                color = NORMAL_COLOR
            
            ax.text(i, 1, str(val), ha="center", va="center",
                    bbox=dict(facecolor=color, edgecolor='white', boxstyle='round,pad=0.45'),
                    fontsize=13, color="black")

        # Index Labels
        for i in range(len(arr_vals)):
            ax.text(i, 1.45, f"{i}", ha="center", fontsize=10, color="#BBBBBB")

        # Hashmap Display
        ax.text(-1.5, -0.2, "📌 Hash Map (Prefix Sum → Index)", fontsize=12, color="#FFD166", weight="bold")
        
        y_offset = -0.6
        for k, v in map_vals.items():
            ax.text(-1.5, y_offset, f"{k} → {v}", fontsize=11, color="#8ecae6")
            y_offset -= 0.35

        # Explanation text
        ax.text(len(arr_vals)/2, -2.2, text, ha="center", fontsize=12, wrap=True, color="white")

        ax.set_xlim(-2, len(arr_vals) + 2)
        ax.set_ylim(-3, 3)
        ax.axis("off")
        plt.draw()


    # ---- Step Control Functions ----
    def next_step(event=None):
        if current['index'] < len(steps) - 1:
            current['index'] += 1
            draw(current['index'])

    def prev_step(event=None):
        if current['index'] > 0:
            current['index'] -= 1
            draw(current['index'])


    # ---- Keyboard Support ----
    def on_key(event):
        if event.key == "right":
            next_step()
        elif event.key == "left":
            prev_step()

    fig.canvas.mpl_connect("key_press_event", on_key)


    # ---- Create UI Buttons ----
    axprev = plt.axes([0.33, 0.05, 0.12, 0.07])
    axnext = plt.axes([0.55, 0.05, 0.12, 0.07])
    bnext = Button(axnext, 'Next ➡️')
    bprev = Button(axprev, '⬅️ Prev')

    # ---- Style Buttons ----
    bnext.ax.set_facecolor("#06D6A0")   # Teal
    bnext.label.set_color("black")

    bprev.ax.set_facecolor("#FFD166")   # Amber
    bprev.label.set_color("black")

    # Borders for both buttons
    for btn in [bnext, bprev]:
        for spine in btn.ax.spines.values():
            spine.set_edgecolor("white")
            spine.set_linewidth(1.3)

    # Assign click actions
    bnext.on_clicked(next_step)
    bprev.on_clicked(prev_step)

    # ---- Initial Draw ----
    draw(0)
    plt.show()


# ---- Example ----
arr = [4, 2, 6, -3, 1, 6, -4, -3, 2, -5, 4]
visualize_zero_sum_subarray(arr)
