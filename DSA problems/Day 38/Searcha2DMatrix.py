import tkinter as tk
from tkinter import *
import time

# ------------------------------
# Search Logic converted to steps
# ------------------------------

def generate_steps(matrix, target):
    steps = []
    n = len(matrix)
    m = len(matrix[0])
    i, j = 0, m - 1

    while i < n and j >= 0:
        steps.append((i, j, f"Checking matrix[{i}][{j}] = {matrix[i][j]}"))
        if matrix[i][j] == target:
            steps.append((i, j, "Target Found!"))
            break
        elif matrix[i][j] > target:
            j -= 1
        else:
            i += 1

    return steps


# ------------------------------
# Tkinter UI
# ------------------------------

class MatrixVisualizer:
    def __init__(self, root, matrix, target):
        self.root = root
        self.matrix = matrix
        self.target = target
        self.steps = generate_steps(matrix, target)
        self.step_index = 0

        self.root.title("2D Matrix Search Visualization")
        self.root.configure(bg="black")

        self.cell_size = 70

        self.canvas = Canvas(root, width=len(matrix[0])*self.cell_size,
                             height=len(matrix)*self.cell_size, bg="black", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.info = Label(root, text="", fg="white", bg="black", font=("Consolas", 16))
        self.info.pack()

        self.btn_frame = Frame(root, bg="black")
        self.btn_frame.pack(pady=10)

        self.prev_btn = Button(self.btn_frame, text="⟵ Previous", command=self.prev_step,
                               width=12, height=2, bg="#222", fg="white", font=("Arial", 12))
        self.prev_btn.grid(row=0, column=0, padx=10)

        self.next_btn = Button(self.btn_frame, text="Next ⟶", command=self.next_step,
                               width=12, height=2, bg="#222", fg="white", font=("Arial", 12))
        self.next_btn.grid(row=0, column=1, padx=10)

        self.draw_matrix()
        self.highlight_step()

    # Draw static matrix grid
    def draw_matrix(self):
        self.cells = []
        for r in range(len(self.matrix)):
            row_cells = []
            for c in range(len(self.matrix[0])):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2, outline="white", width=2
                )
                text = self.canvas.create_text(
                    x1 + 35, y1 + 35, text=str(self.matrix[r][c]),
                    fill="white", font=("Consolas", 18, "bold")
                )
                row_cells.append((rect, text))
            self.cells.append(row_cells)

    # Highlight current step
    def highlight_step(self):
        # Reset all cells to white outline
        for r in range(len(self.matrix)):
            for c in range(len(self.matrix[0])):
                self.canvas.itemconfig(self.cells[r][c][0], outline="white", width=2)

        i, j, msg = self.steps[self.step_index]
        self.canvas.itemconfig(self.cells[i][j][0], outline="red", width=4)

        self.info.config(text=f"Step {self.step_index + 1}/{len(self.steps)}  |  i={i}, j={j}\n{msg}")

    def next_step(self):
        if self.step_index < len(self.steps) - 1:
            self.step_index += 1
            self.highlight_step()

    def prev_step(self):
        if self.step_index > 0:
            self.step_index -= 1
            self.highlight_step()

matrix = [
    [1, 4, 7, 11],
    [2, 5, 8, 12],
    [3, 6, 9, 16],
    [10, 13, 14, 17]
]

target = 10

root = tk.Tk()
app = MatrixVisualizer(root, matrix, target)
root.mainloop()
