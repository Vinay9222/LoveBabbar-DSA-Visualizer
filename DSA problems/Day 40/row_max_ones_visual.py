import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button

matrix = [
    [0, 0, 1, 1],
    [0, 1, 1, 1],
    [0, 0, 0, 1],
    [1, 1, 1, 1]
]

n = len(matrix)
m = len(matrix[0])

steps = []
best_row_at_step = [] 

i, j = 0, m - 1
best_row = None  

while i < n and j >= 0:
    steps.append((i, j))

    if matrix[i][j] == 1:
        best_row = i   
        j -= 1
    else:
        i += 1

    best_row_at_step.append(best_row)  


current_step = 0

def draw(step):
    ax.clear()
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")

    ax.set_xlim(0, m)
    ax.set_ylim(0, n)
    ax.invert_yaxis()
    ax.set_xticks(range(m + 1))
    ax.set_yticks(range(n + 1))
    ax.grid(True, color="#444", linewidth=0.8)

    # Draw matrix numbers + indices
    for r in range(n):
        for c in range(m):
            ax.text(
                c + 0.5, r + 0.5,
                f"{matrix[r][c]}\n({r},{c})",
                color="white", ha="center", va="center", fontsize=12
            )

    # Highlight visited (blue)
    for k in range(step):
        pi, pj = steps[k]
        rect_path = patches.Rectangle(
            (pj, pi), 1, 1,
            linewidth=2,
            edgecolor="#3399FF",
            facecolor='none'
        )
        ax.add_patch(rect_path)

    # Highlight current (green)
    ci, cj = steps[step]
    rect_current = patches.Rectangle(
        (cj, ci), 1, 1,
        linewidth=3,
        edgecolor="#00FFAA",
        facecolor='none'
    )
    ax.add_patch(rect_current)

    # -----------------------------
    # SHOW UPDATED ANSWER (NEW)
    # -----------------------------
    ans = best_row_at_step[step]
    if ans is None:
        answer_text = "Current Best Row: None (no 1s found yet)"
    else:
        answer_text = f"Current Best Row: {ans}"

    ax.set_title(
        f"Step {step+1}/{len(steps)} - Current: ({ci},{cj})\n{answer_text}",
        color="white", fontsize=15
    )

    fig.canvas.draw_idle()


# -------------------------------------------------------
# NEXT & PREVIOUS FUNCTIONS
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
fig, ax = plt.subplots(figsize=(7, 7))
plt.subplots_adjust(bottom=0.2)

axprev = plt.axes([0.2, 0.05, 0.2, 0.1])
axnext = plt.axes([0.6, 0.05, 0.2, 0.1])

btn_prev = Button(axprev, '← Previous')
btn_next = Button(axnext, 'Next →')

btn_prev.on_clicked(prev_step)
btn_next.on_clicked(next_step)

fig.canvas.mpl_connect('key_press_event', on_key)

# Initial draw
draw(current_step)

plt.show()
