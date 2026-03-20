from random import randrange
from math import floor, ceil

class Problem:
    '''
    Problem

    Attributes
    ---
    n: int
        Represents the size of the board (n x n)

    board: nxn 2d int array
        Represents the board, where 0 are the empty spots and 1 are the queens

    queen_pos: n size int array
        Lists the location of every queen on the board. 
        queen_pos[i] gives the row index of the queen in column i
    '''
    def __init__(self, n=8):
        self.n = n
        self.board = [[0 for _ in range(n)] for _ in range(n)]
        self.queen_pos = [0] * n
        self.conflicts = 0

        self.random_assign()

        print("queen_pos: ", self.queen_pos)
        self.calculate_conflicts()
        
    def random_assign(self):
        for i in range(self.n):
            self.queen_pos[i] = randrange(0, self.n)

            self.board[self.queen_pos[i]][i] = 1

    def print_board(self):
        for i in range(self.n):
            print(*self.board[i])

        print("Conflicts: ",self.conflicts)

    def calculate_conflicts(self):
        self.conflicts = 0

        row_counts = {}
        pos_diag = {}   
        neg_diag = {}  

        for col in range(self.n):
            row = self.queen_pos[col]

            row_counts[row] = row_counts.get(row, 0) + 1
            pos_diag[row + col] = pos_diag.get(row + col, 0) + 1
            neg_diag[row - col] = neg_diag.get(row - col, 0) + 1

        # count conflicts
        for count in row_counts.values():
            if count > 1:
                self.conflicts += count * (count - 1) // 2

        for count in pos_diag.values():
            if count > 1:
                self.conflicts += count * (count - 1) // 2

        for count in neg_diag.values():
            if count > 1:
                self.conflicts += count * (count - 1) // 2                       

    def getNeighbor(self):
        bestNeighbor = problem.board.copy()
        bestState = problem.queen_pos.copy()

    

def hillClimbing(problem, useSidewaysMove=False, useRandomRestart=False):
    current = problem
    
    while True:
        neighbor = None


if __name__ == "__main__":
    problem = Problem(7)
    problem.print_board()