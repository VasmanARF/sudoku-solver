import numpy as np
import sudoku_solver as solver

# Load array of hard sudokus
sudoku = np.load("hard_sudokus.npy")

for i in range(len(sudoku)):
    print(f"Solution to sudoku {i + 1} is:\n{solver.sudoku_solver(sudoku[i])}")
