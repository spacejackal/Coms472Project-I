import numpy as np
from typing import List, Tuple, Optional

class MimiNode:
    current = None
    pursued = None
    pursuer = None
    mover = -1
    depth = 0
    parent = None
    children = []
    value = 0
    def __init__(self, current=None, pursued=None, pursuer=None, depth=0, parent=None, mover=-1):
        self.current = current
        self.pursued = pursued
        self.pursuer = pursuer
        self.depth = depth
        self.parent = parent
        self.children = []
        self.value = 0
        self.mover = mover

def best_action(root: MimiNode):
        """
        Returns the best action from the root node of the minimini tree.
        """
        if not root.children:
            return None
        bestMove = None
        bestValue = float('inf')
        for child in root.children:
            if child.value < bestValue and child.current - root.current != (0,0):
                bestValue = child.value
                bestMove = child.current - root.current

        #best_child = min(root.children, key=lambda x: x.value)
        return bestMove

def miniminimini(world, current, pursued, pursuer, maxdepth):
    root = MimiNode(current, pursued, pursuer)
    rows, cols = len(world), len(world[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1), (0,0)]
    depth = 0
    node = root
    while depth <= maxdepth:

        our_action = None
        for dir in directions:
            newNode = MimiNode(node.current + dir, node.pursued, node.pursuer, depth, node)
            #distToEnd = (abs(newNode[0] - end[0]), abs(newNode[1] - end[1]))
            if 0 <= newNode.current[0] < rows and 0 <= newNode.current[1] < cols and world[newNode.current[0]][newNode.current[1]] == 0:
                newNode.value = hurst(newNode.current, newNode.pursued, newNode.pursuer)
                #if(our_action is None or newNode.value < our_action.value):
                our_action = newNode
            if(our_action is not None):
                node.children.append(our_action)

        pursued_action = None
        for ourAction in node.children:
            for dir in directions:
                newNode = MimiNode(ourAction.current, ourAction.pursued+dir, ourAction.pursuer, depth, ourAction)
                if 0 <= newNode.current[0] < rows and 0 <= newNode.current[1] < cols and world[newNode.current[0]][newNode.current[1]] == 0:
                    newNode.value = hurst(newNode.pursued, newNode.pursuer, newNode.current)
                    #if(pursued_action is None or newNode.value < pursued_action.value):
                    pursued_action = newNode
                if(pursued_action is not None):
                    ourAction.children.append(pursued_action)

        pursuer_action = None
        for pursuedAction in our_action.children:
            for dir in directions:
                newNode = MimiNode(pursuedAction.current, pursuedAction.pursued, pursuedAction.pursuer+dir, depth, pursuedAction)
                if 0 <= newNode.current[0] < rows and 0 <= newNode.current[1] < cols and world[newNode.current[0]][newNode.current[1]] == 0:
                    newNode.value = hurst(newNode.pursuer, newNode.current, newNode.pursued)
                    if(tuple(newNode.current) == tuple(newNode.pursuer)):
                        newNode.value = 9999999999999999
                        tempNode = newNode
                        while tempNode.parent is not None:
                            tempNode.value = 9999999999999999
                            tempNode = tempNode.parent
                        
                    #if(pursuer_action is None or newNode.value < pursuer_action.value):
                    pursuer_action = newNode
                if(pursuer_action is not None):
                    pursuedAction.children.append(pursuer_action)
        depth += 1
        node = pursuer_action

    #backValue(root)

    return root

            
def backValue(node: MimiNode):
    if node is None:
        return 0
    




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
            distToEnd = (hurst(newNode, end,avoid))
            if 0 <= newNode[0] < rows and 0 <= newNode[1] < cols and grid[newNode[0]][newNode[1]] == 0 and newNode not in list(pathWeight.keys()):
                    #pathWeight[newNode] = 1 + pathWeight[node] + distToEnd[0] + distToEnd[1]
                    pathWeight[newNode] = 1 + pathWeight[node] + distToEnd
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

        if dist(current, target) > 3:
            temp = tuple(current)
            temp2 = tuple(pursued)
            temp3 = tuple(pursuer)
            pursued_plan = AnotherAnotherStar(world, temp2, temp3, temp)

            for i in range(len(pursued_plan)):
                if dist(pursued_plan[i], current)<dist(target, current):
                    target = pursued_plan[i]
                if pursued_plan[i] == temp:
                    target = pursued_plan[0]
                    break


            our_plan = AnotherAnotherStar(world, temp, temp2, temp3)

            act = our_plan[1] - current



            return act
        else:
            minimini = miniminimini(world, current, pursued, pursuer, 3)
            #act = minimini.children[0].current - current
            act = best_action(minimini)
            return act
    
def dist(current, end):
    temp = abs((current[0] - end[0])^2) + abs((current[1] - end[1])^2) **0.5
    return (temp)
    


