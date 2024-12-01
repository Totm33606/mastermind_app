import random
import tkinter as tk
from collections import Counter
from tkinter import messagebox  # for pop-ups

# Constants for the game
COLORS = ["Red", "Blue", "Green", "Yellow", "Black", "White"]
TARGET_LENGTH = 4  # between 1 and 6
POPULATION_SIZE = 8  # between 4 and 11 (to be lisible)
MUTATION_RATE = 0.1
EXACT_MATCH = 1
PARTIAL_MATCH = 0.5


# Function to generate a random combination
def generate_combination():
    return [random.choice(COLORS) for _ in range(TARGET_LENGTH)]


# Advanced score
def score_combination(combination, target):
    exact_match, partial_match = 0, 0
    remaining_colors, remaining_target = [], []

    for comb_color, target_color in zip(combination, target):
        if comb_color == target_color:
            exact_match += 1
        else:
            remaining_colors.append(comb_color)
            remaining_target.append(target_color)

    target_counts = Counter(remaining_target)
    for color in remaining_colors:
        if target_counts[color] > 0:
            partial_match += 1
            target_counts[color] -= 1

    return exact_match * EXACT_MATCH + partial_match * PARTIAL_MATCH


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


# GUI class for displaying the algorithm process
class MastermindGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind Genetic Algorithm")
        self.root.geometry("1500x1000")  # Increased window size

        # Initialize variables
        self.target_combination = generate_combination()
        self.population = [generate_combination() for _ in range(POPULATION_SIZE)]
        self.generation = 0
        self.found = False

        # Frame for UI organization
        frame = tk.Frame(root)
        frame.pack()

        # Left pane for population and controls
        left_pane = tk.Frame(frame)
        left_pane.pack(side="left")

        # Right pane for secret code
        right_pane = tk.Frame(frame, padx=20, pady=20)
        right_pane.pack(side="right")

        # Set up GUI elements in left pane
        self.label_generation = tk.Label(
            left_pane, text="Generation: 0", font=("Arial", 50), bg="lightgray"
        )
        self.label_generation.pack(pady=10)

        self.canvas_width = 900
        self.canvas_height = 800
        self.canvas = tk.Canvas(
            left_pane, width=self.canvas_width, height=self.canvas_height, bg="white"
        )
        self.canvas.pack(pady=10)

        self.next_button = tk.Button(
            left_pane,
            text="Next Generation",
            command=self.next_generation,
            font=("Arial", 50),
            bg="lightgray",
        )
        self.next_button.pack(pady=10)

        self.run_all_button = tk.Button(
            left_pane,
            text="Run All",
            command=self.run_all_generations,
            font=("Arial", 50),
            bg="lightgray",
        )
        self.run_all_button.pack(pady=10)

        # Secret code display in right pane
        self.label_secret = tk.Label(
            right_pane, text="Secret Code:", font=("Arial", 50), bg="lightgray"
        )
        self.label_secret.pack(pady=10)

        self.secret_code_canvas = tk.Canvas(
            right_pane, width=350, height=100, bg="white"
        )
        self.secret_code_canvas.pack(pady=10)

        # Draw secret code
        self.draw_secret_code()

        # Display initial population
        self.draw_population()

    # Right panel
    def draw_secret_code(self):
        self.secret_code_canvas.delete("all")
        for j, color in enumerate(self.target_combination):
            x0, y0 = 30 + j * 50, 30
            x1, y1 = x0 + 40, y0 + 40
            self.secret_code_canvas.create_oval(
                x0, y0, x1, y1, fill=color.lower(), outline="black"
            )

    # Left panel
    def draw_population(self):
        self.canvas.delete("all")  # Clear the canvas

        # Display each individual in the population
        for i, combo in enumerate(self.population):
            for j, color in enumerate(combo):
                x0, y0 = 50 + j * 100, 50 + i * 70
                x1, y1 = x0 + 40, y0 + 40
                self.canvas.create_oval(
                    x0, y0, x1, y1, fill=color.lower(), outline="black"
                )
            score = score_combination(combo, self.target_combination)
            self.canvas.create_text(
                800,
                70 + i * 70,
                text=f"Score: {score}",
                font=("Arial", 40),
                fill="black",
            )

        # Update generation label
        self.label_generation.config(text=f"Generation: {self.generation}")

    def next_generation(self):
        # Score each combination
        scored_population = [
            (combo, score_combination(combo, self.target_combination))
            for combo in self.population
        ]

        # Check if any combination matches the target
        for combo, score in scored_population:
            if score == TARGET_LENGTH:
                self.found = True
                print(
                    f"Target combination found: {combo} in generation {self.generation}"
                )
                self.label_generation.config(
                    text=f"Target found in generation {self.generation}"
                )
                self.next_button.config(state="disabled")
                self.run_all_button.config(state="disabled")
                messagebox.showinfo(
                    "Winner",
                    f"WINNER \n The target was found in generation {self.generation}!",
                )
                return

        # Divide population by 2, keeping the best ones
        scored_population.sort(key=lambda x: x[1], reverse=True)
        survivors = [
            combo for combo, _ in scored_population[: int(POPULATION_SIZE / 2)]
        ]

        # Perform mutation on the weakest of the survivors
        if random.random() < MUTATION_RATE:
            survivors[-1] = mutate(survivors[-1])

        # Perform crossover to create new combinations
        new_population = survivors[:]
        while len(new_population) < POPULATION_SIZE:
            parents = random.sample(survivors, 2)
            new_population.append(crossover(parents[0], parents[1]))

        # Update population and display
        self.population = new_population
        self.generation += 1
        self.draw_population()

    def run_all_generations(self):
        while not self.found:
            self.next_generation()


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = MastermindGUI(root)
    root.mainloop()
