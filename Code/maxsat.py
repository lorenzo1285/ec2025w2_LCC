import random



def compute_penalty(individual, maxsat_instance):
    total_clauses = len(maxsat_instance.clauses)
    satisfied = maxsat_instance.compute_fitness(individual)
    return total_clauses - satisfied

''' Exercise 1: Clause Class (parsing and evaluating of individual clauses) '''

class Clause:
    def __init__(self, input_line, weighted=False):
        self.weighted = weighted
        self.weight, self.literals = self.parse(input_line)
        #print(f"Clause created with literals: {self.literals}")

    def parse(self, input_line):
        parts = input_line.strip().split()
        weight = float(parts[0])  # Extract the weight separately
        literals = [int(x) for x in parts[1:-1]]  # Correctly ignore first element in weighted case
        return weight, literals

    def evaluate(self, assignment):
        assignment_dict = {i + 1: val == '1' for i, val in enumerate(assignment)}

        for lit in self.literals:
            var_index = abs(lit)
            value = assignment_dict[var_index]

            if (lit > 0 and value) or (lit < 0 and not value):
                return 1

        return 0

''' Exercise 2: WDIMACS Class ( Import and Evaluate File )'''

class WDIMACS:
    def __init__(self, filepath, weighted=False):
        self.clauses = []
        self.num_vars = 0
        self.num_clauses = 0
        self.weighted = weighted
        self.parse(filepath)

    def parse(self, filepath):
        #print("Opening file:", filepath)
        with open(filepath, "r") as file:
            clause_count = 0
            
            for line in file:
                #print("Reading line:", line.strip())  # clearly see each line read
                if line.startswith("c"):
                    continue
                elif line.startswith("p"):
                    parts = line.strip().split()
                    self.num_vars = int(parts[2])
                    self.num_clauses = int(parts[3])
                    #print(f"Parsed num_vars: {self.num_vars}, num_clauses: {self.num_clauses}")
                else:
                    clause = Clause(line, weighted=self.weighted)
                    #print("Parsed clause literals:", clause.literals)
                    self.clauses.append(clause)
                    clause_count += 1 #counter for limiting number of clauses

    def evaluate(self, assignment):
        return sum(clause.evaluate(assignment) for clause in self.clauses)
    

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
