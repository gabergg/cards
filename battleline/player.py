#!/usr/bin/env python

Handsize = 7

class Hand(object):
    def __init__(self):
        self.cards = []
        for i in range(Handsize):
            self.cards.append(TroopDeck.draw())

    def place(card, set):
        if set == 'homeSet':
            self.homeSet.append(card)
        else:
            self.awaySet.append(card)

class Player(object):
    def __init__(self, name):
        self.flags = []
        self.name = name
