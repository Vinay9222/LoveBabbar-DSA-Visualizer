import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

# ---------------- INPUT MATRIX ----------------
mat = np.array([
    [1,  2, -1],
    [-3, 4,  2],
    [5,  1,  6]
])

n, m = mat.shape
dp = np.full((n, m), np.inf)

steps = []
ans = -10**9

# ---------------- PRECOMPUTE STEPS ----------------
dp[0][0] = mat[0][0]
steps.append((0, 0, dp.copy(), ans, "Initialize"))

# First row
for j in range(1, m):
    dp[0][j] = min(dp[0][j-1], mat[0][j])
    steps.append((0, j, dp.copy(), ans, "First Row"))

# First column
for i in range(1, n):
    dp[i][0] = min(dp[i-1][0], mat[i][0])
    steps.append((i, 0, dp.copy(), ans, "First Column"))

# Main DP
for i in range(1, n):
    for j in range(1, m):
        ans = max(ans, mat[i][j] - dp[i-1][j-1])
        dp[i][j] = min(mat[i][j], dp[i-1][j], dp[i][j-1])
        steps.append((i, j, dp.copy(), ans, "Main DP"))

# ---------------- VISUALIZATION ----------------
plt.style.use("dark_background")
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
plt.subplots_adjust(bottom=0.25)

idx = 0

def draw():
    ax[0].clear()
    ax[1].clear()

    i, j, cur_dp, cur_ans, phase = steps[idx]

    # Original matrix
    ax[0].imshow(mat, cmap="cool")
    ax[0].set_title("Original Matrix", color="white")
    ax[0].axis("off")

    for x in range(n):
        for y in range(m):
            ax[0].text(y, x, mat[x][y],
                       ha="center", va="center",
                       color="white", fontsize=12)

    # Highlight current cell
    ax[0].add_patch(
        plt.Rectangle((j-0.5, i-0.5), 1, 1,
                      fill=False, edgecolor="red", linewidth=3)
    )

    # DP matrix
    ax[1].imshow(cur_dp, cmap="summer")
    ax[1].set_title("DP Matrix (Min so far)", color="white")
    ax[1].axis("off")

    for x in range(n):
        for y in range(m):
            if cur_dp[x][y] != np.inf:
                ax[1].text(y, x, int(cur_dp[x][y]),
                           ha="center", va="center",
                           color="black", fontsize=12)

    fig.suptitle(
        f"Step {idx+1}/{len(steps)} | Cell ({i},{j}) | {phase} | Max Diff = {cur_ans}",
        color="cyan", fontsize=12
    )

    fig.canvas.draw_idle()

def next_step(event):
    global idx
    if idx < len(steps) - 1:
        idx += 1
        draw()

def prev_step(event):
    global idx
    if idx > 0:
        idx -= 1
        draw()

# ---------------- BUTTONS ----------------
ax_prev = plt.axes([0.25, 0.05, 0.15, 0.1])
ax_next = plt.axes([0.60, 0.05, 0.15, 0.1])

btn_prev = Button(ax_prev, "Previous")
btn_next = Button(ax_next, "Next")

btn_prev.on_clicked(prev_step)
btn_next.on_clicked(next_step)

draw()
plt.show()
