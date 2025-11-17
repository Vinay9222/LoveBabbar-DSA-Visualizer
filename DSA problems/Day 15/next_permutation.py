import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches

# ============ LOGIC TO CAPTURE EACH STEP ==============

def next_permutation_steps(nums):
    steps = []
    arr = nums[:]
    steps.append(("Initial Array", arr[:], {
        "action": "Start with the given array"
    }))

    n = len(arr)

    # ==============================
    # 1. Find Pivot (with loop steps)
    # ==============================
    pivot = -1
    for i in range(n - 2, -1, -1):

        steps.append((
            f"Pivot loop → checking i = {i}",
            arr[:],
            {
                "check": i,
                "action": f"Compare arr[{i}] ({arr[i]}) < arr[{i+1}] ({arr[i+1]})"
            }
        ))

        if arr[i] < arr[i + 1]:
            pivot = i
            break

    steps.append((
        f"Pivot found at index {pivot}",
        arr[:],
        {
            "pivot": pivot,
            "action": f"arr[{pivot}] ({arr[pivot]}) is the first element where arr[i] < arr[i+1]"
        }
    ))

    if pivot == -1:
        arr.reverse()
        steps.append((
            "No pivot found → reverse whole array",
            arr[:],
            {
                "reverse": True,
                "action": "Array is descending → reverse to get smallest permutation"
            }
        ))
        return steps

    # ====================================
    # 2. Find Successor (with loop steps)
    # ====================================
    for j in range(n - 1, pivot, -1):

        steps.append((
            f"Successor loop → checking j = {j}",
            arr[:],
            {
                "pivot": pivot,
                "check": j,
                "action": f"Find first element greater than arr[pivot] ({arr[pivot]}). Compare arr[{j}] ({arr[j]}) > {arr[pivot]}?"
            }
        ))

        if arr[j] > arr[pivot]:
            successor = j
            break

    steps.append((
        f"Successor found at index {successor}",
        arr[:],
        {
            "pivot": pivot,
            "successor": successor,
            "action": f"arr[{successor}] ({arr[successor]}) is the smallest element > arr[{pivot}] ({arr[pivot]})"
        }
    ))

    # =========================
    # 3. Swap
    # =========================
    arr[pivot], arr[successor] = arr[successor], arr[pivot]
    steps.append((
        "Swap pivot & successor",
        arr[:],
        {
            "pivot": pivot,
            "successor": successor,
            "swap": True,
            "action": f"Swapping arr[{pivot}] and arr[{successor}]"
        }
    ))

    # =========================
    # 4. Reverse Tail
    # =========================
    left, right = pivot + 1, n - 1
    while left < right:

        steps.append((
            f"Reversing → swap index {left} and {right}",
            arr[:],
            {
                "reverse_start": pivot + 1,
                "action": f"Swap arr[{left}] ({arr[left]}) with arr[{right}] ({arr[right]})"
            }
        ))

        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

    steps.append((
        f"Reverse tail (from index {pivot+1})",
        arr[:],
        {
            "reverse_start": pivot + 1,
            "action": "Right-side segment sorted ascending to form the next permutation"
        }
    ))

    # Final state
    steps.append((
        "Final Next Permutation",
        arr[:],
        {
            "action": "This is the next lexicographical permutation"
        }
    ))

    return steps


# ============ VISUALIZATION CODE ===================

class Visualizer:
    def __init__(self, data):
        self.steps = next_permutation_steps(data)
        self.index = 0

        # Dark theme
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(10, 3))
        plt.subplots_adjust(bottom=0.3)

        # Buttons
        axprev = plt.axes([0.25, 0.05, 0.2, 0.12])
        axnext = plt.axes([0.55, 0.05, 0.2, 0.12])

        self.bnext = Button(axnext, 'Next ➜', color="#333", hovercolor="#444")
        self.bprev = Button(axprev, '⟵ Prev', color="#333", hovercolor="#444")

        self.bnext.on_clicked(self.next)
        self.bprev.on_clicked(self.prev)

        self.draw()

    def draw_array(self, arr, info):
        self.ax.clear()
        self.ax.axis('off')

        start_x = 0.1
        y = 0.5
        box_w = 0.08
        box_h = 0.25

        for i, val in enumerate(arr):
            # Default box color
            face = "#1f1f1f"
            edge = "white"
            text_color = "white"

            # Highlight pivot
            if "pivot" in info and i == info["pivot"]:
                face = "#003366"
                edge = "#00aaff"

            # Highlight successor
            if "successor" in info and i == info["successor"]:
                face = "#004422"
                edge = "#00ff88"

            # Highlight swap
            if info.get("swap"):
                text_color = "yellow"

            # Highlight reversed region
            if "reverse_start" in info and i >= info["reverse_start"]:
                face = "#331100"
                edge = "#ff8800"

            rect = patches.FancyBboxPatch(
                (start_x + i * box_w, y),
                box_w, box_h,
                boxstyle="round,pad=0.02",
                linewidth=1.8,
                edgecolor=edge,
                facecolor=face
            )
            self.ax.add_patch(rect)
            self.ax.text(start_x + i * box_w + box_w / 2, y + box_h / 2,
                         str(val), ha='center', va='center',
                         fontsize=14, color=text_color)

        # Step title
        title, _, _ = self.steps[self.index]
        self.ax.text(0.5, 0.85, title, ha='center', va='center',
                     fontsize=16, color="#66ccff")

    def draw(self):
        title, arr, info = self.steps[self.index]
        self.draw_array(arr, info)
        plt.draw()

    def next(self, event):
        if self.index < len(self.steps) - 1:
            self.index += 1
            self.draw()

    def prev(self, event):
        if self.index > 0:
            self.index -= 1
            self.draw()


# Run Visualization
Visualizer([1,3,2,4])
plt.show()
