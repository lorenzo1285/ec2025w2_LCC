import random
import time
from tqdm import tqdm

class IBGA:
    def __init__(self, maxsat_instance):
        self.maxsat_instance = maxsat_instance

    def compute_penalty(self, individual):
        total_clauses = len(self.maxsat_instance.clauses)
        satisfied = self.maxsat_instance.compute_fitness(individual)
        return total_clauses - satisfied

    def stochastic_ranking_classic(self, population, generation, max_generations, p_init=0.65, p_final=0.35):
        """
        Classic stochastic ranking — sorts by constraints or fitness based on dynamic probability.
        """
        p = p_init - (p_init - p_final) * (generation / max_generations)
        num_individuals = len(population)

        def fitness(indiv):
            return self.maxsat_instance.compute_fitness(indiv)

        def penalty(indiv):
            return self.compute_penalty(indiv)

        sorted_population = population.copy()
        for _ in range(num_individuals):
            for i in range(num_individuals - 1):
                s1, s2 = sorted_population[i], sorted_population[i + 1]
                c1, c2 = penalty(s1), penalty(s2)
                f1, f2 = fitness(s1), fitness(s2)

                # With probability p, sort by penalty (constraint first)
                if (c1 > c2 and random.random() < p) or (c1 == c2 and f1 < f2):
                    sorted_population[i], sorted_population[i + 1] = s2, s1

        return sorted_population

    def stochastic_ranking_lagrangian(self, population, lambda_t, generation, max_generations, alpha=0.05, beta=0.2):
        """
        Stochastic ranking with Lagrangian relaxation and adaptive lambda.
        """
        population_size = len(population)
        violated_count = 0
        individuals = []

        for individual in population:
            fitness = self.maxsat_instance.compute_fitness(individual)
            penalty = self.compute_penalty(individual)
            lagrangian_score = fitness - lambda_t * penalty
            if penalty > 0:
                violated_count += 1
            individuals.append((individual, lagrangian_score))

        # Sort by lagrangian score descending
        individuals.sort(key=lambda x: x[1], reverse=True)

        # Adaptive lambda update
        violation_ratio = violated_count / population_size
        lambda_t *= (1 + alpha * (violation_ratio - beta))
        lambda_t = max(lambda_t, 1e-5)

        # Return sorted population and updated lambda
        sorted_population = [indiv[0] for indiv in individuals]
        return sorted_population, lambda_t

    def one_point_crossover(self, parent1, parent2, crossover_prob=0.8):
        """
        Performs one-point crossover between two binary string parents.
        """
        if random.random() < crossover_prob:
            point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        else:
            # No crossover, return copies
            return parent1, parent2

    def bit_flip_mutation(self, individual, mutation_prob=0.01):
        """
        Performs bit-flip mutation on a binary string individual.
        """
        mutated = ''
        for bit in individual:
            if random.random() < mutation_prob:
                mutated += '0' if bit == '1' else '1'
            else:
                mutated += bit
        return mutated
    
    def survivor_selection(self, parents, offspring, elite_size=2):
        """
        Survivor selection with elitism: keeps top elite_size from parents, fills the rest with offspring.
        """
        # Sort parents by fitness
        sorted_parents = sorted(parents, key=lambda ind: self.maxsat_instance.compute_fitness(ind), reverse=True)
        elites = sorted_parents[:elite_size]

        # Fill the rest of the population with offspring
        new_population = elites + offspring[:len(parents) - elite_size]
        return new_population

    def run_bga(self, initial_population, max_generations=50, crossover_prob=0.8, mutation_prob=0.01, elite_size=2, time_budget=10, use_lagrangian=False):
            """
            Full BGA loop including selection, crossover, mutation, and survivor selection.
            Now with time budget constraint (in seconds) and tqdm progress bar.
            Optional Lagrangian selection.
            """
            population = initial_population.copy()
            start_time = time.time()
            generation = 0
            best_fitness = -1
            lambda_t = 1.0

            with tqdm(total=max_generations, desc="Evolving Generations") as pbar:
                while generation < max_generations:
                    if time.time() - start_time >= time_budget:
                        print(f"⏰ Time budget reached at generation {generation}")
                        break

                    # Selection: choose ranking method
                    if use_lagrangian:
                        selected, lambda_t = self.stochastic_ranking_lagrangian(population, lambda_t, generation, max_generations)
                    else:
                        selected = self.stochastic_ranking_classic(population, generation, max_generations)

                    # Crossover + Mutation to generate offspring
                    offspring = []
                    for i in range(0, len(selected) - 1, 2):
                        parent1, parent2 = selected[i], selected[i + 1]
                        child1, child2 = self.one_point_crossover(parent1, parent2, crossover_prob)
                        child1 = self.bit_flip_mutation(child1, mutation_prob)
                        child2 = self.bit_flip_mutation(child2, mutation_prob)
                        offspring.extend([child1, child2])

                    # Survivor selection with elitism
                    population = self.survivor_selection(selected, offspring, elite_size)

                    # Track best solution found so far
                    current_best = max(population, key=lambda ind: self.maxsat_instance.compute_fitness(ind))
                    current_fitness = self.maxsat_instance.compute_fitness(current_best)

                    if current_fitness > best_fitness:
                        best_fitness = current_fitness
                        print(f"✅ Generation {generation}: New best fitness = {best_fitness}")

                    generation += 1
                    pbar.update(1)

            # Return the best individual after all generations or time budget
            best = max(population, key=lambda ind: self.maxsat_instance.compute_fitness(ind))
            return best
