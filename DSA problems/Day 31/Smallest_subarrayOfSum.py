import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button

# -------------------- INPUT --------------------
arr = [1, 4, 45, 6, 0, 19]   # you can change it anytime
X = 51                       # target sum
n = len(arr)

# -------------------- WINDOW VARIABLES --------------------
i = j = 0
sum_val = 0
ans = float('inf')
frames = []  # stores every visual step

# -------------------- RECORD SIMULATION --------------------
while i < n:

    # Step → Expand Right
    sum_val += arr[i]
    frames.append((i, j, sum_val, ans, "Expand window → i++ (Add arr[i])"))

    # Step → Shrink Left
    while j < n and sum_val > X:
        ans = min(ans, i-j+1)
        frames.append((i, j, sum_val, ans, "Sum > X  → Check ans & Shrink from left"))
        
        sum_val -= arr[j]
        frames.append((i, j, sum_val, ans, "Subtract arr[j] → j++"))
        j += 1
    
    i += 1

if ans == float('inf'):
    ans = 0


# =================== VISUALIZER ===================
fig, ax = plt.subplots(figsize=(12,4))
fig.patch.set_facecolor("#0B0B0B")  # deep black
plt.subplots_adjust(bottom=0.25)


def render(step):
    ax.clear()
    ax.set_facecolor("#0B0B0B")   # pitch black canvas
    ax.axis("off")

    i,j,total,best,msg = frames[step]

    # --------- Draw Boxes with Professional Colors ----------
    for idx, value in enumerate(arr):

        # default theme
        box_color = "#454545"       # soft gray outline

        # active pointer highlights
        if idx == i and idx == j:
            box_color = "#00FFC6"   # mint aqua (both meet)
        elif idx == i:
            box_color = "#00A8FF"   # neon blue → RIGHT pointer
        elif idx == j:
            box_color = "#FFAA00"   # bright orange → LEFT pointer

        rect = Rectangle((idx,0.3),1,1,linewidth=2.8,
                         edgecolor=box_color,facecolor="none")
        ax.add_patch(rect)

        ax.text(idx+0.5,0.8,str(value),
                color="white",ha="center",va="center",fontsize=16,fontweight="bold")

        # ======= ADD i and j POINTERS BELOW BOXES =======
        if idx == i:
            ax.text(idx+0.5,0.15,"i",color="#00A8FF",
                    fontsize=13,fontweight="bold",ha="center")

        if idx == j:
            ax.text(idx+0.5,0.02,"j",color="#FFAA00",
                    fontsize=13,fontweight="bold",ha="center")


    # ----------------- Information Panel ------------------
    ax.text(-0.2,-0.35,f"Current Sum = {total}",fontsize=15,color="#00E6FF")
    ax.text(-0.2,-0.70,f"Min Length Found = {best}",fontsize=15,color="#00FF8C")
    ax.text(-0.2,-1.05,msg,fontsize=13,color="#FFDD55")

    ax.set_xlim(-0.5,len(arr)+0.5)
    ax.set_ylim(-1.5,1.6)

    plt.title("Smallest Subarray With Sum > X (Sliding Window)",
              fontsize=15,color="#54FFF3",fontweight="bold")


# ----------------- BUTTON CONTROLS -----------------
current = 0
render(0)

def nxt(event):
    global current
    if current < len(frames)-1:
        current += 1
        render(current)
        fig.canvas.draw_idle()

def prev(event):
    global current
    if current > 0:
        current -= 1
        render(current)
        fig.canvas.draw_idle()

axprev = plt.axes([0.32,0.05,0.14,0.1])
axnext = plt.axes([0.54,0.05,0.14,0.1])

bprev = Button(axprev,'⟵ PREV',color="#FF5C5C",hovercolor="#FF8E8E")
bnext = Button(axnext,'NEXT ⟶',color="#44FF99",hovercolor="#66FFB3")

bprev.on_clicked(prev)
bnext.on_clicked(nxt)

plt.show()
