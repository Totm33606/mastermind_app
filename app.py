from typing import Tuple
import numpy as np
import tkinter as tk
from tkinter import ttk
from mastermind import generate_code, genetic_algorithm, plot_results
from settings import GENERATIONS, CODE_LENGTH


# Main Tkinter app
class MastermindApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Mastermind - Genetic Algorithm")
        self.geometry("800x600")

        # Variables
        self.generation_var = tk.StringVar()
        self.best_code_var = tk.StringVar()
        self.exact_var = tk.StringVar()
        self.partial_var = tk.StringVar()
        self.score_var = tk.StringVar()

        # Font size
        self.font = ("Helvetica", 50)

        self.create_widgets()

        # Launch
        self.secret_code = generate_code()
        self.after(100, self.run_genetic_algorithm)

    def create_widgets(self):
        ttk.Label(self, text="Generation:", font=self.font).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(self, textvariable=self.generation_var).grid(
            row=0, column=1, sticky="w"
        )

        ttk.Label(self, text="Best code:", font=self.font).grid(
            row=1, column=0, sticky="w"
        )
        ttk.Label(self, textvariable=self.best_code_var).grid(
            row=1, column=1, sticky="w"
        )

        ttk.Label(self, text="Exact Matches:", font=self.font).grid(
            row=2, column=0, sticky="w"
        )
        ttk.Label(self, textvariable=self.exact_var).grid(row=2, column=1, sticky="w")

        ttk.Label(self, text="Partial Matches:", font=self.font).grid(
            row=3, column=0, sticky="w"
        )
        ttk.Label(self, textvariable=self.partial_var).grid(row=3, column=1, sticky="w")

        ttk.Label(self, text="Score:", font=self.font).grid(row=4, column=0, sticky="w")
        ttk.Label(self, textvariable=self.score_var).grid(row=4, column=1, sticky="w")

        self.progress_bar = ttk.Progressbar(self, length=400, mode="determinate")
        self.progress_bar.grid(row=5, column=0, columnspan=2, pady=10)

        # Frame to plot
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.grid(row=6, column=0, columnspan=2, pady=10)

    def update_ui(
        self, generation: int, best_code: np.array, best_score: Tuple[int, int, int]
    ):
        self.generation_var.set(generation + 1)
        self.best_code_var.set(" ".join(best_code))
        self.exact_var.set(int(best_score[0]))
        self.partial_var.set(int(best_score[1]))
        self.score_var.set(int(best_score[2]))

        # Update progress bar
        progress = (generation + 1) / GENERATIONS * 100
        self.progress_bar["value"] = progress

        if best_score[0] == CODE_LENGTH:
            self.progress_bar["value"] = 100

        self.update()

    def run_genetic_algorithm(self):
        solution, generations, best_scores = genetic_algorithm(
            self.secret_code, self.update_ui
        )

        if generations == -1:
            print("Secret code not found...")
        else:
            print(f"Solution found in {generations} generations!")
        print(f"The secret code was: {solution}")

        plot_results(best_scores, self.canvas_frame)
