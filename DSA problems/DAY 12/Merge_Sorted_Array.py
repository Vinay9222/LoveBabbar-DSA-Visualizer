import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def visualize_merge_interactive(a, b):
    steps = []  # store every state

    # Simulate the algorithm and record steps
    i = len(a) - 1
    j = 0
    A, B = a[:], b[:]
    while j < len(B):
        steps.append((A[:], B[:], i, j, f"Comparing A[{i}]={A[i]} and B[{j}]={B[j]} is A[{i}] > B[{j}] ?"))
        if A[i] > B[j]:
            A[i], B[j] = B[j], A[i]
            steps.append((A[:], B[:], i, j, f"Swapped: A[{i}] and B[{j}] "))
            i -= 1
        else:
            steps.append((A[:], B[:], i, j, f"No swap needed"))
        j += 1

    A.sort()
    B.sort()
    steps.append((A[:], B[:], -1, -1, f"✅ Final sorted arrays:\nA = {A}\nB = {B}"))

    # --- Visualization ---
    fig, ax = plt.subplots(figsize=(10, 4))
    plt.subplots_adjust(bottom=0.25)
    current = {'index': 0}

    def draw(step_index):
        ax.clear()
        A, B, i, j, text = steps[step_index]
        ax.set_title("Merge Two Sorted Arrays (In-place)", fontsize=14, pad=20)

        # Draw A
        for idx, val in enumerate(A):
            color = 'skyblue' if idx != i else 'lightgreen'
            ax.text(idx, 1, str(val), ha='center', va='center',
                    bbox=dict(facecolor=color, edgecolor='black', boxstyle='round,pad=0.5'), fontsize=12)
        # Draw B
        for idx, val in enumerate(B):
            color = 'lightyellow' if idx != j else 'salmon'
            ax.text(idx, 0, str(val), ha='center', va='center',
                    bbox=dict(facecolor=color, edgecolor='black', boxstyle='round,pad=0.5'), fontsize=12)

        ax.text(-1, 1, "Array A", color='blue', fontsize=12, va='center')
        ax.text(-1, 0, "Array B", color='red', fontsize=12, va='center')

        ax.text(max(len(A), len(B)) / 2 - 0.5, -1.2, text, ha='center', fontsize=11, wrap=True)
        ax.set_xlim(-2, max(len(A), len(B)) + 1)
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


# Example usage
a = [1, 5, 9, 10, 15, 20]
b = [2, 3, 8, 13]
visualize_merge_interactive(a, b)
