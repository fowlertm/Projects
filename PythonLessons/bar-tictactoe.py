# --REQUIREMENTS--
# Create a TicTacToe class with a data structure for your board with initial values, and create a
# method to pretty print the the board.

# Now create a method to start the game, that carries out a basic game loop (asks the user for input # to make a move, and then responds with the computer’s move^). For the moment, have the computer 
# make any random move, and print the board after each move.

# Implement validation for user moves, so that impossible moves are not accepted.

# Implement an AI using a brute force.

# Implement an AI using a standard algorithm / tree data structure.

# Implement an AI using Keras/Tensorflow

import numpy as np

class TicTacToe:
    
    
    def __init__(self):
        self.occupied = set()
        self.board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.available = [x for x in self.board if x not in self.occupied]
        
    def get_user_move(self):
        count = 0
        while count < 10: 
            user_move = input("Specify the integer location where you want to place an 'X'.")
            if user_move in '123456789' and user_move not in self.occupied:
                return user_move
            count += 1
        print("Did not recognize your input.")
     
    
    
    
    def get_computer_move(self, board, available):
        # When we get the AIs move, we need a way of checking the state of the board and 
        # biasing the computer towards expert play.
        
        # What does this entail? We have a 1D representation of the game board in the form of 
        # a list of strings, and we've written some fairly gross conditional architecture to 
        # determine winning. moves. What we want is to have the get_computer_move() method 
        # to take the string representing the board and search over it, looking for two kinds 
        # of moves: those that block a user's victory, and those that maximize the probability 
        # of the computer's victory. 
        
        # If the win_check() function weren't freshman-level code perhaps we could call it within
        # the get_computer_move() function, but as it stands the former just returns None if 
        # if no winning condition is met. So, we'll have to look elsewhere. 
        
        # The MVP would probably be to check for whether or not there are any strings of two 
        # 'X's, and make the computer's next move be to block the next move. God help me, but 
        # I can't think of any way to do this but with yet *more* if/elif/else statements. Actually,
        # maybe I can get a for loop to do it. 
        
        for i in range(len(self.board) - 2): # to prevent IndexOutOfRange
            if self.board[i] == self.board[i + 1] and self.board[i + 2] in self.available:
                computer_move = self.board[i + 2]
                print(computer_move)
            
        computer_move = np.random.choice(self.available, 1)[0]
         
        return str(computer_move)
    
    def pretty_print(self, board):
        return(str(board[:3]) + '\n' + str(board[3:6]) + '\n' + str(board[6:9]))
    
    def win_check(self, board):
        win_patterns = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
        for wp in win_patterns:


        return winner
    
    def start(self):
        
#         print(self.board)
#         while not self.game_over():
        while not self.win_check(self.board):
    
            user_move = self.get_user_move()
            if user_move in self.available:
                self.available.remove(user_move)
                self.occupied.add(user_move)
            # Hey, at least it's pythonic. 
            self.board = ['X' if char == user_move else char for char in self.board]
            self.win_check(self.board)
            
            if len(self.available) > 1:
                comp_move = self.get_computer_move(self.board, self.available)
            if comp_move in self.available:
                self.available.remove(comp_move)
                self.occupied.add(comp_move)
            self.board = ['O' if char == comp_move else char for char in self.board]
            self.win_check(self.board)

            print(self.pretty_print(self.board)) # Define a pretty print function.
        return self.win_check(self.board)
    
    def game_over(self):
        return len(self.available) == 0
