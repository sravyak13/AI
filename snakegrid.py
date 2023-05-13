
#function checks whether a letter can be placed in a cell of the grid, 
# by checking whether the letter is adjacent to any existing letters in the grid 
def validCheck(letter, row, column, grid):
    adjacent_cells = []
    for row_offset, column_offset in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        adjacent_row, adjacent_column = row + row_offset, column + column_offset
        if 0 <= adjacent_row < 5 and 0 <= adjacent_column < 5:
            adjacent_letter = grid[adjacent_row][adjacent_column]
            if adjacent_letter != '-':
                adjacent_cells.append(adjacent_letter)
    if not adjacent_cells: return True
    for adjacent_letter in adjacent_cells:
        if abs(ord(adjacent_letter) - ord(letter)) == 1:
            return True
    return False

def mrv(grid, domain): #returns the cell with the smallest domain
    size_track = float('inf')
    variable_track = None
    for (row, column), d in domain.items():
        if grid[row][column] == '-' and len(d) < size_track:
            size_track = len(d)
            variable_track = (row, column)
    return variable_track

def snake(grid, available, domain, row=0, column=0): # recursive backtracking function that tries assigning letters to each empty cell
    if not available: return True
    if column == 5:
        row += 1
        column = 0
    if grid[row][column] != '-': return snake(grid, available, domain, row, column + 1)
    variable = mrv(grid, domain)

    # Try each letter in the domain of the variable
    for letter in domain[variable] and available:
        if validCheck(letter, variable[0], variable[1], grid):
            grid[variable[0]][variable[1]] = letter     # assign the letter to the cell
            new_available = available - {letter} # update available letters
            impactedcells = [] # update domains of impacted

            for row_inc, column_inc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                row_temp, column_temp = variable[0] + row_inc, variable[1] + column_inc
                if 0 <= row_temp < 5 and 0 <= column_temp < 5 and grid[row_temp][column_temp] == '-':
                    impactedcells.append((row_temp, column_temp))

            for row_temp, column_temp in impactedcells:
                domain[(row_temp, column_temp)] -= {letter}
                if not domain[(row_temp, column_temp)]:
                    grid[variable[0]][variable[1]] = '-'
                    continue

            if snake(grid, new_available, domain, variable[0], variable[1]):
                return True

            for row_temp, column_temp in impactedcells:            # backtrack if the recursive call fails
                domain[(row_temp, column_temp)].add(letter)

            grid[variable[0]][variable[1]] = '-'

    return False     # If no letter in the domain works, backtrack

#returns the set of available letters that can be assigned to empty cells in the grid
def getAvailableLetters(grid):
    unavailable = set()
    for row in grid:
        for cell in row:
            if cell != '-':
                unavailable.add(cell)
    available = set(chr(ord('A') + i) for i in range(25)) - unavailable
    return available

# to initialize the domain using AC3 algorithm by updating the domain of each variable 
# by removing values that are inconsistent with the constraints of the problem
def ac3(domain):
    queue = list(domain.keys()) # initialize queue with all variables
    while queue:
        variable = queue.pop(0)
        for neighbor in getNeighbors(variable):
            if revise(domain, variable, neighbor):
                if not domain[variable]:
                    return False
                for neighbor2 in getNeighbors(variable):
                    if neighbor2 != neighbor:
                        queue.append(neighbor2)
    return True

#returns the domain of each empty cell in the grid
def getCellDomain(grid):
    domain = {}
    for row in range(5):
        for column in range(5):
            if grid[row][column] == '-':
                available_values = getAvailableLetters(grid)
                for row_inc, column_inc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    row_temp, column_temp = row + row_inc, column + column_inc
                    if 0 <= row_temp < 5 and 0 <= column_temp < 5 and grid[row_temp][column_temp] != '-':
                        available_values -= {grid[row_temp][column_temp]}
                if len(available_values) == 0:
                    return {}
                domain[(row, column)] = available_values
    if not ac3(domain):
        return {}
    return domain

#returns the neighbors of a given variable
def getNeighbors(variable):
    neighbors = []
    row, column = variable
    for row_inc, column_inc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        row_temp, column_temp = row + row_inc, column + column_inc
        if 0 <= row_temp < 5 and 0 <= column_temp < 5 and grid[row_temp][column_temp] == '-':
            neighbors.append((row_temp, column_temp))
    return neighbors

#removes values from the domain of variable1 that are inconsistent with the domain of variable2
#returns True if any values are removed, and False otherwise
def revise(domain, variable1, variable2):
    revised = False
    for value in domain[variable1]:
        if not any(value2 != value for value2 in domain[variable2]):
            domain[variable1].remove(value)
            revised = True
    return revised


grid = [['-', '-', '-', '-', 'Y'],
        ['R', 'A', '-', '-', '-'],
        ['-', '-', '-', '-', '-'],
        ['-', 'E', '-', '-', '-'],
        ['-', '-', '-', '-', 'K']]

domain = getCellDomain(grid)
available = getAvailableLetters(grid)
if snake(grid, available, domain):
    for row in grid:
        print(" ".join(row))
else:
    print("No solution found")
