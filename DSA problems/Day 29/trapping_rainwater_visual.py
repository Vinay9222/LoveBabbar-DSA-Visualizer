import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# ---------------- INPUT ----------------
arr = [4, 2, 0, 6, 3, 2, 5]
n = len(arr)

# use None as sentinel so we only show computed entries
left = [None] * n
right = [None] * n
water = [None] * n

# Phase definitions (0..MAX_STEP inclusive)
PHASE_LEFT = n               # steps 0 .. n-1
PHASE_RIGHT = n * 2          # steps n .. 2n-1
MAX_STEP = 3 * n - 1         # steps 2n .. 3n-1 -> final

# starting step
step = 0

# ---------------- FIGURE SETUP ----------------
fig, ax = plt.subplots(figsize=(14, 7))
plt.style.use("dark_background")
fig.canvas.manager.set_window_title("Trapping Rain Water — Interactive")

def render(s):
    """Render the whole screen for step s."""
    ax.clear()
    ax.set_facecolor("black")

    # PHASE LOGIC & index for highlight
    if s < PHASE_LEFT:
        mode = "Building LEFT array"
        idx = s
        # compute left at idx
        if idx == 0:
            left[idx] = arr[idx]
        else:
            # left[idx-1] is already computed (because we build left sequentially)
            left[idx] = max(left[idx - 1], arr[idx])
        right_show_count = 0
        water_show_count = 0

    elif s < PHASE_RIGHT:
        mode = "Building RIGHT array"
        idx = s - PHASE_LEFT
        pos = n - 1 - idx  # fill from right to left
        if pos == n - 1:
            right[pos] = arr[pos]
        else:
            right[pos] = max(right[pos + 1], arr[pos])
        right_show_count = idx + 1
        water_show_count = 0
        # ensure left is fully shown after its build phase
        # left values remain because we computed them previously

    else:
        mode = "Calculating WATER & TOTAL"
        idx = s - PHASE_RIGHT
        # compute water at idx if within bounds
        if idx < n:
            # left[idx] and right[idx] should already be computed by now
            # but guard in case user jumped: compute if missing
            if left[idx] is None:
                # compute missing left up to idx
                for k in range(0, idx + 1):
                    if left[k] is None:
                        left[k] = arr[k] if k == 0 else max(left[k - 1], arr[k])
            if right[idx] is None:
                # compute missing right up to idx
                for k in range(n - 1, idx - 1, -1):
                    if right[k] is None:
                        right[k] = arr[k] if k == n - 1 else max(right[k + 1], arr[k])

            water[idx] = max(0, min(left[idx], right[idx]) - arr[idx])
        right_show_count = n
        water_show_count = sum(1 for x in water if x is not None)

    # ---------- TITLE ----------
    total_so_far = sum([w for w in water if w is not None])
    ax.set_title(f"⛲ Trapping Rain Water  |  STEP {s}  |  MODE: {mode}",
                 fontsize=16, color="white")

    # ---------- BARS ----------
    for i, v in enumerate(arr):
        bar_col = "red" if i == (idx if s < PHASE_RIGHT else (idx if s >= PHASE_RIGHT and idx < n else None)) else "#6e6e6e"
        ax.bar(i, v, color=bar_col, width=0.65, edgecolor="white")
        ax.text(i, v + 0.25, str(v), ha="center", color="white", fontsize=11,
                bbox=dict(boxstyle="round,pad=0.2", fc="black", ec="white"))

    # index labels
    for i in range(n):
        ax.text(i, -0.65, str(i), ha="center", color="yellow", fontsize=10)

    # ---------- RIGHT VECTOR (TOP) ----------
    # show only computed values, else blank boxes
    right_display = []
    for i in range(n):
        if right[i] is not None:
            right_display.append(f"[{right[i]}]")
        else:
            right_display.append("[  ]")
    ax.text(-0.5, max(arr) + 2.8, "RIGHT → " + "  ".join(right_display),
            fontsize=12, color="blue", fontweight="bold")

    # ---------- WATER VECTOR (TOP - below RIGHT) ----------
    if water_show_count > 0:
        water_display = []
        for i in range(n):
            if water[i] is not None:
                water_display.append(f"[{water[i]}]")
            else:
                water_display.append("[  ]")
        ax.text(-0.5, max(arr) + 1.6, "WATER → " + "  ".join(water_display),
                fontsize=12, color="white")

    # ---------- TOTAL ANSWER DISPLAY ----------
    ax.text(-0.5, max(arr) + 4.2, f"Total Water (so far) = {total_so_far}", fontsize=13, color="lime")

    # ---------- LEFT VECTOR (BOTTOM) ----------
    left_display = []
    for i in range(n):
        if left[i] is not None:
            left_display.append(f"[{left[i]}]")
        else:
            left_display.append("[  ]")
    ax.text(-0.5, -2.2, "LEFT  → " + "  ".join(left_display),
            fontsize=12, color="orange", fontweight="bold")

    # layout limits
    ax.set_xlim(-1, n)
    ax.set_ylim(-3, max(arr) + 5)

    # small instructions
    ax.text(n - 2.5, -2.9, "Controls: ⬅ Prev | Next ➡ buttons or keyboard ← / →  (or 'p' / 'n')",
            fontsize=9, color="lightgray")

    fig.canvas.draw_idle()


# ---------- BUTTON CALLBACKS ----------
def next_cb(event=None):
    global step
    if step < MAX_STEP:
        step += 1
        render(step)

def prev_cb(event=None):
    global step
    if step > 0:
        step -= 1
        render(step)

# assign buttons properly (so they stay alive)
axprev = plt.axes([0.30, 0.02, 0.12, 0.06])
axnext = plt.axes([0.55, 0.02, 0.12, 0.06])
btn_prev = Button(axprev, "⬅ Prev", color="#444444", hovercolor="#666666")
btn_next = Button(axnext, "Next ➡", color="#444444", hovercolor="#666666")
btn_prev.on_clicked(lambda ev: prev_cb())
btn_next.on_clicked(lambda ev: next_cb())

# ---------- KEYBOARD HANDLER ----------
def on_key(event):
    # event.key gives 'left'/'right' for arrows, or characters like 'n','p'
    key = event.key
    if key in ("right", "n"):
        next_cb()
    elif key in ("left", "p"):
        prev_cb()
        
# correct small syntax: rebind properly for 'end' and 'home'
def on_key_fixed(event):
    global step
    key = event.key
    if key in ("right", "n"):
        next_cb()
    elif key in ("left", "p"):
        prev_cb()
    elif key == "home":
        step = 0
        render(step)
    elif key == "end":
        step = MAX_STEP
        render(step)

# connect the fixed handler
fig.canvas.mpl_connect("key_press_event", on_key_fixed)

# ---------- INITIAL RENDER ----------
render(step)
plt.show()
