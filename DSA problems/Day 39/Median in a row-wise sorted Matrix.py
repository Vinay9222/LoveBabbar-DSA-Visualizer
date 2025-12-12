import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
import bisect

matrix = [
    [1, 3, 5],
    [2, 6, 9],
    [3, 6, 9]
]

n = len(matrix)
m = len(matrix[0])
desired = (n * m + 1) // 2  # the median position

steps = []  # (low, high, mid, row_counts, total_count)

low = min(row[0] for row in matrix)
high = max(row[-1] for row in matrix)

while low <= high:
    mid = (low + high) // 2

    row_counts = []
    for row in matrix:
        cnt = bisect.bisect_right(row, mid)
        row_counts.append(cnt)

    total = sum(row_counts)

    steps.append((low, high, mid, row_counts, total))

    if total < desired:
        low = mid + 1
    else:
        high = mid - 1

current_step = 0

# -------------------------------------------------------
# DRAW FUNCTION
# -------------------------------------------------------
def draw(step):
    ax.clear()
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")

    low, high, mid, row_counts, total = steps[step]

    ax.set_xlim(0, m)
    ax.set_ylim(0, n)
    ax.invert_yaxis()

    ax.set_xticks(range(m + 1))
    ax.set_yticks(range(n + 1))
    ax.grid(True, color="#444", linewidth=0.8)

    # Draw matrix values + indices
    for r in range(n):
        for c in range(m):
            ax.text(
                c + 0.5,
                r + 0.5,
                f"{matrix[r][c]}\n({r},{c})",
                color="white",
                ha="center",
                va="center",
                fontsize=12
            )

    # Highlight cells <= mid (blue)
    for r in range(n):
        for c in range(row_counts[r]):
            rect = patches.Rectangle(
                (c, r), 1, 1,
                linewidth=2,
                edgecolor="#3399FF",
                facecolor="none"
            )
            ax.add_patch(rect)

    ax.set_title(
        f"Step {step+1}/{len(steps)}\n"
        f"Low={low}   High={high}   Mid={mid}\n"
        f"Count ≤ Mid = {total}   Desired = {desired}",
        color="white",
        fontsize=14
    )

    fig.canvas.draw_idle()


# -------------------------------------------------------
# NEXT AND PREVIOUS
# -------------------------------------------------------
def next_step(event=None):
    global current_step
    if current_step < len(steps) - 1:
        current_step += 1
        draw(current_step)

def prev_step(event=None):
    global current_step
    if current_step > 0:
        current_step -= 1
        draw(current_step)

# -------------------------------------------------------
# KEYBOARD HANDLER
# -------------------------------------------------------
def on_key(event):
    if event.key == "right":
        next_step()
    elif event.key == "left":
        prev_step()

# -------------------------------------------------------
# FIGURE SETUP
# -------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.25)

axprev = plt.axes([0.2, 0.1, 0.2, 0.1])
axnext = plt.axes([0.6, 0.1, 0.2, 0.1])

btn_prev = Button(axprev, "← Previous")
btn_next = Button(axnext, "Next →")

btn_prev.on_clicked(prev_step)
btn_next.on_clicked(next_step)

fig.canvas.mpl_connect("key_press_event", on_key)

draw(current_step)
plt.show()
