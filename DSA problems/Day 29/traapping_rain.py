import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# ---------------- INPUT ----------------
arr = [4, 2, 0, 6, 3, 2, 5]
n = len(arr)

# storage
water = [None] * n

# pointer initial values
i, j = 0, n-1
left = right = 0
ans = 0

# store history for BACK button support
history = []  # stores (i,j,left,right,water_copy,ans)


# ----------- FIGURE SETUP ----------
fig, ax = plt.subplots(figsize=(14, 7))
plt.style.use("dark_background")
fig.canvas.manager.set_window_title("Trapping Rain Water — Two Pointer Method")


def render():
    ax.clear()
    ax.set_facecolor("black")

    # Title
    ax.set_title(
        f"⛲ Two Pointer Trapping Rain Water\ni={i}  j={j}  | left={left}  right={right}  | Total={ans}",
        fontsize=16, color="white"
    )

    # Draw bars
    for idx, v in enumerate(arr):
        col = "#6e6e6e"
        if idx == i: col = "yellow"
        if idx == j: col = "red"

        ax.bar(idx, v, color=col, width=0.65, edgecolor="white")
        ax.text(idx, v+0.25, str(v), ha="center", color="white", fontsize=11,
                bbox=dict(boxstyle="round,pad=0.18", fc="black", ec="white"))

        ax.text(idx, -0.65, str(idx), ha="center", color="cyan", fontsize=10)

    # WATER DISPLAY ROW
    disp = []
    for x in water:
        disp.append(f"[{x}]" if x is not None else "[  ]")
    ax.text(-0.5, max(arr)+2.3, "Water stored → " + "  ".join(disp),
            fontsize=13, color="lime")

    ax.text(0, max(arr)+3.2, f"Total Water Trapped = {ans}", fontsize=16, color="aqua")

    ax.text(n-3.8, -2.3, "⬅ Prev  |  Next ➡   (Keyboard Arrow Keys Also Work)",
            fontsize=9, color="gray")

    ax.set_xlim(-1, n)
    ax.set_ylim(-3, max(arr)+5)
    fig.canvas.draw_idle()



def next_step(event=None):
    global i,j,left,right,ans

    if i>j: return  # completed

    # store snapshot for BACK button
    history.append((i,j,left,right,water.copy(),ans))

    if arr[i] <= arr[j]:
        if arr[i] > left:
            left = arr[i]
        else:
            gained = left-arr[i]
            ans += gained
            water[i] = gained
        i+=1
    else:
        if arr[j] > right:
            right = arr[j]
        else:
            gained = right-arr[j]
            ans+= gained
            water[j]=gained
        j-=1

    render()



def prev_step(event=None):
    global i,j,left,right,water,ans

    if len(history)==0: return

    (i,j,left,right,w,a) = history.pop()
    water = w
    ans = a

    render()



# -------- Buttons --------
axprev = plt.axes([0.30, 0.02, 0.12, 0.06])
axnext = plt.axes([0.55, 0.02, 0.12, 0.06])

btn_prev = Button(axprev, "⬅ Prev", color="#444", hovercolor="#666")
btn_next = Button(axnext, "Next ➡", color="#444", hovercolor="#666")

btn_prev.on_clicked(prev_step)
btn_next.on_clicked(next_step)


# -------- Keyboard Support --------
def on_key(event):
    if event.key in ("right","n"): next_step()
    if event.key in ("left","p"): prev_step()

fig.canvas.mpl_connect("key_press_event",on_key)

# -------- START --------
render()
plt.show()
