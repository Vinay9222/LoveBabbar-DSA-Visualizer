import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches

# ---------------- SETTINGS ----------------
plt.style.use('dark_background')

# COLORS
COLOR_NORMAL = '#4fc3f7'
COLOR_ACTIVE_I = '#ffeb3b'
COLOR_ACTIVE_J = '#00e676'
COLOR_SWAP = '#ff5252'
COLOR_TEXT_DARK = 'black'

# ---------------- INPUT ----------------
arr = [3, 8, 2, 1, 9, 5, 7, 6]
a = 4
b = 7

# STORAGE FOR STEPS
steps = []

# Record a snapshot
def record(arr, i, j, label, swap_indices=None):
    steps.append({
        'arr': arr.copy(),
        'i': i,
        'j': j,
        'label': label,
        'swap': swap_indices
    })

n = len(arr)
j = 0

# ---------------- FIRST PASS (< a) ----------------
for i in range(n):
    record(arr, i, j, f"Checking i={i}, j={j}")
    if arr[i] < a:
        record(arr, i, j, f"Swap arr[{i}] < a → swapping {arr[i]} and {arr[j]}", (i, j))
        arr[i], arr[j] = arr[j], arr[i]
        j += 1
        record(arr, i, j, f"Post-swap i={i}, j={j}")

# ---------------- SECOND PASS (> b) ----------------
j = n - 1
for i in range(n - 1, -1, -1):
    record(arr, i, j, f"Checking i={i}, j={j}")
    if arr[i] > b:
        record(arr, i, j, f"Swap arr[{i}] > b → swapping {arr[i]} and {arr[j]}", (i, j))
        arr[i], arr[j] = arr[j], arr[i]
        j -= 1
        record(arr, i, j, f"Post-swap i={i}, j={j}")

# ---------------- VISUALIZATION ----------------
current_step = 0

fig, ax = plt.subplots(figsize=(12, 4))
plt.subplots_adjust(bottom=0.25)

# Keep references for pointer text so we can update them instead of redrawing everything
box_patches = []
value_texts = []
pointer_i = None
pointer_j = None
title_text = None

# Initialize empty frame (will be populated by draw_step)
def init_draw():
    ax.clear()
    ax.set_xlim(0, max(1, len(steps[0]['arr'])))
    ax.set_ylim(0, 1)
    ax.axis('off')

    # create boxes and texts
    for idx, val in enumerate(steps[0]['arr']):
        rect = patches.Rectangle((idx + 0.05, 0.3), 0.9, 0.4, linewidth=2,
                                 edgecolor='white', facecolor=COLOR_NORMAL)
        ax.add_patch(rect)
        box_patches.append(rect)
        t = ax.text(idx + 0.5, 0.5, str(val), ha='center', va='center', fontsize=14, color=COLOR_TEXT_DARK)
        value_texts.append(t)

    # title and pointers (placeholders)
    global title_text, pointer_i, pointer_j
    title_text = ax.text(0.5, 0.95, '', ha='center', va='center', fontsize=14, transform=ax.transAxes)
    pointer_i = ax.text(0.5, 0.15, '', ha='center', va='center', fontsize=12)
    pointer_j = ax.text(0.5, 0.85, '', ha='center', va='center', fontsize=12)


# Draw current frame (updates existing artists for smoothness)
def draw_step(step_index):
    step = steps[step_index]

    # safety
    arr_local = step['arr']
    m = len(arr_local)

    # If array length has changed (shouldn't), rebuild
    if len(box_patches) != m:
        box_patches.clear()
        value_texts.clear()
        ax.clear()
        init_draw()

    # Update title
    title_text.set_text(step['label'])

    for idx, val in enumerate(arr_local):
        color = COLOR_NORMAL
        if step['swap'] and idx in step['swap']:
            color = COLOR_SWAP
        elif idx == step['i']:
            color = COLOR_ACTIVE_I
        elif idx == step['j']:
            color = COLOR_ACTIVE_J

        box_patches[idx].set_facecolor(color)
        value_texts[idx].set_text(str(val))

    # Update pointers only if indices in range
    if 0 <= step['i'] < m:
        pointer_i.set_text('i')
        pointer_i.set_x(step['i'] + 0.5)
        pointer_i.set_color(COLOR_ACTIVE_I)
        pointer_i.set_y(0.15)
    else:
        pointer_i.set_text('')

    if 0 <= step['j'] < m:
        pointer_j.set_text('j')
        pointer_j.set_x(step['j'] + 0.5)
        pointer_j.set_color(COLOR_ACTIVE_J)
        pointer_j.set_y(0.85)
    else:
        pointer_j.set_text('')

    fig.canvas.draw_idle()


# Button callbacks with bounds checking
def next_step(event):
    global current_step
    if current_step < len(steps) - 1:
        current_step += 1
        draw_step(current_step)


def prev_step(event):
    global current_step
    if current_step > 0:
        current_step -= 1
        draw_step(current_step)


# Keyboard navigation (left/right)
def on_key(event):
    if event.key == 'right':
        next_step(None)
    elif event.key == 'left':
        prev_step(None)


# Buttons (position adjusted for better clickable area)
axprev = plt.axes([0.35, 0.05, 0.12, 0.075])
axnext = plt.axes([0.53, 0.05, 0.12, 0.075])
bprev = Button(axprev, 'Previous')
bnext = Button(axnext, 'Next')
bprev.on_clicked(prev_step)
bnext.on_clicked(next_step)

# Connect keyboard
fig.canvas.mpl_connect('key_press_event', on_key)

# Prepare initial drawing
if len(steps) == 0:
    raise RuntimeError('No steps recorded — check recording logic')

init_draw()
# Draw first step
draw_step(current_step)

plt.show()