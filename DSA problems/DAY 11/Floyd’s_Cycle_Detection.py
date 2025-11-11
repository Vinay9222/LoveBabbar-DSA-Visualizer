import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time

def visualize_floyd_two_phases(nums):
    """
    # Visualize Floyd’s Cycle Detection (Find Duplicate Number)
    Phase 1: Detect cycle
    Phase 2: Find start of cycle (duplicate)
    """

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(12, 3))
    plt.subplots_adjust(bottom=0.25)
    ax.set_xlim(-1, len(nums))
    ax.set_ylim(-1, 3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("🐢🐇 Floyd’s Algorithm Visualization – Find Duplicate", fontsize=15, color="#00FFFF")

    # Draw array boxes
    boxes = []
    for i, val in enumerate(nums):
        rect = plt.Rectangle((i-0.4, 0), 0.8, 1, fill=True, color="#333333", ec="#888888", lw=2)
        ax.add_patch(rect)
        boxes.append(rect)
        ax.text(i, 0.5, str(val), color="white", ha="center", va="center", fontsize=13)

    # Step info
    step_text = ax.text(0, 2.3, "", color="#FFD700", fontsize=13, ha="left")
    phase_text = ax.text(0, 2.0, "", color="#00FFAA", fontsize=12, ha="left")

    # Buttons
    axprev = plt.axes([0.3, 0.05, 0.1, 0.07])
    axnext = plt.axes([0.6, 0.05, 0.1, 0.07])
    bnext = Button(axnext, 'Next ▶')
    bprev = Button(axprev, '◀ Back')

    # Step data
    steps = []

    # ---- Phase 1: Detect cycle ----
    slow = fast = 0
    steps.append(("Phase 1: Detect Cycle", slow, fast, None, None, "Start positions"))

    while True:
        prev_slow, prev_fast = slow, fast
        slow = nums[slow]
        fast = nums[nums[fast]]
        # steps.append(("Previous Phase 1: Slow is {prev_slow}, Fast is {prev_fast}", slow, fast, prev_slow, prev_fast, "Moving slow by 1 step, fast by 2 steps"))
        steps.append(("Phase 1: Detect Cycle", slow, fast, prev_slow, prev_fast, f"Slow at index {slow}, Fast at index {fast}"))
        if slow == fast:
            steps.append(("Phase 1: Detect Cycle", slow, fast, prev_slow, prev_fast, "slow and fast met inside the loop!"))
            break

    # ---- Phase 2: Find duplicate ----
    slow = 0
    steps.append(("Phase 2: Find Duplicate", slow, fast, None, None, "Reset slow to start (index 0)"))
    while slow != fast:
        prev_slow, prev_fast = slow, fast
        slow = nums[slow]
        fast = nums[fast]
        steps.append(("Phase 2: Find Duplicate", slow, fast, prev_slow, prev_fast, "Moving both 1 step"))
    steps.append(("Phase 2: Find Duplicate", slow, fast, prev_slow, prev_fast, f"Duplicate found at index/value {slow}"))

    step_index = 0
    annotations = []

    def update_visual(phase, slow, fast, prev_slow, prev_fast, msg):
        nonlocal annotations
        for b in boxes:
            b.set_color("#333333")
        for ann in annotations:
            ann.remove()
        annotations.clear()

        # Highlight slow/fast boxes
        boxes[slow].set_color("#00FFAA")  # Slow
        boxes[fast].set_color("#FFA500")  # Fast

        # Add text above boxes for movement
        if prev_slow is not None:
            annotations.append(ax.text(prev_slow, 1.8, f"🐢→{slow}", color="#00FFAA", ha="center", fontsize=11))
        if prev_fast is not None:
            annotations.append(ax.text(prev_fast, 2.0, f"🐇→{fast}", color="#FFA500", ha="center", fontsize=11))

        # Mark meeting points
        if slow == fast:
            annotations.append(ax.text(slow, 1.3, "🎯", color="#00FF00", ha="center", fontsize=16))
            boxes[slow].set_color("#00FF00")

        # Step info
        phase_text.set_text(phase)
        step_text.set_text(msg)

        fig.canvas.draw_idle()

    def next_step(event):
        nonlocal step_index
        if step_index < len(steps) - 1:
            time.sleep(1)
            step_index += 1
            phase, s, f, ps, pf, msg = steps[step_index]
            update_visual(phase, s, f, ps, pf, msg)

    def prev_step(event):
        nonlocal step_index
        if step_index > 0:
            step_index -= 1
            phase, s, f, ps, pf, msg = steps[step_index]
            update_visual(phase, s, f, ps, pf, msg)

    bnext.on_clicked(next_step)
    bprev.on_clicked(prev_step)

    # Initialize
    phase, s, f, ps, pf, msg = steps[0]
    update_visual(phase, s, f, ps, pf, msg)
    plt.show()


# ▶ Example usage
visualize_floyd_two_phases([2,5,9,6,9,3,8,9,7,1])


