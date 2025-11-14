import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.widgets import Button

# ---------------------------------------------
# Function: Prepare all steps for visualization
# ---------------------------------------------
def prepare_steps(intervals):
    """Prepare and store each step of the merge process for visualization."""

    # Sort intervals by starting value
    intervals = sorted(intervals)

    merged = []     # Stores merged intervals
    steps = []      # Stores snapshot of every step

    # Helper function to save a snapshot of the current state
    def snapshot(curr_idx, merged_copy, title):
        steps.append({
            "curr": curr_idx,                     # Which interval index we are processing
            "intervals": intervals.copy(),        # Sorted intervals
            "merged": [m.copy() for m in merged_copy],  # Copy of merged intervals
            "title": title                        # Title to display
        })

    # Process each interval
    for i, interval in enumerate(intervals):

        # Step 1: Indicate that we are reading an interval
        snapshot(i, merged, "Reading Interval")

        # Step 2: Check for overlap
        if not merged or merged[-1][1] < interval[0]:
            # No overlap → push new interval into merged list
            merged.append(interval.copy())
            snapshot(i, merged, "No Overlap → Add Interval")
        else:
            # Overlap → update the end of last merged interval
            merged[-1][1] = max(merged[-1][1], interval[1])
            snapshot(i, merged, "Overlap → Merge Interval")

    return steps


# -------------------------------------------------------
# Function: Draw a single visualization step on the plot
# -------------------------------------------------------
def draw_step(ax, step):
    ax.clear()
    ax.set_facecolor("#0f0f0f")
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 20)
    ax.axis("off")

    intervals = step["intervals"]
    merged = step["merged"]
    curr = step["curr"]

    # Title
    ax.set_title(step["title"], fontsize=22, fontweight="bold", color="white")

    # ------------------------------------------------------
    # ALL SORTED INTERVALS IN ONE HORIZONTAL LINE
    # ------------------------------------------------------
    ax.text(0, 18, "Sorted Intervals:", fontsize=15, fontweight="bold", color="white")

    base_y = 16  # one single line
    spacing = 2  # gap between intervals
    x_pos = 1    # starting X

    for i, (s, e) in enumerate(intervals):
        width = e - s
        color = "#4aa3ff" if curr == i else "#444"

        rect = patches.Rectangle(
            (x_pos, base_y),
            width,
            1,
            facecolor=color,
            edgecolor="white",
            linewidth=3,
            zorder=3 if curr == i else 1
        )
        ax.add_patch(rect)

        ax.text(
            x_pos + width / 2,
            base_y + 0.5,
            f"[{s},{e}]",
            ha="center",
            va="center",
            fontsize=12,
            color="white",
            fontweight="bold"
        )

        x_pos += width + spacing


    # ------------------------------------------------------
    # MERGED INTERVALS
    # ------------------------------------------------------
    ax.text(0, 11, "Merged Intervals:",
            fontsize=15, fontweight="bold", color="white")

    merged_start_y = 9.5

    for j, (s, e) in enumerate(merged):
        y = merged_start_y - j * 1.4

        rect = patches.Rectangle(
            (s, y),
            e - s,
            1,
            facecolor="#00dd99",
            edgecolor="white",
            linewidth=2
        )
        ax.add_patch(rect)

        ax.text(
            s + (e - s) / 2,
            y + 0.5,
            f"[{s},{e}]",
            ha="center",
            va="center",
            fontsize=12,
            color="black",
            fontweight="bold"
        )

    # ------------------------------------------------------
# CURRENT INTERVAL VECTOR → (start, end)
# ------------------------------------------------------
    current_start, current_end = intervals[curr]

    ax.text(0, 5.5, "Current Interval Vector:",
            fontsize=15, fontweight="bold", color="#00c8ff")

# FIXED: increased box size + better spacing + single-line format
    ax.text(
        10,
        5.3,
        f"[ {current_start} , {current_end} ]",
        fontsize=15,
        color="#00eaff",
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.6", facecolor="#001a1a", edgecolor="#00eaff", linewidth=1.8)
    )

    # ------------------------------------------------------
    # MERGED ITERATION VECTOR (the list)
    # ------------------------------------------------------
    ax.text(0, 3.5, "Merged Vector:",
            fontsize=15, fontweight="bold", color="#00ffcc")

    vector_text = str(merged)

    ax.text(
        2,
        2.0,
        vector_text,
        fontsize=16,
        color="yellow",
        fontweight="bold",
        bbox=dict(boxstyle="round", facecolor="#222", edgecolor="yellow")
    )


# --------------------------------------------------------------------
# Function: Create GUI with NEXT / PREVIOUS buttons for navigation
# --------------------------------------------------------------------
def visualize_with_buttons(intervals):
    steps = prepare_steps(intervals)  # Pre-calc steps for animation
    current = {"idx": 0}             # Mutable wrapper for index

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 9))
    fig.patch.set_facecolor("#0f0f0f")
    plt.subplots_adjust(bottom=0.18)  # Space for buttons

    # Draw initial step
    draw_step(ax, steps[current["idx"]])

    # Define NEXT button action
    def next_step(event):
        if current["idx"] < len(steps) - 1:
            current["idx"] += 1
            draw_step(ax, steps[current["idx"]])
            plt.draw()

    # Define PREVIOUS button action
    def prev_step(event):
        if current["idx"] > 0:
            current["idx"] -= 1
            draw_step(ax, steps[current["idx"]])
            plt.draw()

    # Create button areas
    axprev = plt.axes([0.26, 0.05, 0.2, 0.08])
    axnext = plt.axes([0.54, 0.05, 0.2, 0.08])

    # Button widgets
    bprev = Button(axprev, "⬅ PREVIOUS", color="#333", hovercolor="#555")
    bnext = Button(axnext, "NEXT ➤", color="#333", hovercolor="#555")

    # Button text color
    bprev.label.set_color("white")
    bnext.label.set_color("white")

    # Bind button events
    bprev.on_clicked(prev_step)
    bnext.on_clicked(next_step)

    # Show plot window
    plt.show()


# -------------------------------------------------------
# RUN THE VISUALIZATION
# -------------------------------------------------------
intervals = [[1,4],[0,2],[3,5],[7,9],[8,10],[12,15],[14,18]]

visualize_with_buttons(intervals)
