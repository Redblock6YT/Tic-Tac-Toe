#Coded with PyCharm IDE to help with syntax and debugging
#GitHub Copilot was used for educational help only

import os
import random

def clear():
    os.system('cls')


# An array which only contains move classes, which represent player moves
# throughout the game.
moves = []

# Styles: Two Player or Computer
play_style = "Computer"

player_1_piece = "X"
# If play style is computer, the computer will be considered player 2
player_2_piece = "O"

# Keeps track of whose turn it is
player_turn = None


def piece_selection(for_who):
    global player_1_piece, player_2_piece

    if for_who == "Computer":
        piece = random.choice(["X", "O"])
        if piece == "X":
            player_1_piece = "O"
        else:
            player_1_piece = "X"

        player_2_piece = piece
        print("Computer selected piece " + piece)
    else:
        while True:
            piece = input(for_who + ": Select a piece (X, O): ")
            if not (piece.upper() == "X" or piece.upper() == "O"):
                print("Invalid Piece. You can only select X or O")
            else:
                if for_who == "Player 1":
                    player_1_piece = piece.upper()
                    player_2_piece = "O" if piece.upper() == "X" else "X"
                else:
                    player_2_piece = piece.upper()
                    player_1_piece = "X" if piece.upper() == "O" else "O"
                print(for_who + " selected piece " + piece.upper())
                break


def get_move_at(x, y):
    global moves

    for move in moves:
        if move.x == x and move.y == y:
            return move
    return None


def request_computer_move():
    global player_1_piece, player_2_piece

    # Will return the space, x, and y values for the space the computer chooses.
    # https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy

    # Check diagonal wins
    print("Computer diagonal check...")
    # (Claude 3.7 Sonnet Thinking)
    # Check diagonals for winning moves or blocks
    # Diagonal 1: top-left to bottom-right
    diagonal1 = [get_move_at(0, 0), get_move_at(1, 1), get_move_at(2, 2)]
    # Diagonal 2: top-right to bottom-left
    diagonal2 = [get_move_at(2, 0), get_move_at(1, 1), get_move_at(0, 2)]

    # Check diagonal win opportunities and blocks
    for diagonal, coords in [(diagonal1, [(0, 0), (1, 1), (2, 2)]), (diagonal2, [(2, 0), (1, 1), (0, 2)])]:
        # First check for computer win (priority)
        computer_count = 0
        player_count = 0
        empty_position = None

        for i, move in enumerate(diagonal):
            if move is None:
                empty_position = coords[i]
            elif move.piece == player_2_piece:
                computer_count += 1
            elif move.piece == player_1_piece:
                player_count += 1

        # If computer has 2 in a row and there's an empty spot, take the win
        if computer_count == 2 and empty_position is not None:
            space_number = empty_position[0] + empty_position[1] * 3 + 1
            return [space_number, empty_position[0], empty_position[1]]

        # If player has 2 in a row and there's an empty spot, block them
        if player_count == 2 and empty_position is not None:
            space_number = empty_position[0] + empty_position[1] * 3 + 1
            return [space_number, empty_position[0], empty_position[1]]
    # End Claude Sonnet

    # Check where the computer has two in a row horizontally
    horizontal_streak = 0
    horizontal_streak_enemy = 0

    # An array that contains the x values of each move at the current y value
    computer_moves_at_y = []
    enemy_moves_at_y = []

    current_x = 0
    current_y = 0

    for i in range(9):
        move = get_move_at(current_x, current_y)
        if move is not None:
            if move.piece == player_2_piece:
                horizontal_streak += 1
                computer_moves_at_y.append(current_x)
            else:
                horizontal_streak_enemy += 1
                enemy_moves_at_y.append(current_x)

            if horizontal_streak == 2:
                computer_moves_at_y.sort()
                for x in range(3):
                    if x in computer_moves_at_y:
                        continue
                    else:
                        if get_move_at(x, current_y) is None:
                            return [i, x, current_y]
            elif horizontal_streak_enemy == 2:
                enemy_moves_at_y.sort()
                for x in range(3):
                    if x in enemy_moves_at_y:
                        continue
                    else:
                        if get_move_at(x, current_y) is None:
                            return [i, x, current_y]

        current_x += 1
        if current_x == 3:
            current_y += 1
            current_x = 0
            horizontal_streak = 0
            computer_moves_at_y = []



    # No moves two and a row horizontally, check vertically
    current_x = 0
    current_y = 0

    vertical_streak = 0
    vertical_streak_enemy = 0

    computer_moves_at_x = []
    enemy_moves_at_x = []

    for i in range(9):
        move = get_move_at(current_x, current_y)
        if move is not None:
            if move.piece == player_2_piece:
                vertical_streak += 1
                computer_moves_at_x.append(current_x)
            else:
                vertical_streak_enemy += 1
                enemy_moves_at_x.append(current_x)

            if vertical_streak == 2:
                computer_moves_at_x.sort()
                for y in range(3):
                    if y in computer_moves_at_y:
                        continue
                    else:
                        if get_move_at(current_x, y) is None:
                            return [i, current_x, y]

        current_y += 1
        if current_y == 3:
            current_x += 1
            current_y = 0
            vertical_streak = 0
            vertical_streak_enemy = 0



    # Go for a corner space
    if get_move_at(0, 0) is None:
        return [0, 0, 0]
    elif get_move_at(2, 0) is None:
        return [3, 2, 0]
    elif get_move_at(0, 2) is None:
        return [7, 0, 2]
    elif get_move_at(2, 2) is None:
        return [9, 2, 2]

    # If there are no corner spaces, go for the center
    if get_move_at(1, 1) is None:
        return [5, 1, 1]

    # If there are no corner or center spaces, go for a side space
    # Copilot
    if get_move_at(1, 0) is None:
        return [2, 1, 0]
    elif get_move_at(0, 1) is None:
        return [4, 0, 1]
    elif get_move_at(2, 1) is None:
        return [6, 2, 1]
    elif get_move_at(1, 2) is None:
        return [8, 1, 2]

    # If there are no other spaces, just return the first empty space
    # Copilot
    for i in range(9):
        if get_move_at(i % 3, i // 3) is None:
            return [i + 1, i % 3, i // 3]


def request_move():
    global player_turn, player_1_piece, player_2_piece, moves

    game_status = check_board()
    if game_status == "No winner":
        clear()
        print("Move " + str(len(moves) + 1))
        print()
        print_board()
        print()
        print(player_turn + "'s Move")
        if player_turn == "Computer":
            computer_move = request_computer_move()
            move = Move("Computer", player_2_piece, computer_move[0], computer_move[1], computer_move[2])
            print(computer_move)
            print(move.print_string())
            moves.append(move)
            player_turn = "Player 1"
        else:
            while True:
                try:
                    space = int(input("Select a space (1-9): "))
                    if space < 1 or space > 9:
                        print("Invalid Space. You can only select a number between 1 and 9.")
                    elif get_move_at((space - 1) % 3, (space - 1) // 3) is not None:
                        print("Invalid Space. Space is already taken.")
                    else:
                        #Copilot
                        if player_turn == "Player 1":
                            moves.append(Move("Player 1", player_1_piece, space, (space - 1) % 3, (space - 1) // 3))
                            if play_style == "Computer":
                                player_turn = "Computer"
                            elif play_style == "Two Player":
                                player_turn = "Player 2"
                        elif player_turn == "Player 2":
                            moves.append(Move("Player 2", player_2_piece, space, (space - 1) % 3, (space - 1) // 3))
                            player_turn = "Player 1"
                        break
                except ValueError:
                    print("Invalid Space. You can only select a number between 1 and 9.")


        print()
        request_move()
    else:
        clear()
        print_board()
        print()
        print(game_status)


class Move:
    # Player: 'Player 1', 'Player 2', or 'Computer'
    # Piece: 'X' or 'O'
    # Space: number 1-9
    #
    def __init__(self, player, piece, space_number, x, y):
        self.player = player
        self.piece = piece
        self.space_number = space_number
        self.x = x
        self.y = y

    def print_string(self):
        print(self.player + " placed an " + self.piece + " at space " + str(self.space_number) + ". [" + str(self.x) + ", " + str(self.y) + "]")


# True - Match
# False - No Match
def check_match(piece, direction, x, y):
    if direction == "vertical":
        move1 = get_move_at(x, 0)
        move2 = get_move_at(x, 1)
        move3 = get_move_at(x, 2)

        if move1 is None or move2 is None or move3 is None:
            return False
        elif (not move1.piece == piece) or (not move2.piece == piece) or (not move3.piece == piece):
            return False
        else:
            return True
    elif direction == "diagonal":
        if x == 1 and not y == 1:
            return False
        elif not x == 1 and y == 1:
            return False

        move1 = get_move_at(0, 0)
        move2 = get_move_at(1, 1)
        move3 = get_move_at(2, 2)

        if move1 is None or move2 is None or move3 is None:
            return False
        elif (not move1.piece == piece) or (not move2.piece == piece) or (not move3.piece == piece):
            move1 = get_move_at(2, 0)
            move2 = get_move_at(1, 1)
            move3 = get_move_at(0, 2)
            if move1 is None or move2 is None or move3 is None:
                return False
            elif (not move1.piece == piece) or (not move2.piece == piece) or (not move3.piece == piece):
                return False
            else:
                return True
        else:
            return True


def check_board():
    horizontal_streak_x = 0
    horizontal_streak_o = 0

    current_x = 0
    current_y = 0
    empty_moves = 9

    for i in range(9):
        move = get_move_at(current_x, current_y)
        if move is not None:
            empty_moves -= 1
            if move.piece == "O":
                horizontal_streak_o += 1
                horizontal_streak_x = 0
            elif move.piece == "X":
                horizontal_streak_o = 0
                horizontal_streak_x += 1

            if horizontal_streak_o == 3:
                return "O: Winner (Horizontal)"
            elif horizontal_streak_x == 3:
                return "X: Winner (Horizontal)"

            if check_match(move.piece, "vertical", current_x, current_y):
                return move.piece + ": Winner (Vertical)"
            elif check_match(move.piece, "diagonal", current_x, current_y):
                return move.piece + ": Winner (Diagonal)"

        current_x += 1
        if current_x == 3:
            horizontal_streak_o = 0
            horizontal_streak_x = 0
            current_y += 1
            current_x = 0
    if empty_moves == 0:
        return "X O: Draw"
    return "No winner"


def print_board():
    # A blank space will have ()
    # Other filled spaces will have an X or an O

    pending_string = ""

    current_x = 0
    current_y = 0

    for i in range(9):
        move = get_move_at(current_x, current_y)

        if move is not None:
            pending_string += " " + move.piece + " "
        else:
            pending_string += " - "

        current_x += 1
        if current_x == 3:
            current_y += 1
            current_x = 0

            print(pending_string)
            pending_string = ""


print("Welcome to Tic Tac Toe")
print()
print_board()
print()
print("Select a play style: 0 - Two Player; 1 - Computer")

while True:
    play_style_select = int(input("Enter your selection (0 or 1): "))

    try:
        if play_style_select == 0:
            # Two Player Style
            play_style = "Two Player"
            break
        elif play_style_select == 1:
            # Computer Play Style
            play_style = "Computer"
            break
        else:
            print("Invalid Value! Only input a number: 0 or 1")
    except ValueError:
        print("Invalid Value! Only input a number: 0 or 1")

clear()
print(play_style + " Selected")

if random.randint(0, 1) == 0:
    if play_style == "Two Player":
        print("Player 1 will go first")
        print()
        piece_selection("Player 1")
        player_turn = "Player 1"
    else:
        print("You will go first")
        print()
        piece_selection("Player 1")
        player_turn = "Player 1"
else:
    if play_style == "Two Player":
        print("Player 2 will go first")
        print()
        piece_selection("Player 2")
        player_turn = "Player 2"
    else:
        print("Computer will go first")
        print()
        piece_selection("Computer")
        player_turn = "Computer"

request_move()