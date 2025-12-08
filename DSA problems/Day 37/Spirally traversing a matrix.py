import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
import matplotlib.patches as Rectangle

matrix = [
    [1, 2, 3, 4],
    [12, 13, 14, 5],
    [11, 16, 15, 6],
    [10, 9, 8, 7]
]

A = np.array(matrix)
nrows, ncols = A.shape

def spiral_steps(arr):
    steps = []
    top, bottom = 0, arr.shape[0] - 1
    left, right = 0, arr.shape[1] - 1
    order = []

    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            order.append((top, j, (top, bottom, left, right)))
        top += 1
        if top > bottom: break

        for i in range(top, bottom + 1):
            order.append((i, right, (top, bottom, left, right)))
        right -= 1
        if left > right: break

        for j in range(right, left - 1, -1):
            order.append((bottom, j, (top, bottom, left, right)))
        bottom -= 1
        if top > bottom: break

        for i in range(bottom, top - 1, -1):
            order.append((i, left, (top, bottom, left, right)))
        left += 1

    steps_data = []
    for idx, (r, c, p) in enumerate(order):
        steps_data.append({
            "step": idx + 1,
            "pos": (r, c),
            "value": arr[r, c],
            "pointers": p
        })
    return steps_data

steps = spiral_steps(A)
total_steps = len(steps)

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1, ncols)
ax.set_ylim(-1, nrows)
ax.invert_yaxis()
ax.set_xticks([])
ax.set_yticks([])

# Draw neon cells
cell_boxes = {}
cell_texts = {}

for i in range(nrows):
    for j in range(ncols):

        # Neon box
        box = Rectangle.Rectangle((j, i), 1, 1,
                                  linewidth=2,
                                  edgecolor="#00FFFF",
                                  facecolor="black")
        ax.add_patch(box)
        cell_boxes[(i, j)] = box

        # Value + (i, j) index
        txt = ax.text(j + 0.5, i + 0.45,
                      f"{A[i,j]}\n({i},{j})",
                      ha='center', va='center',
                      fontsize=12, color="#00FFEA")
        cell_texts[(i, j)] = txt

# Highlight current cell
highlight = Rectangle.Rectangle((0, 0), 1, 1,
                                linewidth=4,
                                edgecolor="#FF00FF",
                                facecolor="none")
ax.add_patch(highlight)

# Step text
step_txt = ax.text(0, -0.6, "", fontsize=14,
                   color="#00FFEA", ha="left")

# Pointer text
pointer_txt = ax.text(ncols - 0.2, -0.6, "",
                      fontsize=12, ha="right",
                      color="#00FFFF")

# ----------------------------------------
# Step Logic
# ----------------------------------------
current_step = 0

def update_display():
    step = steps[current_step]
    r, c = step["pos"]

    # Move highlight
    highlight.set_xy((c, r))

    # Update visited colors
    for i in range(nrows):
        for j in range(ncols):
            if (i, j) == (r, c):
                cell_boxes[(i, j)].set_edgecolor("#FF00FF")  # current
            elif steps.index(step) >= steps.index(
                next((s for s in steps if s["pos"]==(i,j)), step)
            ):
                cell_boxes[(i, j)].set_edgecolor("#00FF7F")  # visited
            else:
                cell_boxes[(i, j)].set_edgecolor("#00FFFF")  # unvisited

    # Update texts
    step_txt.set_text(f"Step {step['step']} → Value = {step['value']}")

    t, b, l, r = step["pointers"]
    pointer_txt.set_text(f"Top={t}   Bottom={b}   Left={l}   Right={r}")

    fig.canvas.draw_idle()


# ----------------------------------------
# Button Controls
# ----------------------------------------
def next_step(event):
    global current_step
    if current_step < total_steps - 1:
        current_step += 1
        update_display()

def prev_step(event):
    global current_step
    if current_step > 0:
        current_step -= 1
        update_display()

def reset(event):
    global current_step
    current_step = 0
    update_display()

def autoplay(event):
    import time
    global current_step
    for _ in range(total_steps):
        update_display()
        plt.pause(0.6)
        if current_step < total_steps - 1:
            current_step += 1

# Buttons
axprev = plt.axes([0.1, 0.02, 0.15, 0.06])
axnext = plt.axes([0.3, 0.02, 0.15, 0.06])
axreset = plt.axes([0.5, 0.02, 0.15, 0.06])
axauto = plt.axes([0.7, 0.02, 0.2, 0.06])

bprev = Button(axprev, "◀ Previous")
bnext = Button(axnext, "Next ▶")
breset = Button(axreset, "Reset")
bauto = Button(axauto, "Auto Play ▶▶")

bprev.on_clicked(prev_step)
bnext.on_clicked(next_step)
breset.on_clicked(reset)
bauto.on_clicked(autoplay)

# Initial display
update_display()

plt.show()
