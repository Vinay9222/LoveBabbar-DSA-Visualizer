import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches

arr = [12, 1, 15, 6, 3, 1, 7, 8, 1, 9]
k = 8

n = len(arr)
good = sum(1 for x in arr if x <= k)

steps = []
bad = 0

for i in range(good):
    if arr[i] > k:
        bad += 1
steps.append((0, good-1, bad))

ans = bad
for i in range(good, n):
    if arr[i] > k:
        bad += 1
    if arr[i-good] > k:
        bad -= 1
    ans = min(ans, bad)
    steps.append((i-good+1, i, bad))

current = 0

fig, ax = plt.subplots(figsize=(10, 3))
plt.subplots_adjust(bottom=0.3)

box_height = 0.5
box_width = 0.8


def draw_step(step_id):
    ax.clear()
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    start, end, bad_count = steps[step_id]

    ax.set_title(f"Sliding Window Step {step_id+1} | Bad Count: {bad_count}", fontsize=14)
    ax.set_xlim(0, len(arr))
    ax.set_ylim(0, 2)
    ax.axis('off')

    for i, val in enumerate(arr):
        # Box Color
        if start <= i <= end:
            facecolor = 'yellow'  # Window highlight
        else:
            facecolor = 'lightgray'

        # Values > k marked red
        if val > k:
            edgecolor = 'red'
            linewidth = 3
        else:
            edgecolor = 'black'
            linewidth = 1

        rect = patches.Rectangle((i, 1), box_width, box_height, linewidth=linewidth,
                                 edgecolor=edgecolor, facecolor=facecolor)
        ax.add_patch(rect)
        ax.text(i + box_width/2, 1 + box_height/2, str(val), ha='center', va='center', fontsize=12)

        # Pointer
        if i == start:
            ax.text(i + box_width/2, 0.7, 'Start', ha='center', fontsize=10, color='blue')
        if i == end:
            ax.text(i + box_width/2, 0.4, 'End', ha='center', fontsize=10, color='green')

    # Display good, bad, ans values
    ax.text(0.1, 1.8, f"good = {good}", color='cyan', fontsize=12)
    ax.text(2.5, 1.8, f"bad = {bad_count}", color='red', fontsize=12)
    ax.text(4.5, 1.8, f"ans = {ans}", color='lime', fontsize=12)

    plt.draw()


def next_event(event):
    global current
    if current < len(steps) - 1:
        current += 1
        draw_step(current)


def prev_event(event):
    global current
    if current > 0:
        current -= 1
        draw_step(current)


# Buttons
axprev = plt.axes([0.3, 0.05, 0.15, 0.1])
axnext = plt.axes([0.55, 0.05, 0.15, 0.1])
bprev = Button(axprev, 'Previous')
bnext = Button(axnext, 'Next')
bprev.on_clicked(prev_event)
bnext.on_clicked(next_event)

draw_step(0)
plt.show()
