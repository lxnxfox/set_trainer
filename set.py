import numpy as np
import pygame
#from pygame.font import get_default_font TODO ???

class Game:
    def __init__(self):
        pygame.init()

        self.window_width = 800
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("SET Trainer")
        self.font = pygame.font.Font(None, 36)
        self.restart_button_text = self.font.render("Restart", True, "black")
        self.text_area = self.restart_button_text.get_rect(center=(640, 400))
        self.restart_button = pygame.Rect(590, 385, 100, 30)
        self.all_cards = self.generate_cards()
        self.chosen_cards = []
        self.traffic_light = self.Traffic_light()

        mix_cards(self.all_cards)
        self.run()

    class Traffic_light:
        radius = 35
        position_red = (645, 95)
        position_green = (645, 195)
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

    def generate_cards(self):
        all_cards = []  # list of all 81 cards
        for i in range(3):
            for j in range(3):  
                for k in range(3):
                    for l in range(3):
                        all_cards.append(Card(np.array([i, j, k, l]), 0, 0, False))
        return all_cards
    
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
                        self.all_cards = self.generate_cards()
                        mix_cards(self.all_cards)
                        self.traffic_light.reset()
                        self.chosen_cards = []

                if len(self.chosen_cards) == 3:
                    self.traffic_light.update(check_is_set(self.chosen_cards))
                    self.chosen_cards = []

            self.window.fill((45, 45, 45))
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
    #values = np.array([])
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

    def get_values(self):
        return self.values




def check_is_set(chosen_cards):
    is_set = True
    for i in range(4): # compares values of each attribute
        values = [chosen_cards[0].get_values()[i], chosen_cards[1].get_values()[i], chosen_cards[2].get_values()[i]]
        #unique_count = len(set(values))
        unique_count = len(np.unique(values))
        if(unique_count == 2):  # exact two values are identical
            is_set = False  
    print("is set: ",is_set)    #TODO delete this line
    return is_set

    
def mix_cards(all_cards): # generates 3x4 matrix of 12 random different cards
    active_cards = np.full((3, 4), Card([],0,0,False))
    for i in range(3):
        for j in range(4):
            while True:
                index = np.random.randint(0, 81)
                #if not np.any(active_cards == all_cards[index]): # card already in active_cards
                if not all_cards[index] in active_cards:
                    active_cards[i][j] = all_cards[index]
                    all_cards[index].x_position = 30 + 130*j
                    all_cards[index].y_position = 30 + 180*i
                    all_cards[index].is_visible = True
                    break
    return active_cards


# draws attributes amount [0], shape [1], color [2], strength of color [3]
def draw_content(card, window):
    # filling
    if card.get_values()[3] == 1: # no filling
        border_width = 5
    else:   # transparent or complete filling
        border_width = 0
    surface = pygame.Surface((800, 600), pygame.SRCALPHA)
    if card.get_values()[3] == 2: # transparent
        transparency = 100
    else:
        transparency = 255 

    # color
    all_colors = [(170, 0, 0, transparency), (0, 150, 0, transparency), (0, 0, 170, transparency)]    # red, green, blue
    color = all_colors[card.get_values()[2]]

    # amount and shape
    if card.get_values()[0] == 0: # 1 element
        if card.get_values()[1] == 0: # rectangle
            pygame.draw.rect(surface, color, (card.x_position+21, card.y_position+65, 60, 20), border_width)
        elif card.get_values()[1] == 1: # circle
            pygame.draw.circle(surface, color, (card.x_position+50, card.y_position+75), 20, border_width)
        else: # ellipse
            pygame.draw.ellipse(surface, color, (card.x_position+22, card.y_position+70, 60, 20), border_width)
    elif card.get_values()[0] == 1: # 2 elements
        if card.get_values()[1] == 0: # rectangle
            pygame.draw.rect(surface, color, (card.x_position+21, card.y_position+45, 60, 20), border_width)
            pygame.draw.rect(surface, color, (card.x_position+21, card.y_position+90, 60, 20), border_width)
        elif card.get_values()[1] == 1: # circle
            pygame.draw.circle(surface, color, (card.x_position+50, card.y_position+50), 20, border_width)
            pygame.draw.circle(surface, color, (card.x_position+50, card.y_position+100), 20, border_width)
        else: # ellipse
            pygame.draw.ellipse(surface, color, (card.x_position+22, card.y_position+45, 60, 20), border_width)
            pygame.draw.ellipse(surface, color, (card.x_position+22, card.y_position+90, 60, 20), border_width)
    elif card.get_values()[0] == 2: # 3 elements
        if card.get_values()[1] == 0: # rectangle
            pygame.draw.rect(surface, color, (card.x_position+21, card.y_position+35, 60, 20), border_width)
            pygame.draw.rect(surface, color, (card.x_position+21, card.y_position+65, 60, 20), border_width)
            pygame.draw.rect(surface, color, (card.x_position+21, card.y_position+95, 60, 20), border_width)
        elif card.get_values()[1] == 1: # circle
            pygame.draw.circle(surface, color, (card.x_position+50, card.y_position+40), 16, border_width)
            pygame.draw.circle(surface, color, (card.x_position+50, card.y_position+75), 16, border_width)
            pygame.draw.circle(surface, color, (card.x_position+50, card.y_position+110), 16, border_width)
        else: # ellipse
            pygame.draw.ellipse(surface, color, (card.x_position+22, card.y_position+40, 60, 20), border_width)
            pygame.draw.ellipse(surface, color, (card.x_position+22, card.y_position+70, 60, 20), border_width)
            pygame.draw.ellipse(surface, color, (card.x_position+22, card.y_position+100, 60, 20), border_width)
    window.blit(surface, (0, 0))



# main 
game = Game()

