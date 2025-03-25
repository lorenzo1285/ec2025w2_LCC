from maxsat import MaxSAT
from IBGA import IBGA
import time
import argparse
import pandas as pd

# ✅ Argument parser for the WCNF file path
parser = argparse.ArgumentParser(description="Run MAXSAT evolutionary algorithm.")
parser.add_argument('--path', type=str, required=True, help='Path to the .wcnf file')
args = parser.parse_args()
maxsat = MaxSAT()
maxsat.load_wcnf(args.path)
maxsat.display_info()

print(f"\n✅ Running sample with {maxsat.num_variables} variables and {maxsat.num_clauses} valid clauses")

# ✅ Evolutionary Algorithm Parameters (editable)
population_size = 38
repetitions = 1           # ✅ Number of repetitions (Exercise 3)
time_budget = 10          # ✅ Time budget per repetition (seconds)
max_generations = 20      # ✅ Generations per repetition
crossover_prob = 0.88
mutation_prob = 0.04
elite_size = 4
use_lagrangian = False     # ✅ Optional: switch between classic / lagrangian ranking



def main():

    start_time = time.time() # ✅ Start time for the algorithm

    # ✅ Repeat the evolutionary process and output 't nsat xbest'
    for rep in range(repetitions):
        # ✅ Initialize random population for each repetition (as required)
        initial_population = maxsat.initialize_population_heuristic(population_size)
        print(f"\n✅ Repetition {rep + 1}: Initial Population Example: {initial_population[0]}")

        # ✅ Initialize IBGA solver
        ibga = IBGA(maxsat)

        # ✅ Run the evolutionary algorithm with time budget
        best_individual = ibga.run_bga(
            initial_population=initial_population,
            max_generations=max_generations,
            crossover_prob=crossover_prob,
            mutation_prob=mutation_prob,
            elite_size=elite_size,
            time_budget=time_budget,
            use_lagrangian=use_lagrangian
        )

        # ✅ Compute fitness (number of satisfied clauses)
        nsat = maxsat.compute_fitness(best_individual)

    results = maxsat.evaluate_individual_against_clauses(maxsat.clauses, best_individual)


    results_df = pd.DataFrame(results)
    end_time = time.time()  # ✅ End timing
    execution_time = end_time - start_time  # ✅ Compute execution time (t)
    print(results_df)

    pct = results_df['satisfied'].mean() * 100
    print(f"Percentage of Satisfied Clauses: {pct:.2f}%")
    print(f"Best Individual (xbest): {best_individual}")
    print(f"Number of Satisfied Clauses (nsat): {nsat}")
    print(f"Total Execution Time (t): {execution_time:.4f} seconds")  # ✅ Print execution time
    
if __name__ == '__main__':
    main()