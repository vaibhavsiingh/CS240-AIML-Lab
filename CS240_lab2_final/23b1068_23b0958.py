import heapq
import json
from typing import List, Tuple


def check_valid(
    state: list, max_missionaries: int, max_cannibals: int
) -> bool:  # 10 marks
    """
    Graded
    Check if a state is valid. State format: [m_left, c_lright boat_position].
    """
    m_left, c_left, boat_pos = state
    m_right = max_missionaries - m_left
    c_right = max_cannibals - c_left

    if boat_pos !=0 and boat_pos != 1:
        return False

    if m_left < 0 or m_right < 0 or c_left < 0 or c_right < 0:
        return False
    if m_left < c_left and m_left != 0:
        return False
    if m_right < c_right and m_right != 0:
        return False
    return True


def get_neighbours(
    state: list, max_missionaries: int, max_cannibals: int
) -> List[list]:  # 10 marks
    """
    Graded
    Generate all valid neighbouring states.
    """
    m_left, c_left, boat_pos = state
    m_right = max_missionaries - m_left
    c_right = max_cannibals - c_left
    neighbours = []
    moves = [(1,0),(2,0),(0,1),(0,2),(1,1)]
    if boat_pos == 1:
        for move in moves:
            m_move, c_move = move
            new_m_left = m_left - m_move
            new_c_left = c_left - c_move
            new_state = (new_m_left,new_c_left,0)
            if(check_valid(new_state,max_missionaries,max_cannibals)):
                neighbours.append(new_state)
    else:
        for move in moves:
            m_move, c_move = move
            new_m_right = m_right - m_move
            new_c_right = c_right - c_move
            new_state = (max_missionaries- new_m_right,max_cannibals - new_c_right,1)
            if(check_valid(new_state,max_missionaries,max_cannibals)):
                neighbours.append(new_state)
    return neighbours




def gstar(state: list, new_state: list) -> int:  # 5 marks
    """
    Graded
    The weight of the edge between state and new_state, this is the number of people on the boat.
    """
    m_left, c_left, boat_pos = state
    new_m_left, new_c_left, new_boat_pos = new_state
    if new_boat_pos == 1:
        return new_m_left-m_left + new_c_left - c_left
    else:
        return m_left - new_m_left + c_left - new_c_left



def h1(state: list) -> int:  # 3 marks
    """
    Graded
    h1 is the number of people on the left bank.
    """
    """
    We need to prove that for any states s and s', if s' is a successor of s, then h1(s) <= h1(s') + cost(s, s').

    Here, h1 is the number of people on the left bank.
    If the boat carries k people from left to right, h1(s') will be h1(s)-k, and cost will be k
    So
    h1(s) <= h1(s')+ cost(s,s')
    In the other case, when boat carries k people from right to left, h1(s') >= h1(s). 
    Hence, monotonic
    """
    return state[0]+state[1]
    

def h2(state: list) -> int:  # 3 marks
    """
    Graded
    h2 is the number of missionaries on the left bank. 
    """
    '''
    We need to prove that for any states s and s', if s' is a successor of s, then h2(s) <= h2(s') + cost(s, s').

    Here, h2 is the number of missionaries on the left bank.
    If the boat carries k missionaries from left to right, h2(s') will be h2(s)-k, and cost will be atleast k
    So
    h2(s) <= h2(s')+ cost(s,s')
    In the other case, when boat carries k missionaries from right to left, h2(s') >= h2(s). 
    Hence, monotonic
    
    '''
    return state[0]


def h3(state: list) -> int:  # 3 marks
    """
    Graded
    h3 is the number of cannibals on the left bank.
    """
    '''
    We need to prove that for any states s and s', if s' is a successor of s, then h3(s) <= h3(s') + cost(s, s').

    Here, h3 is the number of cannibals on the left bank.
    If the boat carries k cannibals from left to right, h3(s') will be h3(s)-k, and cost will be atleast k
    So
    h3(s) <= h3(s')+ cost(s,s')
    In the other case, when boat carries k cannibals from right to left, h3(s') >= h3(s). 
    Hence, monotonic
    '''
    return state[1]


def h4(state: list) -> int:  # 3 marks
    """
    Graded
    Weights of missionaries is higher than cannibals.
    h4 = missionaries_left * 1.5 + cannibals_left
    """
    return 1.5*state[0] + state[1]


def h5(state: list) -> int:  # 3 marks
    """
    Graded
    Weights of missionaries is lower than cannibals.
    h5 = missionaries_left + cannibals_left*1.5
    """
    return state[0] + 1.5*state[1]


def astar_h1(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 28 marks
    """
    Graded
    Implement A* with h1 heuristic.
    This function must return path obtained and a boolean which says if the heuristic chosen satisfies Monotone restriction property while exploring or not.
    """
    open_list = []
    close_list = {}
    parent_map = {}
    g_map = {}
    g = 0
    init_state = tuple(init_state)
    final_state = tuple(final_state)
    g_map[init_state] = 0
    h = h1(init_state)
    f = g + h
    heapq.heappush(open_list, (f, g, init_state))
    parent_map[init_state] = None
    monotone = True

    while open_list:
        f, g, curr_state = heapq.heappop(open_list)

        if curr_state == final_state:
            path = []
            while curr_state is not None:
                path.append(curr_state)
                curr_state = parent_map[curr_state]
            return path[::-1], monotone

        close_list[curr_state] = g

        for neighbour in get_neighbours(curr_state, max_missionaries, max_cannibals):
            new_g = g + gstar(curr_state, neighbour)
            new_h = h1(neighbour)
            new_f = new_g + new_h

            if neighbour in close_list:
                if h1(curr_state) > new_h + new_g:
                    monotone = False
                continue
            
            if neighbour not in g_map or g_map[neighbour] > new_g:
                heapq.heappush(open_list, (new_f, new_g, neighbour))
                parent_map[neighbour] = curr_state
                g_map[neighbour] = new_g

    return [], monotone


def astar_h2(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 8 marks
    """
    Graded
    Implement A* with h2 heuristic.
    """
    open_list = []
    close_list = {}
    parent_map = {}
    g_map = {}
    g = 0
    init_state = tuple(init_state)
    final_state = tuple(final_state)
    g_map[init_state] = 0
    h = h1(init_state)
    f = g + h
    heapq.heappush(open_list, (f, g, init_state))
    parent_map[init_state] = None
    monotone = True

    while open_list:
        f, g, curr_state = heapq.heappop(open_list)

        if curr_state == final_state:
            path = []
            while curr_state is not None:
                path.append(curr_state)
                curr_state = parent_map[curr_state]
            return path[::-1], monotone

        close_list[curr_state] = g

        for neighbour in get_neighbours(curr_state, max_missionaries, max_cannibals):
            new_g = g + gstar(curr_state, neighbour)
            new_h = h1(neighbour)
            new_f = new_g + new_h

            if neighbour in close_list:
                if h1(curr_state) > new_h + new_g:
                    monotone = False
                continue
            
            if neighbour not in g_map or g_map[neighbour] > new_g:
                heapq.heappush(open_list, (new_f, new_g, neighbour))
                parent_map[neighbour] = curr_state
                g_map[neighbour] = new_g

    return [], monotone
    


def astar_h3(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 8 marks
    """
    Graded
    Implement A* with h3 heuristic.
    """
    open_list=[]
    close_list={}
    g=0
    init_state = tuple(init_state)
    final_state = tuple(final_state)
    h=h3(init_state)
    f=g+h
    heapq.heappush(open_list,(f,g,init_state,[]))
    monotone=True
    
    while open_list:
        f,g,curr_state,path=heapq.heappop(open_list)

        if curr_state== final_state:
            return path+[curr_state],monotone
        
        
        close_list[curr_state]=g

        for neighbour in get_neighbours(curr_state,max_missionaries,max_cannibals):
            new_g=g=gstar(curr_state,neighbour)
            new_h=h3(neighbour)
            new_f=new_g+new_h

            if neighbour in close_list:
                if h3(curr_state)> new_h+new_g:
                    monotone=False
                if new_g >=close_list[neighbour]:
                    continue
            heapq.heappush(open_list,(new_f,new_g,neighbour,path+[curr_state]))
            close_list[neighbour]=new_g

    return [],monotone
    raise ValueError("astar_h3 not implemented")

def astar_h4(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 8 marks
    """
    Graded
    Implement A* with h4 heuristic.
    """
    open_list=[]
    close_list={}
    g=0
    init_state = tuple(init_state)
    final_state = tuple(final_state)
    h=h4(init_state)
    f=g+h
    heapq.heappush(open_list,(f,g,init_state,[]))
    monotone=True
    
    while open_list:
        f,g,curr_state,path=heapq.heappop(open_list)

        if curr_state== final_state:
            return path+[curr_state],monotone
        
        
        close_list[curr_state]=g

        for neighbour in get_neighbours(curr_state,max_missionaries,max_cannibals):
            new_g=g=gstar(curr_state,neighbour)
            new_h=h4(neighbour)
            new_f=new_g+new_h

            if neighbour in close_list:
                if h4(curr_state)> new_h+new_g:
                    monotone=False
                if new_g >=close_list[neighbour]:
                    continue
            heapq.heappush(open_list,(new_f,new_g,neighbour,path+[curr_state]))
            close_list[neighbour]=new_g

    return [],monotone


def astar_h5(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 8 marks
    """
    Graded
    Implement A* with h5 heuristic.
    """
    open_list=[]
    close_list={}
    g=0
    init_state = tuple(init_state)
    final_state = tuple(final_state)
    h=h5(init_state)
    f=g+h
    heapq.heappush(open_list,(f,g,init_state,[]))
    monotone=True
    
    while open_list:
        f,g,curr_state,path=heapq.heappop(open_list)

        if curr_state== final_state:
            return path+[curr_state],monotone
        
        
        close_list[curr_state]=g

        for neighbour in get_neighbours(curr_state,max_missionaries,max_cannibals):
            new_g=g=gstar(curr_state,neighbour)
            new_h=h5(neighbour)
            new_f=new_g+new_h

            if neighbour in close_list:
                if h5(curr_state)> new_h+new_g:
                    monotone=False
                if new_g >=close_list[neighbour]:
                    continue
            heapq.heappush(open_list,(new_f,new_g,neighbour,path+[curr_state]))
            close_list[neighbour]=new_g

    return [],monotone


def print_solution(solution: List[list],max_mis,max_can):
    """
    Prints the solution path. 
    """
    if not solution:
        print("No solution exists for the given parameters.")
        return
        
    print("\nSolution found! Number of steps:", len(solution) - 1)
    print("\nLeft Bank" + " "*20 + "Right Bank")
    print("-" * 50)
    
    for state in solution:
        if state[-1]:
            boat_display = "(B) " + " "*15
        else:
            boat_display = " "*15 + "(B) "
            
        print(f"M: {state[0]}, C: {state[1]}  {boat_display}" 
              f"M: {max_mis-state[0]}, C: {max_can-state[1]}")


def print_mon(ism: bool):
    """
    Prints if the heuristic function is monotone or not.
    """
    if ism:
        print("-" * 10)
        print("|Monotone|")
        print("-" * 10)
    else:
        print("-" * 14)
        print("|Not Monotone|")
        print("-" * 14)


def main():
    try:
        testcases = [{"m": 3, "c": 3}]

        for case in testcases:
            max_missionaries = case["m"]
            max_cannibals = case["c"]
            
            init_state = [max_missionaries, max_cannibals, 1] #initial state 
            final_state = [0, 0, 0] # final state
            
            if not check_valid(init_state, max_missionaries, max_cannibals):
                print(f"Invalid initial state for case: {case}")
                continue
                
            path_h1,ism1 = astar_h1(init_state, final_state, max_missionaries, max_cannibals)
            path_h2,ism2 = astar_h2(init_state, final_state, max_missionaries, max_cannibals)
            path_h3,ism3 = astar_h3(init_state, final_state, max_missionaries, max_cannibals)
            path_h4,ism4 = astar_h4(init_state, final_state, max_missionaries, max_cannibals)
            path_h5,ism5 = astar_h5(init_state, final_state, max_missionaries, max_cannibals)
            print_solution(path_h1,max_missionaries,max_cannibals)
            print_mon(ism1)
            print("-"*50)
            print_solution(path_h2,max_missionaries,max_cannibals)
            print_mon(ism2)
            print("-"*50)
            print_solution(path_h3,max_missionaries,max_cannibals)
            print_mon(ism3)
            print("-"*50)
            print_solution(path_h4,max_missionaries,max_cannibals)
            print_mon(ism4)
            print("-"*50)
            print_solution(path_h5,max_missionaries,max_cannibals)
            print_mon(ism5)
            print("="*50)

    except KeyError as e:
        print(f"Missing required key in test case: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()