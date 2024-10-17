## Note: This file is independant from others files

import random

# Define the constants for the game
COLORS = ["Red", "Blue", "Green", "Yellow", "Black", "White"]
TARGET_LENGTH = 4
POPULATION_SIZE = 8
MUTATION_RATE = 0.1


# Function to generate a random combination
def generate_combination():
    return [random.choice(COLORS) for _ in range(TARGET_LENGTH)]


# Function to score a combination
def score_combination(combination, target):
    return sum(1 for i in range(TARGET_LENGTH) if combination[i] == target[i])


# Function to perform crossover between two parents
def crossover(parent1, parent2):
    return [random.choice([parent1[i], parent2[i]]) for i in range(TARGET_LENGTH)]


# Function to mutate a combination
def mutate(combination):
    index_to_mutate = random.randint(0, TARGET_LENGTH - 1)
    new_color = random.choice(
        [color for color in COLORS if color != combination[index_to_mutate]]
    )
    combination[index_to_mutate] = new_color
    return combination


if __name__ == "__main__":
    # Initialize the target combination and the first population
    target_combination = generate_combination()
    population = [generate_combination() for _ in range(POPULATION_SIZE)]

    generation = 0
    found = False

    # Main loop: continue until the target combination is found
    while not found:
        generation += 1

        # Score each combination
        scored_population = [
            (combo, score_combination(combo, target_combination))
            for combo in population
        ]

        # Check if any combination matches the target
        for combo, score in scored_population:
            if score == TARGET_LENGTH:
                found = True
                print(f"Target combination found: {combo} in generation {generation}")
                break

        if found:
            break

        # Select the best 4 combinations
        scored_population.sort(key=lambda x: x[1], reverse=True)
        survivors = [combo for combo, _ in scored_population[:4]]

        # Perform mutation on the weakest of the survivors
        if random.random() < MUTATION_RATE:
            survivors[-1] = mutate(survivors[-1])

        # Perform crossover to create new combinations
        new_population = survivors[:]
        while len(new_population) < POPULATION_SIZE:
            parents = random.sample(survivors, 2)
            new_population.append(crossover(parents[0], parents[1]))

        population = new_population
