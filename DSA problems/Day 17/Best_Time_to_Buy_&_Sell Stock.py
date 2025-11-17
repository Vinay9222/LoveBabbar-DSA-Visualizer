import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button


prices = [7, 1, 5, 3, 6, 4]

steps = []
min_price = float('inf')
min_index = -1
max_profit = 0
sell_index = -1


# ---------- PREPARE STEP DATA ----------
for i in range(len(prices)):
    price = prices[i]

    # Update min (buy)
    if price < min_price:
        min_price = price
        min_index = i

    # Calculate potential profit
    profit = price - min_price
    if profit > max_profit:
        max_profit = profit
        sell_index = i

    steps.append({
        "i": i,
        "prices": prices,
        "min_index": min_index,
        "sell_index": sell_index
    })


# ---------- VISUALIZATION ----------
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(bottom=0.25)

current_step = 0


def draw(step_id):
    ax.clear()
    step = steps[step_id]

    prices = step["prices"]
    min_idx = step["min_index"]
    sell_idx = step["sell_index"]

    ax.set_title("Best Time to Buy & Sell Stock – Step Visualization", fontsize=16, weight='bold')

    # Draw array boxes
    for i, v in enumerate(prices):
        box = patches.Rectangle((i, 0), 1, 1, edgecolor="black", facecolor="#20232a")
        ax.add_patch(box)
        ax.text(i + 0.5, 0.5, str(v), ha="center", va="center", color="white", fontsize=12, weight='bold')

    # Arrow for min (BUY)
    ax.annotate(
        "BUY (min)",
        xy=(min_idx + 0.5, 1.05),
        xytext=(min_idx + 0.5, 1.6),
        arrowprops=dict(arrowstyle="->", lw=2),
        ha="center",
        fontsize=12,
        color="green",
        weight='bold'
    )

    # Arrow for max SELL
    if sell_idx != -1 and sell_idx != min_idx:
        ax.annotate(
            "SELL (max)",
            xy=(sell_idx + 0.5, 1.05),
            xytext=(sell_idx + 0.5, 1.6),
            arrowprops=dict(arrowstyle="->", lw=2),
            ha="center",
            fontsize=12,
            color="orange",
            weight='bold'
        )

    # Step info
    ax.text(0, -0.4, f"Step: {step_id + 1}/{len(steps)}", fontsize=12, weight='bold')
    ax.text(0, -0.7, f"Current Index: {step['i']}   |   Price = {prices[step['i']]}", fontsize=11)
    ax.text(0, -1.0, f"Min Price Index = {min_idx} (Price {prices[min_idx]})", fontsize=11, color="green")
    if sell_idx != -1:
        ax.text(0, -1.3, f"Sell Index = {sell_idx} (Price {prices[sell_idx]})", fontsize=11, color="orange")

    ax.set_xlim(0, len(prices))
    ax.set_ylim(-1.6, 2.2)
    ax.axis("off")
    fig.canvas.draw_idle()


# Button callbacks
def next_step(event):
    global current_step
    if current_step < len(steps) - 1:
        current_step += 1
    draw(current_step)


def prev_step(event):
    global current_step
    if current_step > 0:
        current_step -= 1
    draw(current_step)


# Buttons
axprev = plt.axes([0.25, 0.05, 0.15, 0.08])
axnext = plt.axes([0.60, 0.05, 0.15, 0.08])

bnext = Button(axnext, "NEXT →")
bprev = Button(axprev, "← PREV")

bnext.on_clicked(next_step)
bprev.on_clicked(prev_step)

draw(0)
plt.show()
