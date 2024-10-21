# import numpy as np
from math import gcd
from graph import *

def is_valid(matrix: MatrixGraph, i, j, num):
    """
    Returns a boolean value indicating whether a number is coprime with values of
    every filled node adjacent to the given grid coordinate
    """
    neighbors_value_raw = (neighbor.get_value() for neighbor in matrix.get_node_by_coord([i, j]).get_neighbors())
    neighbors_value = (value for value in neighbors_value_raw if value is not None)
    return all(gcd(num, neighbor_value) == 1 for neighbor_value in neighbors_value)


def generate_prime_grid(n, m) -> list[list[int]]:
    """
    Backtracking approach that uses most_factors_first to try to place factor-heavy numbers
    in the beginning to prevent impossible states later.
    """
    print(f"Generating {n}x{m} grid ({n*m} values)")

    # grid = np.zeros((n, m), dtype=int)
    grid = MatrixGraph(n, m)

    sorted_numbers = most_factors_first(n * m)
    stack = []
    index = 0

    while index < n * m:
        row, col = divmod(index, m)
        placed = False
        tried_numbers = set()

        for num in sorted_numbers:
            if num not in tried_numbers and is_valid(grid, row, col, num):
                # grid[row, col] = num
                grid.get_node_by_coord([row, col]).set_value(num)
                stack.append((index, num))
                sorted_numbers.remove(num)
                placed = True
                break
            tried_numbers.add(num)

        if placed:
            index += 1
        else:
            if not stack:
                return None
            # Backtrack startin from here
            while stack:
                prev_index, prev_num = stack.pop()
                row, col = divmod(prev_index, m)
                # grid[row, col] = 0
                grid.get_node_by_coord([row, col]).set_value(0)
                sorted_numbers.append(prev_num)
                tried_numbers.add(prev_num)
                index = prev_index
                if len(tried_numbers) < len(sorted_numbers):
                    break
            else:
                return None
    # If the placement of all numbers is valid, return the grid
    return grid if index == n * m else None
