
grid = [['-', '-', '-', '-', 'Y'],
        ['R', 'A', '-', '-', '-'],
        ['-', '-', '-', '-', '-'],
        ['-', 'E', '-', '-', '-'],
        ['-', '-', '-', '-', 'K']]

#function checks whether a given letter can be placed in a given cell of the grid, 
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


def getAvailableLetters(grid): # returns the set of available letters
    unavailable = set()
    for row in grid:
        for cell in row:
            if cell != '-':
                unavailable.add(cell)
    available = set(chr(ord('A') + i) for i in range(25)) - unavailable
    return available

def getCellDomain(grid): # returns the domain of each cell
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
    return domain



domain = getCellDomain(grid)
available = getAvailableLetters(grid)
if snake(grid, available, domain):
    for row in grid:
        print(" ".join(row))
else:
    print("No solution available")
