# -*- coding: utf-8 -*-
# tic tac toe
import sys

class Game:

    @classmethod
    def play(self):
        items = self.board
        items.update(dict(d=self.display, q=self.quit)) # .update() required b/c dict. 
        while True:
            print('Starting game.')
            count = 0
            player = self.players[0] # This lets us start with X
            map(self.wp.reset, (wps)) # ?
            while count < 9:
                user_in = input(f'player {player} row and column of cell (rc) or d=display or q=quit')
                item = items.get(user_in, error)
                result = item(player)
                if result == 'O': print('Cell is occupied')
                elif result == 'W': print(f'Player {player} wins.')
                elif result == 'P': player = Player.swap(); count+=1
                if count == 9: print('Game ends in a draw.', end='')
    
    def display(*args):
        for cell in board.values():
            print(cell, sep='|', end='')
            if cell.div: print('\n-+-+-')

    def quit(*args): sys.exit(0)
        
    def error(*args): print('invalid move')

class Setup():
    def __init_subclass__(cls):
        cls.setup(cls)

class Player(Setup):
    def setup(cls): Game.players = [cls(x) for x in ('X-1', ' 0', 'O1')]
    def __init__(self, x): self.code = x[0]; self.value = int(x[1:])
    def swap(self): self.player = players[-self.player.value+1]; return self.player
    def __bool__(self): return self.value != 0
    def __str__(self): return self.code
    
class WP(Setup):

    def setup(cls):
        Game.wps = [cls() for x in range(8)]
        Game.row_wps = Game.wps[:3]
        Game.col_wps = Game.wps[3:6]
        Game.diag_wps = Game.wps[6:]

    def play(self, player, x=0):
        self.value += player.value
        self.plays[x] = player
        return abs(self.value) == 3

    def reset(self):
        for wp in Game.wps: wp.value = 0; wp.plays = [None]*3

class Cell(Setup):

    player = Game.players[1]

    def setup(cls): Game.board = {(r + c): cls(r,c) for r in '123' for c in '123'}
    def __init__(self, r, c):
        self.r = int(r) - 1; self.c = int(c) - 1; self.div = r < '3' and c == '3'
        self.wps = [Game.row_wps[self.r], Game.col_wps[self.c]]
        if (r + c) in ('11', '22', '33'): self.wps.append(Game.diag_wps[0])
        if (r + c) in ('13', '22', '31'): self.wps.append(Game.diag_wps[1])
    
    def __bool__(self): return False 
    
    def __call__(self, player):
        if self.player: return 'O'
        self.player = player 
        for wp in self.wps:
            if wp.play(player): return 'W'
        return 'P'

    def __str__(self): return self.player

Game.play()