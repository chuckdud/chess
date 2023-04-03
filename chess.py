import numpy as np
from colorama import Fore, Back, Style

WHITE, BLACK = 0, 1
LIGHT, DARK = 2, 3
POTENTIAL = 4

move_labels = ['a', 'c', 'd', 'e', 'f', 'g', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
               'q', 's', 't', 'u', 'v', 'w', 'y', 'z']


def dictify(actions):
    ret_dict = {}
    label_num = 0
    for a in actions:
        ret_dict[move_labels[label_num]] = a
        label_num += 1

    return ret_dict


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


def alt_init_board():
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
        str_move = "BLACK" if self.to_move == BLACK else "WHITE"
        ret = f"To move: {str_move}\n"
        ret += Style.RESET_ALL + "   a  b  c  d  e  f  g  h \n"
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

    def apply_action(self, a):
        p = self.board[a.old_y][a.old_x].piece
        p.y = a.new_y
        p.x = a.new_x
        if isinstance(p, Pawn):
            p.moved = True
            if abs(a.new_y - a.old_y) == 2:
                p.just_doubled = True
            else:
                p.just_doubled = False
        self.board[a.old_y][a.old_x].piece = None
        self.board[a.new_y][a.new_x].piece = p
        if a.passant:
            print("wow, en passant")
            self.board[a.passant_y][a.passant_x].piece = None

    def print_with_actions(self, actions, action_dict):
        # action_counter = 0
        # to_print = np.zeros((8, 8))
        # for a in actions:
        #     to_print[a.new_y][a.new_x] = POTENTIAL
        str_move = "BLACK" if self.to_move == BLACK else "WHITE"
        ret = f"To move: {str_move}\n"
        ret += Style.RESET_ALL + "   a  b  c  d  e  f  g  h \n"

        for y in range(8):
            ret += str(8 - y) + " "
            for x in range(8):
                found_action = None
                for a in actions:
                    if a.new_y == y and a.new_x == x:
                        found_action = a
                        break
                if found_action is not None:
                    for lbl in move_labels:
                        if action_dict[lbl] == found_action:
                            ret += Back.RED + Fore.WHITE + f" {lbl} " + Style.RESET_ALL
                            break
                    continue
                # if self.board[y][x].is_empty() and to_print[y][x] == POTENTIAL:
                #     ret += Back.RED + f"{move_labels[action_counter]}" + Style.RESET_ALL
                #     action_counter += 1
                if self.board[y][x].is_empty():
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
        self.passant = False
        self.passant_x = -1
        self.passant_y = -1

    def set_passant(self, x, y):
        self.passant = True
        self.passant_x = x
        self.passant_y = y


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
        super().__init__(color, x, y)
        self.moved = False
        self.just_doubled = False

    def __str__(self):
        if self.color == BLACK:
            return Fore.BLACK + Style.BRIGHT + " p "
        else:
            return Fore.LIGHTWHITE_EX + Style.BRIGHT + " p "

    def find_actions(self, board):
        actions = []
        left = True
        right = True
        if self.x - 1 < 0:
            left = False
        right = True
        if self.x + 1 > 7:
            right = False
        # TODO: prevent moving into check
        if self.color == WHITE:
            if not self.moved and board[self.y - 2][self.x].is_empty():
                actions.append(Action(self.x, self.y, self.x, self.y - 2))
            if board[self.y - 1][self.x].is_empty():
                actions.append(Action(self.x, self.y, self.x, self.y - 1))
            if left and not board[self.y - 1][self.x - 1].is_empty():
                actions.append(Action(self.x, self.y, self.x - 1, self.y - 1))
            if right and not board[self.y - 1][self.x + 1].is_empty():
                actions.append(Action(self.x, self.y, self.x + 1, self.y - 1))
            # en passant
            if left and isinstance(board[self.y][self.x - 1].piece, Pawn):
                if board[self.y][self.x - 1].piece.just_doubled:
                    a = Action(self.x, self.y, self.x - 1, self.y - 1)
                    a.set_passant(self.x - 1, self.y)
                    actions.append(a)
            if right and isinstance(board[self.y][self.x + 1].piece, Pawn):
                if board[self.y][self.x + 1].piece.just_doubled:
                    a = Action(self.x, self.y, self.x + 1, self.y - 1)
                    a.set_passant(self.x + 1, self.y)
                    actions.append(a)
        if self.color == BLACK:
            if not self.moved and board[self.y + 2][self.x].is_empty():
                actions.append(Action(self.x, self.y, self.x, self.y + 2))
            if board[self.y + 1][self.x].is_empty():
                actions.append(Action(self.x, self.y, self.x, self.y + 1))
            if left and not board[self.y + 1][self.x - 1].is_empty():
                actions.append(Action(self.x, self.y, self.x - 1, self.y + 1))
            if right and not board[self.y + 1][self.x + 1].is_empty():
                actions.append(Action(self.x, self.y, self.x + 1, self.y + 1))
            # en passant
            if left and isinstance(board[self.y][self.x - 1].piece, Pawn):
                if board[self.y][self.x - 1].piece.just_doubled:
                    a = Action(self.x, self.y, self.x - 1, self.y - 1)
                    a.set_passant(self.x - 1, self.y)
                    actions.append(a)
            if right and isinstance(board[self.y][self.x + 1].piece, Pawn):
                if board[self.y][self.x + 1].piece.just_doubled:
                    a = Action(self.x, self.y, self.x + 1, self.y - 1)
                    a.set_passant(self.x - 1, self.y)
                    actions.append(a)
        return actions


class Rook(Piece):
    def __str__(self):
        if self.color == BLACK:
            return Fore.BLACK + Style.BRIGHT + " r "
        else:
            return Fore.LIGHTWHITE_EX + Style.BRIGHT + " r "

    def find_actions(self, board):
        actions = []

        # LEFT
        i = 1
        while self.x - i >= 0 and board[self.y][self.x - i].is_empty():
            actions.append(Action(self.x, self.y, self.x - 1, self.y))
            i += 1
        # found opponent's piece
        if self.x - i >= 0 and board[self.y][self.x - i].piece.color == other_player(self.color):
            actions.append(Action(self.x, self.y, self.x - i, self.y))

        # RIGHT
        i = 1
        while self.x + i < 8 and board[self.y][self.x + i].is_empty():
            actions.append(Action(self.x, self.y, self.x + i, self.y))
            i += 1
        # found opponent's piece
        if self.x + i < 8 and board[self.y][self.x + i].piece.color == other_player(self.color):
            actions.append(Action(self.x, self.y, self.x + i, self.y))

        # UP
        i = 1
        while self.y - i >= 0 and board[self.y - i][self.x].is_empty():
            actions.append(Action(self.x, self.y, self.x, self.y - i))
            i += 1
        # found opponent's piece
        if self.y - i >= 0 and board[self.y - i][self.x].piece.color == other_player(self.color):
            actions.append(Action(self.x, self.y, self.x, self.y - i))

        # DOWN
        i = 1
        while self.y + i < 8 and board[self.y + i][self.x].is_empty():
            actions.append(Action(self.x, self.y, self.x, self.y + i))
            i += 1
        # found opponent's piece
        if self.y + i < 8 and board[self.y + i][self.x].piece.color == other_player(self.color):
            actions.append(Action(self.x, self.y, self.x, self.y + i))

        return actions


class Knight(Piece):
    def __str__(self):
        if self.color == BLACK:
            return Fore.BLACK + Style.BRIGHT + " h "
        else:
            return Fore.LIGHTWHITE_EX + Style.BRIGHT + " h "

    def find_actions(self, board):
        actions = []
        # LEFT UP
        if self.x > 1 and self.y > 0 and \
                (board[self.y + 1][self.x - 2].is_empty() or board[self.y + 1][self.x - 2].piece.color == other_player(self.color)):
            actions.append(Action(self.x, self.y, self.x - 2, self.y - 1))
        # LEFT DOWN
        if self.x > 1 and self.y < 7 and \
                (board[self.y + 1][self.x - 2].is_empty() or board[self.y + 1][self.x - 2].piece.color == other_player(self.color)):
            actions.append(Action(self.x, self.y, self.x - 2, self.y + 1))

        # RIGHT UP
        if self.x < 6 and self.y > 0 and \
                (board[self.y - 1][self.x + 2].is_empty() or board[self.y - 1][self.x + 2].piece.color == other_player(self.color)):
            actions.append(Action(self.x, self.y, self.x + 2, self.y - 1))
        # RIGHT DOWN
        if self.x < 6 and self.y < 7 and \
                (board[self.y + 1][self.x + 2].is_empty() or board[self.y + 1][self.x + 2].piece.color == other_player(self.color)):
            actions.append(Action(self.x, self.y, self.x + 2, self.y + 1))

        # DOWN LEFT
        if self.x > 0 and self.y < 6 and \
                (board[self.y + 2][self.x - 1].is_empty() or board[self.y + 2][self.x - 1].piece.color == other_player(self.color)):
            actions.append(Action(self.x, self.y, self.x - 1, self.y + 2))
        # DOWN RIGHT
        if self.x < 7 and self.y < 6 and \
                (board[self.y + 2][self.x + 1].is_empty() or board[self.y + 2][self.x + 1].piece.color == other_player(self.color)):
            actions.append(Action(self.x, self.y, self.x + 1, self.y + 2))

        # UP LEFT
        if self.x > 0 and self.y > 1 and \
                (board[self.y - 2][self.x - 1].is_empty() or board[self.y - 2][self.x - 1].piece.color == other_player(self.color)):
            actions.append(Action(self.x, self.y, self.x - 1, self.y - 2))
        # UP RIGHT
        if self.x < 7 and self.y > 1 and \
                (board[self.y - 2][self.x + 1].is_empty() or board[self.y - 2][self.x + 1].piece.color == other_player(self.color)):
            actions.append(Action(self.x, self.y, self.x + 1, self.y - 2))
        return actions


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
        print("Invalid selection. Try again.")
        return -1
    print(f"Selected {type(p).__name__} at {x_in}{y_in}")
    actions = p.find_actions(state.board)
    if len(actions) > 0:
        action_dict = dictify(actions)
        print(state.print_with_actions(actions, action_dict))
        print("Please enter the character associated with a move, or 'x' to cancel.")
        sel = input()
        if sel == 'x':
            return -1
        if not sel in action_dict:
            print("Invalid input. Please try again.")
            return -1
        action = action_dict.get(sel)
        state.apply_action(action)
        return 0

    else:
        print("Selected piece cannot move. Please try again.")
        return -1


def play():
    s = State()
    print(s)
    while True:
        x = user_move(s)
        while x == -1:
            print(s)
            x = user_move(s)
        s.to_move = other_player(s.to_move)
        print(s)


play()
