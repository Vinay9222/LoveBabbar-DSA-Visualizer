import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches

# =========================================================
#         LOGIC TO CAPTURE EACH STEP (FULL ITERATION)
# =========================================================

def common_unique_steps(A, B, C):
    steps = []
    
    i = j = k = 0
    result = []

    # Continue until ALL pointers reach end
    while i <= len(A) or j <= len(B) or k <= len(C):

        # Protect out-of-range access
        Ai = A[i] if i < len(A) else None
        Bj = B[j] if j < len(B) else None
        Ck = C[k] if k < len(C) else None

        step_info = {
            "i": i,
            "j": j,
            "k": k,
            "A": A,
            "B": B,
            "C": C,
            "result": result[:],
            "Ai": Ai,
            "Bj": Bj,
            "Ck": Ck,
            "action": ""
        }

        # Stop comparison when any array ends, but still move pointers visually
        if Ai is None or Bj is None or Ck is None:
            step_info["action"] = "One array exhausted → Iterating remaining pointers"
            if i < len(A): i += 1
            elif j < len(B): j += 1
            elif k < len(C): k += 1
            else: break

        else:
            # Full common element logic
            if Ai == Bj == Ck:
                if Ai not in result:
                    result.append(Ai)
                    step_info["action"] = f"Common Found → {Ai} added"
                else:
                    step_info["action"] = f"{Ai} already in result → skip"

                i += 1; j += 1; k += 1

            elif Ai < Bj:
                step_info["action"] = "A[i] < B[j] → Move i"
                i += 1
            elif Bj < Ck:
                step_info["action"] = "B[j] < C[k] → Move j"
                j += 1
            else:
                step_info["action"] = "C[k] smallest → Move k"
                k += 1

        steps.append(step_info)

    return steps


# =========================================================
#                     DARK MODE VISUALS
# =========================================================

def draw_array(ax, arr, y, pointer_index, color, title):
    box_w = 1.1
    box_h = 0.8
    gap = 1.6  # extra spacing for dark mode clarity

    ax.text(-2.5, y + 0.25, title,
            fontsize=16, fontweight="bold", color="white")

    for idx, val in enumerate(arr):
        x = idx * gap

        rect = patches.FancyBboxPatch(
            (x, y), box_w, box_h,
            boxstyle="round,pad=0.25",
            facecolor=color,
            edgecolor="white",
            linewidth=2
        )
        ax.add_patch(rect)

        ax.text(x + box_w/2, y + box_h/2, str(val),
                ha="center", va="center",
                fontsize=14, fontweight="bold", color="white")

        # pointer
        if pointer_index == idx:
            ax.text(x + box_w/2, y + box_h + 0.15, "▲",
                    ha="center", fontsize=12, color="#FF5555")
            ax.text(
                x + box_w/2, y + box_h + 0.55,
                f"ptr={idx}", ha="center",
                fontsize=11, color="#FFBBBB"
            )


def visualize_steps(steps):
    fig, ax = plt.subplots(figsize=(18, 10))
    plt.subplots_adjust(bottom=0.18)

    fig.patch.set_facecolor("#111111")
    ax.set_facecolor("#111111")

    current_step = 0

    def draw():
        ax.clear()
        ax.set_xlim(-3, 25)
        ax.set_ylim(-7, 12)
        ax.axis("off")
        ax.set_facecolor("#111111")

        step = steps[current_step]

        # Arrays
        draw_array(ax, step["A"], 8, step["i"],
                   "#004488", "Array A")
        draw_array(ax, step["B"], 5, step["j"],
                   "#AA5500", "Array B")
        draw_array(ax, step["C"], 2, step["k"],
                   "#2B8A3E", "Array C")

        # Result row
        ax.text(-2.5, -1.5, "Result:",
                fontsize=16, fontweight="bold", color="white")

        for idx, val in enumerate(step["result"]):
            rect = patches.FancyBboxPatch(
                (idx * 1.5, -3),
                1.2, 0.8,
                boxstyle="round,pad=0.25",
                facecolor="#3CB043",
                edgecolor="white",
                linewidth=2
            )
            ax.add_patch(rect)

            ax.text(idx * 1.5 + 0.6, -3 + 0.4,
                    str(val), ha="center", va="center",
                    fontsize=14, fontweight="bold", color="white")

        # Action description
        ax.text(
            -2.5, 10.2,
            f"Step {current_step + 1}/{len(steps)} → {step['action']}",
            fontsize=17, fontweight="bold",
            color="#FFDD55"
        )

        fig.canvas.draw_idle()

    # button layout
    axprev = plt.axes([0.32, 0.05, 0.16, 0.08])
    axnext = plt.axes([0.56, 0.05, 0.16, 0.08])
    bprev = Button(axprev, "Previous")
    bnext = Button(axnext, "Next")

    bprev.on_clicked(lambda e: step_change(-1))
    bnext.on_clicked(lambda e: step_change(1))

    def step_change(direction):
        nonlocal current_step
        current_step = max(0, min(len(steps) - 1, current_step + direction))
        draw()

    draw()
    plt.show()


# =========================================================
#                     RUN
# =========================================================

A = [1, 5, 10, 20, 20, 40, 80]
B = [6, 7, 20, 20, 80, 100]
C = [3, 4, 15, 20, 20, 30, 70, 80, 120]

steps = common_unique_steps(A, B, C)
visualize_steps(steps)
