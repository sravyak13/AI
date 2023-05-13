from queue import PriorityQueue
from typing import List, Tuple
from heapq import heapify, heappush, heappop


class State:
    def __init__(self, array: List[List[str]]):
        self.array = array
        self.g = 0  # The cost to reach this state
        self.h = 0  # The heuristic value
        self.f = 0  # The sum of g and h
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.array == other.array

    def __hash__(self):
        return hash(str(self.array))

    def swap(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> 'State':
        #Return a new state by swapping the fruits at pos1 and pos2
        new_array = [row[:] for row in self.array]
        new_array[pos1[0]][pos1[1]], new_array[pos2[0]][pos2[1]] = new_array[pos2[0]][pos2[1]], new_array[pos1[0]][pos1[1]]
        new_state = State(new_array)
        return new_state

    def compute_h(self, targets: List[List[str]]) -> int:
        # Compute the heuristic function with Manhattan Distance to all targets
        h = float("inf")
        for target in targets:
            h_target = 0
            for i in range(len(self.array)):
                for j in range(len(self.array[i])):
                    if self.array[i][j] == "":
                        continue
                    h_value = float("inf")
                    for target_pos in find_all_positions(target, self.array[i][j]):
                        h_value = min(h_value, abs(target_pos[0] - i) + abs(target_pos[1] - j))
                    h_target += h_value
            h = min(h, h_target)
        self.h = h
        return h
    
    def compute_f(self) -> int:
        #Compute the f value
        self.f = self.g + self.h
        return self.f
        
    def get_successors(self, targets: List[List[str]]) -> List['State']:
        successors = []
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                for di, dj in [(0, 1), (1, 0)]:
                    ni, nj = i + di, j + dj
                    if ni < 0 or ni >= len(self.array) or nj < 0 or nj >= len(self.array[i]):
                        continue
                    new_state = self.swap((i, j), (ni, nj))
                    new_state.compute_h(targets)
                    new_state.g = self.g + 1
                    new_state.compute_f()
                    new_state.parent = self
                    successors.append(new_state)
        return successors
    
def find_all_positions(array: List[List[str]], value: str) -> List[Tuple[int, int]]:
    # Find all positions of a value in a 2D array
    positions = []
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == value:
                positions.append((i, j))
    return positions

def astar(start_state: State, targets: List[List[List[str]]]) -> Tuple[List[List[str]], int]:
    # initialize starting state and frontier
    frontier = PriorityQueue()
    frontier.put(start_state)
    explored = set()
    g = {start_state: 0}

    while not frontier.empty():
        current_state = frontier.get()
        if current_state.array in targets:
            # Compute the number of fruits not in their correct position
            num_misplaced_fruits = 0
            for i in range(len(current_state.array)):
                for j in range(len(current_state.array[i])):
                    if current_state.array[i][j] != targets[i][j]:
                        num_misplaced_fruits += 1
            return current_state.array, num_misplaced_fruits
        
        explored.add(current_state)
        successors = []
        for target in targets:
            successors.extend(current_state.get_successors(target))
        
        for successor in successors:
            if successor in explored:
                continue
            
            new_g = g[current_state] + 1
            if successor not in g or new_g < g[successor]:
                g[successor] = new_g
                frontier.put(successor)
    return None, float("inf")



start = [
    ['banana_3', 'orange_2', 'apple_1', 'orange_1'],
    ['apple_2', 'banana_1', 'apple_4', 'banana_4'],
    ['orange_4', 'banana_2', 'apple_3', 'orange_3']
]

targets = [
    [
        ['apple_1', 'apple_2', 'apple_3', 'apple_4'],
        ['banana_1', 'banana_2', 'banana_3', 'banana_4'],
        ['orange_1', 'orange_2', 'orange_3', 'orange_4']
    ],
    [
        ['apple_1', 'apple_2', 'apple_3', 'apple_4'],
        ['orange_1', 'orange_2', 'orange_3', 'orange_4'],
        ['banana_1', 'banana_2', 'banana_3', 'banana_4']
    ],
    [
        ['banana_1', 'banana_2', 'banana_3', 'banana_4'],
        ['orange_1', 'orange_2', 'orange_3', 'orange_4'],
        ['apple_1', 'apple_2', 'apple_3', 'apple_4']
    ],
    [
        ['orange_1', 'orange_2', 'orange_3', 'orange_4'],
        ['banana_1', 'banana_2', 'banana_3', 'banana_4'],
        ['apple_1', 'apple_2', 'apple_3', 'apple_4']
    ],
    [
        ['banana_1', 'banana_2', 'banana_3', 'banana_4'],
        ['apple_1', 'apple_2', 'apple_3', 'apple_4'],
        ['orange_1', 'orange_2', 'orange_3', 'orange_4']
    ],
    [
        ['orange_1', 'orange_2', 'orange_3', 'orange_4'],
        ['apple_1', 'apple_2', 'apple_3', 'apple_4'],
        ['banana_1', 'banana_2', 'banana_3', 'banana_4']
    ]
]

solution, moves = astar(State(start), targets)

if solution is None:
    print("No solution found.")
else:
    for step in solution:
        print(step)
    print(f"Solution found in {moves} moves")
