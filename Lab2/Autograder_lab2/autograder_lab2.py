import os
import importlib.util
import sys
import math
import json
import signal
from typing import List, Tuple, Any

def timeout_handler(signum, frame):
    raise TimeoutError("Function execution timed out")

def run_with_timeout(func, args=(), kwargs={}, timeout=2):
    """Run a function with a time limit."""
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        result = func(*args, **kwargs)
    finally:
        signal.alarm(0)  # Disable alarm
    return result   

def ref_check_valid(state: list, max_missionaries: int, max_cannibals: int) -> bool: # 10 marks 
    """
    Check if a state is valid. State format: [m_left, c_left, boat_position]
    """
    if not (0 <= state[0] <= max_missionaries and 0 <= state[1] <= max_cannibals):
        return False
    if (state[0] > 0 and state[0] < state[1]) or ((max_missionaries-state[0]) > 0 and (max_missionaries-state[0]) < (max_cannibals-state[1])):
        return False
        
    return True

def ref_get_neighbours(state: list, max_missionaries: int, max_cannibals: int) -> List[list]: # 10 marks
    """Generate all valid neighbouring states"""
    moves = [(0,1), (1,0), (1,1), (0,2), (2,0)]
    new_boat_state = 1 - state[-1]
    possible_states = []
    
    for dm, dc in moves:
        new_state = state.copy()
        
        if state[-1] == 1:  # Boat is on left bank
            new_state[0] -= dm
            new_state[1] -= dc
        else:  # Boat is on right bank
            new_state[0] += dm
            new_state[1] += dc
            
        new_state[-1] = new_boat_state
        
        if ref_check_valid(new_state, max_missionaries, max_cannibals):
            possible_states.append(new_state)
    
    return possible_states

def load_student_solution(file_path: str) -> Any:
    """Load student's solution file as a module."""
    spec = importlib.util.spec_from_file_location("student_solution", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["student_solution"] = module
    spec.loader.exec_module(module)
    return module

def test_check_valid(solution: Any) -> Tuple[int, str]:
    """Test the check_valid function"""
    test_cases = [
        # state, max_missionaries, max_cannibals, expected
        ([3, 3, 1], 3, 3, True),
        ([4, 3, 1], 4, 3, True),
        ([2, 3, 1], 3, 3, False),  # more cannibals than missionaries
        ([5, 3, 1], 4, 3, False),  # Exceeds max missionaries
        ([3, 4, 1], 3, 3, False),  # Exceeds max cannibals
        ([-1, 3, 1], 3, 3, False),  # Negative missionaries
        ([3, -1, 1], 3, 3, False),  # Negative cannibals
        ([2, 3, 1], 2, 3, False),  # more cannibals than missionaries
        ([3, 3, 0], 2, 3, False),  # Exceeds max missionaries
        ([3, 3, 1], 3, 2, False)  # Exceeds max cannibals
    ]
    
    score = 0
    # max_score = 10
    errors = []
    
    for state, max_m, max_c, expected in test_cases:
        try:
            result = run_with_timeout(solution.check_valid,(state, max_m, max_c))
            if result == expected:
                score += 1
            else:
                errors.append(f"Failed for state {state}, expected {expected}, got {result}")
        except TimeoutError:
            errors.append(f"Timeout for state {state}")
        except Exception as e:
            errors.append(f"Error: {str(e)}")
            
    return score, "; ".join(errors) if errors else "All tests passed"

def test_get_neighbours(solution: Any) -> Tuple[int, str]:
    """Test the get_neighbours function"""
    test_cases = [
        ([3, 3, 1], 3, 3),  # Initial state
        ([2, 2, 0], 3, 3),  # Middle state
        ([0, 0, 0], 3, 3),  # Final state
        ([4,3,1],4,3),
        ([7,4,1],7,4)
    ]

    score = 0
    # max_score = 10
    errors = []
    
    for state, max_m, max_c in test_cases:
        try:
            student_neighbours = run_with_timeout(solution.get_neighbours,(state, max_m, max_c))
            reference_neighbours = ref_get_neighbours(state, max_m, max_c)
            
            # Convert lists to tuples for comparison since lists aren't hashable
            student_states = {tuple(state) for state in student_neighbours}
            reference_states = {tuple(state) for state in reference_neighbours}
            
            # Check if all generated states are valid using reference solution
            all_valid = all(ref_check_valid(list(state), max_m, max_c) for state in student_states)
            
            # Check if student solution generates all valid states
            missing_states = reference_states - student_states
            extra_states = student_states - reference_states
            

            if not all_valid:
                errors.append(f"Generated invalid states for {state}")
            
            if missing_states or extra_states :
                if missing_states:
                    errors.append(f"Missing valid states: {missing_states}")
                if extra_states:
                    errors.append(f"Generated invalid extra states: {extra_states}")
                
            # Check if boat position alternates
            if all(s[-1] != state[-1] for s in student_neighbours) and all_valid and not missing_states and not extra_states:
                score += 2
            else:
                errors.append(f"Boat position doesn't alternate correctly for {state}")
        except TimeoutError:
            errors.append(f"Timeout for state {state}")        
        except Exception as e:
            errors.append(f"Error: {str(e)}")
    
    return score, "; ".join(errors) if errors else "All tests passed"

def test_gstar(solution: Any) -> Tuple[int, str]:
    """Test the gstar function"""
    test_cases = [
        ([3, 3, 1], [2, 2, 0], 2),  # Two people move
        ([3, 3, 1], [3, 2, 0], 1),  # One person moves
        ([2, 2, 0], [3, 3, 1], 2),  # Two people move back
        ([1, 1, 1],[0, 0, 0], 2),  # Two people move to the right
        ([7, 4, 1], [7, 3, 0], 1),  # One person moves
        ([7, 4, 1], [6, 3, 0], 2),  # Two people move
        ([7, 2, 1], [5, 2, 0], 2),  # Two people move
        ([1000,1234,1],[1000,1232,0],2),  # Two people move
        ([3, 3, 0], [4, 3, 1], 1),  # One person moves
        ([13, 13, 1], [13, 12, 0], 1)  # One person moves
    ]
    
    score = 0
    # max_score = 5
    errors = []
    
    for state, new_state, expected in test_cases:
        try:
            result = run_with_timeout(solution.gstar,(state, new_state))
            if result == expected:
                score += 0.5
            else:
                errors.append(f"Failed for states {state}->{new_state}, expected {expected}, got {result}")
        except TimeoutError:
            errors.append(f"Timeout for states {state}->{new_state}")
        except Exception as e:
            errors.append(f"Error: {str(e)}")
            
    return score, "; ".join(errors) if errors else "All tests passed"

def test_heuristic(solution: Any, heuristic_name: str, test_cases: List[Tuple]) -> Tuple[int, str]:
    """Test a heuristic function"""
    score = 0
    errors = []
    
    heuristic_func = getattr(solution, heuristic_name)
    
    for state, expected in test_cases:
        try:
            result = heuristic_func(state)
            if result == expected:
                score += 0.5
            else:
                errors.append(f"Failed for state {state}, expected {expected}, got {result}")
        except TimeoutError:
            errors.append(f"Timeout for state {state}")
        except Exception as e:
            errors.append(f"Error: {str(e)}")
            
    return score, "; ".join(errors) if errors else "All tests passed"

def test_astar(solution: Any, astar_func_name: str) -> Tuple[int, str]:
    """Test an A* implementation"""
    test_cases = [
        (4,3),  # Standard case
        (3,3),  # Classic case
        (5,4),
        (5,3),
        (7,4)
    ]
    
    score = 0
    max_score = 7
    errors = []
    if astar_func_name == "astar_h1":
        max_score = 26

    astar_func = getattr(solution, astar_func_name)
    
    for max_m, max_c in test_cases:
        try:
            result = run_with_timeout(astar_func, ([max_m, max_c, 1], [0, 0, 0], max_m, max_c), timeout=5)
            path, is_monotone = result
            
            # Check if solution exists
            if not path:
                errors.append(f"No solution found for {max_m},{max_c}")
                continue
                
            # Check if path is valid
            valid_path = True
            for i in range(len(path)-1):
                if path[i+1] not in ref_get_neighbours(path[i], max_m, max_c):
                    valid_path = False
                    break
                    
            if valid_path:
                score += 1
            else:
                errors.append(f"Invalid path for {max_m},{max_c}")
        except TimeoutError:
            errors.append(f"Timeout for {max_m},{max_c}")
        except Exception as e:
            errors.append(f"Error: {str(e)}")
            
    return math.ceil(score*(max_score/5)), "; ".join(errors) if errors else "All tests passed"

def grade_submission(file_path: str) -> dict:
    """Grade a single submission"""
    try:
        solution = load_student_solution(file_path)
        
        results = {
            "filename": os.path.basename(file_path),
            "check_valid_score": 0,
            "check_valid_feedback": "",
            "get_neighbours_score": 0,
            "get_neighbours_feedback": "",
            "gstar_score": 0,
            "gstar_feedback": "",
            "h1_score": 0,
            "h1_feedback": "",
            "h2_score": 0,
            "h2_feedback": "",
            "h3_score": 0,
            "h3_feedback": "",
            "astar_h1_score": 0,
            "astar_h1_feedback": "",
            "astar_h2_score": 0,
            "astar_h2_feedback": "",
            "astar_h3_score": 0,
            "astar_h3_feedback": ""
        }
        
        # Test basic functions
        results["check_valid_score"], results["check_valid_feedback"] = test_check_valid(solution)
        results["get_neighbours_score"], results["get_neighbours_feedback"] = test_get_neighbours(solution)
        results["gstar_score"], results["gstar_feedback"] = test_gstar(solution)
        
        # Test heuristics
        h1_cases = [([3, 3, 1], 6), ([2, 2, 0], 4),([4,1,0],5),([4,2,0],6),([4,3,0],7),([114,4,0],118),([4,3425,0],3429),([13444,43216,0],56660),([100004,123127,1],223131),([4,8,0],12)]
        h2_cases = [([3, 3, 1], 3), ([2, 2, 0], 2),([4,1,0],4),([4,2,0],4),([4,3,0],4),([114,4,0],114),([4,3425,0],4),([13444,43216,0],13444),([100004,123127,1],100004),([4,8,0],4)]
        h3_cases = [([3, 3, 1], 3), ([2, 2, 0], 2),([4,1,0],1),([4,2,0],2),([4,3,0],3),([114,4,0],4),([4,3425,0],3425),([13444,43216,0],43216),([100004,123127,1],123127),([4,8,0],8)]
        
        results["h1_score"], results["h1_feedback"] = test_heuristic(solution, "h1", h1_cases)
        results["h2_score"], results["h2_feedback"] = test_heuristic(solution, "h2", h2_cases)
        results["h3_score"], results["h3_feedback"] = test_heuristic(solution, "h3", h3_cases)
        
        # Test A* implementations
        results["astar_h1_score"], results["astar_h1_feedback"] = test_astar(solution, "astar_h1")
        results["astar_h2_score"], results["astar_h2_feedback"] = test_astar(solution, "astar_h2")
        results["astar_h3_score"], results["astar_h3_feedback"] = test_astar(solution, "astar_h3")
        
        # Calculate total score
        results["total_score"] = (
            results["check_valid_score"] +
            results["get_neighbours_score"] +
            results["gstar_score"] +
            results["h1_score"] +
            results["h2_score"] +
            results["h3_score"] +
            results["astar_h1_score"] +
            results["astar_h2_score"] +
            results["astar_h3_score"]
        )
        
        return results
        
    except Exception as e:
        return {
            "filename": os.path.basename(file_path),
            "error": f"Failed to grade submission: {str(e)}",
            "total_score": 0
        }

def main():
    # Create results directory if it doesn't exist
    if not os.path.exists("results"):
        os.makedirs("results")
        
    # Get all Python files in the Submissions directory
    submission_files = [f for f in os.listdir("submissions") if f.endswith(".py")]
    
    # Grade each submission
    results = []
    for file in submission_files:
        file_path = os.path.join("submissions", file)
        result = grade_submission(file_path)
        results.append(result)
    
    # Write results to a JSON file
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"Grading complete. Results written to results.json")

if __name__ == "__main__":
    main()