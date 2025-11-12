import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches
import numpy as np

def visualize_kadane(arr):
    steps = []
    current_sum = 0
    max_sum = float('-inf')

    # --- Build Steps for Each Iteration ---
    for i, num in enumerate(arr):
        prev_sum = current_sum
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
        explanation = (
            f"Step {i+1}:\n"
            f"Element = {num}\n"
            f"Previous currentSum = {prev_sum}\n"
            f"New currentSum = max({num}, {prev_sum}+{num}) = {current_sum}\n"
            f"maxSum so far = {max_sum}"
        )
        steps.append((arr[:], i, current_sum, max_sum, explanation))

    # --- Setup Figure and Axes ---
    fig, ax = plt.subplots(figsize=(11, 6))
    plt.subplots_adjust(bottom=0.25)
    current = {'index': 0}

    def draw_background():
        """Draw a soft gradient-style background."""
        x = np.linspace(0, 1, 256)
        y = np.linspace(0, 1, 256)
        X, Y = np.meshgrid(x, y)
        gradient = np.outer(np.ones_like(y), x)
        ax.imshow(gradient, extent=[-2, len(arr), -2, 2],
                  origin='lower', cmap='Greys', alpha=0.2)

    def draw(step_index):
        ax.clear()
        draw_background()

        arr, idx, curr, maxs, exp = steps[step_index]
        ax.set_title("Kadane’s Algorithm Visualization", fontsize=16, pad=20, color="#2C3E50")

        # --- Draw array boxes ---
        for i, val in enumerate(arr):
            color = '#82E0AA' if i == idx else '#AED6F1'
            rect = patches.FancyBboxPatch(
                (i, 0), 0.8, 0.6,
                boxstyle="round,pad=0.2",
                edgecolor='black',
                facecolor=color,
                mutation_aspect=1.5,
                lw=1.5
            )
            ax.add_patch(rect)
            ax.text(i + 0.4, 0.3, str(val), ha='center', va='center', fontsize=14, color='#1B2631')

        # --- Draw boxes for currentSum & maxSum ---
        ax.text(-1.5, 0.5, f"currentSum = {curr}", fontsize=12,
                bbox=dict(facecolor='#F9E79F', edgecolor='black', boxstyle='round,pad=0.4'))
        ax.text(-1.5, -0.2, f"maxSum = {maxs}", fontsize=12,
                bbox=dict(facecolor='#F5B041', edgecolor='black', boxstyle='round,pad=0.4'))

        # --- Draw explanation text below ---
        ax.text(len(arr) / 2 - 0.5, -1.2, exp, ha='center', fontsize=11, wrap=True, color='#2C3E50')

        ax.set_xlim(-2, len(arr))
        ax.set_ylim(-2, 2)
        ax.axis('off')
        plt.draw()

    # --- Button Controls ---
    def next_step(event):
        if current['index'] < len(steps) - 1:
            current['index'] += 1
            draw(current['index'])

    def prev_step(event):
        if current['index'] > 0:
            current['index'] -= 1
            draw(current['index'])

    axprev = plt.axes([0.3, 0.05, 0.1, 0.075])
    axnext = plt.axes([0.6, 0.05, 0.1, 0.075])
    bnext = Button(axnext, 'Next ➡️')
    bprev = Button(axprev, '⬅️ Prev')

    bnext.on_clicked(next_step)
    bprev.on_clicked(prev_step)

    draw(0)
    plt.show()


# Example array to visualize
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
visualize_kadane(arr)
