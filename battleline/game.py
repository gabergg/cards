#!/usr/bin/env python

from battleline.deck import TroopDeck, TacticDeck
from battleline.board import Board
from battleline.player import Player

Handsize = 7
Numplayers = 2

class Game(object):
    def __init__(self, creator):
        self.players = []
        self.troopDeck = TroopDeck()
        self.tacticDeck = TacticDeck()
        self.numPlayers = Numplayers
        self.board = Board();
        self.players.append(Player(creator, self))
        # for i in range(Numplayers):
        #     self.players.append(Player(i+1))

    def checkWin(self, playerIndex):
        player = self.players[playerIndex]
        if len(player.flags) > 4:
            return true
        prevValue = -5
        breachSize = 0
        for flag in player.flags: #assuming this is sorted. sort on insertion
            if flag == prevValue + 1:
                breachSize += 1
            else:
                breachSize = 0
            prevValue = flag
        if breachSize > 2:
            return true
        return false

    def send(self, message, recipient=None):
        if not recipient:
            for player in self.players:
                if hasattr(player, 'socket') and player.socket:
                    try:
                        player.socket.write_message(message)
                    except IOError, e:
                        print str(e)
        else:
            if hasattr(recipient, 'socket') and recipient.socket:
                try:
                    recipient.socket.write_message(message)
                except IOError:
                    pass

    def __repr__(self):
        return 'he he heh eh e'