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

    def get_best_neighbor(self, allow_sideways=False):  # ADDED: allow_sideways param
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
                # ADDED: also accept equal conflicts if sideways moves are allowed
                if self.conflicts < best_conflicts or (allow_sideways and self.conflicts == best_conflicts):
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

    Returns success bool and the number of steps the solution took

    :param problem: Problem object
    :param use_sideways_move: bool
        Determines if sideways moves are allowed
    :param use_random_restart: bool
        Determines if random restards are allowed
    '''   
    steps = 0
    sideways_streak = 0  # ADDED: track consecutive sideways moves
    MAX_SIDEWAYS = 100   # ADDED: limit on consecutive sideways moves

    while True:
        # If 0 conflicts, the problem has been solved
        if problem.conflicts == 0:
            return True, steps  # CHANGED: return (success, steps)
        
        # Get the best state with the least num of conflicts
        best_queen_pos, best_conflicts = problem.get_best_neighbor(allow_sideways=use_sideways_move)  # CHANGED: pass sideways flag

        # If the next best state is worse, stop
        if best_conflicts > problem.conflicts:
            return False, steps  # CHANGED: return (success, steps)

        # ADDED: handle sideways moves (equal conflicts)
        if best_conflicts == problem.conflicts:
            if not use_sideways_move:
                return False, steps
            sideways_streak += 1
            if sideways_streak > MAX_SIDEWAYS:
                return False, steps
        else:
            sideways_streak = 0  # reset streak on improvement
        
        # Move the board to the best next move
        problem.queen_pos = best_queen_pos
        problem.conflicts = best_conflicts
        steps += 1


# ADDED: random restart wrapper
def randomRestartHillClimbing(n=8, use_sideways_move=False):
    '''
    Repeatedly restarts hill climbing from a random state until a solution is found.

    Returns the total steps taken and number of restarts needed.
    '''
    restarts = 0
    total_steps = 0

    while True:
        problem = Problem(n)
        success, steps = hillClimbing(problem, use_sideways_move=use_sideways_move)
        total_steps += steps

        if success:
            return total_steps, restarts

        restarts += 1


# ADDED: run stats for hill climbing over multiple trials
def runHillClimbingStats(n=8, runs=100, use_sideways_move=False):
    '''
    Runs hill climbing a given number of times and reports success/failure rates
    and average steps.
    '''
    successes, failures = 0, 0
    success_steps, failure_steps = [], []

    for _ in range(runs):
        problem = Problem(n)
        success, steps = hillClimbing(problem, use_sideways_move=use_sideways_move)
        if success:
            successes += 1
            success_steps.append(steps)
        else:
            failures += 1
            failure_steps.append(steps)

    avg_success = sum(success_steps) / len(success_steps) if success_steps else 0
    avg_failure = sum(failure_steps) / len(failure_steps) if failure_steps else 0

    return {
        "success_rate": successes / runs * 100,
        "failure_rate": failures / runs * 100,
        "avg_steps_success": avg_success,
        "avg_steps_failure": avg_failure,
    }


# ADDED: print the conflict sequence for a single run (for search sequence reporting)
def printSearchSequence(n=8, use_sideways_move=False):
    '''
    Runs hill climbing once and prints the conflict count at each step.
    '''
    problem = Problem(n)
    print(f"  Initial positions: {problem.queen_pos}  (conflicts={problem.conflicts})")

    steps = 0
    sideways_streak = 0
    MAX_SIDEWAYS = 100
    sequence = [problem.conflicts]

    while True:
        if problem.conflicts == 0:
            print(f"  Solution found in {steps} steps!")
            break

        best_queen_pos, best_conflicts = problem.get_best_neighbor(allow_sideways=use_sideways_move)

        if best_conflicts > problem.conflicts:
            print(f"  Local minimum at step {steps} (conflicts={problem.conflicts})")
            break

        if best_conflicts == problem.conflicts:
            if not use_sideways_move:
                print(f"  Local minimum at step {steps} (conflicts={problem.conflicts})")
                break
            sideways_streak += 1
            if sideways_streak > MAX_SIDEWAYS:
                print(f"  Sideways limit reached at step {steps}")
                break
        else:
            sideways_streak = 0

        problem.queen_pos = best_queen_pos
        problem.conflicts = best_conflicts
        steps += 1
        sequence.append(problem.conflicts)

    print(f"  Conflict sequence: {sequence}\n")


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
    # All stats reported for 8-queens as required by the instructions
    N = 8

    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("A. HILL CLIMBING SEARCH")
    print("="*60)

    for runs in [50, 100, 200, 500, 1000, 1500]:
        stats = runHillClimbingStats(n=N, runs=runs, use_sideways_move=False)
        print(f"\n  Runs = {runs}")
        print(f"    Success rate: {stats['success_rate']:.1f}%   Failure rate: {stats['failure_rate']:.1f}%")
        print(f"    Avg steps (success): {stats['avg_steps_success']:.2f}")
        print(f"    Avg steps (failure): {stats['avg_steps_failure']:.2f}")

    print("\n  --- Search sequences from four random initial configurations ---")
    for i in range(1, 5):
        print(f"\n  Sequence {i}:")
        printSearchSequence(n=N, use_sideways_move=False)

    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("B. HILL CLIMBING WITH SIDEWAYS MOVE")
    print("="*60)

    for runs in [50, 100, 200, 500, 1000, 1500]:
        stats = runHillClimbingStats(n=N, runs=runs, use_sideways_move=True)
        print(f"\n  Runs = {runs}")
        print(f"    Success rate: {stats['success_rate']:.1f}%   Failure rate: {stats['failure_rate']:.1f}%")
        print(f"    Avg steps (success): {stats['avg_steps_success']:.2f}")
        print(f"    Avg steps (failure): {stats['avg_steps_failure']:.2f}")

    print("\n  --- Search sequences from four random initial configurations ---")
    for i in range(1, 5):
        print(f"\n  Sequence {i}:")
        printSearchSequence(n=N, use_sideways_move=True)

    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("C. RANDOM-RESTART HILL CLIMBING")
    print("="*60)

    RESTART_TRIALS = 100
    print(f"\n  (Averaged over {RESTART_TRIALS} trials)")

    all_restarts, all_steps = [], []
    for _ in range(RESTART_TRIALS):
        total_steps, restarts = randomRestartHillClimbing(n=N, use_sideways_move=False)
        all_restarts.append(restarts)
        all_steps.append(total_steps)
    print(f"\n  Without sideways move:")
    print(f"    Avg restarts: {sum(all_restarts)/RESTART_TRIALS:.2f}")
    print(f"    Avg total steps: {sum(all_steps)/RESTART_TRIALS:.2f}")

    all_restarts, all_steps = [], []
    for _ in range(RESTART_TRIALS):
        total_steps, restarts = randomRestartHillClimbing(n=N, use_sideways_move=True)
        all_restarts.append(restarts)
        all_steps.append(total_steps)
    print(f"\n  With sideways move:")
    print(f"    Avg restarts: {sum(all_restarts)/RESTART_TRIALS:.2f}")
    print(f"    Avg total steps: {sum(all_steps)/RESTART_TRIALS:.2f}")

    # -------------------------------------------------------------------------
    # Run with user-specified n if different from 8
    if n != N:
        print(f"\n{'='*60}")
        print(f"Running a quick demo with your n={n}...")
        print(f"{'='*60}")
        problem = Problem(n)
        problem.print_board()
        success, steps = hillClimbing(problem)
        print("Result:", "Solved" if success else "Failed", "| Steps:", steps)


if __name__ == "__main__":
    # User input for n (5-point rubric item)
    try:
        n = int(input("Enter the value of n (default 8): ").strip() or "8")
        if n < 1:
            raise ValueError
    except ValueError:
        print("Invalid input — using n=8.")
        n = 8

    output_file = "results.txt"
    original_stdout = sys.stdout

    # Run tests with output to both console and file
    # Use UTF-8 encoding to handle special characters on Windows
    with open(output_file, 'w', encoding='utf-8') as f:
        sys.stdout = DualOutput(f, original_stdout)
        run_all(n)
        sys.stdout = original_stdout

    print(f"\nResults saved to {output_file}")