import numpy as np

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
        if(unique_count == 2):
            is_set = False
    print("is set: ", is_set)

a = Card(np.array([0,1,2,0]))
b = Card(np.array([0,1,2,0]))
c = Card(np.array([1,1,2,0]))

compare_if_is_set(a, b, c)
print(a.equals(b))
            
