import random
import numpy as np
import tkinter as tk
from typing import List, Tuple, Any
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from settings import *


def count_exact_matches(
    guess: np.ndarray, secret: np.ndarray
) -> Tuple[int, np.ndarray, np.ndarray]:
    """
    Count the number of exact matches (correct color and position).
    """
    exact_mask = guess == secret
    exact_matches = np.sum(exact_mask)
    remaining_guess = guess[~exact_mask]
    remaining_secret = secret[~exact_mask]
    return exact_matches, remaining_guess, remaining_secret


def count_partial_matches(
    remaining_guess: np.ndarray, remaining_secret: np.ndarray
) -> int:
    """
    Count the number of correct colors in the wrong positions after removing exact matches.
    """
    color_match = 0
    for color in remaining_guess:
        if color in remaining_secret:
            color_match += 1
    return color_match


def fitness(guess: np.ndarray, secret: np.ndarray) -> Tuple[int, int, int]:
    """
    Calculate the fitness score in two steps:
    1. Number of exact matches (correct color and position).
    2. Number of correct colors but in wrong positions.
    """
    # Step 1: Count exact matches and get remaining lists
    exact_match, remaining_guess, remaining_secret = count_exact_matches(guess, secret)

    # Step 2: Count partial matches
    partial_match = count_partial_matches(remaining_guess, remaining_secret)

    # Choose any score you want : for example
    score = exact_match * EXACT_MATCH + partial_match * PARTIAL_MATCH

    return exact_match, partial_match, score


def generate_code() -> np.ndarray:
    """
    Generates a random code.
    """
    return np.random.choice(COLORS, CODE_LENGTH)


def initial_population() -> List[np.ndarray]:
    """
    Creates an initial random population.
    """
    return [generate_code() for _ in range(POPULATION_SIZE)]


def select_parents(
    population: List[np.ndarray], scores: List[Tuple[int, int, int]]
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Selects the best individuals (roulette selection) to reproduce.
    """
    total_score = sum(score[2] for score in scores)
    weights = [score[2] / total_score for score in scores]
    selected = random.choices(population, weights=weights, k=2)
    return selected[0], selected[1]


def crossover(parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
    """
    Crosses two parents.
    """
    point = random.randint(1, CODE_LENGTH - 1)
    child = np.concatenate([parent1[:point], parent2[point:]])
    return child


def mutate(child: np.ndarray) -> np.ndarray:
    """
    Mutates a child with a certain probability.
    """
    if random.random() < MUTATION_RATE:
        index = random.randint(0, CODE_LENGTH - 1)
        child[index] = np.random.choice(COLORS)
    return child


def genetic_algorithm(
    secret: np.array, update_ui_callback
) -> Tuple[Any, int, List[Tuple[int, int, int]]]:
    """
    Main program to launch to solve the mastermind secret code using genetic algorithm.
    """
    population = initial_population()
    best_scores = []

    for generation in range(GENERATIONS):
        scores = np.zeros((POPULATION_SIZE, 3))
        for j, code in enumerate(population):
            scores[j] = fitness(np.array(code), np.array(secret))

        index = np.argmax(scores[:, 2])
        best_scores.append(scores[index])

        # Updates app's prints
        update_ui_callback(generation, population[index], best_scores[-1])

        if scores[index][0] == CODE_LENGTH:
            return population[index], generation, best_scores

        new_population = []
        for _ in range(POPULATION_SIZE // 2):
            parent1, parent2 = select_parents(population, scores)
            child1 = mutate(crossover(parent1, parent2))
            child2 = mutate(crossover(parent2, parent1))
            new_population += [child1, child2]

        population = new_population

    return secret, -1, best_scores


def plot_results(best_scores: List[Tuple[int, int, int]], canvas_frame: tk.Frame):
    """
    Plots results at the end of genetic algorithm.
    """
    best_scores = np.array(best_scores)
    generations = list(range(len(best_scores)))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(generations, best_scores[:, 0], label="Exact Matches", color="green")
    ax.scatter(generations, best_scores[:, 1], label="Partial Matches", color="orange")
    ax.scatter(generations, best_scores[:, 2], label="Scores", color="blue")

    # Connection lines between points
    ax.plot(
        generations, best_scores[:, 0], color="green", alpha=0.3
    )  # Exact Matches line
    ax.plot(
        generations, best_scores[:, 1], color="orange", alpha=0.3
    )  # Partial Matches line
    ax.plot(generations, best_scores[:, 2], color="blue", alpha=0.3)  # Scores line

    ax.set_xlabel("Generations")
    ax.set_ylabel("Matches/Scores")
    ax.set_title("Evolution des scores du meilleur individu")
    ax.legend()

    # Plots in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
