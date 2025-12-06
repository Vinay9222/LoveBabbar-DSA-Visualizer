import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np

# a = [3, 5, 6, 12, 15]
# b = [3, 4, 6, 10, 10, 12]

a = [1,2,3,4,5,8]
b = [6,7,8,9,10,11]

def median_steps(a, b):
    steps = []
    n = len(a)
    m = len(b)
    total = n + m
    idx1 = (total - 1) // 2
    idx2 = total // 2

    i = 0
    j = 0
    count = 0
    mid1 = None
    mid2 = None

    while count <= idx2:
        if i < n and (j >= m or a[i] < b[j]):
            val = a[i]
            i += 1
            from_arr = 'A'
            pos = i - 1
        else:
            val = b[j]
            j += 1
            from_arr = 'B'
            pos = j - 1

        if count == idx1:
            mid1 = val
        if count == idx2:
            mid2 = val

        steps.append({
            "i": i,
            "j": j,
            "count": count,
            "mid1": mid1,
            "mid2": mid2
        })

        count += 1

    return steps

steps = median_steps(a, b)
current_step = 0

fig, ax = plt.subplots(figsize=(12, 6))
plt.style.use("dark_background")
ax.set_facecolor("black")
fig.patch.set_facecolor("black")

plt.subplots_adjust(bottom=0.2)

def draw_array(arr, y, label, pointer_index, mid_indices):
    for i, val in enumerate(arr):
        color = "gray"
        if i == pointer_index:
            color = "yellow"
        if i in mid_indices:
            color = "cyan"

        ax.text(i, y, f"[{val}]", fontsize=18, color=color,
                ha="center", va="center", fontweight="bold")
        ax.text(i, y - 0.35, f"{i}", fontsize=12, color="white",
                ha="center")

    ax.text(-1.5, y, label, fontsize=18, color="white", fontweight="bold")


def render(step_index):
    ax.clear()
    ax.set_facecolor("black")

    step = steps[step_index]
    i_ptr = step["i"]
    j_ptr = step["j"]
    mid1 = step["mid1"]
    mid2 = step["mid2"]

    midA, midB = [], []
    if mid1 in a:
        midA.append(a.index(mid1))
    if mid2 in a:
        midA.append(a.index(mid2))
    if mid1 in b:
        midB.append(b.index(mid1))
    if mid2 in b:
        midB.append(b.index(mid2))

    draw_array(a, 1.5, "Array A", i_ptr if i_ptr < len(a) else -1, midA)
    draw_array(b, 0.5, "Array B", j_ptr if j_ptr < len(b) else -1, midB)

    ax.text(0, -0.2,
            f"Step: {step['count']}    Mid1: {mid1}    Mid2: {mid2}",
            fontsize=18, color="white", fontweight="bold")

    ax.set_xlim(-2, max(len(a), len(b)) + 1)
    ax.set_ylim(-1, 2.2)
    ax.axis("off")

    fig.canvas.draw_idle()


render(0)

axprev = plt.axes([0.25, 0.05, 0.2, 0.1])
axnext = plt.axes([0.55, 0.05, 0.2, 0.1])

btn_prev = Button(axprev, 'Previous', color='gray', hovercolor='white')
btn_next = Button(axnext, 'Next', color='gray', hovercolor='white')

def next_step(event):
    global current_step
    if current_step < len(steps) - 1:
        current_step += 1
        render(current_step)

def prev_step(event):
    global current_step
    if current_step > 0:
        current_step -= 1
        render(current_step)

btn_next.on_clicked(next_step)
btn_prev.on_clicked(prev_step)

plt.show()
