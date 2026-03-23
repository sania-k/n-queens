from random import randrange

class Problem:
    '''
    Problem

    Attributes
    ---
    n: int
        Represents the size of the board (n x n)

    queen_pos: n size int array
        Lists the location of every queen on the board. 
        queen_pos[i] gives the row index of the queen in column i

    conflicts: int
        Count of pairs of queens attacking each other
    '''
    def __init__(self, n=8):
        self.n = n
        self.queen_pos = [0] * n
        self.conflicts = 0

        self.random_assign()
        self.calculate_conflicts()
        
    def random_assign(self):
        '''
        Randomly puts queens on the board such that there is one queen per column
        '''
        for i in range(self.n):
            self.queen_pos[i] = randrange(0, self.n)

    def print_board(self):
        '''
        Prints board for debugging
        '''        
        board = [[0]*self.n for _ in range(self.n)]

        for col,row in enumerate(self.queen_pos):
            board[row][col] = 1

        for r in board:
            print(*r)

        print("Queen Positions: ", self.queen_pos)
        print("Conflicts: ",self.conflicts)

    def calculate_conflicts(self):
        '''
        Calculates the conflicts between queens on the board
        '''
        self.conflicts = 0

        # Track queens per line
        row_counts = {} # This direction: -
        pos_diag_counts = {}   # This direction: /
        neg_diag_counts = {}   # This direction: \

        # Iterates through queen positions
        for col in range(self.n):
            row = self.queen_pos[col]

            # Counting queens in each line
            row_counts[row] = row_counts.get(row, 0) + 1
            pos_diag_counts[row + col] = pos_diag_counts.get(row + col, 0) + 1
            neg_diag_counts[row - col] = neg_diag_counts.get(row - col, 0) + 1

        # If more than one queen, count the pairs and add them to conflict count
        for count in row_counts.values():
            if count > 1:
                self.conflicts += count * (count - 1) // 2

        for count in pos_diag_counts.values():
            if count > 1:
                self.conflicts += count * (count - 1) // 2

        for count in neg_diag_counts.values():
            if count > 1:
                self.conflicts += count * (count - 1) // 2                       

    def get_best_neighbor(self):
        '''
        Get the best neighbor (one with the lowest conflict count) of the current state

        Returns the amount of conflicts and the position of each queen in that best state
        '''
        # Track the best position and conflict count
        best_queen_pos = self.queen_pos.copy()
        best_conflicts = self.conflicts

        original_conflicts = self.conflicts

        # Iterate through each possible neighbor state of the board
        for col in range(self.n):
            # Keep track of the original configuration before changing it
            original_row = self.queen_pos[col]

            for row in range(self.n):
                if row == original_row:
                    continue

                # create neighbor and calculate conflicts
                self.queen_pos[col] = row
                self.calculate_conflicts()

                # If this neighbor is better than the current minimum, replace it
                if self.conflicts < best_conflicts:
                    best_conflicts = self.conflicts
                    best_queen_pos = self.queen_pos.copy()

            # restore original position
            self.queen_pos[col] = original_row

        # restore original conflict count
        self.conflicts = original_conflicts

        return best_queen_pos, best_conflicts

    

def hillClimbing(problem, use_sideways_move=False, use_random_restart=False): 
    '''
    Runs the hill climbing algorithm on an n-queens problem in order to find the 
    best conflicuration (least conflicts).

    Returns the solved problem and the number of steps the solution took

    :param problem: Problem object
    :param use_sideways_move: bool
        Determines if sideways moves are allowed
    :param use_random_restart: bool
        Determines if random restards are allowed
    '''   
    steps = 0

    while True:
        # If 0 conflicts, the problem has been solved
        if problem.conflicts == 0:
            print("solution found")
            return problem, steps        
        
        # Get the best state with the least num of conflicts
        best_queen_pos, best_conflicts = problem.get_best_neighbor()

        # If the next best state is the same or worse than the current one,
        # return the local min
        if best_conflicts >= problem.conflicts:
            print("local min found")
            return problem, steps # Return found minimum
        
        # Move the board to the best next move
        problem.queen_pos = best_queen_pos
        problem.conflicts = best_conflicts
        steps += 1


if __name__ == "__main__":
    problem = Problem(10)
    problem.print_board()

    print("solving...")

    solution, steps = hillClimbing(problem)
    solution.print_board()
    print("Steps: ", steps)