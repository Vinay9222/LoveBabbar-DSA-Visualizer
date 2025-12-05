import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.style.use("dark_background")

def draw_array(arr, mid_idxs, title=""):
    plt.clf()
    plt.title(title, fontsize=20, color="cyan")
    
    ax = plt.gca()
    ax.set_xlim(0, len(arr))
    ax.set_ylim(0, 2)
    ax.axis("off")

    for i, val in enumerate(arr):

        # Default neon cyan color for boxes
        box_color = "#00eaff"
        text_color = "white"

        # If index is middle index (or 2 indices)
        if i in mid_idxs:
            box_color = "magenta"
            text_color = "white"

        # Draw element box
        rect = patches.Rectangle(
            (i + 0.05, 1), 0.9, 0.7,
            linewidth=2.5,
            edgecolor="white",
            facecolor=box_color
        )
        ax.add_patch(rect)

        # Element value text
        ax.text(i + 0.5, 1.35, str(val), ha="center", va="center",
                fontsize=16, color=text_color, weight="bold")

        # Index label
        ax.text(i + 0.5, 0.6, f"i={i}", ha="center", va="center",
                fontsize=12, color="cyan")

    plt.pause(1.0)


def visualize_median(arr):
    print(f"Original Array: {arr}")

    # Sort array
    sorted_arr = sorted(arr)
    print(f"Sorted Array: {sorted_arr}")

    n = len(sorted_arr)
    mid = n // 2

    # Determine mid index(es)
    if n % 2 == 1:
        mid_indices = [mid]
        title = "Highlighting Middle Index (Odd Length)"
        median_value = sorted_arr[mid]
    else:
        mid_indices = [mid - 1, mid]
        title = "Highlighting Two Middle Indices (Even Length)"
        median_value = (sorted_arr[mid - 1] + sorted_arr[mid]) / 2

    draw_array(sorted_arr, mid_indices, title)

    print("Median =", median_value)

    plt.show()


# ---------------------------
# Example
# ---------------------------
arr = [12, 5, 8, 20, 3, 15]
visualize_median(arr)
