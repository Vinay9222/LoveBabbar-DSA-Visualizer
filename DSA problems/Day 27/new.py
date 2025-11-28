import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button

# ------------ ARRAYS --------------------
A = [11, 7, 1, 13, 21, 3, 7, 3]
B = [11, 3, 7, 1, 7, 7]

steps = []
mp = {}

# Build frequency map from A
for i, x in enumerate(A):
    mp[x] = mp.get(x, 0) + 1
    steps.append({
        "phase":"Building Map",
        "pointerA":i,
        "pointerB":None,
        "action":f"Insert {x} into map",
        "map":mp.copy(),
        "result":"Building frequency table of A",
        "color":"blue"
    })

# Checking subset
subset=True
for j, y in enumerate(B):
    if mp.get(y,0)>0:
        mp[y]-=1
        steps.append({
            "phase":"Checking Subset",
            "pointerA":None,
            "pointerB":j,
            "action":f"{y} Found → Reduce Frequency",
            "map":mp.copy(),
            "result":"Match Found ✔ Continue",
            "color":"green"
        })
    else:
        subset=False
        steps.append({
            "phase":"Checking Subset",
            "pointerA":None,
            "pointerB":j,
            "action":f"{y} Not Found!!",
            "map":mp.copy(),
            "result":"❌ Not a Subset → Stop",
            "color":"red"
        })
        break

final_text = "✔ B IS A SUBSET OF A" if subset else "❌ B IS NOT A SUBSET OF A"

# ---------------- VISUAL ENGINE -------------------
fig, ax = plt.subplots(figsize=(11,6))
plt.subplots_adjust(bottom=0.25)
index=0

def draw():
    ax.clear()
    ax.set_title("ARRAY SUBSET VISUALIZER", fontsize=18, fontweight="bold")

    step=steps[index]

    # ----------- Display Array A -----------------
    ax.text(0.02,0.9,"Array A:",fontsize=15,fontweight="bold")
    for i,val in enumerate(A):
        x,y=0.02+i*0.08,0.78
        rect=Rectangle((x,y),0.07,0.07,fill=False,linewidth=2)
        ax.add_patch(rect)
        ax.text(x+0.025,y+0.025,str(val),fontsize=13)

        # pointer highlight
        if step['pointerA']==i:
            rect=Rectangle((x,y),0.07,0.07,fill=True,alpha=0.4,color="yellow")
            ax.add_patch(rect)

    # ----------- Display Array B -----------------
    ax.text(0.02,0.70,"Array B:",fontsize=15,fontweight="bold")
    for j,val in enumerate(B):
        x,y=0.02+j*0.10,0.52
        rect=Rectangle((x,y),0.09,0.08,fill=False,linewidth=2)
        ax.add_patch(rect)
        ax.text(x+0.03,y+0.03,str(val),fontsize=13)

        if step["pointerB"]==j:
            c="lime" if step["color"]=="green" else ("red" if step["color"]=="red" else "yellow")
            rect=Rectangle((x,y),0.09,0.08,fill=True,alpha=0.5,color=c)
            ax.add_patch(rect)

    # ---------------- DETAILS PANEL ---------------
    info = (
        f"Step {index+1}/{len(steps)}\n"
        f"Phase      : {step['phase']}\n"
        f"Action     : {step['action']}\n"
        f"Map        : {step['map']}\n"
        f"Status     : {step['result']}\n"
    )
    ax.text(0.02,0.0,info,fontsize=13,fontweight="bold",
            color=step["color"],bbox=dict(facecolor="black",alpha=0.2,pad=10))

    if index==len(steps)-1:
        ax.text(0.02,0.0,f"FINAL RESULT : {final_text}",
                fontsize=10,fontweight="bold",
                color=("lime" if subset else "red"))

    ax.axis("off")
    fig.canvas.draw()

# ------------ BUTTONS -----------------
def next_step(e):
    global index
    if index < len(steps)-1: index+=1
    draw()

def prev_step(e):
    global index
    if index>0:index-=1
    draw()

btn_next = plt.axes([0.70,0.08,0.20,0.10])
btn_prev = plt.axes([0.10,0.08,0.20,0.10])

next_b=Button(btn_next,"Next →")
prev_b=Button(btn_prev,"← Previous")
next_b.on_clicked(next_step)
prev_b.on_clicked(prev_step)

draw()
plt.show()
