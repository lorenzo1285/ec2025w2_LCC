import random



def compute_penalty(individual, maxsat_instance):
    total_clauses = len(maxsat_instance.clauses)
    satisfied = maxsat_instance.compute_fitness(individual)
    return total_clauses - satisfied

class MaxSAT:
    """
    A class to handle MAX-SAT problems, including parsing WCNF files
    and integrating solvers.
    """

    def __init__(self):
        """
        Initializes an empty MaxSAT problem.
        """
        self.num_variables = 0
        self.num_clauses = 0
        self.clauses = []

    def load_wcnf(self, file_path):
        """
        Parses a WCNF file and extracts the clauses and metadata.
        
        Parameters:
            file_path (str): Path to the WCNF file.
        """
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("c"):  # Ignore comments
                    continue
                if line.startswith("p"):  # Problem line
                    parts = line.split()
                    self.num_variables = int(parts[2])
                    self.num_clauses = int(parts[3])
                else:
                    # Store clause (ignoring the last '0' in each line)
                    literals = list(map(int, line.split()[1:-1]))
                    self.clauses.append(literals)

    def display_info(self):
        """
        Prints the details of the loaded MaxSAT problem.
        """
        print(f"📌 MaxSAT Instance Loaded")
        print(f"   - Variables: {self.num_variables}")
        print(f"   - Clauses: {self.num_clauses}")
        print("   - Sample Clauses:")
        for i, clause in enumerate(self.clauses[:5]):  # Show first 5 clauses
            print(f"     Clause {i+1}: {clause}")



    def is_clause_satisfied(self, clause, assignment):
        """
        Checks if a given clause is satisfied by a given assignment.

        Parameters:
            clause (list): A list of literals representing a clause.
            assignment (str): A bitstring (e.g., "1010") representing variable assignments.

        Returns:
            bool: True if the clause is satisfied, False otherwise.
        """
        for literal in clause:
            var_index = abs(literal) - 1  # Convert 1-based index to 0-based
            
            # Check if the assignment is too short
            if var_index >= len(assignment):
                print(f"Warning: Assignment '{assignment}' is too short for clause {clause}")
                return False  # Consider the clause unsatisfied
            
            var_value = int(assignment[var_index])
            
            if (literal > 0 and var_value == 1) or (literal < 0 and var_value == 0):
                return True  # Clause is satisfied

        return False  # Clause is not satisfied
    
    def evaluate_individual_against_clauses(self, clauses, assignment):
        """
        Evaluates each clause against the assignment (bitstring).
        For each clause, prints the clause, the relevant assignment bits, and satisfaction.
        """
        results = []
        for idx, clause in enumerate(clauses):
            satisfied = 0
            relevant_bits = []
            for literal in clause:
                var_index = abs(literal) - 1  # Variable indices start at 1
                if var_index >= len(assignment):
                    relevant_bits.append('X')  # Out of bounds (should not happen in correct usage)
                    continue
                var_value = int(assignment[var_index])
                relevant_bits.append(str(var_value))
                if (literal > 0 and var_value == 1) or (literal < 0 and var_value == 0):
                    satisfied = 1

            result = {
                "clause": " ".join(str(l) for l in clause),
                "assignment": "".join(relevant_bits),
                "satisfied": satisfied
            }
            results.append(result)

        
        return results


    def compute_fitness(self, assignment):
        """
        Computes the fitness score for a given assignment.
        
        Parameters:
            assignment (str): A bitstring representing a variable assignment.
        
        Returns:
            int: Number of satisfied clauses (fitness score).
        """
        satisfied_count = sum(1 for clause in self.clauses if self.is_clause_satisfied(clause, assignment))
        return satisfied_count
    
    def initialize_population_heuristic(self, size):
        """
        Generates a population of pseudo-random assignments where each clause
        is more likely to be satisfied at least once.

        Parameters:
            size (int): The number of individuals in the population.

        Returns:
            list: A list of bitstrings where solutions are more likely to be partially feasible.
        """
        population = []
        
        for _ in range(size):
            assignment = ["0"] * self.num_variables  # Start with all zeros
            covered_clauses = set()
            
            # Prioritize satisfying each clause at least once
            for clause in self.clauses:
                if any(abs(lit) - 1 in covered_clauses for lit in clause):
                    continue  # Skip if clause is already covered

                # Select a random literal from the clause to satisfy
                chosen_literal = random.choice(clause)
                var_index = abs(chosen_literal) - 1  # Convert to 0-based index
                assignment[var_index] = "1" if chosen_literal > 0 else "0"
                covered_clauses.add(var_index)
            
            # Convert assignment list to bitstring
            population.append("".join(assignment))
        
        return population
