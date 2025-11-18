import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches

# =====================================
# LOGIC + VISUAL MESSAGE CAPTURE
# =====================================

def two_sum_zero_steps(arr):
    steps = []
    nums = sorted(arr)
    n = len(nums)

    l, r = 0, n - 1
    result = []

    steps.append(("Initial Sorted Array", nums[:], l, r, None, result[:], "normal"))

    while l < r:
        current_sum = nums[l] + nums[r]

        steps.append((
            f"Checking nums[{l}] + nums[{r}] = {nums[l]} + {nums[r]} = {current_sum}",
            nums[:],
            l,
            r,
            current_sum,
            result[:],
            "normal"
        ))

        # CASE 1: PAIR FOUND
        if current_sum == 0:
            pair = [nums[l], nums[r]]

            if not result or result[-1] != pair:
                result.append(pair)
                steps.append((
                    f"Found Unique Pair → {pair}",
                    nums[:],
                    l,
                    r,
                    current_sum,
                    result[:],
                    "pair"
                ))

            l += 1
            r -= 1

        # CASE 2: SUM TOO SMALL
        elif current_sum < 0:
            l += 1

        # CASE 3: SUM TOO LARGE
        else:
            r -= 1

        # GLOBAL DUPLICATE SKIPS (Both Sides)
        while l < r and (l - 1) >= 0 and nums[l] == nums[l - 1]:
            steps.append((
                f"Duplicate at LEFT → nums[{l}] = {nums[l]} (Skipping)",
                nums[:],
                l,
                r,
                current_sum,
                result[:],
                "duplicate"
            ))
            l += 1

        while l < r and (r + 1) < n and nums[r] == nums[r + 1]:
            steps.append((
                f"Duplicate at RIGHT → nums[{r}] = {nums[r]} (Skipping)",
                nums[:],
                l,
                r,
                current_sum,
                result[:],
                "duplicate"
            ))
            r -= 1

    steps.append(("Final Result", nums[:], -1, -1, None, result[:], "final"))
    return steps


# SAMPLE ARRAY
arr = [2, 8, -2, 1, -1, 5, -5, 3, -3, 0, 0, -5, 2, -2, 4, -4]
steps = two_sum_zero_steps(arr)
index = 0

# =====================================
# VISUALIZATION
# =====================================

fig, ax = plt.subplots(figsize=(14, 7))
plt.subplots_adjust(bottom=0.25)
fig.patch.set_facecolor("#111")


def draw_step():
    ax.clear()
    ax.set_facecolor("#111")

    title, nums, l, r, current_sum, result, status = steps[index]

    # Title
    ax.set_title(title, fontsize=20, color="white", fontweight="bold", pad=20)
    ax.set_xlim(0, len(nums))
    ax.set_ylim(-4, 5)
    ax.axis('off')

    # Draw Array Boxes
    for i, val in enumerate(nums):
        # Normal Box
        color_box = "#222"
        edge = "#00FFFF"

        # Highlight pair found
        if status == "pair" and (i == l or i == r):
            color_box = "#003300"
            edge = "lime"

        rect = patches.Rectangle(
            (i, 2), 0.9, 0.9,
            linewidth=2.5,
            edgecolor=edge,
            facecolor=color_box
        )
        ax.add_patch(rect)

        ax.text(i + 0.45, 2.45, str(val),
                ha='center', va='center',
                fontsize=16, color="white", fontweight="bold")

        ax.text(i + 0.45, 1.75, str(i),
                ha='center', va='center',
                fontsize=10, color="cyan")

    # Pointer Arrows
    if l >= 0 and r >= 0:
        # Left pointer
        ax.annotate("L", xy=(l + 0.45, 3),
                    xytext=(l + 0.45, 3.7),
                    fontsize=16, color="cyan",
                    ha='center',
                    arrowprops=dict(arrowstyle="->", color="cyan", lw=2))

        # Right pointer
        ax.annotate("R", xy=(r + 0.45, 3),
                    xytext=(r + 0.45, 3.7),
                    fontsize=16, color="orange",
                    ha='center',
                    arrowprops=dict(arrowstyle="->", color="orange", lw=2))

    # Current SUM
    if current_sum is not None:
        ax.text(0, 0.5, f"Current Sum = {current_sum}",
                fontsize=18, color="yellow", fontweight="bold")

    # Duplicate Skip Highlight
    if status == "duplicate":
        ax.text(0, -0.2, "Duplicate Detected → Skipping Pointer",
                fontsize=20, color="red", fontweight="bold")

    # Pair Found Highlight
    if status == "pair":
        ax.text(0, -0.2, "PAIR FOUND!",
                fontsize=22, color="lime", fontweight="bold")

    # Result Vector
    ax.text(0, -1.0, "Result Pairs:", fontsize=18, color="#62D0FF")
    ax.text(0, -2.0, str(result), fontsize=22, color="lime")

    plt.draw()


def next_step(event):
    global index
    if index < len(steps) - 1:
        index += 1
    draw_step()

def prev_step(event):
    global index
    if index > 0:
        index -= 1
    draw_step()


# BUTTONS
axprev = plt.axes([0.25, 0.05, 0.15, 0.1])
axnext = plt.axes([0.60, 0.05, 0.15, 0.1])

btn_prev = Button(axprev, 'Previous', color="#444", hovercolor="#666")
btn_next = Button(axnext, 'Next', color="#444", hovercolor="#666")

btn_prev.on_clicked(prev_step)
btn_next.on_clicked(next_step)

draw_step()
plt.show()
