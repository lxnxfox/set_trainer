import numpy as np
import pygame
#from pygame.font import get_default_font

class Game:
    def __init__(self):
        pygame.init()

        self.window_width = 800
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("SET Trainer")
        self.window.fill((25, 25, 25))
        self.font = pygame.font.Font(None, 36)
        self.restart_button_text = self.font.render("Restart", True, "black")
        self.text_area = self.restart_button_text.get_rect(center=(640, 400))
        self.restart_button = pygame.Rect(590, 385, 100, 30)
        self.all_cards = generate_cards()
        self.chosen_cards = []
        self.traffic_light = Traffic_light()

        mix_cards(self.all_cards)
        self.run()

    def run(self):
        running = True
        while running:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for card in self.all_cards:
                        rect = pygame.Rect(card.x_position, card.y_position, card.card_width, card.card_height)
                        if card.is_visible and rect.collidepoint(event.pos):
                            self.chosen_cards.append(card)
                            card.is_visible = False
                    if self.restart_button.collidepoint(event.pos):
                        self.all_cards = generate_cards()
                        mix_cards(self.all_cards)
                        self.traffic_light.reset()

                if len(self.chosen_cards) == 3:
                    self.traffic_light.update(compare_if_is_set(self.chosen_cards))
                    self.chosen_cards = []

            self.window.fill((25, 25, 25))
            for card in self.all_cards:
                if card.is_visible:
                    pygame.draw.rect(self.window, "white", (card.x_position, card.y_position, card.card_width, card.card_height))
                    draw_content(card, self.window)
            
            # draw traffic_light
            pygame.draw.rect(self.window, "black", self.traffic_light.rect)
            pygame.draw.circle(self.window, self.traffic_light.red, (self.traffic_light.position_red), self.traffic_light.radius)
            pygame.draw.circle(self.window, self.traffic_light.green, (self.traffic_light.position_green), self.traffic_light.radius)

            pygame.draw.rect(self.window, "white", self.restart_button)
            self.window.blit(self.restart_button_text, self.text_area)


            pygame.display.flip()

        pygame.quit()



class Card:
    values = np.array([])
    card_width = 100
    card_height = 150
    def __init__(self, values, x_position, y_position, is_visible):
        self.values = values
        self.x_position = x_position
        self.y_position = y_position
        self.is_visible = is_visible

    def __str__(self) -> str:
        output = f"values: {self.values}\nx_position: {self.x_position}\ny_position: {self.y_position}\nis_visible: {self.is_visible}"
        return output

    def equals(self, card):
        return np.array_equal(self.values, card)


class Traffic_light:
    radius = 35
    position_red = (650, 100)
    position_green = (650, 190)
    def __init__(self):
        self.rect = (580, 30, 130, 230)
        self.red = (80, 0, 0)
        self.green = (0, 80, 0)
    def update(self, is_set):
        if is_set:
            self.red = (80, 0, 0)
            self.green = (0, 255, 0)
        else:
            self.red = (255, 0, 0)
            self.green = (0, 80, 0)
    def reset(self):
        self.red = (80, 0, 0)
        self.green = (0, 80, 0)


def compare_if_is_set(chosen_cards):
    is_set = True
    for i in range(4): # compares values of each attribute
        values = [chosen_cards[0].values[i], chosen_cards[1].values[i], chosen_cards[2].values[i]]
        unique_count = len(set(values))
        if(unique_count == 2):  # exact two values are identical
            is_set = False  
    print("is set: ",is_set)
    return is_set

    
def mix_cards(all_cards): # generates 3x4 matrix of 12 random different cards
    active_cards = np.full((3, 4), Card([],0,0,False))
    for i in range(3):
        for j in range(4):
            card_exists = True
            while card_exists:
                index = np.random.randint(0, 81)
                if not np.any(active_cards == all_cards[index]): # card already in active_cards
                    active_cards[i][j] = all_cards[index]
                    all_cards[index].x_position = 30 + 130*j
                    all_cards[index].y_position = 30 + 180*i
                    all_cards[index].is_visible = True
                    card_exists = False
    return active_cards


# draws attributes amount [0], shape [1], color [2], strength of color [3]
def draw_content(card, window):
    #color
    strength_of_color = 255 - 87 * card.values[3]
    if card.values[2] == 0: # red
        color = (strength_of_color, 0, 0)
    elif card.values[2] == 1: # green
        color = (0, strength_of_color, 0)
    else: # blue
        if card.values[3] == 0:
            color = (0,180, strength_of_color)
        else:
            color = (0,0, strength_of_color)
    # amount and shape
    if card.values[0] == 0: # 1 element
        if card.values[1] == 0: # rectangle
            pygame.draw.rect(window, color, (card.x_position+25, card.y_position+70, 60, 20))
        elif card.values[1] == 1: # circle
            pygame.draw.circle(window, color, (card.x_position+45, card.y_position+75), 20)
        else: # ellipse
            pygame.draw.ellipse(window, color, (card.x_position+25, card.y_position+70, 60, 20))
    elif card.values[0] == 1: # 2 elements
        if card.values[1] == 0: # rectangle
            pygame.draw.rect(window, color, (card.x_position+25, card.y_position+45, 60, 20))
            pygame.draw.rect(window, color, (card.x_position+25, card.y_position+95, 60, 20))
        if card.values[1] == 1: # circle
            pygame.draw.circle(window, color, (card.x_position+45, card.y_position+50), 20)
            pygame.draw.circle(window, color, (card.x_position+45, card.y_position+100), 20)
        else: # ellipse
            pygame.draw.ellipse(window, color, (card.x_position+25, card.y_position+45, 60, 20))
            pygame.draw.ellipse(window, color, (card.x_position+25, card.y_position+95, 60, 20))
    elif card.values[0] == 2: # 3 elements
        if card.values[1] == 0: # rectangle
            pygame.draw.rect(window, color, (card.x_position+25, card.y_position+40, 60, 20))
            pygame.draw.rect(window, color, (card.x_position+25, card.y_position+70, 60, 20))
            pygame.draw.rect(window, color, (card.x_position+25, card.y_position+100, 60, 20))
        if card.values[1] == 1: # circle
            pygame.draw.circle(window, color, (card.x_position+45, card.y_position+40), 16)
            pygame.draw.circle(window, color, (card.x_position+45, card.y_position+75), 16)
            pygame.draw.circle(window, color, (card.x_position+45, card.y_position+110), 16)
        else: # ellipse
            pygame.draw.ellipse(window, color, (card.x_position+25, card.y_position+40, 60, 20))
            pygame.draw.ellipse(window, color, (card.x_position+25, card.y_position+70, 60, 20))
            pygame.draw.ellipse(window, color, (card.x_position+25, card.y_position+100, 60, 20))

def generate_cards():
    all_cards = []  # list of all 81 cards
    for i in range(3):
        for j in range(3):  
            for k in range(3):
                for l in range(3):
                    all_cards.append(Card(np.array([i, j, k, l]), 0, 0, False))
    return all_cards


# test
game = Game()

