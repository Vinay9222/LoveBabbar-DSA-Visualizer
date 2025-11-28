import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
import copy
import math

EXAMPLE_ARRAY = [2, 2, 4, 2, 1, 3, 2, 5, 2]
K = 4  # threshold divisor (n/k)
BOX_HEIGHT = 0.5
BOX_WIDTH = 0.9

# Color constants
BG_COLOR = "#111111"
TEXT_COLOR = "#FFFFFF"
BOX_FACE = "#1f1f1f"
BOX_EDGE = "#CCCCCC"
CURRENT_POINTER_COLOR = "#00FFFF"  # cyan
FINAL_GREEN = "#2ecc71"            # green
FINAL_LIME_BORDER = "#AEFF6F"      # lime-ish for glow
UPDATE_YELLOW = "#ffd54f"          # yellow for hashmap update
IGNORED_RED = "#e74c3c"            # red for ignored elements

# -------------------------
# Algorithm Step Recorder
# -------------------------
def build_steps(arr, k):
    steps = []
    n = len(arr)
    threshold = n // k if k != 0 else math.inf  # avoid div by zero
    mp = {}  # dictionary to emulate unordered_map<int,int>
    ans = 0

    for i in range(n):
        val = arr[i]
        pre_mp = copy.deepcopy(mp)

        # default action/state
        action = "none"
        status = "checking"
        message = f"Checking index {i}, value = {val}."

        # emulate: if(mp[arr[i]] == -1) continue;
        # note: if key absent, mp[val] -> missing, treat missing as 0 (we will increment)
        if mp.get(val, 0) == -1:
            # ignored
            action = "ignored"
            status = "ignored"
            message = f"Ignoring index {i} (value {val}) — already finalized (mp[{val}] == -1)."
            # post_mp is same as pre_mp
            post_mp = copy.deepcopy(mp)
        else:
            # increment count
            prev_count = mp.get(val, 0)
            new_count = prev_count + 1
            mp[val] = new_count
            action = "incremented"
            status = "updated"
            message = f"Incremented count: value {val} -> {new_count}."

            # check threshold
            if mp[val] > threshold:
                # finalize this element (set to -1) and increment ans
                mp[val] = -1
                ans += 1
                action = "finalized"
                status = "found"
                message = (f"Frequency exceeded threshold (>{threshold}). "
                           f"Marking value {val} as finalized and incrementing ans -> {ans}.")

            post_mp = copy.deepcopy(mp)

        step = {
            "idx": i,
            "value": val,
            "pre_mp": pre_mp,
            "post_mp": post_mp,
            "action": action,
            "ans": ans,
            "threshold": threshold,
            "status": status,
            "message": message
        }
        steps.append(step)

    # Add final "after loop" step for summary
    final_msg = f"Finished. Total elements found (ans) = {ans}."
    steps.append({
        "idx": None,
        "value": None,
        "pre_mp": copy.deepcopy(mp),
        "post_mp": copy.deepcopy(mp),
        "action": "final",
        "ans": ans,
        "threshold": threshold,
        "status": "final",
        "message": final_msg
    })

    return steps

# -------------------------
# Drawing / Visualization
# -------------------------
class Visualizer:
    def __init__(self, arr, k):
        self.arr = arr
        self.k = k
        self.steps = build_steps(arr, k)
        self.step_index = 0

        # Setup figure
        self.fig = plt.figure(figsize=(12, 5), facecolor=BG_COLOR)
        # main axis where boxes and text live
        self.ax = self.fig.add_axes([0.03, 0.22, 0.94, 0.72], facecolor=BG_COLOR)
        self.ax.set_xlim(-0.5, max(len(arr) - 0.5, 1.5))
        self.ax.set_ylim(-1.5, 2.0)
        self.ax.axis("off")

        # Buttons axes
        axprev = self.fig.add_axes([0.25, 0.04, 0.15, 0.08])
        axnext = self.fig.add_axes([0.6, 0.04, 0.15, 0.08])
        axprev.set_facecolor("#222")
        axnext.set_facecolor("#222")
        self.btn_prev = Button(axprev, "⬅ Previous", color="#333", hovercolor="#444")
        self.btn_next = Button(axnext, "Next ➜", color="#333", hovercolor="#444")
        self.btn_prev.on_clicked(self.prev_step)
        self.btn_next.on_clicked(self.next_step)

        # Top and bottom text holders (these will be recreated each draw)
        self.top_text = None
        self.bottom_texts = []

        # Draw initial state
        self.draw_step()

    def draw_boxes(self, step):
        """Draw the array as boxes and apply highlights based on step state."""
        self.ax.clear()
        self.ax.set_xlim(-0.5, max(len(self.arr) - 0.5, 1.5))
        self.ax.set_ylim(-1.5, 2.0)
        self.ax.axis("off")
        # Top step message
        msg = step["message"]
        self.ax.text(0.02, 1.55, msg, transform=self.ax.transData, fontsize=12,
                     color=TEXT_COLOR, weight="bold", va="center")

        # draw boxes for each array element
        n = len(self.arr)
        for i, val in enumerate(self.arr):
            x = i - 0.45  # left
            y = 0.4
            rect = patches.FancyBboxPatch((x, y),
                                          BOX_WIDTH, BOX_HEIGHT,
                                          boxstyle="round,pad=0.02",
                                          linewidth=1.2,
                                          edgecolor=BOX_EDGE,
                                          facecolor=BOX_FACE,
                                          mutation_scale=4)
            self.ax.add_patch(rect)

            # default outline and text color
            edge_color = BOX_EDGE
            lw = 1.2
            zorder_val = 2

            # apply highlights:
            # - current pointer (cyan)
            if step["idx"] is not None and i == step["idx"]:
                edge_color = CURRENT_POINTER_COLOR
                lw = 2.8
                zorder_val = 5
            # - if this value was finalized previously (mp == -1 in pre or post)
            #   show green with glowing border if finalized at this step (post_mp shows -1 and action==finalized)
            post_mp = step["post_mp"]
            pre_mp = step["pre_mp"]
            val_status = None
            if pre_mp.get(val, 0) == -1:
                # already finalized earlier => red outline for ignored
                edge_color = IGNORED_RED
                lw = 2.2
                val_status = "already_finalized"
            if step["action"] == "finalized" and step["value"] == val and i == step["idx"]:
                # newly finalized at this step
                edge_color = FINAL_LIME_BORDER
                lw = 3.6
                # draw a thicker glow rectangle underneath to simulate glow
                glow = patches.FancyBboxPatch((x-0.03, y-0.03),
                                              BOX_WIDTH+0.06, BOX_HEIGHT+0.06,
                                              boxstyle="round,pad=0.02",
                                              linewidth=0.0,
                                              edgecolor=FINAL_LIME_BORDER,
                                              facecolor=FINAL_GREEN,
                                              alpha=0.18,
                                              mutation_scale=4,
                                              zorder=1)
                self.ax.add_patch(glow)
                val_status = "finalized_this_step"
            # - HashMap update event (increment) highlight -> yellow outline if action is incremented at this idx
            if step["action"] == "incremented" and step["idx"] == i:
                edge_color = UPDATE_YELLOW
                lw = 2.6
                val_status = "updated_this_step"
            # - ignored element at this step
            if step["action"] == "ignored" and step["idx"] == i:
                edge_color = IGNORED_RED
                lw = 2.6
                val_status = "ignored_this_step"

            # apply the computed edge color/lw by drawing a new rect overlay (so facecolor remains)
            outline = patches.FancyBboxPatch((x, y),
                                            BOX_WIDTH, BOX_HEIGHT,
                                            boxstyle="round,pad=0.02",
                                            linewidth=lw,
                                            edgecolor=edge_color,
                                            facecolor=BOX_FACE,
                                            mutation_scale=4,
                                            zorder=zorder_val)
            self.ax.add_patch(outline)

            # Element value text (centered)
            # scale font depending on text length
            font_size = 12
            text = str(val)
            if len(text) > 4:
                font_size = 9
            self.ax.text(x + BOX_WIDTH / 2, y + BOX_HEIGHT / 2,
                         text, fontsize=font_size, color=TEXT_COLOR,
                         ha="center", va="center", weight="bold", zorder=6)

            # index below each box
            self.ax.text(x + BOX_WIDTH / 2, y - 0.15,
                         str(i), fontsize=10, color="#cccccc",
                         ha="center", va="center", zorder=6)

            # small marker showing if this value is currently -1 in post_mp or pre_mp
            if post_mp.get(val, None) == -1:
                # finalized state indicator top-right of box
                self.ax.text(x + BOX_WIDTH - 0.05, y + BOX_HEIGHT - 0.05,
                             "✓", fontsize=10, color=FINAL_GREEN,
                             ha="right", va="top", weight="bold", zorder=7)

        # bottom info box: prefix/ans/hashmap show
        # Draw a dark rounded rectangle background for bottom info
        info_bg = patches.FancyBboxPatch((-0.5, -1.3),
                                         max(n + 0.5, 3.0), 0.9,
                                         boxstyle="round,pad=0.3",
                                         linewidth=0.5,
                                         edgecolor="#222",
                                         facecolor="#0d0d0d",
                                         mutation_scale=4,
                                         zorder=0)
        self.ax.add_patch(info_bg)

        # Display hashmap contents in a readable form
        mp_display = step["post_mp"]
        mp_items = [f"{k}:{v}" for k, v in sorted(mp_display.items(), key=lambda x: (str(x[0])))]
        mp_text = "  ".join(mp_items) if mp_items else "(empty)"
        threshold_text = f"Threshold (n/k) = {step['threshold']}"
        ans_text = f"ans = {step['ans']}"

        self.ax.text(0.02, -1.05, f"HashMap: {mp_text}", transform=self.ax.transData,
                     fontsize=10, color="#e6e6e6", va="center")
        self.ax.text(0.02, -1.25, f"{threshold_text}    |    {ans_text}",
                     transform=self.ax.transData, fontsize=10, color="#bfbfbf", va="center")

        # If found this step, show details prominently
        if step["action"] == "finalized":
            self.ax.text(2.6, -1.05, f"Found: value {step['value']} occurs > {step['threshold']} times.",
                         transform=self.ax.transData, fontsize=11, color=FINAL_GREEN, weight="bold", va="center")

        if step["action"] == "ignored":
            self.ax.text(2.6, -1.05, f"Ignored value {step['value']}: previously finalized.",
                         transform=self.ax.transData, fontsize=11, color=IGNORED_RED, weight="bold", va="center")

        # small legend on right
        # legend_x = max(n - 2.0, 2.5)
        # self.ax.text(legend_x, 2.45, "Legend:", color="#cccccc", fontsize=10, weight="bold")
        # self.ax.text(legend_x, 2.28, "Current pointer", color=CURRENT_POINTER_COLOR, fontsize=9)
        # self.ax.text(legend_x, 2.1, "Updated (incremented)", color=UPDATE_YELLOW, fontsize=9)
        # self.ax.text(legend_x, 1.94, "Finalized (>threshold)", color=FINAL_GREEN, fontsize=9)
        # self.ax.text(legend_x, 1.78, "Ignored (already -1)", color=IGNORED_RED, fontsize=9)

        # draw index progress (like steps / progress bar)
        # progress_text = f"Step {self.step_index+1} / {len(self.steps)}"
        # self.ax.text(legend_x, 0.58, progress_text, color="#aaaaaa", fontsize=10)

        # Refresh
        self.fig.canvas.draw_idle()

    def draw_step(self):
        """Draw visuals corresponding to current step index."""
        step = self.steps[self.step_index]
        # ensure the axis facecolor remains dark
        self.ax.set_facecolor(BG_COLOR)
        self.draw_boxes(step)

    def next_step(self, event):
        if self.step_index < len(self.steps) - 1:
            self.step_index += 1
            self.draw_step()

    def prev_step(self, event):
        if self.step_index > 0:
            self.step_index -= 1
            self.draw_step()

# -------------------------
# Runner
# -------------------------
def main():
    print("More-than-n/k Occurrences Visualizer")
    print("Editing EXAMPLE_ARRAY and K at top of script lets you test different inputs.")
    print("Close the figure window to end the program.\n")

    arr = EXAMPLE_ARRAY
    k = K
    # safeguard for k values
    if k <= 0:
        print("Warning: K should be > 0; using K=1 instead to avoid division by zero.")
        k = 1

    viz = Visualizer(arr, k)
    plt.show()

if __name__ == "__main__":
    main()
