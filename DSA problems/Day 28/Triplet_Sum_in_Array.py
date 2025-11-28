import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.widgets import Button

# ---------- CONFIG ----------
arr = [6,3,4,6,2,1,1,4,6,8,10,45]
target = 22
# arr = [6,3,4,4,6,8]
# target = 18
# ----------------------------

arr_sorted = sorted(arr)
n = len(arr_sorted)
steps = []

# Store all states (two-pointer approach)
for i in range(n-2):
    l, r = i+1, n-1
    while l < r:
        s = arr_sorted[i] + arr_sorted[l] + arr_sorted[r]
        steps.append((i,l,r,s))
        if s == target: break
        elif s < target: l += 1
        else: r -= 1

# for i in range(n-2):
#     for l in range(i+1, n-1):
#         for r in range(l+1, n):
#             s = arr_sorted[i] + arr_sorted[l] + arr_sorted[r]
#             steps.append((i,l,r,s))
#             if s == target:
#                 break
#         else:
#             continue
#         break

# ---------- DRAW FUNCTION ----------
fig, ax = plt.subplots(figsize=(12,5))
plt.subplots_adjust(bottom=0.28)
fig.patch.set_facecolor("black")
ax.set_facecolor("black")
step = 0

def draw(step):
    ax.clear()
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")
    i,l,r,s = steps[step]

    ax.set_xlim(0,len(arr_sorted))
    ax.set_ylim(0,5)
    ax.axis('off')

    for idx,val in enumerate(arr_sorted):
        x = idx + 0.15

        # base color
        color = "#3A3A3A" 

        if idx==i: color="royalblue"      # i pointer
        if idx==l: color="lime"           # left pointer
        if idx==r: color="red"            # right pointer

        # triplet match highlight
        if s==target and idx in (i,l,r):
            color="gold"

        # element box
        box = FancyBboxPatch((x,3),0.7,1.0,
            boxstyle="round,pad=0.3",fc=color,ec="white",lw=1.5)
        ax.add_patch(box)
        ax.text(x+0.35,3.5,str(val),ha='center',va='center',
                color="black" if color=="gold" else "white",
                fontsize=14,fontweight="bold")

        # index below box
        ax.text(x+0.35,2.5,str(idx),
                ha="center",color="cyan",fontsize=12)

    # status text
    ax.text(0.05,4.6,f"Step: {step+1}/{len(steps)}  |  i={i}, l={l}, r={r}  |  sum={s}",
            color="white",fontsize=14)

    if s==target:
        ax.text(2,1.2,f"🎉 Triplet Found = ({arr_sorted[i]}, {arr_sorted[l]}, {arr_sorted[r]})",
                color="yellow",fontsize=18,fontweight="bold")
    elif s < target:
        ax.text(2,1.2,"Sum < Target → Move L Forward",color="lime",fontsize=14)
    else:
        ax.text(2,1.2,"Sum > Target → Move R Back",color="red",fontsize=14)

    plt.draw()

# ---------- BUTTONS ----------
def next_step(e):
    global step
    if step < len(steps)-1:
        step+=1; draw(step)

def prev_step(e):
    global step
    if step>0:
        step-=1; draw(step)

axprev=plt.axes([0.25,0.08,0.2,0.12])
axnext=plt.axes([0.55,0.08,0.2,0.12])

bprev=Button(axprev,"◀ PREV",color="gray",hovercolor="white")
bnext=Button(axnext,"NEXT ▶",color="gray",hovercolor="white")

bprev.on_clicked(prev_step)
bnext.on_clicked(next_step)

draw(0)
plt.show()
