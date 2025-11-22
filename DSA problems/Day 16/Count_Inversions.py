import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
from matplotlib.patches import FancyArrowPatch
import time

# Animation tuning (slow & visible)
FRAMES_PER_MOVE = 20
FRAME_DELAY = 0.03

# ----------------------------------------------------------
# Recorder: capture merge-sort steps + binary recursion tree
# ----------------------------------------------------------
class MergeRecorderClassroom:
    def __init__(self, arr):
        self.arr = arr[:]
        self.steps = []   # left,right,merged,sequence,inversions,total,hint,node
        self.nodes = []   # nodes: {l,r,left,right,parent,visited_at_step}
        self._record_all()

    def _record_all(self):
        self.total_inv = 0

        def make_node(l, r, parent):
            idx = len(self.nodes)
            self.nodes.append({'l': l, 'r': r, 'left': None, 'right': None, 'parent': parent, 'visited_at_step': None})
            if parent is not None:
                p = self.nodes[parent]
                if p['left'] is None:
                    p['left'] = idx
                else:
                    p['right'] = idx
            return idx

        def merge_sort(a, l, r, parent):
            node_idx = make_node(l, r, parent)
            if l == r:
                # single element step
                self.steps.append({
                    'left': [a[l]], 'right': [], 'merged': [a[l]],
                    'sequence': [('single', a[l])],
                    'inversions': 0, 'total': self.total_inv,
                    'hint': f"Single {a[l]} — already sorted",
                    'node': node_idx
                })
                self.nodes[node_idx]['visited_at_step'] = len(self.steps) - 1
                return [a[l]]
            mid = (l + r) // 2
            L = merge_sort(a, l, mid, node_idx)
            R = merge_sort(a, mid + 1, r, node_idx)
            merged, inv, seq, hint = self._merge_with_seq(L, R)
            self.total_inv += inv
            self.steps.append({
                'left': L, 'right': R, 'merged': merged,
                'sequence': seq, 'inversions': inv, 'total': self.total_inv,
                'hint': hint, 'node': node_idx
            })
            self.nodes[node_idx]['visited_at_step'] = len(self.steps) - 1
            return merged

        merge_sort(self.arr, 0, len(self.arr) - 1, None)

    def _merge_with_seq(self, L, R):
        i = j = 0
        merged = []
        seq = []
        inv = 0
        # sequence entries:
        # ('compare', left_val, right_val)
        # ('inversion', left_val, right_val, count)
        # ('take-left', val)
        # ('take-right', val)
        # ('single', val)
        while i < len(L) and j < len(R):
            seq.append(('compare', L[i], R[j]))
            if L[i] <= R[j]:
                merged.append(L[i])
                seq.append(('take-left', L[i]))
                i += 1
            else:
                merged.append(R[j])
                cnt = len(L) - i
                inv += cnt
                seq.append(('inversion', L[i], R[j], cnt))
                seq.append(('take-right', R[j]))
                j += 1
        while i < len(L):
            seq.append(('take-left', L[i])); merged.append(L[i]); i += 1
        while j < len(R):
            seq.append(('take-right', R[j])); merged.append(R[j]); j += 1
        hint = f"Added {inv} inversion(s) in this merge" if inv else "No inversions in this merge"
        return merged, inv, seq, hint

# ----------------------------------------------------------
# Tree node helper and layout (balanced inorder placement)
# ----------------------------------------------------------
def compute_subtree_sizes(nodes):
    # nodes is list of dicts with .left and .right indices (or None)
    def size(idx):
        if idx is None:
            return 0
        left = nodes[idx]['left']
        right = nodes[idx]['right']
        ls = size(left) if left is not None else 0
        rs = size(right) if right is not None else 0
        nodes[idx]['subsize'] = ls + rs + 1
        return nodes[idx]['subsize']
    if nodes:
        size(0)

def compute_inorder_positions(nodes):
    # returns dictionaries node_x, node_y mapping node index -> coordinates in [0..1]
    node_x = {}
    node_y = {}
    if not nodes:
        return node_x, node_y
    total = len(nodes)
    counter = {'v': 0}

    def inorder(idx, depth):
        if idx is None:
            return
        inorder(nodes[idx]['left'], depth + 1)
        t = total - 1 if total > 1 else 1
        if total > 1:
            x = 0.06 + 0.88 * (counter['v'] / t)
        else:
            x = 0.5
        y = 0.88 - depth * 0.10
        node_x[idx] = x
        node_y[idx] = y
        counter['v'] += 1
        inorder(nodes[idx]['right'], depth + 1)

    inorder(0, 0)
    return node_x, node_y

# ----------------------------------------------------------
# Classroom visualizer with tree boxes + indices and animation
# ----------------------------------------------------------
class ClassroomVisualizerTree:
    def __init__(self, arr):
        self.arr = arr[:]
        self.rec = MergeRecorderClassroom(self.arr)
        self.steps = self.rec.steps
        self.nodes = self.rec.nodes
        self.step_index = 0
        self.total_steps = len(self.steps)

        # compute tree layout
        compute_subtree_sizes(self.nodes)
        self.node_x, self.node_y = compute_inorder_positions(self.nodes)

        # figure
        self.fig = plt.figure(figsize=(12, 7))
        self.ax = self.fig.add_axes([0.02, 0.06, 0.96, 0.92])
        self.ax.set_facecolor('#0d0d0f')  # dark background
        self.ax.set_xticks([]); self.ax.set_yticks([])

        # buttons
        ax_prev = self.fig.add_axes([0.28, 0.01, 0.18, 0.055])
        ax_next = self.fig.add_axes([0.54, 0.01, 0.18, 0.055])
        self.btn_prev = Button(ax_prev, "Previous")
        self.btn_next = Button(ax_next, "Next")
        self.btn_prev.on_clicked(self.on_prev)
        self.btn_next.on_clicked(self.on_next)

        # cached faint lines (for static draw)
        self._prepare_faint_lines()

        # draw initial snapshot
        self.draw_static_step(self.step_index)
        plt.show()

    def _prepare_faint_lines(self):
        # store parent-child pairs to draw lines easily
        self.lines_pc = []
        for idx, nd in enumerate(self.nodes):
            p = nd['parent']
            if p is not None:
                self.lines_pc.append((p, idx))

    # draw one node box (values inside, index range below). highlight if active
    def _draw_node_box(self, ax, idx, highlight=False, visited=False):
        x = self.node_x[idx]; y = self.node_y[idx]
        node = self.nodes[idx]
        box_w = 0.16  # width in axis fraction
        box_h = 0.07
        # colors
        if highlight:
            fc = '#ffd54f'   # bright
            ec = '#ffd54f'
            txtc = '#000000'
            lw = 2.4
        elif visited:
            fc = '#1a2330'
            ec = '#7fbfff'
            txtc = '#e6f7ff'
            lw = 1.2
        else:
            fc = '#141417'
            ec = '#3a3a44'
            txtc = '#777777'
            lw = 1.0

        rect = patches.FancyBboxPatch((x - box_w/2, y - box_h/2), box_w, box_h,
                                      boxstyle="round,pad=0.02", ec=ec, fc=fc, linewidth=lw)
        ax.add_patch(rect)

        # values inside (space separated)
        vals = node['l']  # left index
        # build values by reading from original array slice
        try:
            # we stored ranges, but node only has l and r indices: compute values from original arr
            values_list = self.arr[node['l']: node['r'] + 1]
        except Exception:
            values_list = []

        values_text = "  ".join(str(v) for v in values_list)
        ax.text(x, y, values_text, ha='center', va='center', color=txtc, fontsize=10, weight='bold' if highlight else 'normal')

        # index range below the box
        range_text = f"{node['l']} – {node['r']}"
        ax.text(x, y - box_h/2 - 0.035, range_text, ha='center', va='center', color='white' if highlight else '#bfc7d6', fontsize=9)

    # draw entire tree boxes + connecting lines, with highlights according to current step
    def _draw_tree(self, current_step_idx, ax):
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        # draw lines first: faint baseline lines
        for (p, c) in self.lines_pc:
            x1, y1 = self.node_x[p], self.node_y[p]
            x2, y2 = self.node_x[c], self.node_y[c]
            ax.plot([x1, x2], [y1 - 0.035, y2 + 0.035], color='#2b2b2b', linewidth=1.0, alpha=0.45)

        # now highlight visited links and active subtree
        active_node = self.steps[current_step_idx]['node']
        # set visited flags
        for idx, nd in enumerate(self.nodes):
            visited_at = nd.get('visited_at_step')
            visited = visited_at is not None and visited_at <= current_step_idx
            is_active = (idx == active_node)
            if is_active:
                # draw parent-child edges brighter for active node
                # parent line
                parent = nd['parent']
                if parent is not None:
                    x1, y1 = self.node_x[parent], self.node_y[parent]
                    x2, y2 = self.node_x[idx], self.node_y[idx]
                    ax.plot([x1, x2], [y1 - 0.035, y2 + 0.035], color='#ffd54f', linewidth=2.0, alpha=0.95)
                # children lines
                left = nd['left']; right = nd['right']
                for ch in (left, right):
                    if ch is not None:
                        x1, y1 = self.node_x[idx], self.node_y[idx]
                        x2, y2 = self.node_x[ch], self.node_y[ch]
                        ax.plot([x1, x2], [y1 - 0.035, y2 + 0.035], color='#ffd54f', linewidth=2.0, alpha=0.95)
        # finally draw nodes boxes: visited ones bright, active highlighted
        for idx, nd in enumerate(self.nodes):
            visited_at = nd.get('visited_at_step')
            visited = visited_at is not None and visited_at <= current_step_idx
            is_active = (idx == active_node)
            self._draw_node_box(ax, idx, highlight=is_active, visited=visited)

    # draw left/right/merged blocks static (no animation)
    def _draw_blocks_static(self, step, ax):
        left_x, left_w = 0.06, 0.24
        merged_x, merged_w = 0.36, 0.28
        right_x, right_w = 0.70, 0.24
        base_y = 0.26

        L = step['left']; R = step['right']; M = step['merged']

        # left block (big boxes for classroom)
        if L:
            w = left_w / max(1, len(L))
            for i, v in enumerate(L):
                x = left_x + i * w + w / 2
                rect = patches.Rectangle((x - 0.045, base_y + 0.06), 0.09, 0.09, ec='white', fc='#2D82F0', linewidth=1.2)
                ax.add_patch(rect)
                ax.text(x, base_y + 0.11, str(v), ha='center', va='center', color='white', fontsize=14, weight='bold')

        # right block
        if R:
            w2 = right_w / max(1, len(R))
            for i, v in enumerate(R):
                x = right_x + i * w2 + w2 / 2
                rect = patches.Rectangle((x - 0.045, base_y + 0.06), 0.09, 0.09, ec='white', fc='#F08B3A', linewidth=1.2)
                ax.add_patch(rect)
                ax.text(x, base_y + 0.11, str(v), ha='center', va='center', color='white', fontsize=14, weight='bold')

        # merged block
        if M:
            w3 = merged_w / max(1, len(M))
            for i, v in enumerate(M):
                x = merged_x + i * w3 + w3 / 2
                rect = patches.Rectangle((x - 0.045, base_y - 0.03), 0.09, 0.09, ec='white', fc='#4CAF50', linewidth=1.2)
                ax.add_patch(rect)
                ax.text(x, base_y + 0.01, str(v), ha='center', va='center', color='white', fontsize=14, weight='bold')

    # static draw for a given step - used for initial display and Previous
    def draw_static_step(self, idx):
        ax = self.ax
        ax.clear()
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xticks([]); ax.set_yticks([])

        # draw tree with highlights
        self._draw_tree(idx, ax)

        # draw blocks
        step = self.steps[idx]
        self._draw_blocks_static(step, ax)

        # minimal hint text
        ax.text(0.5, 0.57, f"Hint: {step['hint']}", ha='center', va='center', color='white', fontsize=14)
        ax.set_title(f"Step {idx+1}/{self.total_steps}  —  Inversions this step: {step['inversions']}  Total: {step['total']}", color='white', fontsize=12)
        plt.pause(0.01)

    # semi-slide movement helper
    def _semi_slide(self, rect, txt, start, target, frames=FRAMES_PER_MOVE):
        sx, sy = start; tx, ty = target
        dx = (tx - sx) / frames; dy = (ty - sy) / frames
        for _ in range(frames):
            sx += dx; sy += dy
            rect.set_xy((sx - 0.045, sy))
            txt.set_position((sx, sy + 0.045))
            plt.pause(FRAME_DELAY)

    # small arrow pulse (visual comparison)
    def _arrow_pulse(self, ax, p1, p2, repeats=1):
        arrow = FancyArrowPatch((p1[0], p1[1] + 0.08), (p2[0], p2[1] + 0.08), arrowstyle='-|>', mutation_scale=20, color='yellow', alpha=0.0)
        ax.add_patch(arrow)
        for _ in range(repeats):
            for f in range(4):
                arrow.set_alpha((f + 1) / 4)
                plt.pause(FRAME_DELAY)
            time.sleep(FRAME_DELAY * 4)
            for f in range(4):
                arrow.set_alpha(1 - (f + 1) / 4)
                plt.pause(FRAME_DELAY)
        arrow.remove()

    # animate a step semi-smoothly (Next -> animation)
    def animate_step(self, idx):
        step = self.steps[idx]
        ax = self.ax
        ax.clear()
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xticks([]); ax.set_yticks([])

        # draw tree boxes with active highlighted
        self._draw_tree(idx, ax)

        # prepare left / right rectangles and merged placeholders
        left_x, left_w = 0.06, 0.24
        merged_x, merged_w = 0.36, 0.28
        right_x, right_w = 0.70, 0.24
        base_y = 0.26

        L = step['left'][:]; R = step['right'][:]; M = step['merged'][:]

        left_objs = []
        if L:
            w = left_w / max(1, len(L))
            for i, v in enumerate(L):
                x = left_x + i * w + w / 2
                rect = patches.Rectangle((x - 0.045, base_y + 0.06), 0.09, 0.09, ec='white', fc='#2D82F0', linewidth=1.2)
                txt = ax.text(x, base_y + 0.11, str(v), ha='center', va='center', color='white', fontsize=14, weight='bold')
                ax.add_patch(rect)
                left_objs.append({'rect': rect, 'txt': txt, 'x': x, 'y': base_y + 0.06, 'val': v})

        right_objs = []
        if R:
            w2 = right_w / max(1, len(R))
            for i, v in enumerate(R):
                x = right_x + i * w2 + w2 / 2
                rect = patches.Rectangle((x - 0.045, base_y + 0.06), 0.09, 0.09, ec='white', fc='#F08B3A', linewidth=1.2)
                txt = ax.text(x, base_y + 0.11, str(v), ha='center', va='center', color='white', fontsize=14, weight='bold')
                ax.add_patch(rect)
                right_objs.append({'rect': rect, 'txt': txt, 'x': x, 'y': base_y + 0.06, 'val': v})

        merged_slots = []
        if M:
            w3 = merged_w / max(1, len(M))
            for i in range(len(M)):
                x = merged_x + i * w3 + w3 / 2
                rect = patches.Rectangle((x - 0.045, base_y - 0.03), 0.09, 0.09, ec='white', fc='#222222', linewidth=1.2)
                txt = ax.text(x, base_y + 0.01, '', ha='center', va='center', color='white', fontsize=14, weight='bold')
                ax.add_patch(rect)
                merged_slots.append({'rect': rect, 'txt': txt, 'x': x, 'y': base_y - 0.03, 'val': None})

        plt.pause(0.01)

        # helpers to pop specific left/right items
        def pop_left(val):
            for i, it in enumerate(left_objs):
                if it['val'] == val:
                    return left_objs.pop(i)
            return left_objs.pop(0) if left_objs else None

        def pop_right(val):
            for i, it in enumerate(right_objs):
                if it['val'] == val:
                    return right_objs.pop(i)
            return right_objs.pop(0) if right_objs else None

        merged_idx = 0

        # execute sequence
        for action in step['sequence']:
            typ = action[0]
            if typ == 'compare':
                a, b = action[1], action[2]
                la = next((it for it in left_objs if it['val'] == a), None)
                rb = next((it for it in right_objs if it['val'] == b), None)
                if la and rb:
                    self._arrow_pulse(ax, (la['x'], la['y']), (rb['x'], rb['y']), repeats=1)
                    time.sleep(FRAME_DELAY * 3)
                else:
                    time.sleep(FRAME_DELAY * 4)
            elif typ == 'inversion':
                a, b, cnt = action[1], action[2], action[3]
                la = next((it for it in left_objs if it['val'] == a), None)
                rb = next((it for it in right_objs if it['val'] == b), None)
                if la: la['rect'].set_facecolor('#ff6b6b')
                if rb: rb['rect'].set_facecolor('#ff6b6b')
                plt.pause(FRAME_DELAY * 8)
                if la: la['rect'].set_facecolor('#2D82F0')
                if rb: rb['rect'].set_facecolor('#F08B3A')
                time.sleep(FRAME_DELAY * 2)
            elif typ == 'take-left':
                v = action[1]
                obj = pop_left(v)
                if obj:
                    tx, ty = merged_slots[merged_idx]['x'], merged_slots[merged_idx]['y']
                    # arrow + slide
                    self._arrow_pulse(ax, (obj['x'], obj['y']), (tx, ty), repeats=1)
                    self._semi_slide(obj['rect'], obj['txt'], (obj['x'], obj['y']), (tx, ty))
                    merged_slots[merged_idx]['txt'].set_text(str(obj['val']))
                    merged_slots[merged_idx]['rect'].set_facecolor('#4CAF50')
                    merged_slots[merged_idx]['val'] = obj['val']
                    merged_idx += 1
                    time.sleep(FRAME_DELAY * 2)
            elif typ == 'take-right':
                v = action[1]
                obj = pop_right(v)
                if obj:
                    tx, ty = merged_slots[merged_idx]['x'], merged_slots[merged_idx]['y']
                    self._arrow_pulse(ax, (obj['x'], obj['y']), (tx, ty), repeats=1)
                    self._semi_slide(obj['rect'], obj['txt'], (obj['x'], obj['y']), (tx, ty))
                    merged_slots[merged_idx]['txt'].set_text(str(obj['val']))
                    merged_slots[merged_idx]['rect'].set_facecolor('#E04C4C')  # red for inverted move visuals
                    merged_slots[merged_idx]['val'] = obj['val']
                    merged_idx += 1
                    time.sleep(FRAME_DELAY * 2)
            elif typ == 'single':
                v = action[1]
                # find in left or right
                obj = next((it for it in left_objs if it['val'] == v), None)
                if obj is None:
                    obj = next((it for it in right_objs if it['val'] == v), None)
                if obj:
                    tx, ty = merged_slots[merged_idx]['x'], merged_slots[merged_idx]['y']
                    self._arrow_pulse(ax, (obj['x'], obj['y']), (tx, ty), repeats=1)
                    self._semi_slide(obj['rect'], obj['txt'], (obj['x'], obj['y']), (tx, ty))
                    merged_slots[merged_idx]['txt'].set_text(str(obj['val']))
                    merged_slots[merged_idx]['rect'].set_facecolor('#4CAF50')
                    merged_slots[merged_idx]['val'] = obj['val']
                    if obj in left_objs: left_objs.remove(obj)
                    if obj in right_objs: right_objs.remove(obj)
                    merged_idx += 1
                    time.sleep(FRAME_DELAY * 2)

            plt.pause(0.001)

        # final small pause and restore colors
        time.sleep(0.6)
        for ms in merged_slots:
            ms['rect'].set_facecolor('#2D82F0')  # final nice blue
        plt.pause(0.02)

    # button callbacks
    def on_next(self, event):
        if self.step_index < self.total_steps - 1:
            self.step_index += 1
            self.animate_step(self.step_index)

    def on_prev(self, event):
        if self.step_index > 0:
            self.step_index -= 1
            self.draw_static_step(self.step_index)

# ----------------------------------------------------------
# Run the visualizer (change arr below to try other examples)
# ----------------------------------------------------------
if __name__ == "__main__":
    # Example classroom arrays (choose one)
    # arr = [2, 4, 1, 3, 5]
    # arr = [3, 1, 4, 2]
    arr = [5, 3, 2, 4, 1]   # default example, change as needed

    vis = ClassroomVisualizerTree(arr)
