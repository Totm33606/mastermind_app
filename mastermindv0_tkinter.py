import random
import tkinter as tk
from collections import Counter
from tkinter import messagebox

COLORS = ["Red", "Blue", "Green", "Yellow", "Black", "White"]
MUTATION_RATE = 0.1
EXACT_MATCH = 1
PARTIAL_MATCH = 0


def generate_combination(length):
    return [random.choice(COLORS) for _ in range(length)]


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

    return int(exact_match * EXACT_MATCH + partial_match * PARTIAL_MATCH)


def crossover(parent1, parent2, length):
    return [random.choice([parent1[i], parent2[i]]) for i in range(length)]


def mutate(combination, length):
    index_to_mutate = random.randint(0, length - 1)
    new_color = random.choice(
        [color for color in COLORS if color != combination[index_to_mutate]]
    )
    combination[index_to_mutate] = new_color
    return combination


class StartScreen:
    def __init__(self, root, start_callback):
        self.root = root
        self.root.title("Mastermind Genetic Algorithm")
        self.root.geometry("1000x350")
        self.start_callback = start_callback

        self.target_length = tk.IntVar(value=4)  # default value is 4
        self.population_size = tk.IntVar(value=8)  # default value is 8

        tk.Label(root, text="Configure the game parameters:", font=("Times", 70)).pack(
            pady=5
        )

        self.create_input_field("Target Length (1-6):", self.target_length)
        self.create_input_field("Population Size (4-11):", self.population_size)

        tk.Button(
            root,
            text="Start Game",
            command=self.start_game,
            font=("Times", 70),
            bg="lightgreen",
        ).pack(pady=20)

    def create_input_field(self, label_text, variable):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, font=("Times", 60)).pack(
            side=tk.LEFT, padx=5, pady=10
        )
        tk.Entry(frame, textvariable=variable, font=("Times", 60), width=10).pack(
            side=tk.LEFT
        )

    def start_game(self):
        length = self.target_length.get()
        size = self.population_size.get()

        if not (1 <= length <= 6 and 4 <= size <= 11):
            messagebox.showerror("Invalid Input", "Please enter valid values.")
            return

        self.start_callback(length, size)
        self.root.destroy()


class MastermindGUI:
    def __init__(self, root, target_length, population_size):
        self.root = root
        self.root.title("Mastermind Genetic Algorithm")
        self.root.geometry("1500x1100")

        # Initialisation
        self.target_length = target_length
        self.population_size = population_size
        self.target_combination = generate_combination(target_length)
        self.population = [
            generate_combination(target_length) for _ in range(population_size)
        ]
        self.generation = 0
        self.found = False
        self.scored_population = []

        # Building panels
        frame = tk.Frame(root)
        frame.pack()

        # Left panel
        left_pane = tk.Frame(frame)
        left_pane.pack(side="left")

        # Right panel
        right_pane = tk.Frame(frame, padx=20, pady=20)
        right_pane.pack(side="right")

        # Canvas
        self.population_canvas = tk.Canvas(left_pane, width=900, height=800, bg="white")
        self.population_canvas.pack(pady=10)

        self.secret_code_canvas = tk.Canvas(
            right_pane, width=400, height=100, bg="white"
        )
        self.secret_code_canvas.pack(pady=10)

        # Labels
        self.label_generation = tk.Label(
            left_pane, text="Generation: 0", font=("Times", 60)
        )
        self.label_generation.pack(pady=10)

        self.label_secret = tk.Label(
            right_pane, text="Secret Code:", font=("Times", 60)
        )
        self.label_secret.pack(pady=10)

        # Buttons
        self.next_button = tk.Button(
            left_pane,
            text="Next Generation",
            command=self.next_generation,
            font=("Times", 60),
            bg="lightgreen",
        )
        self.next_button.pack(pady=10)

        self.run_all_button = tk.Button(
            left_pane,
            text="Run All",
            command=self.run_all_generations,
            font=("Times", 60),
            bg="lightblue",
        )
        self.run_all_button.pack(pady=10)

        self.draw_secret_code()
        self.draw_population()

    def draw_secret_code(self):
        self.secret_code_canvas.delete("all")
        for j, color in enumerate(self.target_combination):
            x0, y0 = 30 + j * 50, 30
            x1, y1 = x0 + 40, y0 + 40
            self.secret_code_canvas.create_oval(x0, y0, x1, y1, fill=color.lower())

    def draw_population(self):
        self.population_canvas.delete("all")
        self.scored_population.clear()
        for i, combination in enumerate(self.population):
            for j, color in enumerate(combination):
                x0, y0 = 50 + j * 100, 50 + i * 70
                x1, y1 = x0 + 40, y0 + 40
                self.population_canvas.create_oval(x0, y0, x1, y1, fill=color.lower())
            score = score_combination(combination, self.target_combination)
            self.scored_population.append((combination, score))
            self.population_canvas.create_text(
                800, 70 + i * 70, text=f"Score: {score}", font=("Times", 40)
            )

        self.label_generation.config(text=f"Generation: {self.generation}")

    def next_generation(self):
        # Check if any combination matches the target
        for combination, score in self.scored_population:
            if score == self.target_length:
                self.found = True
                print(
                    f"Target combination found: {combination} in generation {self.generation}"
                )
                self.label_generation.config(
                    text=f"Target found in generation {self.generation}"
                )
                self.next_button.config(state="disabled")
                self.run_all_button.config(state="disabled")
                # messagebox.showinfo(
                #    "Winner",
                #    f"WINNER \n The target was found in generation {self.generation}!",
                # )
                return

        self.scored_population.sort(key=lambda x: x[1], reverse=True)
        survivors = [
            combo for combo, _ in self.scored_population[: self.population_size // 2]
        ]
        if random.random() < MUTATION_RATE:
            survivors[-1] = mutate(survivors[-1], self.target_length)

        new_population = survivors[:]
        while len(new_population) < self.population_size:
            parents = random.sample(survivors, 2)
            new_population.append(crossover(parents[0], parents[1], self.target_length))

        self.population = new_population
        self.generation += 1
        self.draw_population()

    def run_all_generations(self):
        while not self.found:
            self.next_generation()


if __name__ == "__main__":
    root = tk.Tk()

    def start_game(target_length, population_size):
        main_window = tk.Tk()
        MastermindGUI(main_window, target_length, population_size)
        main_window.mainloop()

    StartScreen(root, start_game)
    root.mainloop()
