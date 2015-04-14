#!/usr/bin/env python

class Column(object):
    def __init__(self):
        self.homeSet = []
        self.awaySet = []
        self.size = 3
        self.closed = False

    def place(self, card, set):
        if set == 'homeSet':
            self.homeSet.append(card)
        else:
            self.awaySet.append(card)

   # def resolve(self):


class Board(object):
    def __init__(self):
        self.columns = []
        for i in range(9):
            self.columns.append(Column())
