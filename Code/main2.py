import time
import argparse
from maxsat import Clause, WDIMACS, MaxSAT

maxsat = MaxSAT()

# ✅ Evolutionary Algorithm Parameters (editable)
population_size = 38         
time_budget = 10         
max_generations = 20     
crossover_prob = 0.88
mutation_prob = 0.04
elite_size = 4
use_lagrangian = False 

def question_1(assignment, clause):
    c = Clause(clause)
    return c.evaluate(assignment)

def question_2(wdimacs, assignment):
    w = WDIMACS(wdimacs)
    return w.evaluate(assignment)

def question_3(wdimacs, time_budget, repetitions):

    start_time = time.time()
    w = WDIMACS(wdimacs)
    population = maxsat.initialize_population_heuristic(population_size)

    for i in range(0,repetitions):
        # print(f"\n Running Repetition {i+1} / {repetitions}")
        best_solution, best_fitness, generations = 
        print(f'{generations*population_size}\t{best_fitness}\t{best_solution}')
    return


def main():
    parser = argparse.ArgumentParser(description="MAXSAT Solver, Experiment Runner, and Results Visualiser")
    parser.add_argument("-question", required=True, help="Question number (1, 2, 3, 5, or 6)")
    parser.add_argument("-assignment", help="Assignment as a bitstring (e.g. '0000') for Q1/Q2")
    parser.add_argument("-clause", help="Clause description for Exercise 1")
    parser.add_argument("-wdimacs", help="Path to WDIMACS file for Exercises 2/3")
    parser.add_argument("-time_budget", help="Time budget in seconds for Exercise 3", default="1")
    parser.add_argument("-repetitions", help="Number of repetitions for Exercise 3", default="1")
    
    args = parser.parse_args()
    
    if args.question == "1":
        if args.assignment is None or args.clause is None:
            print("Error: For question 1, both -assignment and -clause must be provided.")
        print(question_1(args.assignment, args.clause))
    
    elif args.question == "2":
        if args.assignment is None or args.wdimacs is None:
            print("Error: For question 2, both -assignment and -wdimacs must be provided.")
            return
        print(question_2(args.wdimacs, args.assignment))
    
    elif args.question == "3":
        if args.wdimacs is None or args.time_budget is None or args.repetitions is None:
            print("Error: For question 3, -wdimacs, -time_budget, and -repetitions must be provided.")
            return
        question_3(args.wdimacs, args.time_budget, int(args.repetitions))

    else:
        print("Invalid question number.")

if __name__ == "__main__":
    main()