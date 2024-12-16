import pygame
import random
from collections import Counter

# Constants
COLORS = ["Red", "Blue", "Green", "Yellow", "Black", "White"]
MUTATION_RATE = 0.8
EXACT_MATCH = 1
PARTIAL_MATCH = 0.5
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

# Input fields for parameters
input_active_target_length = False
input_active_population_size = False
target_length_input = ""
population_size_input = ""

def generate_combination(length):
    return [random.choice(COLORS) for _ in range(length)]

def score_combination(combination, target, exact_only=False):
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

def crossover(parent1, parent2, length):
    return [random.choice([parent1[i], parent2[i]]) for i in range(length)]

def mutate(combination, length):
    index_to_mutate = random.randint(0, length - 1)
    new_color = random.choice([color for color in COLORS if color != combination[index_to_mutate]])
    combination[index_to_mutate] = new_color
    return combination

class StartScreen:
    def __init__(self):
        self.target_length = 4
        self.population_size = 8
        self.show_secret_code = True
        self.show_best = True  
        self.input_active_target_length = False
        self.input_active_population_size = False
        self.target_length_input = str(self.target_length)
        self.population_size_input = str(self.population_size)

    def draw_input_field(self, x, y, width, text, active):
        color = (0, 0, 0) if not active else (255, 0, 0)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, width, 40), border_radius=10)
        pygame.draw.rect(screen, color, (x, y, width, 40), 2, border_radius=10)
        text_surface = font_small.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (x + 10, y + 10))
    
    def draw_button(self, x, y, text, font, bg_color, text_color, border_color, padding=20, hover=False):
        text_surface = font.render(text, True, text_color)
        text_width, text_height = text_surface.get_size()
        button_width = text_width + padding * 2
        button_height = text_height + padding

        final_bg_color = tuple(min(c + 40, 255) for c in bg_color) if hover else bg_color
        pygame.draw.rect(screen, final_bg_color, (x, y, button_width, button_height), border_radius=10)  # Fond 
        pygame.draw.rect(screen, border_color, (x, y, button_width, button_height), width=3, border_radius=10)  # Bordure

        text_x = x + (button_width - text_width) // 2
        text_y = y + (button_height - text_height) // 2
        screen.blit(text_surface, (text_x, text_y))
        return pygame.Rect(x, y, button_width, button_height)

    def draw_checkbox(self, x, y, text, checked):
        text_surface = font_medium.render(text, True, (0, 0, 0))
        text_width, _ = text_surface.get_size()
        screen.blit(text_surface, (x, y + 2))
        box_size = 40
        box_x = x + text_width + 10
        box_y = y
        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_size, box_size), 2)

        # Dessin du "tick" si la case est cochée (plus épais)
        if checked:
            pygame.draw.line(screen, (0, 0, 0), (box_x + 5, box_y + box_size // 2), (box_x + 8, box_y + box_size - 5), 2)
            pygame.draw.line(screen, (0, 0, 0), (box_x + 8, box_y + box_size - 5), (box_x + box_size - 5, box_y + 5), 2)

        return pygame.Rect(box_x, box_y, box_size, box_size)

    def show(self):
        running = True
        while running:
            screen.fill((240, 248, 255))  # Fond bleu clair (AliceBlue)

            # Titre
            title_text = font_large.render("Mastermind Genetic Algorithm", True, (86, 180, 233))
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

            # Labels et champs de saisie
            label_x = SCREEN_WIDTH // 2 + 10
            input_x = SCREEN_WIDTH // 2 + 20
            input_width = 150

            # Target Length
            target_label = font_medium.render("Target Length", True, (0, 0, 0))
            screen.blit(target_label, (label_x - target_label.get_width(), 180))
            self.draw_input_field(input_x, 180, input_width, self.target_length_input, self.input_active_target_length)

            # Population Size
            population_label = font_medium.render("Population Size", True, (0, 0, 0))
            screen.blit(population_label, (label_x - population_label.get_width(), 260))
            self.draw_input_field(input_x, 260, input_width, self.population_size_input, self.input_active_population_size)

            # Case à cocher pour afficher/cacher le code secret
            checkbox_show_secret = self.draw_checkbox(SCREEN_WIDTH // 2 - 180, 325, "Show Secret Code", self.show_secret_code)
            
            # Case à cocher pour afficher ou non les meilleurs scores
            checkbox_show_best = self.draw_checkbox(SCREEN_WIDTH // 2 - 180, 400, "Show Best codes", self.show_best)


            # Bouton Start Game
            mouse_pos = pygame.mouse.get_pos()
            start_hover = SCREEN_WIDTH // 2 - 100 < mouse_pos[0] < SCREEN_WIDTH // 2 + 100 and 400 < mouse_pos[1] < 470
            start_button = self.draw_button(
                x=SCREEN_WIDTH // 2 - 100,
                y=500,
                text="Start Game",
                font=font_medium,
                bg_color=(0, 158, 115),         # Couleur verte
                text_color=(0, 0, 0),         # Texte noir
                border_color=(0, 0, 0),       # Bordure noire
                padding=20,
                hover=start_hover
            )

            pygame.display.update()

            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        self.start_game()
                        return
                    elif checkbox_show_secret.collidepoint(event.pos):
                        self.show_secret_code = not self.show_secret_code  # Inverser l'état de la case à cocher
                    elif checkbox_show_best.collidepoint(event.pos):
                        self.show_best= not self.show_best 
                    elif input_x < event.pos[0] < input_x + input_width and 180 < event.pos[1] < 220:
                        self.input_active_target_length = True
                        self.input_active_population_size = False
                    elif input_x < event.pos[0] < input_x + input_width and 260 < event.pos[1] < 300:
                        self.input_active_population_size = True
                        self.input_active_target_length = False
                elif event.type == pygame.KEYDOWN:
                    if self.input_active_target_length:
                        if event.key == pygame.K_BACKSPACE:
                            self.target_length_input = self.target_length_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.input_active_target_length = False
                        else:
                            self.target_length_input += event.unicode
                    elif self.input_active_population_size:
                        if event.key == pygame.K_BACKSPACE:
                            self.population_size_input = self.population_size_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.input_active_population_size = False
                        else:
                            self.population_size_input += event.unicode

    def start_game(self):
        try:
            target_length = int(self.target_length_input) if self.target_length_input else self.target_length
            population_size = int(self.population_size_input) if self.population_size_input else self.population_size
        except ValueError:
            target_length = self.target_length
            population_size = self.population_size

        # Passer le paramètre show_secret_code au jeu
        game = MastermindGame(target_length, population_size, show_secret_code=self.show_secret_code, show_best=self.show_best)
        game.run_game()


class MastermindGame:
    def __init__(self, target_length, population_size, show_secret_code=True, show_best=True):
        self.target_length = target_length
        self.population_size = population_size
        self.show_secret_code = show_secret_code
        self.show_best = show_best
        self.target_combination = generate_combination(target_length)
        self.population = [generate_combination(target_length) for _ in range(population_size)]
        scored_population = [(combo, score_combination(combo, self.target_combination, exact_only=True)) for combo in self.population]
        scored_population.sort(key=lambda x: x[1], reverse=True)
        self.survivors = [combo for combo, _ in scored_population[:self.population_size // 2]]
        self.generation = 0
        self.found = False
        self.secrets_found = []
    
    def get_color_from_name(self, color_name):
        color_map = {
            "Red": (230, 159, 0),
            "Blue": (86, 180, 233),
            "Green": (0, 158, 115),
            "Yellow": (240, 228, 66),
            "Black": (0, 0, 0),
            "White": (255, 255, 255)
        }
        return color_map.get(color_name, (255, 255, 255))

    def draw_population(self):
        y_offset = 100
        for i, combination in enumerate(self.population):
            for j, color in enumerate(combination):
                # Dessiner un cercle noir pour le contour
                pygame.draw.circle(screen, (0, 0, 0), (100 + j * 80, y_offset + i * 70), 22)  # Contour noir, rayon 22

                # Dessiner le cercle colorÃ©
                pygame.draw.circle(screen, self.get_color_from_name(color), (100 + j * 80, y_offset + i * 70), 20)  # Cercle colorÃ©, rayon 20

            # Afficher le score de chaque combinaison
            score = score_combination(combination, self.target_combination, exact_only=True)
            score_text = font_small.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (650, y_offset + i * 69))

            if self.show_best and combination in self.survivors:
                pygame.draw.rect(screen, (0, 0, 0), (75, y_offset + i * 70 - 25, 560, 50), 4, border_radius=5)

    def draw_secret_code(self):
        for i, color in enumerate(self.target_combination):
            # Dessiner un cercle noir pour le contour
            pygame.draw.circle(screen, (0, 0, 0), (1050 + i * 70, 100), 22)  # Contour noir, rayon 22
            pygame.draw.circle(screen, self.get_color_from_name(color), (1050 + i * 70, 100), 20)
    
    def draw_gradient_background(self, screen, color1, color2):
        for y in range(SCREEN_HEIGHT):
            blend_ratio = y / SCREEN_HEIGHT
            blended_color = tuple(
                int(color1[i] * (1 - blend_ratio) + color2[i] * blend_ratio) for i in range(3)
            )
            pygame.draw.line(screen, blended_color, (0, y), (SCREEN_WIDTH, y))

    def draw_button(self, x, y, text, font, bg_color, text_color, border_color, padding=20, hover=False):
        # Mesure la taille du texte
        text_surface = font.render(text, True, text_color)
        text_width, text_height = text_surface.get_size()

        # Taille dynamique du bouton
        button_width = text_width + padding * 2
        button_height = text_height + padding

        # Couleur de fond si survol
        final_bg_color = tuple(min(c + 40, 255) for c in bg_color) if hover else bg_color
        pygame.draw.rect(screen, final_bg_color, (x, y, button_width, button_height), border_radius=10) # Fond
        pygame.draw.rect(screen, border_color, (x, y, button_width, button_height), width=3, border_radius=10) # Bordure

        # Dessin du texte centré
        text_x = x + (button_width - text_width) // 2
        text_y = y + (button_height - text_height) // 2
        screen.blit(text_surface, (text_x, text_y))
        return pygame.Rect(x, y, button_width, button_height)
    
    def draw_histogram(self):
        if len(self.secrets_found) > 10:
            temp = self.secrets_found[-1]
            del self.secrets_found
            self.secrets_found = [temp]

        # Dimensions et position de l'histogramme
        histogram_width = 500
        histogram_height = 200
        histogram_x = 900
        histogram_y = SCREEN_HEIGHT - histogram_height - 200

        # Calcul des échelles
        max_iterations = max(self.secrets_found) if self.secrets_found else 1
        bar_width = histogram_width / 10
        scale = histogram_height / max_iterations

        # Dessiner le fond de l'histogramme
        pygame.draw.rect(screen, (240, 240, 240), (histogram_x, histogram_y, histogram_width, histogram_height))
        pygame.draw.rect(screen, (0, 0, 0), (histogram_x, histogram_y, histogram_width, histogram_height), 2)

        # Dessiner les barres
        for i, iterations in enumerate(self.secrets_found):
            bar_height = iterations * scale
            bar_x = histogram_x + i * bar_width
            bar_y = histogram_y + histogram_height - bar_height

            # Barre 
            pygame.draw.rect(screen, (86, 180, 233), (bar_x, bar_y, bar_width - 2, bar_height))

            # Bordure
            pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width - 2, bar_height), width=2)

            # Affichage nombre de générations
            value_text = font_small.render(str(iterations), True, (0, 0, 0))  # Texte noir
            text_x = bar_x + (bar_width - value_text.get_width()) // 2  # Centrer le texte horizontalement
            text_y = bar_y - value_text.get_height() - 2  # Placer au-dessus de la barre
            screen.blit(value_text, (text_x, text_y))

    def check_solution(self):
        for combination in self.population:
            if combination == self.target_combination and not self.found:
                self.found = True
                self.secrets_found.append(self.generation)
                break

    def reset_game(self):
        # Reset game variables
        self.generation = 0
        self.found = False

        del self.target_combination
        self.target_combination = generate_combination(self.target_length)

        del self.population
        self.population = [generate_combination(self.target_length) for _ in range(self.population_size)]

        del self.survivors
        scored_population = [(combo, score_combination(combo, self.target_combination, exact_only=True)) for combo in self.population]
        scored_population.sort(key=lambda x: x[1], reverse=True)
        self.survivors = [combo for combo, _ in scored_population[:self.population_size // 2]]

    def next_generation(self):
        if self.found:
            return
        
        self.generation += 1
        scored_population = [(combo, score_combination(combo, self.target_combination, exact_only=True)) for combo in self.population]
        scored_population.sort(key=lambda x: x[1], reverse=True)
        survivors = [combo for combo, _ in scored_population[:self.population_size // 2]]
        del self.survivors
        self.survivors = survivors

        if random.random() < MUTATION_RATE:
            survivors[-1] = mutate(survivors[-1], self.target_length)

        new_population = survivors[:]
        while len(new_population) < self.population_size:
            parents = random.sample(survivors, 2)
            new_population.append(crossover(parents[0], parents[1], self.target_length))

        del self.population
        self.population = new_population

    def run_game(self):
        running = True
        run_all = False
        self.check_solution() # Si dans la pop init on trouve par miracle le code du 1er coup
        while running:
            # Dessiner le fond dégradé
            self.draw_gradient_background(screen, (200, 200, 200), (100, 100, 100))  # Gris clair vers gris foncé

            if self.show_secret_code:
                 # Affichage de 'Secret Code'
                self.draw_secret_code()
                secret_text = font_medium.render("Secret code:", True, (0, 0, 0))
                screen.blit(secret_text, (SCREEN_WIDTH - 375 - secret_text.get_width() // 2, 25))

            self.draw_population()
            self.draw_histogram()

            # Affichage de la génération
            generation_text = font_medium.render(f"Generation: {self.generation}", True, (0, 0, 0))
            screen.blit(generation_text, (SCREEN_WIDTH // 2 - generation_text.get_width() // 2, 25))

            # Coordonnées des boutons
            button_y = SCREEN_HEIGHT - 55

            # Boutons interactifs
            mouse_pos = pygame.mouse.get_pos()
            next_gen_hover = 0 < mouse_pos[0] < 180 and button_y < mouse_pos[1] < button_y + 70
            run_all_hover = SCREEN_WIDTH - 200 < mouse_pos[0] < SCREEN_WIDTH and button_y < mouse_pos[1] < button_y + 70
            reset_hover = SCREEN_WIDTH // 2 - 90 < mouse_pos[0] < SCREEN_WIDTH // 2 + 90 and button_y < mouse_pos[1] < button_y + 70

            # Dessiner les boutons
            next_gen_button = self.draw_button(
                20, button_y, "Next Generation", font_medium, (0, 158, 115), (0, 0, 0), (0, 0, 0), hover=next_gen_hover
            )
            run_all_button = self.draw_button(
                SCREEN_WIDTH - 180, button_y, "Run All", font_medium, (86, 180, 233), (0, 0, 0), (0, 0, 0), hover=run_all_hover
            )
            reset_button = self.draw_button(
                SCREEN_WIDTH // 2 - 100, button_y, "Reset Game", font_medium, (230, 159, 0), (0, 0, 0), (0, 0, 0), hover=reset_hover
            )

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Clic sur le bouton Next Generation
                    if next_gen_button.collidepoint(event.pos):
                        self.next_generation()
                        self.check_solution()
                    # Clic sur le bouton Run All
                    elif run_all_button.collidepoint(event.pos):
                        run_all = True
                    # Clic sur le bouton Reset Game
                    elif reset_button.collidepoint(event.pos):
                        self.reset_game()
                        run_all = False
                        self.check_solution()

            # Run all generations automatically
            if run_all:
                while not self.found:
                    self.next_generation()
                    self.check_solution()

if __name__ == "__main__":
    start_screen = StartScreen()
    start_screen.show()
