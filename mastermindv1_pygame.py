"""
Mastermind Genetic Algorithm Game using Pygame

This code contains the various modules needed to run the mastermind game.
The game is solved for a set of adjustable parameters. The main aim of this game
is to introduce students to genetic algorithms and artificial intelligence.

Authors:
- Thomas CHAMBON (t_chambo@insa-toulouse.fr)
- Adam MEDBOUHI (medbouhi@insa-toulouse.fr)

Date: 01/01/2025

This code is part of an educational project aimed at exploring genetic algorithms
through an interactive Mastermind game.
"""

##---IMPORTS---##
##-------------##
import pygame
import random
from collections import Counter
import heapq

##---CONSTANTS VARIABLES AND INIT---##
##----------------------------------##
COLORS = ["Red", "Blue", "Green", "Yellow", "Black", "White"]
EXACT_MATCH = 1
PARTIAL_MATCH = 0.5
MIN_TARGET_LENGTH = 1
MAX_TARGET_LENGTH = 7
MIN_POPULATION_SIZE = 4
MAX_POPULATION_SIZE = 10
MIN_MUTATION_RATE = 0.0
MAX_MUTATION_RATE = 1.0
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800

# Initialization of Pygame
pygame.init()

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mastermind Genetic Algorithm")

# Fonts
font_large = pygame.font.Font(None, 70)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 40)


##---GENERIC FUNCTIONS---##
##-----------------------##
def generate_combination(length):
    return [random.choice(COLORS) for _ in range(length)]


def score_combination(combination, target, exact_only=True):
    exact_match, partial_match = 0, 0
    remaining_colors, remaining_target = [], []

    for comb_color, target_color in zip(combination, target):
        if comb_color == target_color:
            exact_match += 1
        else:
            remaining_colors.append(comb_color)
            remaining_target.append(target_color)

    if exact_only:
        score = exact_match * EXACT_MATCH
    else:
        target_counts = Counter(remaining_target)
        for color in remaining_colors:
            if target_counts[color] > 0:
                partial_match += 1
                target_counts[color] -= 1
        score = exact_match * EXACT_MATCH + partial_match * PARTIAL_MATCH
    return score


def score_population(population, target, scoring_function=score_combination):
    return {
        index: scoring_function(combination, target)
        for index, combination in population.items()
    }


def get_top_combinations(population, scores, n):
    top_scores = heapq.nlargest(
        n, scores.items(), key=lambda x: x[1]
    )  # [(index, score), ...]
    survivors = {index: population[index] for index, _ in top_scores}
    return survivors  # dict {index: combination}


def crossover(parent1, parent2, length):
    return [random.choice([parent1[i], parent2[i]]) for i in range(length)]


def mutate(combination, length):
    index_to_mutate = random.randint(0, length - 1)
    new_color = random.choice(
        [color for color in COLORS if color != combination[index_to_mutate]]
    )
    combination[index_to_mutate] = new_color
    return combination


##---START SCREEN---##
##------------------##
class StartScreen:
    def __init__(self):
        self.settings = {
            "target_length": {"value": 4, "active": False, "input": "4"},
            "population_size": {"value": 8, "active": False, "input": "8"},
            "mutation_rate": {"value": 0.8, "active": False, "input": "0.8"},
        }
        self.show_secret_code = True
        self.show_best = True

    def draw_input_field(self, x, y, width, key):
        field = self.settings[key]
        color = (0, 0, 0) if not field["active"] else (255, 0, 0)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, width, 40), border_radius=10)
        pygame.draw.rect(screen, color, (x, y, width, 40), 2, border_radius=10)
        text_surface = font_small.render(field["input"], True, (0, 0, 0))
        screen.blit(text_surface, (x + 10, y + 10))

    def draw_button(
        self, x, y, text, font, bg_color, text_color, border_color, hover=False
    ):
        text_surface = font.render(text, True, text_color)
        text_width, text_height = text_surface.get_size()
        button_width = text_width + 40
        button_height = text_height + 20
        final_bg_color = (
            tuple(min(c + 40, 255) for c in bg_color) if hover else bg_color
        )

        pygame.draw.rect(
            screen,
            final_bg_color,
            (x, y, button_width, button_height),
            border_radius=10,
        )
        pygame.draw.rect(
            screen,
            border_color,
            (x, y, button_width, button_height),
            3,
            border_radius=10,
        )

        screen.blit(
            text_surface,
            (
                x + (button_width - text_width) // 2,
                y + (button_height - text_height) // 2,
            ),
        )
        return pygame.Rect(x, y, button_width, button_height)

    def draw_checkbox(self, x, y, text, checked):
        text_surface = font_medium.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (x, y + 2))
        box_size = 40
        box_x = x + text_surface.get_width() + 10
        pygame.draw.rect(screen, (0, 0, 0), (box_x, y, box_size, box_size), 2)

        if checked:
            pygame.draw.line(
                screen, (0, 0, 0), (box_x + 5, y + 20), (box_x + 15, y + 35), 3
            )
            pygame.draw.line(
                screen, (0, 0, 0), (box_x + 15, y + 35), (box_x + 35, y + 5), 3
            )

        return pygame.Rect(box_x, y, box_size, box_size)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for key, field in self.settings.items():
                if field["rect"].collidepoint(mouse_pos):
                    self.activate_field(key)
            if self.checkbox_secret_rect.collidepoint(mouse_pos):
                self.show_secret_code = not self.show_secret_code
            if self.checkbox_best_rect.collidepoint(mouse_pos):
                self.show_best = not self.show_best
            if self.start_button_rect.collidepoint(mouse_pos):
                self.start_game()
        elif event.type == pygame.KEYDOWN:
            for key, field in self.settings.items():
                if field["active"]:
                    if event.key == pygame.K_BACKSPACE:
                        field["input"] = field["input"][:-1]
                    elif event.key == pygame.K_RETURN:
                        field["active"] = False
                        self.apply_field_value(key)
                    else:
                        field["input"] += event.unicode

    def activate_field(self, key):
        for field_key in self.settings.keys():
            self.settings[field_key]["active"] = field_key == key

    def apply_field_value(self, key):
        try:
            if key == "mutation_rate":
                self.settings[key]["value"] = float(self.settings[key]["input"])
            else:
                self.settings[key]["value"] = int(self.settings[key]["input"])
        except ValueError:
            self.settings[key]["input"] = str(self.settings[key]["value"])

    def validate_value(self, key, value):
        if key == "target_length":
            return max(MIN_TARGET_LENGTH, min(MAX_TARGET_LENGTH, value))
        elif key == "population_size":
            return max(MIN_POPULATION_SIZE, min(MAX_POPULATION_SIZE, value))
        elif key == "mutation_rate":
            return max(MIN_MUTATION_RATE, min(MAX_MUTATION_RATE, value))
        return value

    def start_game(self):
        try:
            target_length = self.validate_value(
                "target_length", int(self.settings["target_length"]["input"])
            )
            population_size = self.validate_value(
                "population_size", int(self.settings["population_size"]["input"])
            )
            mutation_rate = self.validate_value(
                "mutation_rate", float(self.settings["mutation_rate"]["input"])
            )
        except ValueError:
            # Fallback to the last valid settings in case of unexpected issues
            target_length = self.settings["target_length"]["value"]
            population_size = self.settings["population_size"]["value"]
            mutation_rate = self.settings["mutation_rate"]["value"]

        # Launch the game with validated settings
        game = MastermindGame(
            target_length=target_length,
            population_size=population_size,
            mutation_rate=mutation_rate,
            show_secret_code=self.show_secret_code,
            show_best=self.show_best,
        )
        game.run_game()

    def show(self):
        running = True
        while running:
            screen.fill((240, 248, 255))  # AliceBlue background
            title_text = font_large.render(
                "Mastermind Genetic Algorithm", True, (86, 180, 233)
            )
            screen.blit(
                title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50)
            )

            y_offset = 180
            for key, label, label_x in [
                ("target_length", "Target Length", 240),
                ("population_size", "Population Size", 275),
                ("mutation_rate", "Mutation Rate", 240),
            ]:
                label_surface = font_medium.render(label, True, (0, 0, 0))
                label_x = SCREEN_WIDTH // 2 - label_x
                input_x = SCREEN_WIDTH // 2
                screen.blit(label_surface, (label_x, y_offset))
                self.settings[key]["rect"] = pygame.Rect(input_x, y_offset, 150, 40)
                self.draw_input_field(input_x, y_offset, 150, key)
                y_offset += 80

            # Checkboxes
            self.checkbox_secret_rect = self.draw_checkbox(
                SCREEN_WIDTH // 2 - 180, 405, "Show Secret Code", self.show_secret_code
            )
            self.checkbox_best_rect = self.draw_checkbox(
                SCREEN_WIDTH // 2 - 180, 480, "Show Best Codes", self.show_best
            )

            # Start Button
            mouse_pos = pygame.mouse.get_pos()
            start_hover = pygame.Rect(
                SCREEN_WIDTH // 2 - 100, 700, 200, 60
            ).collidepoint(mouse_pos)
            self.start_button_rect = self.draw_button(
                SCREEN_WIDTH // 2 - 100,
                700,
                "Start Game",
                font_medium,
                (0, 158, 115),
                (0, 0, 0),
                (0, 0, 0),
                hover=start_hover,
            )

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_events(event)


##---MAIN GAME CLASS---##
##---------------------##
class MastermindGame:
    def __init__(
        self,
        target_length,
        population_size,
        mutation_rate,
        show_secret_code,
        show_best,
    ):
        self.target_length = target_length
        self.population_size = population_size
        self.show_secret_code = show_secret_code
        self.show_best = show_best
        self.mutation_rate = mutation_rate
        self.target_combination = generate_combination(target_length)
        self.generation = 0
        self.found = False
        self.secrets_found = []

        # dict {index: combination}
        self.population = {
            i: generate_combination(target_length)
            for i in range(1, population_size + 1)
        }

        # dict {index: score}
        self.scores = score_population(self.population, self.target_combination)

        # dict {index: combination}
        self.survivors = get_top_combinations(
            self.population, self.scores, self.population_size // 2
        )

    def get_color_from_name(self, color_name):
        color_map = {
            "Red": (230, 159, 0),
            "Blue": (86, 180, 233),
            "Green": (0, 158, 115),
            "Yellow": (240, 228, 66),
            "Black": (0, 0, 0),
            "White": (255, 255, 255),
        }
        return color_map.get(color_name, (255, 255, 255))

    def draw_population(self):
        y_offset = 25
        for idx, combination in self.population.items():
            for j, color in enumerate(combination):
                # Draw a black circle for the outline
                pygame.draw.circle(
                    screen, (0, 0, 0), (100 + j * 80, y_offset + idx * 70), 22
                )  # Black outline, radius 22

                # Draw the filled circle
                pygame.draw.circle(
                    screen,
                    self.get_color_from_name(color),
                    (100 + j * 80, y_offset + idx * 70),
                    20,
                )  # Filled circle, radius 20

            # Display the score of each combination
            score_text = font_small.render(
                f"Score: {self.scores[idx]}", True, (0, 0, 0)
            )
            screen.blit(score_text, (650, y_offset + idx * 69))

            # Highlight the best combinations if show_best is True
            if self.show_best and idx in self.survivors.keys():
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (75, y_offset + idx * 70 - 25, 560, 50),
                    4,
                    border_radius=5,
                )

    def draw_secret_code(self):
        for i, color in enumerate(self.target_combination):
            # Draw a black circle for the outline
            pygame.draw.circle(
                screen, (0, 0, 0), (1050 + i * 70, 100), 22
            )  # Black outline, radius 22
            pygame.draw.circle(
                screen, self.get_color_from_name(color), (1050 + i * 70, 100), 20
            )

    def draw_gradient_background(self, screen, color1, color2):
        for y in range(SCREEN_HEIGHT):
            blend_ratio = y / SCREEN_HEIGHT
            blended_color = tuple(
                int(color1[i] * (1 - blend_ratio) + color2[i] * blend_ratio)
                for i in range(3)
            )
            pygame.draw.line(screen, blended_color, (0, y), (SCREEN_WIDTH, y))

    def draw_button(
        self,
        x,
        y,
        text,
        font,
        bg_color,
        text_color,
        border_color,
        padding=20,
        hover=False,
    ):
        # Measure the size of the text
        text_surface = font.render(text, True, text_color)
        text_width, text_height = text_surface.get_size()

        # Dynamically size the button
        button_width = text_width + padding * 2
        button_height = text_height + padding

        # Background color on hover
        final_bg_color = (
            tuple(min(c + 40, 255) for c in bg_color) if hover else bg_color
        )
        pygame.draw.rect(
            screen,
            final_bg_color,
            (x, y, button_width, button_height),
            border_radius=10,
        )  # Background
        pygame.draw.rect(
            screen,
            border_color,
            (x, y, button_width, button_height),
            width=3,
            border_radius=10,
        )  # Border

        # Draw the centered text
        text_x = x + (button_width - text_width) // 2
        text_y = y + (button_height - text_height) // 2
        screen.blit(text_surface, (text_x, text_y))
        return pygame.Rect(x, y, button_width, button_height)

    def draw_histogram(self):
        if len(self.secrets_found) > 10:
            temp = self.secrets_found[-1]
            del self.secrets_found
            self.secrets_found = [temp]

        # Histogram dimensions and position
        histogram_width = 500
        histogram_height = 200
        histogram_x = 900
        histogram_y = SCREEN_HEIGHT - histogram_height - 200

        # Scale calculations
        max_iterations = max(self.secrets_found) if self.secrets_found else 1
        bar_width = histogram_width / 10
        scale = histogram_height / max_iterations

        # Draw the histogram background
        pygame.draw.rect(
            screen,
            (240, 240, 240),
            (histogram_x, histogram_y, histogram_width, histogram_height),
        )
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (histogram_x, histogram_y, histogram_width, histogram_height),
            2,
        )

        # Draw the bars
        for i, iterations in enumerate(self.secrets_found):
            bar_height = iterations * scale
            bar_x = histogram_x + i * bar_width
            bar_y = histogram_y + histogram_height - bar_height

            # Bar
            pygame.draw.rect(
                screen, (86, 180, 233), (bar_x, bar_y, bar_width - 2, bar_height)
            )

            # Border
            pygame.draw.rect(
                screen, (0, 0, 0), (bar_x, bar_y, bar_width - 2, bar_height), width=2
            )

            # Display the number of generations
            value_text = font_small.render(
                str(iterations), True, (0, 0, 0)
            )  # Black text
            text_x = (
                bar_x + (bar_width - value_text.get_width()) // 2
            )  # Center text horizontally
            text_y = bar_y - value_text.get_height() - 2  # Place above the bar
            screen.blit(value_text, (text_x, text_y))

    def check_solution(self):
        if self.target_length in self.scores.values() and not self.found:
            self.found = True
            self.secrets_found.append(self.generation)

    def reset_game(self):
        # Reset variables
        self.generation = 0
        self.found = False

        del self.target_combination
        self.target_combination = generate_combination(self.target_length)

        del self.population
        self.population = {
            i: generate_combination(self.target_length)
            for i in range(1, self.population_size + 1)
        }

        del self.scores
        self.scores = score_population(self.population, self.target_combination)

        del self.survivors
        self.survivors = get_top_combinations(
            self.population, self.scores, self.population_size // 2
        )

    def next_generation(self):
        if self.found:
            return

        self.generation += 1

        del self.population
        self.population = self.survivors

        # Mutation step
        if random.random() < self.mutation_rate:
            random_index = random.choice(list(self.population.keys()))
            self.population[random_index] = mutate(
                self.population[random_index], self.target_length
            )

        # Fill up the population
        survivors = list(self.population.values())
        missing_idx = list(
            set(range(1, self.population_size + 1)) - set(self.population.keys())
        )
        idx_count = 0
        while (
            len(self.population) < self.population_size
            and idx_count < self.population_size - self.population_size // 2
        ):
            parents = random.sample(survivors, 2)
            self.population[missing_idx[idx_count]] = crossover(
                parents[0], parents[1], self.target_length
            )
            idx_count += 1

        # Calculate new scores
        del self.scores
        self.scores = score_population(self.population, self.target_combination)

        # Determine new survivors
        del self.survivors
        self.survivors = get_top_combinations(
            self.population, self.scores, self.population_size // 2
        )

    def run_game(self):
        running = True
        run_all = False
        self.check_solution()  # If the initial population contains the solution
        while running:
            # Draw gradient background
            self.draw_gradient_background(
                screen, (200, 200, 200), (100, 100, 100)
            )  # Light gray to dark gray

            if self.show_secret_code:
                # Display 'Secret Code'
                self.draw_secret_code()
                secret_text = font_medium.render("Secret code:", True, (0, 0, 0))
                screen.blit(
                    secret_text, (SCREEN_WIDTH - 375 - secret_text.get_width() // 2, 25)
                )

            self.draw_population()
            self.draw_histogram()

            # Display generation number
            generation_text = font_medium.render(
                f"Generation: {self.generation}", True, (0, 0, 0)
            )
            screen.blit(
                generation_text,
                (SCREEN_WIDTH // 2 - generation_text.get_width() // 2, 25),
            )

            # Button coordinates
            button_y = SCREEN_HEIGHT - 55

            # Interactive buttons
            mouse_pos = pygame.mouse.get_pos()
            next_gen_hover = (
                0 < mouse_pos[0] < 180 and button_y < mouse_pos[1] < button_y + 70
            )
            run_all_hover = (
                SCREEN_WIDTH - 200 < mouse_pos[0] < SCREEN_WIDTH
                and button_y < mouse_pos[1] < button_y + 70
            )
            reset_hover = (
                SCREEN_WIDTH // 2 - 90 < mouse_pos[0] < SCREEN_WIDTH // 2 + 90
                and button_y < mouse_pos[1] < button_y + 70
            )

            # Draw buttons
            next_gen_button = self.draw_button(
                20,
                button_y,
                "Next Generation",
                font_medium,
                (0, 158, 115),
                (0, 0, 0),
                (0, 0, 0),
                hover=next_gen_hover,
            )
            run_all_button = self.draw_button(
                SCREEN_WIDTH - 180,
                button_y,
                "Run All",
                font_medium,
                (86, 180, 233),
                (0, 0, 0),
                (0, 0, 0),
                hover=run_all_hover,
            )
            reset_button = self.draw_button(
                SCREEN_WIDTH // 2 - 100,
                button_y,
                "Reset Game",
                font_medium,
                (230, 159, 0),
                (0, 0, 0),
                (0, 0, 0),
                hover=reset_hover,
            )

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Click on "Next Generation"
                    if next_gen_button.collidepoint(event.pos):
                        self.next_generation()
                        self.check_solution()
                    # Click on "Run All"
                    elif run_all_button.collidepoint(event.pos):
                        run_all = True
                    # Click on "Reset Game"
                    elif reset_button.collidepoint(event.pos):
                        self.reset_game()
                        run_all = False
                        self.check_solution()

            # Automatically run all generations
            if run_all:
                while not self.found:
                    self.next_generation()
                    self.check_solution()


if __name__ == "__main__":
    start_screen = StartScreen()
    start_screen.show()
