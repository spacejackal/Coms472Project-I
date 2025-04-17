import math
import random
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

class PlannerAgent2:
	
	def __init__(self):
		pass
	
	def plan_action(self, world: np.ndarray, current: Tuple[int, int], pursued: Tuple[int, int], pursuer: Tuple[int, int]) -> Optional[np.ndarray]:
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
		
		directions = np.array([[0,0], [-1, 0], [1, 0], [0, -1], [0, 1],
                  	  		   [-1, -1], [-1, 1], [1, -1], [1, 1]]) 

		return directions[np.random.choice(9)]


class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state  # (current position, pursued position, pursuer position)
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0.0

    def is_fully_expanded(self):
        return len(self.children) == len(self.get_possible_moves())

    def get_possible_moves(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Up, Down, Left, Right
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal moves
        return directions

    def best_child(self, exploration_weight=1.0):
        return max(self.children, key=lambda child: child.value / (child.visits + 1e-6) +
                   exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6)))


class PlannerAgent:
    def __init__(self):
        pass

    def plan_action(self, world: np.ndarray, current: Tuple[int, int], pursued: Tuple[int, int], pursuer: Tuple[int, int]) -> Optional[np.ndarray]:
        
        root = MCTSNode((current, pursued, pursuer))
        for _ in range(100):  # Number of simulations
            node = self._select(root)
            reward = self._simulate(node, world)
            self._backpropagate(node, reward)

        best_move = root.best_child(exploration_weight=0).state[0]  # Best move based on simulations
        return np.array(best_move)

    def _select(self, node):
        while not node.is_fully_expanded():
            if len(node.children) < len(node.get_possible_moves()):
                return self._expand(node)
            node = node.best_child()
        return node

    def _expand(self, node):
        untried_moves = [move for move in node.get_possible_moves() if move not in [child.state[0] for child in node.children]]
        move = random.choice(untried_moves)
        new_state = self._apply_move(node.state, move)
        child_node = MCTSNode(new_state, parent=node)
        node.children.append(child_node)
        return child_node

    def _simulate(self, node, world):
        state = node.state
        for _ in range(10):  # Simulate up to 10 steps
            possible_moves = node.get_possible_moves()
            move = random.choice(possible_moves)
            state = self._apply_move(state, move)
            if np.array_equal(state[0],state[1]):  # Reached the pursued
                return 1.0  # Reward for catching the pursued
            if np.array_equal(state[0],state[2]):  # Caught by the pursuer
                return -1.0  # Penalty for being caught
        return 0.0  # Neutral outcome

    def _backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent

    def _apply_move(self, state, move):
        current, pursued, pursuer = state
        new_current = (current[0] + move[0], current[1] + move[1])
        new_current = (max(0, min(29, new_current[0])), max(0, min(29, new_current[1])))  # Stay within bounds
        return (new_current, pursued, pursuer)
