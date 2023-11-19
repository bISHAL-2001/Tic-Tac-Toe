# Author: BISHAL KUMAR GHOSH
# Created: Sun Nov 19 23:54:33 IST 2023
# Email: bkg.official.0601@gmail.com

from tkinter import *
import numpy as np

size_of_board = 700
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#DE3163'
symbol_O_color = '#1F51FF'
Green_color = '#50C878'


class Tic_Tac_Toe():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.canvas.configure(bg="#36454F")
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        def create_bold_line(canvas, x1, y1, x2, y2, line_color, bold_color, bold_width):
            # Draw the main line
            line = canvas.create_line(x1, y1, x2, y2, fill=line_color, width=bold_width*2)

            # Draw thinner lines on top to create a bold effect
            for i in range(0, bold_width):
                canvas.create_line(x1, y1 - i, x2, y2 - i, fill=bold_color, width=2)
        
        for i in range(2):
            # Bold width
            bold_width = 5

            # Create the bold line
            create_bold_line(self.canvas, (i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board, "black", "white", bold_width)

        for i in range(2):
            # Bold width
            bold_width = 5

            # Create the bold line
            create_bold_line(self.canvas, 0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3, "black", "white", bold_width)
        

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size - 4, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline="black")
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)


    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        
        self.canvas.create_line(grid_position[0] - symbol_size-4, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill="black")
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size - 4, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill="black")
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
    
    
    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            text = 'WINNER: PLAYER 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'WINNER: PLAYER 2 (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'TIE'
            color = 'white'

        self.canvas.delete("all")
        if text == 'TIE':    
            self.canvas.create_text(size_of_board / 2 + 4, size_of_board / 3, font="cmr 90 bold", fill="black", text=text)
            self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 90 bold", fill=color, text=text)
        else:
            self.canvas.create_text(size_of_board / 2 + 4, size_of_board / 3, font="cmr 60 bold", fill="black", text=text)
            self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'SCORES \n'
        self.canvas.create_text(size_of_board / 2 + 4, 5 * size_of_board / 8, font="Helvetica 40 bold", fill="black",
                                text=score_text)
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="Helvetica 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'PLAYER 1 (X): ' + str(self.X_score) + '\n'
        score_text += 'PLAYER 2 (O): ' + str(self.O_score) + '\n'
        score_text += 'TIE: ' + str(self.tie_score)
        
        self.canvas.create_text(size_of_board / 2 + 4, 3 * size_of_board / 4, font="cmr 30 bold", fill="black",
                                text=score_text)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'CLICK TO PLAY AGAIN\n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="white",
                                text=score_text)

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie
        

        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return gameover





    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = not self.player_X_turns
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns

            # Check if game is concluded
            if self.is_gameover():
                self.display_gameover()
                # print('Done')
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


game_instance = Tic_Tac_Toe()
game_instance.mainloop()