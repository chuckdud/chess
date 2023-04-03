import numpy as np
from colorama import Fore, Back, Style

BLACK, WHITE = 0, 1
LIGHT, DARK = 2, 3
POTENTIAL = 4


def other_player(color):
    return BLACK if color == WHITE else WHITE

def init_board():
    board = np.ndarray((8, 8), dtype=Space)
    dark = 0
    for y in range(8):
        for x in range(8):
            if dark == 0:
                board[y][x] = Space(DARK, x, y)
                dark += 1
            else:
                board[y][x] = Space(LIGHT, x, y)
                dark = 0
        if dark == 0:
            dark = 1
        else:
            dark = 0
    for i in range(8):
        board[1][i].piece = Pawn(BLACK, i, 1)
    board[0][0].piece = Rook(BLACK, 0, 0)
    board[0][7].piece = Rook(BLACK, 7, 0)
    board[0][1].piece = Knight(BLACK, 1, 0)
    board[0][6].piece = Knight(BLACK, 6, 0)
    board[0][2].piece = Bishop(BLACK, 2, 0)
    board[0][5].piece = Bishop(BLACK, 5, 0)
    board[0][3].piece = Queen(BLACK, 3, 0)
    board[0][4].piece = King(BLACK, 4, 0)
    for i in range(8):
        board[6][i].piece = Pawn(WHITE, i, 6)
    board[7][0].piece = Rook(WHITE, 0, 7)
    board[7][7].piece = Rook(WHITE, 7, 7)
    board[7][1].piece = Knight(WHITE, 1, 7)
    board[7][6].piece = Knight(WHITE, 6, 7)
    board[7][2].piece = Bishop(WHITE, 2, 7)
    board[7][5].piece = Bishop(WHITE, 5, 7)
    board[7][3].piece = Queen(WHITE, 3, 7)
    board[7][4].piece = King(WHITE, 4, 7)
    return board


class State:
    def __init__(self):
        self.board = init_board()
        self.to_move = WHITE
        self.check = ""

    def __str__(self):
        ret = Style.RESET_ALL + "   a  b  c  d  e  f  g  h \n"
        for row in self.board:
            ret += str(8 - row[0].y) + " "
            for space in row:
                if space.is_empty():
                    ret += str(space)
                else:
                    ret += str(space) + str(space.piece)
            ret += Style.RESET_ALL + " " + str(8 - row[0].y) + "\n"
        ret += "   a  b  c  d  e  f  g  h \n"
        return ret

    def print_with_actions(self, actions):
        to_print = np.zeros((8, 8))
        for a in actions:
            to_print[a.new_y][a.new_x] = POTENTIAL
        ret = Style.RESET_ALL + "   a  b  c  d  e  f  g  h \n"

        for y in range(8):
            ret += str(8 - y) + " "
            for x in range(8):
                if self.board[y][x].is_empty() and to_print[y][x] == POTENTIAL:
                    ret += Back.RED + "   " + Style.RESET_ALL
                elif self.board[y][x].is_empty():
                    ret += str(self.board[y][x])
                else:
                    ret += str(self.board[y][x]) + str(self.board[y][x].piece)
            ret += Style.RESET_ALL + " " + str(8 - y) + "\n"
        ret += "   a  b  c  d  e  f  g  h \n"
        return ret


class Action:
    def __init__(self, old_x, old_y, new_x, new_y):
        self.old_x = old_x
        self.old_y = old_y
        self.new_x = new_x
        self.new_y = new_y


class Space:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.piece = None

    def is_empty(self):
        return self.piece is None

    def take(self, piece):
        self.piece = piece

    def __str__(self):
        to_print = ""
        if self.is_empty():
            to_print = "   "
        if self.color == DARK:
            return Back.LIGHTGREEN_EX + to_print
        else:
            return Back.WHITE + to_print


class Piece:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def find_actions(self, board):
        pass


class Pawn(Piece):

    def __init__(self, color, x, y):
        super(Pawn, self).__init__(color, x, y)
        self.moved = False

    def __str__(self):
        if self.color == BLACK:
            return Fore.BLACK + Style.BRIGHT + " p "
        else:
            return Fore.LIGHTWHITE_EX + Style.BRIGHT + " p "

    def find_actions(self, board):
        actions = []
        left = self.x - 1
        if left < 0:
            left = 0
        right = self.x + 1
        if right > 7:
            right = 7
        if self.color == WHITE:
            if not self.moved and board[self.y-2][self.x].is_empty():
                actions.append(Action(self.x, self.y, self.x, self.y-2))
                # must ensure that not moving into check
            if board[self.y-1][self.x].is_empty():
                actions.append(Action(self.x, self.y, self.x, self.y-1))
                # must ensure that not moving into check
            if not board[self.y-1][left].is_empty():
                actions.append(Action(self.x, self.y, left, self.y-1))
                # must ensure that not moving into check
            if not board[self.y-1][right].is_empty():
                actions.append(Action(self.x, self.y, right, self.y-1))
                # must ensure that not moving into check
        if self.color == BLACK:
            if not self.moved and board[self.y+2][self.x].is_empty():
                actions.append(Action(self.x, self.y, self.x, self.y+2))
                # must ensure that not moving into check
            if board[self.y+1][self.x].is_empty():
                actions.append(Action(self.x, self.y, self.x, self.y+1))
                # must ensure that not moving into check
            if not board[self.y+1][left].is_empty():
                actions.append(Action(self.x, self.y, left, self.y-1))
                # must ensure that not moving into check
            if not board[self.y+1][right].is_empty():
                actions.append(Action(self.x, self.y, right, self.y-1))
                # must ensure that not moving into check
        return actions


class Rook(Piece):
    def __str__(self):
        if self.color == BLACK:
            return Fore.BLACK + Style.BRIGHT + " r "
        else:
            return Fore.LIGHTWHITE_EX + Style.BRIGHT + " r "


class Knight(Piece):
    def __str__(self):
        if self.color == BLACK:
            return Fore.BLACK + Style.BRIGHT + " h "
        else:
            return Fore.LIGHTWHITE_EX + Style.BRIGHT + " h "


class Bishop(Piece):
    def __str__(self):
        if self.color == BLACK:
            return Fore.BLACK + Style.BRIGHT + " b "
        else:
            return Fore.LIGHTWHITE_EX + Style.BRIGHT + " b "


class Queen(Piece):
    def __str__(self):
        if self.color == BLACK:
            return Fore.BLACK + Style.BRIGHT + " Q "
        else:
            return Fore.LIGHTWHITE_EX + Style.BRIGHT + " Q "


class King(Piece):
    def __str__(self):
        if self.color == BLACK:
            return Fore.BLACK + Style.BRIGHT + " K "
        else:
            return Fore.LIGHTWHITE_EX + Style.BRIGHT + " K "


# step one:
# select a piece and display possible places it can move to
def user_move(state):
    print("Select a piece to move by providing its coordinates (space separated):")
    x_in, y_in = map(str, input().split())
    # convert to array indices
    x = ord(x_in) - ord('a')
    y = 8 - (ord(y_in) - ord('0'))
    p = state.board[y][x].piece
    if p is None or p.color != state.to_move:
        return -1
    print(f"Selected {type(p).__name__} at {x_in}{y_in}")
    actions = p.find_actions(state.board)
    print(state.print_with_actions(actions))


def play():
    s = State()
    print(s)
    while True:
        x = user_move(s)
        while x == -1:
            print("Invalid selection. Try again.")
            x = user_move(s)
        s.to_move = other_player(s.to_move)

play()