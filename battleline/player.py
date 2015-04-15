#!/usr/bin/env python

from battleline.deck import TroopDeck

Handsize = 7

class Hand(object):
    def __init__(self, game):
        self.cards = []
        for i in range(Handsize):
            self.cards.append(game.troopDeck.draw())

class Player(object):
    def __init__(self, name, game):
        self.flags = []
        self.name = name
        self.hand = Hand(game)