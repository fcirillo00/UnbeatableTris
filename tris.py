from copy import copy
import random
from time import time

class Tris:
    def __init__(self, turn = 'x'):
        self.board = ['_', '_', '_',
                      '_', '_', '_',
                      '_', '_', '_']
        self.turn = turn

    def showBoard(self):
        board = copy(self.board)
        for i in range(9):
            if board[i] == "_":
                board[i] = " "
        print(board[0] + " | " + board[1] + " | " + board[2])
        print("__|___|__")
        print(board[3] + " | " + board[4] + " | " + board[5])
        print("__|___|__")
        print(board[6] + " | " + board[7] + " | " + board[8])
        print("  |   |  ")

    def getCell(self, row, column):
        return self.board[row*3 + column]

    def setCell(self, row, column):
        self.board[row*3 + column] = self.turn

    def makeMove(self, row, column):
        # rows start at 1
        # columns start at 1
        if row < 1 or row > 3 or column < 1 or column > 3:
            print("Wrong row or column number, try again.")
            return False
        row -= 1
        column -= 1
        if self.getCell(row,column) == '_':
            self.setCell(row, column)
            self.turn = 'o' if self.turn == 'x' else 'x'
            return True
        else:
            print("Cell occupied, try again.")
            return False

    def makeMoveBoard(self, board):
        self.board = board
        self.turn = 'o' if self.turn == 'x' else 'x'

    def getRows(self):
        rows = []
        for i in range(3):
            row = [self.getCell(i,j) for j in range(3)]
            rows.append(row)
        return rows

    def getColumns(self):
        columns = []
        for j in range(3):
            column = [self.getCell(i,j) for i in range(3)]
            columns.append(column)
        return columns

    def getDiagonals(self):
        first_diag = [self.getCell(x,x) for x in range(3)]
        second_diag = [self.getCell(x, 2-x) for x in range(3)]
        return [first_diag, second_diag]

    def result(self):
        # returns 1 if it's a win, 0 if draw/unfinished, -1 if it's a loss
        win = ['x', 'x', 'x']
        lose = ['o', 'o', 'o']

        rows = self.getRows()
        columns = self.getColumns()
        diagonals = self.getDiagonals()
        all = rows + columns + diagonals
        
        if win in all:
            return 1
        if lose in all:
            return -1
        # draw/unfinished
        return 0  

    def countEmptyCells(self):
        return self.board.count('_')

    def isGameOver(self):
        return self.countEmptyCells() == 0 or self.result() != 0

    def createCopy(self):
        trisCopy = Tris()
        trisCopy.board = copy(self.board)
        trisCopy.turn = self.turn
        return trisCopy

    def getNextPossibleMoves(self):
        indices = [i for i, cell in enumerate(self.board) if cell == "_"]
        father = self.createCopy()
        children = []
        for i in indices:
            child = father.createCopy()
            child.board[i] = self.turn
            child.turn = 'o' if self.turn == 'x' else 'x'
            children.append(child.createCopy())
        return children

    def utility(self):    
        # utility value changes depending on how many rounds are left
        # a win with 4 empty cells is worth more than a win with no cells left
        
        # if win
        if self.result() == 1:
            return 1 + self.countEmptyCells()
        # if loss
        if self.result() == -1:
            return - (1 + self.countEmptyCells())
        # if draw
        return 0



# minimax with no pruning, much slower at first
def minimax(node: Tris):
    children = node.getNextPossibleMoves() 

    if not children or node.isGameOver():
        return node.utility(), node
    
    if node.turn == 'x':
        # player MAX
        max_utility = -1000
        best_node = None
        for child in children:
            utility, current_node = minimax(child)
            if utility > max_utility:
                max_utility = utility 
                best_node = child
        return max_utility, best_node

    if node.turn == 'o':
        # player MIN
        min_utility = 1000
        best_node = None
        for child in children:
            utility, current_node = minimax(child)
            if utility < min_utility:
                min_utility = utility 
                best_node = child
        return min_utility, best_node

# minimax with pruning, almost instantaneous
def minimaxPruning (node: Tris, alpha = -1000, beta = 1000):
    children = node.getNextPossibleMoves()
    if not children or node.isGameOver():
        return node.utility(), node

    if node.turn == 'x':
        # alpha is the best explored option for player X (max)
        max_utility = -1000
        best_node = None
        for child in children:
            utility, current_node = minimaxPruning(child, alpha, beta)
            if utility > max_utility: 
                max_utility = utility
                best_node = child

            alpha = max(max_utility, alpha)
            if alpha >= beta:
                break
                
        return max_utility, best_node
    
    if node.turn == 'o':
        # beta is the best explored option for player O (min)
        min_utility = 1000
        best_node = None
        for child in children:
            utility, game_state = minimaxPruning(child, alpha, beta)
            if utility < min_utility: 
                min_utility = utility
                best_node = child

            beta = min(min_utility, beta)
            if alpha >= beta:
                break
                
        return min_utility, best_node
            

def main():
    inp = 'a'
    while inp.lower() != 'q':
        first = str(input("Do you want to play first? (Y o N)\n"))
        print("You are playing as O.")
        if first.lower() != 'y':
            game = Tris('x')
            # all moves at the first round are of equal utility
            # add randomness: 
            game.board[random.randint(0,8)] = 'x'
            game.turn = 'o'
        else:
            game = Tris('o')
        while (not game.isGameOver()):
            game.showBoard()
            row, col = map(int, input("Insert row and column separated by a space.\n").split())
            while (not game.makeMove(row,col)):
                row, col = map(int, input("Insert row and column separated by a space.\n").split())
            if not game.isGameOver():
                utility, best_move = minimaxPruning(game)
                game.makeMoveBoard(best_move.board)

        game.showBoard()
        if game.utility() > 0:
            print("X won!")
        elif game.utility() < 0:
            print("O won!")
        else:
            print("It's a draw.")
        inp = input("Send Q to exit, or any key to restart.\n")
    
if __name__== "__main__":
    random.seed()
    main()

