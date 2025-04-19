import numpy as np
from typing import List, Tuple, Optional

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

    return None


def AnotherAnotherStar(grid, start, end, avoid):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1), (0,0)]
    pathWeight = {start: 0}
    parent = {start: None}

    open = [start]

    found = False
    while not found and len(open) > 0:
        node = None
        for newNode in open:
            if node is None or pathWeight[newNode] <= pathWeight[node]:
                node = newNode
        
        open.remove(node)

        for dir in directions:
            newNode = (node[0] + dir[0], node[1] + dir[1])
            #distToEnd = (abs(newNode[0] - end[0]), abs(newNode[1] - end[1]))
            ##distToEnd = (hurst(newNode, end,avoid))
            if 0 <= newNode[0] < rows and 0 <= newNode[1] < cols and grid[newNode[0]][newNode[1]] == 0 and newNode not in list(pathWeight.keys()):
                    #pathWeight[newNode] = 1 + pathWeight[node] + distToEnd[0] + distToEnd[1]
                    #pathWeight[newNode] = 1 + pathWeight[node] + distToEnd
                    pathWeight[newNode] = hurst(newNode, end,avoid) + pathWeight[node] + dist(start, end)
                    parent[newNode] = node
                    open.append(newNode)
                    if newNode == end:
                        found = True
                        break

    if found:
            path = []
            parentNode = end
            while parentNode is not None:
                path.append(parentNode)
                if parent[parentNode] is None:
                    break
                parentNode = parent[parentNode]
            return path[::-1]
    return None

def hurst(current, end, pursuer):
    temp = abs((current[0] - end[0])^2) + abs((current[1] - end[1])^2) **0.5
    temp2 = abs((current[0] - pursuer[0])^2) + abs((current[1] - pursuer[1])^2) **0.5

    if temp2 == 0:
        return 9999999999999999

    return ((1/temp2) *temp)


class PlannerAgent:
    
    def __init__(self):
        pass
    
    def plan_action(self, world: np.ndarray, current: np.ndarray, pursued: np.ndarray, pursuer: np.ndarray) -> Optional[np.ndarray]:
        """
        Computes a action to take from the current position caputure the pursued while evading from the pursuer

        Parameters:
        - world (np.ndarray): A 2D numpy array representing the grid environment.
        - 0 represents a walkable cell.
        - 1 represents an obstacle.
        - current (np.ndarray): The (row, column) coordinates of the current position.
        - pursued (np.ndarray): The (row, column) coordinates of the agent to be pursued.
        - pursuer (np.ndarray): The (row, column) coordinates of the agent to evade from.

        Returns:
        - np.ndarray: one of the 9 actions from 
                              [0,0], [-1, 0], [1, 0], [0, -1], [0, 1],
                                [-1, -1], [-1, 1], [1, -1], [1, 1]
        """
        
        directions = np.array([[0,0], [-1, 0], [1, 0], [0, -1], [0, 1],
                                   [-1, -1], [-1, 1], [1, -1], [1, 1]]) 
          
        target = pursued
        pursued_plan = AnotherAnotherStar(world, tuple(pursued), tuple(pursuer), tuple(current))
        
        for i in range(len(pursued_plan)):
            if i == 0:
              continue  
            elif pursued_plan[i] == tuple(current):
                target = pursued_plan[1]
                break
            elif dist(pursued_plan[i], current)<dist(target, current):
                target = pursued_plan[i]
            

        our_plan = AnotherAnotherStar(world, tuple(current), tuple(target), tuple(pursuer))

        act = our_plan[1] - current


        
        return act
    
def dist(current, end):
    temp = abs((current[0] - end[0])^2) + abs((current[1] - end[1])^2) **0.5
    return (temp)
    


