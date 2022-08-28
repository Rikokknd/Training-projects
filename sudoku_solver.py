import numpy as np

def solve_sudoku(puzzle):
    """Accepts puzzle as 2D 9 x 9 array of integers with zero's as blank space.
    Returns solved puzzle as a 2D array 9 x 9. Can be used for easy puzzles."""

    def check(brd): # check if puzzle is solved correctly
        rows = np.array(brd)
        cols = rows.T
        squares = np.array([rows[x:x+3, y:y+3].flatten() for x in [0, 3, 6] for y in [0, 3, 6]])
        full = np.vstack((rows, cols, squares))
        for i in full:
            if len(np.unique(i)) != 9:
                return False
        return True

    def find_square_start(row, col):  
        """return coordinates of top left cell of the square that contains sent cell.
        with those coords we can get a 3 x 3 square from board"""
        while row not in [0, 3, 6]:
            row -= 1
        while col not in [0, 3, 6]:
            col -= 1
        return row, col

    board = np.array(puzzle)
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    iterations = 0
    while 0 in board: # running through board until there are no blank cells left

        if iterations > 1000:
            # usually it takes 50-200 iterations to solve a puzzle. If we didn't make it with 1000, then we accept defeat.
            return "Failed"
        
        for digit in digits: # taking digits one by one
            iterations += 1
            digit_coords = np.c_[np.nonzero(board == digit)] # getting a list of tuples (x, y) coordinates of every cell with this digit
            if digit_coords.size == 9: # there cannot be more than 9 of the same digits on board
                continue
            
            if digit_coords.size >= 1:
                temp_brd = board.copy() # making temp copy of board to do things in it

                for digit_row, digit_col in digit_coords:
                    temp_brd[digit_row, :] += 1 # incrementing a whole row with this digit
                    temp_brd[:, digit_col] += 1 # also every col
                    block_st_row, block_st_col = find_square_start(digit_row, digit_col) # finding top left cell of the square 
                    temp_brd[block_st_row:block_st_row + 3, block_st_col:block_st_col + 3] += 1 # incrementing whole square

                # only zero's at the moment are cells where it is possible to put a digit that we are processing right now
                empty_coords = np.c_[np.nonzero(temp_brd == 0)] # obtain coordinates of all those possible cells

                for digit_row, digit_col in empty_coords:
                    # if this cell is the only empty one in the row/col/square, then our digits goes here
                    block_st_row, block_st_col = find_square_start(digit_row, digit_col)
                    if (temp_brd[digit_row, :] == 0).sum() == 1: # if there is only one zero in the row
                        board[digit_row, digit_col] = digit # we change it to our digit in the main board
                    elif (temp_brd[:, digit_col] == 0).sum() == 1: # also col
                        board[digit_row, digit_col] = digit
                    elif (temp_brd[block_st_row:block_st_row + 3, block_st_col:block_st_col + 3] == 0).sum() == 1: # and square
                        board[digit_row, digit_col] = digit
                
    return board if check(board) else "Failed"


if __name__ == '__main__':
    puz =  [[5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    hard_puz = [[4, 0, 0, 0, 0, 0, 8, 0, 5],
                [0, 3, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 7, 0, 0, 0, 0, 0],
                [0, 2, 0, 0, 0, 0, 0, 6, 0],
                [0, 0, 0, 0, 8, 0, 4, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 6, 0, 3, 0, 7, 0],
                [5, 0, 0, 2, 0, 0, 0, 0, 0],
                [1, 0, 4, 0, 0, 0, 0, 0, 0]]

    solution = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                [6, 7, 2, 1, 9, 5, 3, 4, 8],
                [1, 9, 8, 3, 4, 2, 5, 6, 7],
                [8, 5, 9, 7, 6, 1, 4, 2, 3],
                [4, 2, 6, 8, 5, 3, 7, 9, 1],
                [7, 1, 3, 9, 2, 4, 8, 5, 6],
                [9, 6, 1, 5, 3, 7, 2, 8, 4],
                [2, 8, 7, 4, 1, 9, 6, 3, 5],
                [3, 4, 5, 2, 8, 6, 1, 7, 9]]

    print(solve_sudoku(puz))