import numpy as np

# Game parameters
CODE_LENGTH = 4  # Length of the secret code
COLORS = np.array(
    ["R", "G", "B", "Y", "O", "P"]
)  # Possible colors (red, green, blue, yellow, orange, purple)
POPULATION_SIZE = 8  # Population size
GENERATIONS = 1000  # Maximum number of generations
MUTATION_RATE = 0.1  # Probability of mutation
EXACT_MATCH = 2  # 2 points for an exact match (color and position)
PARTIAL_MATCH = 1  # 1 point for a partial match (color only)
