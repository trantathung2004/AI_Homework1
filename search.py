from copy import deepcopy 
from node import Node
"""Implement search algorithm
"""
from queue import PriorityQueue
import heapq
import time

def BFS(root: Node):
    """Runs the BFS algorithm given the root node. The class of the root node
    defines the problem that's being solved. The algorithm either returns the solution
    as a path from the start node to the goal node or returns None if there's no solution.

    Parameters
    ----------
    root: Node
        The start node of the problem to be solved.

    Returns
    -------
        path: list of Nodes or None
            The solution, a path from the initial node to the goal node.
            If there is no solution it should return None
    """
    # TODO: add your code here
    # Some helper pseudo-code:
    # 1. Create an empty fringe and add your root node (you can use lists, sets, heaps, ... )
    # 2. While the container is not empty:
    # 3.      Pop the first node
    # 4.      If that's a goal node, return node.get_path()
    # 5.      Otherwise, add the children of the node to the end of the fringe
    # 6. Return None
    fringe = [root]
    visited = set()
    while fringe:
        node = fringe.pop(0)
        if node.is_goal():
            return node.get_path()
        for child in node.generate_children():
            if child not in visited:
                fringe.append(child)
                visited.add(child)
    return None
    raise NotImplementedError

def DFS(root: Node):
    """Runs the DFS algorithm given the root node. The class of the root node
    defines the problem that's being solved. The algorithm either returns the solution
    as a path from the start node to the goal node or returns None if there's no solution.

    Parameters
    ----------
    root: Node
        The start node of the problem to be solved.

    Returns
    -------
        path: list of Nodes or None
            The solution, a path from the initial node to the goal node.
            If there is no solution it should return None
    """
    # TODO: add your code here
    # Some helper pseudo-code:
    # 1. Create an empty fringe and add your root node (you can use lists, sets, heaps, ... )
    # 2. While the container is not empty:
    # 3.      Pop the first node
    # 4.      If that's a goal node, return node.get_path()
    # 5.      Otherwise, add the children of the node to the beginning of the fringe
    # 6. Return None
    fringe = [root]
    visited = set()
    while fringe:
        node = fringe.pop()
        if node.is_goal():
            return node.get_path()
        for child in node.generate_children():
            if child not in visited:
                fringe.append(child)
                visited.add(child)
    return None
    raise NotImplementedError

def Astar(root: Node):
    """Runs the A* algorithm given the root node. The class of the root node
    defines the problem that's being solved. The algorithm either returns the solution
    as a path from the start node to the goal node or returns None if there's no solution.

    Parameters
    ----------
    root: Node
        The start node of the problem to be solved.

    Returns
    -------
        path: list of Nodes or None
            The solution, a path from the initial node to the goal node.
            If there is no solution it should return None
    """

    # TODO: add your code here
    # Some helper pseudo-code:
    # 1. Create an empty fringe and add your root node (you can use lists, sets, heaps, ... )
    # 2. While the container is not empty:
    # 3.      Pop the best? node (Use the attribute `node.f` in comparison)
    # 4.      If that's a goal node, return node.get_path()
    # 5.      Otherwise, add the children of the node to the fringe
    # 6. Return None
    #
    # Some notes:
    # You can access the state of a node by `node.state`. (You may also want to store evaluated states)
    # You should consider the states evaluated and the ones in the fringe to avoid repeated calculation in 5. above.
    # You can compare two node states by node1.state == node2.state 

    # fringe = [(root.f, root)]
    # heapq.heapify(fringe)
    # visited = set()

    # while fringe:
    #     f, node = heapq.heappop(fringe)
    #     if node.is_goal():
    #         return node.get_path()
    #     for child in node.generate_children():
    #         if child not in visited or (child.f, child) in fringe:
    #             heapq.heappush(fringe, (child.f, child))
    #             visited.add(child)
    # return None

    fringe = PriorityQueue()
    visited = []

    fringe.put((root.f, root))
    while not fringe.empty():
        element = fringe.get()
        current = element[1]
        if current._get_state() not in visited:
            visited.append(current._get_state())
            if current.is_goal():
                return current.get_path()
            for child in current.generate_children():
                if child._get_state() not in visited:
                    fringe.put((child.f, child))
    return None
    raise NotImplementedError