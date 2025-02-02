import numpy as np
from collections import deque
import heapq
from typing import List, Tuple, Set, Dict


"""
Do not import any other package unless allowed by te TAs in charge of the lab.
Do not change the name of any of the functions below.
"""
def find_gap(state: np.ndarray) -> Tuple[int, int]:
    return tuple(np.argwhere(state == 0)[0])

def state_to_string(state):
    return ''.join(str(c) for c in state.ravel())

def string_to_state(state_str):
    return np.array([int(c) for c in state_str]).reshape(3, 3)


def get_neighbours(state: np.ndarray) -> List[Tuple[np.ndarray,str]]:
    moves = []
    x,y = find_gap(state)
    directions = {
        'U': (-1,0),
        'L': (0,-1),
        'R': (0,1),
        'D': (1,0)
    }

    for direction_str,direction in directions.items():
        dx,dy  = direction
        if x+dx >= 0 and x+dx < 3 and y+dy >=0 and y+dy < 3:
            new_state = state.copy()
            new_state[x][y] = state[x+dx][y+dy]
            new_state[x+dx][y+dy] = 0
            moves.append((new_state,direction_str)) 

    return moves


def bfs(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int]:
    """
    Implement Breadth-First Search algorithm to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array.
                            Example: np.array([[1, 2, 3], [4, 0, 5], [6, 7, 8]])
                            where 0 represents the blank space
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array.
                          Example: np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    
    Returns:
        Tuple[List[str], int]: A tuple containing:
            - List of moves to reach the goal state. Each move is represented as
              'U' (up), 'D' (down), 'L' (left), or 'R' (right), indicating how
              the blank space should move
            - Number of nodes expanded during the search

    Example return value:
        (['R', 'D', 'R'], 12) # Means blank moved right, down, right; 12 nodes were expanded
              
    """    
    # TODO: Implement this function
    initial_str = state_to_string(initial)
    goal_str = state_to_string(goal)

    open_list = []
    heapq.heappush(open_list,(0,initial_str,0,[]))
    closed_list = set()
    closed_list.add(initial_str)
    explored_nodes = 0

    while open_list:
        f_cost,current_str,current_cost,path = heapq.heappop(open_list)
        explored_nodes += 1
        current = string_to_state(current_str)

        if current_str == goal_str:
            return path,explored_nodes
        
        for neighbour,move in get_neighbours(current):
            neighbour_str = state_to_string(neighbour)
            g_cost = current_cost + 1
            h_cost = 0
            f_cost = g_cost+h_cost

            if neighbour_str not in closed_list:
                closed_list.add(neighbour_str)
                heapq.heappush(open_list, (f_cost, neighbour_str, g_cost, path + [move]))

    return [], 0



def dfs(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int]:
    closed_list = set()
    open_list = [(initial, [])] 
    n_nodes = 0

    while open_list:
        n_nodes += 1
        current, path = open_list.pop()
        current_str = state_to_string(current)

        if current_str in closed_list:
            continue

        closed_list.add(current_str)

        if np.array_equal(current, goal):
            return path, n_nodes

        for neighbour, move in get_neighbours(current):
            open_list.append((neighbour, path + [move]))

    return [], 0





# def dfs(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int]:
#     """
#     Implement Depth-First Search algorithm to solve 8-puzzle problem.
    
#     Args:
#         initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array
#         goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array
    
#     Returns:
#         Tuple[List[str], int]: A tuple containing:
#             - List of moves to reach the goal state
#             - Number of nodes expanded during the search
#     """
    
#     # TODO: Implement this function
#     initial_str = state_to_string(initial)
#     goal_str = state_to_string(goal)

#     pq = []
#     heapq.heappush(pq,(0,initial_str,0,[]))
#     distances = {initial_str: 0}
#     explored_nodes = 0

#     while pq:
#         f_cost,current_str,current_cost,path = heapq.heappop(pq)
#         explored_nodes += 1
#         current = string_to_state(current_str)

#         if current_str == goal_str:
#             return path,explored_nodes
        
#         for neighbour,move in get_neighbours(current):
#             neighbour_str = state_to_string(neighbour)
#             if len(path) == 0:
#                 g_cost = 1.1
#             else:
#                 g_cost = 1/(len(path))
#             h_cost = 0
#             f_cost = g_cost+h_cost

#             if neighbour_str not in distances.keys() or g_cost < distances[neighbour_str]:
#                 distances[neighbour_str] = g_cost
#                 heapq.heappush(pq, (f_cost, neighbour_str, g_cost, path + [move]))

#     return [], explored_nodes




def dijkstra(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int, int]:
    """
    Implement Dijkstra's algorithm to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array
    
    Returns:
        Tuple[List[str], int, int]: A tuple containing:
            - List of moves to reach the goal state
            - Number of nodes expanded during the search
            - Total cost of the path for transforming initial into goal configuration
            
    """
    
    # TODO: Implement this function
    initial_str = state_to_string(initial)
    goal_str = state_to_string(goal)

    open_list = []
    heapq.heappush(open_list,(0,initial_str,0,[]))
    closed_list = {initial_str: 0}
    explored_nodes = 0

    while open_list:
        f_cost,current_str,current_cost,path = heapq.heappop(open_list)
        explored_nodes += 1
        current = string_to_state(current_str)

        if current_str == goal_str:
            return path,explored_nodes, len(path)
        
        for neighbour,move in get_neighbours(current):
            neighbour_str = state_to_string(neighbour)
            g_cost = current_cost + 1
            h_cost = 0
            f_cost = g_cost+h_cost

            if neighbour_str not in closed_list.keys() or g_cost < closed_list[neighbour_str]:
                closed_list[neighbour_str] = g_cost
                heapq.heappush(open_list, (f_cost, neighbour_str, g_cost, path + [move]))

    return [], 0, 0
    

def astar_dt(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int, int]:
    """
    Implement A* Search with Displaced Tiles heuristic to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array
    
    Returns:
        Tuple[List[str], int, int]: A tuple containing:
            - List of moves to reach the goal state
            - Number of nodes expanded during the search
            - Total cost of the path for transforming initial into goal configuration
              
    
    """
    def displaced_tiles_heuristic(state):
        count = 0
        for i, x in enumerate(state.flatten()):
            if x != 0 and x != goal.flatten()[i]:
                count += 1
        return count
    
    
    # TODO: Implement this function
    initial_str = state_to_string(initial)
    goal_str = state_to_string(goal)

    open_list = []
    heapq.heappush(open_list,(0,initial_str,0,[]))
    closed_list = {initial_str: 0}
    explored_nodes = 0

    while open_list:
        f_cost,current_str,current_cost,path = heapq.heappop(open_list)
        explored_nodes += 1
        current = string_to_state(current_str)

        if current_str == goal_str:
            return path,explored_nodes,len(path)
        
        for neighbour,move in get_neighbours(current):
            neighbour_str = state_to_string(neighbour)
            g_cost = current_cost + 1
            h_cost = displaced_tiles_heuristic(current)
            f_cost = g_cost+h_cost

            if neighbour_str not in closed_list.keys()  or g_cost < closed_list[neighbour_str]:
                closed_list[neighbour_str] = g_cost
                heapq.heappush(open_list, (f_cost, neighbour_str, g_cost, path + [move]))

    return [], 0,0

def astar_md(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int, int]:
    """
    Implement A* Search with Manhattan Distance heuristic to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array
    
    Returns:
        Tuple[List[str], int, int]: A tuple containing:
            - List of moves to reach the goal state
            - Number of nodes expanded during the search
            - Total cost of the path for transforming initial into goal configuration
    """
    # TODO: Implement this function
    def displaced_tiles_heuristic(state):
        distance = 0
        for x, y in np.ndindex(state.shape):
            value = state[x, y]
            if value != 0:
                goal_x, goal_y = np.argwhere(goal == value)[0]
                distance += abs(x - goal_x) + abs(y - goal_y)
        return distance
    
    
    # TODO: Implement this function
    initial_str = state_to_string(initial)
    goal_str = state_to_string(goal)

    open_list = []
    heapq.heappush(open_list,(0,initial_str,0,[]))
    closed_list = {initial_str: 0}
    explored_nodes = 0

    while open_list:
        f_cost,current_str,current_cost,path = heapq.heappop(open_list)
        explored_nodes += 1
        current = string_to_state(current_str)

        if current_str == goal_str:
            return path,explored_nodes,len(path)
        
        for neighbour,move in get_neighbours(current):
            neighbour_str = state_to_string(neighbour)
            g_cost = current_cost + 1
            h_cost = displaced_tiles_heuristic(current)
            f_cost = g_cost+h_cost

            if neighbour_str not in closed_list.keys() or g_cost < closed_list[neighbour_str]:
                closed_list[neighbour_str] = g_cost
                heapq.heappush(open_list, (f_cost, neighbour_str, g_cost, path + [move]))

    return [], 0,0
    

# Example test case to help verify your implementation
if __name__ == "__main__":
    # Example puzzle configuration
    initial_state = np.array([
        [3, 2, 1],
        [4, 0, 6],
        [5, 7, 8]
    ])
    
    goal_state = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ])
    
    #Test each algorithm
    print("Testing BFS...")
    bfs_moves, bfs_expanded = bfs(initial_state, goal_state)
    print(f"BFS Solution: {bfs_moves}")
    print(f"Nodes expanded: {bfs_expanded}")
    
    # print("\nTesting DFS...")
    # dfs_moves, dfs_expanded = dfs(initial_state, goal_state)
    # print(f"DFS Solution: {dfs_moves}")
    # print(f"Nodes expanded: {dfs_expanded}")
    
    print("\nTesting Dijkstra...")
    dijkstra_moves, dijkstra_expanded, dijkstra_cost = dijkstra(initial_state, goal_state)
    print(f"Dijkstra Solution: {dijkstra_moves}")
    print(f"Nodes expanded: {dijkstra_expanded}")
    print(f"Total cost: {dijkstra_cost}")
    
    print("\nTesting A* with Displaced Tiles...")
    dt_moves, dt_expanded, dt_fscore = astar_dt(initial_state, goal_state)
    print(f"A* (DT) Solution: {dt_moves}")
    print(f"Nodes expanded: {dt_expanded}")
    print(f"Total cost: {dt_fscore}")
    
    print("\nTesting A* with Manhattan Distance...")
    md_moves, md_expanded, md_fscore = astar_md(initial_state, goal_state)
    print(f"A* (MD) Solution: {md_moves}")
    print(f"Nodes expanded: {md_expanded}")
    print(f"Total cost: {md_fscore}")