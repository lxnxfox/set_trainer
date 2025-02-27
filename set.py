import numpy as np
import pygame

pygame.init()

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
window.fill((25, 25, 25))

class Card:
    values = np.array([])
    card_width = 80
    card_height = 100
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


def compare_if_is_set(card1, card2, card3):
    is_set = True
    for i in range(4):
        values = [card1.values[i], card2.values[i], card3.values[i]]
        unique_count = len(set(values))
        if(unique_count == 2):  # exact two values are identical
            is_set = False
    return is_set

    
def mix_cards(): # generates 3x4 matrix of 12 random different cards
    active_cards = np.full((3, 4), Card([],0,0,False))
    for i in range(3):
        for j in range(4):
            card_exists = True
            while card_exists:
                index = np.random.randint(0, 81)
                if not np.any(active_cards == all_cards[index]): # card already in active_cards
                    active_cards[i][j] = all_cards[index]
                    all_cards[index].x_position = 30 + 100*j
                    all_cards[index].y_position = 30 + 120*i
                    all_cards[index].is_visible = True
                    card_exists = False
    return active_cards


all_cards = []  # list of all 81 cards
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                all_cards.append(Card(np.array([i, j, k, l]), 0, 0, False))


# test
mix_cards()


#all_cards.append(Card(np.array([1,1,2,0]), 210, 30, True))

print("is set: ",compare_if_is_set(all_cards[0], all_cards[1], all_cards[2]))
print("is equal: ",all_cards[0].equals(all_cards[1]))


# main
running = True
while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for card in all_cards:
                rect = pygame.Rect(card.x_position, card.y_position, card.card_width, card.card_height)
                if card.is_visible and rect.collidepoint(event.pos):
                    card.is_visible = False
    window.fill((25, 25, 25))
    for card in all_cards:
        if card.is_visible:
            pygame.draw.rect(window, "white", (card.x_position, card.y_position, card.card_width, card.card_height))

    # pygame.draw.rect(window, "red", (x, y, width, height))
    # pygame.circle(window, "blue", (x, y))
    #pygame.draw.rect(window, "white", (30, 30, 60, 80))

    pygame.display.flip()

pygame.quit()




