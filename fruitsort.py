from typing import List, Tuple
from heapq import heapify, heappush, heappop

# used these to test the code but length 10 takes too long still
start10 = [
    ['banana_3', 'orange_7', 'apple_1', 'orange_1', 'banana_6', 'apple_2', 'orange_2', 'banana_2', 'apple_6', 'banana_1'],
    ['apple_9', 'orange_9', 'banana_10', 'apple_4', 'banana_5', 'orange_10', 'apple_5', 'banana_8', 'orange_8', 'apple_8'],
    ['orange_3', 'banana_9', 'apple_3', 'orange_4', 'apple_7', 'banana_4', 'orange_6', 'apple_10', 'banana_7', 'orange_5']
]

target10 = [
    ['apple_1', 'apple_2', 'apple_3', 'apple_4', 'apple_5', 'apple_6', 'apple_7', 'apple_8', 'apple_9', 'apple_10'],
    ['banana_1', 'banana_2', 'banana_3', 'banana_4', 'banana_5', 'banana_6', 'banana_7', 'banana_8', 'banana_9', 'banana_10'],
    ['orange_1', 'orange_2', 'orange_3', 'orange_4', 'orange_5', 'orange_6', 'orange_7', 'orange_8', 'orange_9', 'orange_10']
]

start4 = [
    ['banana_3', 'orange_2', 'apple_1', 'orange_1'],
    ['apple_2', 'banana_1', 'apple_4', 'banana_4'],
    ['orange_4', 'banana_2', 'apple_3', 'orange_3']
]

target4 = [
    ['apple_1', 'apple_2', 'apple_3', 'apple_4'],
    ['banana_1', 'banana_2', 'banana_3', 'banana_4'],
    ['orange_1', 'orange_2', 'orange_3', 'orange_4']
]

start = [
    ['banana_3', 'orange_2', 'banana_9', 'apple_6', 'apple_1', 'apple_7', 'orange_1', 'banana_4', 'apple_8'],
    ['apple_5', 'banana_6', 'orange_5', 'banana_1', 'orange_7', 'orange_8', 'apple_9', 'apple_4', 'banana_5'],
    ['orange_4', 'orange_9', 'banana_2', 'apple_3', 'orange_3', 'banana_8', 'orange_6', 'banana_7', 'apple_2']
]

target = [
    ['apple_1', 'apple_2', 'apple_3', 'apple_4', 'apple_5', 'apple_6', 'apple_7', 'apple_8', 'apple_9'],
    ['banana_1', 'banana_2', 'banana_3', 'banana_4', 'banana_5', 'banana_6', 'banana_7', 'banana_8', 'banana_9'],
    ['orange_1', 'orange_2', 'orange_3', 'orange_4', 'orange_5', 'orange_6', 'orange_7', 'orange_8', 'orange_9']
]


class State:
    def __init__(self, array: List[List[str]]):
        self.array = array
        self.g = 0 # The cost to reach this state
        self.h = 0 # The heuristic value
        self.f = 0 # The sum of g and h
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
        
    def compute_h(self, target: List[List[str]]) -> int:
        #compute the heuristic function
        h = 0
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                if self.array[i][j] == "":
                    continue
                target_pos = find_position(target, self.array[i][j])
                h += abs(target_pos[0] - i) + abs(target_pos[1] - j)
        self.h = h
        return h
    
    def compute_f(self) -> int:
        #Compute the f value
        self.f = self.g + self.h
        return self.f
    
    def get_successors(self, target: List[List[str]]) -> List['State']:
        successors = []
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                for di, dj in [(0, 1), (1, 0)]:
                    ni, nj = i + di, j + dj
                    if ni < 0 or ni >= len(self.array) or nj < 0 or nj >= len(self.array[i]):
                        continue
                    new_state = self.swap((i, j), (ni, nj))
                    new_state.compute_h(target)
                    new_state.g = self.g + 1
                    new_state.compute_f()
                    new_state.parent = self
                    successors.append(new_state)
        return successors
    
def find_position(array: List[List[str]], value: str) -> Tuple[int, int]:
   #Find the position of a value in a 2D array
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == value:
                return (i, j)
    return None


def astar(start: List[List[str]], target: List[List[str]]) -> Tuple[List[List[str]], int]:
    start_state = State(start)
    start_state.compute_h(target)
    start_state.compute_f()
    
    frontier = [start_state]
    visited = set()
    
    while frontier: #continues until frontier is empty goal is found 
        current_state = heappop(frontier) # pops the state with the lowest f value
        visited.add(current_state)
        
        if current_state.array == target: 
            moves = current_state.g
            path = []
            while current_state:
                path.append(current_state.array)
                current_state = current_state.parent
            path.reverse()
            return (path, moves)
        
        for successor in current_state.get_successors(target): #successors are added to frontier
            if successor in visited: #
                continue
            if successor not in frontier:
                heappush(frontier, successor)
            else: #if successor is already in frontier, check if cost is lower
                index = frontier.index(successor)
                if frontier[index].f > successor.f:
                    frontier[index] = successor
                    heapify(frontier)
                    
    return (None, None)


# Call the astar solve function to find the solution
solution, moves = astar(start, target)

if solution is None:
    print("No solution found.")
else:
    for step in solution:
        print(step)
    print(f"Solution found in {moves} moves") 
