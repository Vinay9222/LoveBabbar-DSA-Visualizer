import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# ---------------- INPUT ----------------
arr = [3, 4, 1, 9, 56, 7, 9, 12]
m = 5     # students
# ---------------------------------------

arr.sort()
n = len(arr)

diffs = [None] * n
current_index = 0

min_diff = float('inf')
best_pair = None

# ----------- VISUAL SETUP -----------
fig, ax = plt.subplots(figsize=(11,3))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")
plt.subplots_adjust(bottom=0.25)

def draw():
    ax.clear()
    ax.set_facecolor("black")
    ax.set_xticks(range(n))
    ax.set_yticks([])

    end_index = current_index + m - 1  # second pointer

    for i in range(n):
        # highlight both indices
        if i == current_index:  
            color = "yellow"
        elif i == end_index and end_index < n:
            color = "red"
        else:
            color = "cyan"

        ax.text(i, 0.6, str(arr[i]),
                fontsize=18, color="black",
                bbox=dict(boxstyle="round,pad=0.6", fc=color, ec="white", lw=2),
                ha="center")

    # show differences
    for i in range(n):
        if diffs[i] is not None:
            ax.text(i, 0.1, f"{diffs[i]}", fontsize=14, color="white", ha="center")

    # status text
    ax.text(0,1.35,f"Checking Window: {current_index} → {end_index if end_index<n else '-'}",
            fontsize=14,color="white")
    ax.text(0,1.20,f"Minimum Difference: {min_diff}",fontsize=14,color="yellow")
    if best_pair:
        ax.text(0,1.05,f"Best Window: {best_pair[0]} to {best_pair[1]}",
                fontsize=14,color="orange")

    plt.draw()


def next_step(event):
    global current_index, min_diff, best_pair

    if current_index + m - 1 < n:
        diff = arr[current_index+m-1] - arr[current_index]
        diffs[current_index] = diff

        if diff < min_diff:
            min_diff = diff
            best_pair = (arr[current_index], arr[current_index+m-1])

    draw()
    current_index += 1


def prev_step(event):
    global current_index
    if current_index > 0:
        current_index -= 1
    draw()


# Buttons
ax_next = plt.axes([0.80,0.05,0.15,0.10])
b_next = Button(ax_next,'NEXT',color='white',hovercolor='gray')
b_next.on_clicked(next_step)

ax_prev = plt.axes([0.60,0.05,0.15,0.10])
b_prev = Button(ax_prev,'PREV',color='white',hovercolor='gray')
b_prev.on_clicked(prev_step)

draw()
plt.show()
