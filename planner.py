import numpy as np
from typing import List, Tuple, Optional
import matplotlib.pyplot as plt
import scipy

def AStar(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    explored = []
    frontier = [start]
    visited = set()
    parent = {start: None}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    weight = 1
    minWeight = float("inf")
    nextNode = None
    while True:
        for node in frontier:
            minWeight = float("inf")
            nextNode = None
            bourder = False
            for dir in directions:
                x, y = node[0] + dir[0], node[1] + dir[1]
                if 0 <= x < rows and 0 <= y < cols and grid[x][y] == 0 and (x, y) not in visited and (x,y) not in explored and (x,y) not in frontier:
                    weight = 1 + abs((x - end[0])) + abs((y - end[1])) + parent[(x,y)].weight
                    bourder = True
                    if weight < minWeight:
                        minWeight = weight
                        nextNode = (x,y)
            if bourder == False:
                explored.append(node)
                frontier.remove(node)
        frontier.append(nextNode)
        parent[nextNode] = node
        if nextNode == end:
            path = []
            while nextNode is not None:
                path.append(nextNode)
                if parent[nextNode] is None:
                    break
                nextNode = parent[nextNode]
            return path[::-1]



        




    

def dfs(grid, start, end):
    """A DFS example"""
    rows, cols = len(grid), len(grid[0])
    stack = [start]
    visited = set()
    parent = {start: None}

    # Consider all 8 possible moves (up, down, left, right, and diagonals)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Up, Down, Left, Right
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal moves

    while stack:
        x, y = stack.pop()
        if (x, y) == end:
            # Reconstruct the path
            path = []
            while (x, y) is not None:
                path.append((x, y))
                if parent[(x, y)] is None:
                    break  # Stop at the start node
                x, y = parent[(x, y)]
            return path[::-1]  # Return reversed path

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0 and (nx, ny) not in visited:
                stack.append((nx, ny))
                parent[(nx, ny)] = (x, y)

    return None  # Return None if no path is found

def plan_path(world: np.ndarray, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[np.ndarray]:
    """
    Computes a path from the start position to the end position 
    using a certain planning algorithm (DFS is provided as an example).

    Parameters:
    - world (np.ndarray): A 2D numpy array representing the grid environment.
      - 0 represents a walkable cell.
      - 1 represents an obstacle.
    - start (Tuple[int, int]): The (row, column) coordinates of the starting position.
    - end (Tuple[int, int]): The (row, column) coordinates of the goal position.

    Returns:
    - np.ndarray: A 2D numpy array where each row is a (row, column) coordinate of the path.
      The path starts at 'start' and ends at 'end'. If no path is found, returns None.
    """
    # Ensure start and end positions are tuples of integers
    start = (int(start[0]), int(start[1]))
    end = (int(end[0]), int(end[1]))

    # Convert the numpy array to a list of lists for compatibility with the example DFS function
    world_list: List[List[int]] = world.tolist()

    # Perform DFS pathfinding and return the result as a numpy array
    #path = dfs(world_list, start, end)
    path = AStar(world_list, start, end)

    return np.array(path) if path else None

def hurst(current, end):
    temp = abs((current[0] - end[0])) + abs((current[1] - end[1]))
    return temp