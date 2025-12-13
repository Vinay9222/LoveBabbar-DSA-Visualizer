import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
import copy

# ---------------- MATRIX ----------------
matrix = [
    [1,1,1,0,1],
    [1,1,1,1,1],
    [1,1,1,1,1],
    [1,1,0,1,1],
]

nrows, ncols = len(matrix), len(matrix[0])

# ---------------- GENERATE STEPS ----------------
steps = []
heights = [0]*ncols
max_area = 0
max_rect_coords = None

for r, row in enumerate(matrix):
    # Update heights
    for c, val in enumerate(row):
        heights[c] = heights[c]+1 if val==1 else 0

    # Stack-based Largest Rectangle logic
    stack = []
    h = heights + [0]  # sentinel
    for i, height in enumerate(h):
        step = {'row': copy.deepcopy(row), 'heights': copy.deepcopy(heights),
                'cur_row': r, 'stack': copy.deepcopy(stack),
                'action': None, 'action_index': None,
                'max_rect': copy.deepcopy(max_rect_coords), 'max_area': max_area}
        
        while stack and h[stack[-1]] > height:
            top = stack.pop()
            h_val = h[top]
            width = i if not stack else i - stack[-1] - 1
            area = h_val * width
            if area > max_area:
                max_area = area
                col1 = 0 if not stack else stack[-1]+1
                col2 = i-1
                row2 = r
                row1 = row2 - h_val +1
                max_rect_coords = (row1, col1, row2, col2)
            step['action'] = 'pop'
            step['action_index'] = top
            step['stack'] = copy.deepcopy(stack)
            step['max_rect'] = copy.deepcopy(max_rect_coords)
            step['max_area'] = max_area
            steps.append(copy.deepcopy(step))
        
        stack.append(i)
        step_push = {'row': copy.deepcopy(row), 'heights': copy.deepcopy(heights),
                     'cur_row': r, 'stack': copy.deepcopy(stack),
                     'action': 'push', 'action_index': i,
                     'max_rect': copy.deepcopy(max_rect_coords),
                     'max_area': max_area}
        steps.append(copy.deepcopy(step_push))

# ---------------- VISUALIZATION ----------------
current_idx = [0]
fig, ax = plt.subplots(figsize=(9,6))
plt.subplots_adjust(bottom=0.25)

def draw_step(step):
    ax.clear()
    # Extend y-axis to leave space below for text
    ax.set_xlim(0,ncols)
    ax.set_ylim(-4,nrows)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    ax.set_xticks(range(ncols))
    ax.set_yticks(range(nrows))
    ax.grid(True)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Draw matrix
    for r in range(nrows):
        for c in range(ncols):
            color = "#AAAAAA" if matrix[r][c]==1 else "#DDDDDD"
            if r==step['cur_row']:
                color = "#87CEFA" if matrix[r][c]==1 else "#B0E0E6"
            rect = patches.Rectangle((c,r),1,1,facecolor=color,edgecolor="black")
            ax.add_patch(rect)
            ax.text(c+0.5,r+0.5,str(matrix[r][c]),ha='center',va='center',fontsize=12,fontweight='bold')

    # Highlight max rectangle
    if step['max_rect']:
        r1,c1,r2,c2 = step['max_rect']
        width = c2 - c1 +1
        height = r2 - r1 +1
        rect = patches.Rectangle((c1,r1),width,height,linewidth=3,edgecolor="green",facecolor="none")
        ax.add_patch(rect)

    # Heights vector display (below matrix)
    ax.text(0,nrows+0.2,"Heights vector: " + str(step['heights']),
            ha='left',va='center',fontsize=12,fontweight='bold',color='black')
    ax.text(0,nrows+0.7,f"Stack indices: {step['stack']}",
            ha='left',va='center',fontsize=12,fontweight='bold',color='orange')
    ax.text(0,nrows+1.2,f"Action: {step['action'].upper() if step['action'] else 'None'}",
            ha='left',va='center',fontsize=12,fontweight='bold',color='red')
    ax.text(0,nrows+1.7,f"Max area so far: {step['max_area']}",
            ha='left',va='center',fontsize=12,fontweight='bold',color='green')

    ax.set_title(f"Row {step['cur_row']} Traversal",fontsize=14,fontweight='bold')
    fig.canvas.draw_idle()

# ---------------- BUTTON CALLBACKS ----------------
def next_step(event=None):
    if current_idx[0] < len(steps)-1:
        current_idx[0] +=1
        draw_step(steps[current_idx[0]])

def prev_step(event=None):
    if current_idx[0] >0:
        current_idx[0] -=1
        draw_step(steps[current_idx[0]])

# Buttons
axprev = plt.axes([0.7,0.05,0.1,0.05])
axnext = plt.axes([0.81,0.05,0.1,0.05])
btn_prev = Button(axprev,'Previous')
btn_next = Button(axnext,'Next')
btn_prev.on_clicked(prev_step)
btn_next.on_clicked(next_step)

# Keyboard navigation
def on_key(event):
    if event.key=='left': prev_step()
    elif event.key=='right': next_step()

fig.canvas.mpl_connect('key_press_event',on_key)

draw_step(steps[current_idx[0]])
plt.show()
