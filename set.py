import numpy as np
import pygame

pygame.init()

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

window.fill((25, 25, 25))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    pygame.display.update()


pygame.quit()

class Card:
    values = np.array([])
    def __init__(self, values):
        self.values = values
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

# test
a = Card(np.array([0,1,2,0]))
b = Card(np.array([0,1,2,0]))
c = Card(np.array([1,1,2,0]))

print("is set: ",compare_if_is_set(a, b, c))
print("is equal: ",a.equals(b))
            
