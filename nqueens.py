import sys
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

    def print_board(self, indent=""):
        board = [[0]*self.n for _ in range(self.n)]

        for col, row in enumerate(self.queen_pos):
            board[row][col] = 1

        for r in board:
            print(indent + " ".join(map(str, r)))

        print(indent + f"Queen Positions: {self.queen_pos}")
        print(indent + f"Conflicts: {self.conflicts}")

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

    def get_best_neighbor(self, allow_sideways=False):
        '''
        Get the best neighbor (one with the lowest conflict count) of the current state.
        Can allow for sideways moves (meaning return a best neighbor with the same number
        of conflicts)

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

                # Accept equal conflicts if sideways moves are allowed
                elif allow_sideways and self.conflicts == best_conflicts:
                    best_queen_pos = self.queen_pos.copy()                  
 
            # restore original position
            self.queen_pos[col] = original_row

        # restore original conflict count
        self.conflicts = original_conflicts

        return best_queen_pos, best_conflicts


def hill_climbing(problem, use_sideways_moves=False): 
    '''
    Runs the hill climbing algorithm on an n-queens problem in order to find the 
    best configuration (least conflicts).

    Returns (success bool, the number of steps that result took)

    :param problem: Problem object
    :param use_sideways_moves: bool
        Determines if sideways moves are allowed
    '''   
    # Counters for solution statistics
    steps = 0
    
    MAX_SIDEWAYS = n * 5   # limit on consecutive sideways moves
    sideways_streak = 0     # track consecutive sideways moves

    while True:
        # If 0 conflicts, the problem has been solved
        if problem.conflicts == 0:
            return True, steps  # return (success, steps)
        
        # Get the best state with the least num of conflicts
        best_queen_pos, best_conflicts = problem.get_best_neighbor(allow_sideways=use_sideways_moves)  
        
        # Local minimum has been found, return failure
        if best_conflicts > problem.conflicts:
            return False, steps 

        # Local plateau/shoulder has been found
        if best_conflicts == problem.conflicts:
            # return failure if sideways moves aren't allowed
            if not use_sideways_moves:
                return False, steps
            
            # Make a sideways move
            sideways_streak += 1

            # If too many sideways moves have been made,  return failure to prevent infinite loop
            if sideways_streak > MAX_SIDEWAYS:
                return False, steps
        else:
            sideways_streak = 0  # reset streak on improvement
        
        # Move the board to the next move
        problem.queen_pos = best_queen_pos
        problem.conflicts = best_conflicts
        steps += 1


def hill_climbing_random_restart(n=8, use_sideways_moves=False):
    '''
    Hill climbing wrapper function. 
    Repeatedly restarts hill climbing from a random state until a solution is found.

    Returns (the total steps taken, number of restarts needed)

    :param problem: Problem object
    :param use_sideways_moves: bool
        Determines if sideways moves are allowed
    '''
    restarts = 0
    total_steps = 0

    # Loops until a solution is found
    while True:
        problem = Problem(n)
        success, steps = hill_climbing(problem, use_sideways_moves=use_sideways_moves)
        total_steps += steps

        if success:
            return total_steps, restarts

        restarts += 1


def n_queens_stats(n=8, runs=100, use_sideways_moves=False):
    '''
    Creates n_queens problems and runs hill climbing on them a given number of times.

    Returns dictionary object {success_rate, failure_rate, avg_steps_success, avg_steps_failure}

    :param n: int
        Size on the nqueen boards
    :param runs: int
        The number of times nqueens will run to determine average rates
    :param use_sideways_moves: bool
    '''
    successes, failures = 0, 0
    success_steps, failure_steps = [], []

    # Creating problems and running hill climbing on them to collect numbers
    for _ in range(runs):
        problem = Problem(n)
        success, steps = hill_climbing(problem, use_sideways_moves=use_sideways_moves)
        if success:
            successes += 1
            success_steps.append(steps)
        else:
            failures += 1
            failure_steps.append(steps)

    # Calculating rates
    avg_success = sum(success_steps) / len(success_steps) if success_steps else 0
    avg_failure = sum(failure_steps) / len(failure_steps) if failure_steps else 0

    return {
        "success_rate": successes / runs * 100,
        "failure_rate": failures / runs * 100,
        "avg_steps_success": avg_success,
        "avg_steps_failure": avg_failure,
    }


def print_hill_climbing_sequence(n=8, use_sideways_moves=False):
    ''' 
    Runs hill climbing algorithm once and prints out details (conflict count, queen positions, boards). 
    
    :param n: int Size on the nqueen boards 
    :param runs: int 
        The number of times nqueens will run to determine average rates 
    :param use_sideways_moves: bool 
    '''
    problem = Problem(n)

    print(f"\tInitial state (conflicts={problem.conflicts}):")
    problem.print_board("\t\t")

    steps = 0
    sideways_streak = 0
    MAX_SIDEWAYS = n * 5

    success = False

    # Track sequence of positions + conflicts
    sequence = [(problem.queen_pos.copy(), problem.conflicts)]

    # Runs hill climbing until success or failure
    while True:
        if problem.conflicts == 0:
            print(f"\n\tSolution found in {steps} steps!")
            success = True
            break

        # Finding best neighbor
        best_queen_pos, best_conflicts = problem.get_best_neighbor(
            allow_sideways=use_sideways_moves
        )

        # Checking for plateaus/shoulders and moving sideways/returning failure if found
        if best_conflicts > problem.conflicts:
            print(f"\n\tLocal minimum at step {steps} (conflicts={problem.conflicts})")
            break

        if best_conflicts == problem.conflicts:
            if not use_sideways_moves:
                print(f"\n\tLocal minimum at step {steps} (conflicts={problem.conflicts})")
                break
            sideways_streak += 1
            if sideways_streak > MAX_SIDEWAYS:
                print(f"\n\tSideways limit reached at step {steps}")
                break
        else:
            sideways_streak = 0

        # Move to next state
        problem.queen_pos = best_queen_pos
        problem.conflicts = best_conflicts
        steps += 1

        # Store only positions + conflicts
        sequence.append((problem.queen_pos.copy(), problem.conflicts))

    # Once hill climbing is done, print out the details of the solution path
    print("\n\t--- Step Sequence ---")
    for i, (pos, conf) in enumerate(sequence):
        print(f"\tStep {i}: {pos} (conflicts={conf})")

    # Print the final board
    print("\n\tFinal configuration:")
    temp = Problem(n)
    temp.queen_pos = sequence[-1][0]
    temp.calculate_conflicts()
    temp.print_board("\t\t")


class DualOutput:
    """Write to both file and terminal simultaneously"""
    def __init__(self, file, terminal):
        self.terminal = terminal
        self.file = file
    
    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)
    
    def flush(self):
        self.terminal.flush()
        self.file.flush()


def run_all(n):
    '''
    Runs and prints all statistics required by the assignment
    '''
    print(f"TESTING {n}-QUEENS")
    
    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("A. HILL CLIMBING SEARCH")
    print("="*60)

    for runs in [50, 100, 200, 500, 1000, 1500]:
        stats = n_queens_stats(n=n, runs=runs, use_sideways_moves=False)
        print(f"\n  Runs = {runs}")
        print(f"    Success rate: {stats['success_rate']:.1f}%   Failure rate: {stats['failure_rate']:.1f}%")
        print(f"    Avg steps (success): {stats['avg_steps_success']:.2f}")
        print(f"    Avg steps (failure): {stats['avg_steps_failure']:.2f}")

    print("\n  --- Search sequences from four random initial configurations ---")
    for i in range(1, 5):
        print(f"\n  Sequence {i}:")
        print_hill_climbing_sequence(n=n, use_sideways_moves=False)

    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("B. HILL CLIMBING WITH SIDEWAYS MOVE")
    print("="*60)

    for runs in [50, 100, 200, 500, 1000, 1500]:
        stats = n_queens_stats(n=n, runs=runs, use_sideways_moves=True)
        print(f"\n  Runs = {runs}")
        print(f"    Success rate: {stats['success_rate']:.1f}%   Failure rate: {stats['failure_rate']:.1f}%")
        print(f"    Avg steps (success): {stats['avg_steps_success']:.2f}")
        print(f"    Avg steps (failure): {stats['avg_steps_failure']:.2f}")

    print("\n  --- Search sequences from four random initial configurations ---")
    for i in range(1, 5):
        print(f"\n  Sequence {i}:")
        print_hill_climbing_sequence(n=n, use_sideways_moves=True)

    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("C. RANDOM-RESTART HILL CLIMBING")
    print("="*60)

    RESTART_TRIALS = 100
    print(f"\n  (Averaged over {RESTART_TRIALS} trials)")

    all_restarts, all_steps = [], []
    for _ in range(RESTART_TRIALS):
        total_steps, restarts = hill_climbing_random_restart(n=n, use_sideways_moves=False)
        all_restarts.append(restarts)
        all_steps.append(total_steps)
    print(f"\n  Without sideways move:")
    print(f"    Avg restarts: {sum(all_restarts)/RESTART_TRIALS:.2f}")
    print(f"    Avg total steps: {sum(all_steps)/RESTART_TRIALS:.2f}")

    all_restarts, all_steps = [], []
    for _ in range(RESTART_TRIALS):
        total_steps, restarts = hill_climbing_random_restart(n=n, use_sideways_moves=True)
        all_restarts.append(restarts)
        all_steps.append(total_steps)
    print(f"\n  With sideways move:")
    print(f"    Avg restarts: {sum(all_restarts)/RESTART_TRIALS:.2f}")
    print(f"    Avg total steps: {sum(all_steps)/RESTART_TRIALS:.2f}")


if __name__ == "__main__":
    # User input for n
    try:
        n = int(input("Enter the value of n (default 8): ").strip() or "8")
        if n < 1:
            raise ValueError
    except ValueError:
        print("Invalid input — using n=8.")
        n = 8

    output_file = f"{n}queens_results.txt"
    original_stdout = sys.stdout

    # Run tests with output to both console and file
    # Use UTF-8 encoding to handle special characters on Windows
    with open(output_file, 'w', encoding='utf-8') as f:
        sys.stdout = DualOutput(f, original_stdout)
        run_all(n)
        sys.stdout = original_stdout

    print(f"\nResults saved to {output_file}")