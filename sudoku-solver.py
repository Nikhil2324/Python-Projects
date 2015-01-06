def mapping(row, col):
    return [a+b for a in row for b in col]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = mapping(rows, cols)
unitlist = ([mapping(rows, c) for c in cols] + [mapping(r, cols) for r in rows] + [mapping(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]) #cols, rows, boxes
units = dict((square, [u for u in unitlist if square in u]) for square in squares) #col, row, and box for each square
peers = dict((square, set(sum(units[square],[]))-set([square])) for square in squares) #unit for each square in unit of s, but not s

#possibilities is dict mapping each square to every value it can have
#possibilities[s] is specific square

def parse_grid(board):
    possibilities = dict((square, digits) for square in squares) #each square has every possible answer
    for square,digit in grid_values(board).items():
        if digit in digits and not assign(possibilities, square, digit): #assign if d is a digit
            return False
    return possibilities

def grid_values(board):
    values = [c for c in board if c in digits or c in '0.'] #list of squares values (0 or . for empty/unknown squares)
    return dict(zip(squares, values)) #map each square to its value

def assign(possibilities, square, digit):
    other_possibilities = possibilities[square].replace(digit, '') #other_values is every possiblity except digit
    if all(remove(possibilities, square, d2) for d2 in other_possibilities): #if those values are all invalid, found answer
        return possibilities
    else:
        return False

def remove(possibilities, square, digit): #eliminate d from values[s]
    if digit not in possibilities[square]:
        return possibilities #eliminated
    
    possibilities[square] = possibilities[square].replace(digit, '') #remove possibility from square
    
    if len(possibilities[square]) == 0:
        return False #removed last value, should be impossible
    
    elif len(possibilities[square]) == 1:
        d2 = possibilities[square]
        if not all(remove(possibilities, s2, d2) for s2 in peers[square]): #should be impossible
            return False
        
    for u in units[square]:
        dplaces = [square for square in u if digit in possibilities[square]] #valid places to put d
        if len(dplaces) == 0: #no valid places
            return False
        elif len(dplaces) == 1:
            if not assign(possibilities, dplaces[0], digit):
                return False
    return possibilities

def display(possibilities):
    width = 1+max(len(possibilities[square]) for square in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print ''.join(possibilities[r+c].center(width)+('|' if c in '36' else '') for c in cols)
        if r in 'CF':
            print line
    print

def search(possibilities):
    if possibilities is False:
        return False
    if all(len(possibilities[square]) == 1 for square in squares): #if each square has one solution, solved
        return possibilities
    n, square = min((len(possibilities[square]), square) for square in squares if len(possibilities[square]) > 1) #find square with min guesses not already solved
    return find_element(search(assign(possibilities.copy(), square, digit)) for digit in possibilities[square]) #for each square, reduce the possiblities, go through each square (depth first)

def find_element(values):
    for e in values:
        if e:
            return e
    return False

def solve(board):
    return search(parse_grid(board))

def convert(string): #dots to 0's, or vice versa
    newString = ""
    for i in string:
        if i == '0':
            newString += '.'

        elif i == '.':
            newString += '0'
        
        else:
            newString += i
    return newString

def main():
    ''' #test sudoku (apparently the hardest one created)
    hardestSudoku = '800000000003600000070090200050007000000045700000100030001000068008500010090000400'
    #display(grid_values(convert(hardestSudoku))) #converts 0's to .'s, shows unsolved sudoku
    if not solve(hardestSudoku):
        print "Not a valid sudoku"
    else:
        display(solve(hardestSudoku))
    '''

if __name__ == "__main__":
    main()
