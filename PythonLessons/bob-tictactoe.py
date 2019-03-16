# -*- coding: utf-8 -*-
# tic tac toe
import sys
    
class Player():

  def __init__(self, x): self.code = x[0]; self.value = int(x[1:]) # used by WP

  def __bool__(self): return self.value != 0 # for cell occupied test

  def __str__(self): return self.code # for print player
  
class WP(): # win_pattern: mechanism to accumulate moves & signal a winner
  # Each WP instance represents a line of 3 cells.
  # Filling all 3 of these cells with the same player is a win.
  # Each row, each column and each diagonal is represented by a WP instance
  # Each cell is gets a list of those wp's that represent that cell
  # Each play results in the player's value being added to each of its wp's
  # 3 X's in a wp's cells result in its value ==3; 3 O's - value == -3
  # AI: to support AI development it might be a good idea to store the player(s)in a 3 element list.  
  
  def play(self, player, x=0): # add player (1 or -1) to its value x is index of plays
    self.value += player.value
    self.plays[x] = player
    return abs(self.value) == 3 # indicate a winner

class Cell(): # a square on the board
  
  dummy_player = Player(' 0') # dummy player indicating each cell initially unoccupied
  wps = [WP() for x in range(8)]
  row_wps = wps[:3]
  col_wps = wps[3:6]
  diag_wps = wps[6:]

  def __init__(self, r, c):
    self.r = int(r)-1
    self.c = int(c)-1
    self.div = r < '3' and c == '3'
    # collect win_patterns affected by a play in this cell
    self.wps = [self.row_wps[self.r], self.col_wps[self.c]]
    if (r+c) in ('11', '22', '33'): self.wps.append(self.diag_wps[0])
    if (r+c) in ('13', '22', '31'): self.wps.append(self.diag_wps[1])    

  def __bool__(self): return False # detect item is a cell for display

  def __call__(self, player):
    if self.player: return 'O' # occupied
    self.player = player
    for wp in self.wps:
      if wp.play(player): return 'W' # winner
    return 'P' # next player
        
  def reset(self):
    self.player = self.dummy_player

  @classmethod
  def reset_wp(self):
    for wp in wps: wp.value = 0; wp.plays = [None]*3

class Game:

  board = {(row+col):Cell(row, col) for row in '123' for col in '123'}
  players = [Player(x) for x in ('X-1','O1')]

  def play(self):
    items = self.board
    items.update(dict(d=display, q=quit))
    while True:
      print('Starting game.')
      count = 0
      for cell in board: cell.reset()
      Cell.reset_wp()
      player = players[0] # start with X
      while count < 9: # go thru moves until win, quit or out of moves
        user_in = input(f'player {player} row and column of cell (rc) or d=display, q=quit')
        item = items.get(user_in, error)
        result = item(player) # item could be a cell or a function
        if result == 'O': print('Cell is occupied.')
        elif result == 'W': print(f'Player {player} wins. ', end=''); break
        elif result == 'P': player = players[player.value-1]; count += 1
        elif result is not None: print('Unexpected result" {result}"') 
        if count == 9: print('Game ends in a draw. ', end='')      

  def display(*args):
    for cell in board.values():
      print(cell.code, sep='|', end='')
      if cell.div: print('\n-+-+-')
      
  def quit(*args): sys.exit(0)

  def error(*args): print('invalid move')

Game().play()