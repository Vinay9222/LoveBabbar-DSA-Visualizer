import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button

plt.style.use("dark_background")


# -----------------------------
# FUNCTION TO GENERATE FRAMES
# -----------------------------
def generate_frames(arr):
    frames = []

    for idx, num in enumerate(arr):

        original = num
        rev = 0

        # Step 1: Pick number
        frames.append(("Pick Number",
                       arr, idx,
                       f"Selected element = {num}",
                       "cyan"))

        # Reverse calculation
        step = 1
        temp = num
        while temp > 0:
            digit = temp % 10
            rev = rev * 10 + digit
            temp //= 10

            frames.append((f"Reversing (Step {step})",
                           arr, idx,
                           f"Extracted: {digit}, New Reverse: {rev}",
                           "yellow"))
            step += 1

        # Final comparison
        result = "Palindrome ✔" if rev == original else "Not Palindrome ✘"
        color = "green" if rev == original else "red"

        frames.append(("Final Check",
                       arr, idx,
                       f"{original} vs {rev} → {result}",
                       color))

    return frames


# -----------------------------
# RENDER A FRAME
# -----------------------------
def draw_frame(frame):
    title, arr, idx, text, color = frame

    ax.clear()
    ax.set_xlim(0, len(arr) + 2)
    ax.set_ylim(0, 3)
    ax.axis("off")

    # Title
    ax.text(0.5, 2.6, title, fontsize=18, ha="center")

    # Draw array
    for i, val in enumerate(arr):
        rect = patches.Rectangle((i + 0.2, 1.5), 0.8, 0.6,
                                 linewidth=2,
                                 edgecolor="cyan" if i == idx else "white",
                                 facecolor='none')
        ax.add_patch(rect)
        ax.text(i + 0.6, 1.8, str(val), ha="center", fontsize=14)

    # Step text
    ax.text(0.5, 0.7, text, fontsize=16, ha="center", color=color)

    plt.draw()


# -----------------------------
# BUTTON CALLBACKS
# -----------------------------
def next_frame(event):
    global index
    if index < len(frames) - 1:
        index += 1
    draw_frame(frames[index])


def prev_frame(event):
    global index
    if index > 0:
        index -= 1
    draw_frame(frames[index])


# -----------------------------
# MAIN EXECUTION
# -----------------------------
arr = [121, 131, 20, 545, 999]
frames = generate_frames(arr)
index = 0

fig, ax = plt.subplots(figsize=(14, 4))
plt.subplots_adjust(bottom=0.25)

# Buttons
ax_prev = plt.axes([0.35, 0.05, 0.1, 0.1])
ax_next = plt.axes([0.55, 0.05, 0.1, 0.1])

btn_prev = Button(ax_prev, "Previous")
btn_next = Button(ax_next, "Next")

btn_prev.on_clicked(prev_frame)
btn_next.on_clicked(next_frame)

# Show first frame
draw_frame(frames[index])

plt.show()
