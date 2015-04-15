#!/usr/bin/env python

from random import shuffle

Troops = {
    '1' : 'Skirmisher',
    '2' : 'Peltast',
    '3' : 'Javalineers',
    '4' : 'Hoplites',
    '5' : 'Phalangists',
    '6' : 'Hypaspist',
    '7' : 'Light Cavalry',
    '8' : 'Heavy Cavalry',
    '9' : 'Chariots',
    '10' : 'Elephants'
}

Colors = ['Blue', 'Red', 'Yellow', 'Green', 'Purple', 'Orange']

Tactics = ['Darius', 'Alexander', 'Cavalry Companion', 'Shield Bearers', 'Scout', 'Fog', 'Mud', 'Redeploy', 'Deserter', 'Traitor']

class Card(object):
    def __init__(self, name):
        self.name = name

    def image(self):
        return u'<img border="0" src="/static/cards/%s.png"/>'.encode('utf-8') % (self.name)

    def __repr__(self):
        return self.name

class Troop(Card):
    def __init__(self, name, color, value):
        Card.__init__(self, name)
        self.color = color
        self.value = value

    def image(self):
        return u'<img border="0" src="/static/cards/%s%s.png"/>'.encode('utf-8') % (self.color, self.name)

    def __repr__(self):
        return u'%s %s' % (self.color, self.name)

class TroopDeck(object):
    def __init__(self):
        self.cards = []
        for value in Troops.keys():
            for color in Colors:
                self.cards.append(Troop(Troops[value], color, value))
        shuffle(self.cards)

    def draw(self):
        if self.cards:
            return self.cards.pop()
        return 0

class TacticDeck(object):
    def __init__(self):
        self.cards = []
        for name in Tactics:
            self.cards.append(Card(name))
        shuffle(self.cards)

    def draw(self):
        if self.cards:
            return self.cards.pop()
        return 0