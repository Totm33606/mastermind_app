import pygame
import random
from collections import Counter

# Constants
COLORS = ["Red", "Blue", "Green", "Yellow", "Black", "White"]
MUTATION_RATE = 0.1
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
        self.running = True
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
        # Rendu du texte
        text_surface = font.render(text, True, text_color)
        text_width, text_height = text_surface.get_size()
        button_width = text_width + padding * 2
        button_height = text_height + padding

        final_bg_color = tuple(min(c + 40, 255) for c in bg_color) if hover else bg_color
        pygame.draw.rect(screen, final_bg_color, (x, y, button_width, button_height), border_radius=10) # Fond 
        pygame.draw.rect(screen, border_color, (x, y, button_width, button_height), width=3, border_radius=10) # Bordure

        # Positionnement du texte pour le centrer dans le bouton
        text_x = x + (button_width - text_width) // 2
        text_y = y + (button_height - text_height) // 2
        screen.blit(text_surface, (text_x, text_y))

        # Retourne un objet Rect pour détecter les clics
        return pygame.Rect(x, y, button_width, button_height)


    def show(self):
        while self.running:
            screen.fill((240, 248, 255))  # Fond bleu clair (AliceBlue)

            # Titre
            title_text = font_large.render("Mastermind Genetic Algorithm", True, (25, 25, 112))
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

            # Labels et champs de saisie
            label_x = SCREEN_WIDTH // 2 - 10
            input_x = SCREEN_WIDTH // 2
            input_width = 150

            # Target Length
            target_label = font_medium.render("Target Length", True, (0, 0, 0))
            screen.blit(target_label, (label_x - target_label.get_width(), 180))
            self.draw_input_field(input_x, 180, input_width, self.target_length_input, self.input_active_target_length)

            # Population Size
            population_label = font_medium.render("Population Size", True, (0, 0, 0))
            screen.blit(population_label, (label_x - population_label.get_width(), 260))
            self.draw_input_field(input_x, 260, input_width, self.population_size_input, self.input_active_population_size)

            # Bouton Start Game
            mouse_pos = pygame.mouse.get_pos()
            start_hover = SCREEN_WIDTH // 2 - 100 < mouse_pos[0] < SCREEN_WIDTH // 2 + 100 and 350 < mouse_pos[1] < 420
            start_button = self.draw_button(
                x=SCREEN_WIDTH // 2 - 100,
                y=350,
                text="Start Game",
                font=font_medium,
                bg_color=(0, 255, 0),         # Couleur verte
                text_color=(0, 0, 0),         # Texte noir
                border_color=(0, 0, 0),       # Bordure noire
                padding=20,
                hover=start_hover
            )

            pygame.display.update()

            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        self.start_game()
                        return
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

        game = MastermindGame(target_length, population_size)
        game.run_game()

class MastermindGame:
    def __init__(self, target_length, population_size):
        self.target_length = target_length
        self.population_size = population_size
        self.target_combination = generate_combination(target_length)
        self.population = [generate_combination(target_length) for _ in range(population_size)]
        self.generation = 0
        self.found = False
    
    def get_color_from_name(self, color_name):
        color_map = {
            "Red": (255, 0, 0),
            "Blue": (0, 0, 255),
            "Green": (0, 255, 0),
            "Yellow": (255, 255, 0),
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
            score = score_combination(combination, self.target_combination)
            score_text = font_small.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (650, y_offset + i * 69))

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

    def check_solution(self):
        for combination in self.population:
            if combination == self.target_combination:
                self.found = True
                break

    def reset_game(self):
        # Reset game variables
        self.generation = 0
        self.found = False
        self.target_combination = generate_combination(self.target_length)
        self.population = [generate_combination(self.target_length) for _ in range(self.population_size)]

    def next_generation(self):
        if self.found:
            return
        
        self.generation += 1
        scored_population = [(combo, score_combination(combo, self.target_combination)) for combo in self.population]
        scored_population.sort(key=lambda x: x[1], reverse=True)
        survivors = [combo for combo, _ in scored_population[:self.population_size // 2]]

        if random.random() < MUTATION_RATE:
            survivors[-1] = mutate(survivors[-1], self.target_length)

        new_population = survivors[:]
        while len(new_population) < self.population_size:
            parents = random.sample(survivors, 2)
            new_population.append(crossover(parents[0], parents[1], self.target_length))

        self.population = new_population

    def run_game(self):
        running = True
        run_all = False
        self.check_solution() # Si dans la pop init on trouve par miracle le code du 1er coup

        while running:
            # Dessiner le fond dégradé
            self.draw_gradient_background(screen, (135, 206, 250), (25, 25, 112))  # Bleu ciel vers bleu nuit

            # Dessiner le reste de l'interface
            self.draw_secret_code()
            self.draw_population()

            # Affichage de la génération
            generation_text = font_medium.render(f"Generation: {self.generation}", True, (0, 0, 0))
            screen.blit(generation_text, (SCREEN_WIDTH // 2 - generation_text.get_width() // 2, 25))

            # Affichage de 'Secret Code'
            secret_text = font_medium.render("Secret code:", True, (0, 0, 0))
            screen.blit(secret_text, (SCREEN_WIDTH - 375 - secret_text.get_width() // 2, 25))

            # Coordonnées des boutons
            button_y = SCREEN_HEIGHT - 50

            # Boutons interactifs
            mouse_pos = pygame.mouse.get_pos()
            next_gen_hover = 0 < mouse_pos[0] < 180 and button_y < mouse_pos[1] < button_y + 70
            run_all_hover = SCREEN_WIDTH - 200 < mouse_pos[0] < SCREEN_WIDTH and button_y < mouse_pos[1] < button_y + 70
            reset_hover = SCREEN_WIDTH // 2 - 90 < mouse_pos[0] < SCREEN_WIDTH // 2 + 90 and button_y < mouse_pos[1] < button_y + 70

            # Dessiner les boutons
            next_gen_button = self.draw_button(
                20, button_y, "Next Generation", font_small, (0, 255, 0), (0, 0, 0), (0, 200, 0), hover=next_gen_hover
            )
            run_all_button = self.draw_button(
                SCREEN_WIDTH - 180, button_y, "Run All", font_medium, (0, 0, 255), (0, 0, 0), (0, 0, 200), hover=run_all_hover
            )
            reset_button = self.draw_button(
                SCREEN_WIDTH // 2 - 100, button_y, "Reset Game", font_medium, (255, 0, 0), (0, 0, 0), (200, 0, 0), hover=reset_hover
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
