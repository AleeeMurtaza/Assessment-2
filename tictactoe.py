import random

# Initialize an empty board
board = [" " for _ in range(9)]


def display_board():
    """Show the current game board in a neat 3x3 grid."""
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()


def is_winner(player):
    """Check Winner."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    return any(all(board[i] == player for i in combo) for combo in win_conditions)


def is_draw():
    """True if board is Full and Nobbody Wins."""
    return all(cell != " " for cell in board)


def make_move(position, player):
    """Make a move on a free cell."""
    if board[position] == " ":
        board[position] = player
        return True
    else:
        print("That spot is already taken. Try another one.")
        return False


def reset_board():
    """Clears the board for a new match."""
    global board
    board = [" " for _ in range(9)]


def get_computer_move():
    """Computer chooses a random empty cell."""
    available_moves = [i for i, cell in enumerate(board) if cell == " "]
    return random.choice(available_moves)


def play_pvp():
    """Human vs Human mode."""
    current_player = "X"
    while True:
        display_board()
        print(f"Player {current_player}'s turn. Choose a position (1-9):")

        try:
            choice = int(input("> ")) - 1
            if choice not in range(9):
                print("Please enter a number between 1 and 9.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if not make_move(choice, current_player):
            continue

        if is_winner(current_player):
            display_board()
            print(f" Player {current_player} wins!")
            break
        elif is_draw():
            display_board()
            print("Game Draw!")
            break

        current_player = "O" if current_player == "X" else "X"


def play_pvc():
    """Human vs Computer mode."""
    human = "X"
    computer = "O"
    current_player = human  # Human to start first.

    while True:
        display_board()
        if current_player == human:
            print("Your turn! Choose a position (1-9):")
            try:
                choice = int(input("> ")) - 1
                if choice not in range(9):
                    print(" Please enter a number between 1 and 9.")
                    continue
            except ValueError:
                print(" Invalid input. Please enter a number.")
                continue

            if not make_move(choice, human):
                continue
        else:
            print(" Computer's turn...")
            move = get_computer_move()
            make_move(move, computer)

        if is_winner(current_player):
            display_board()
            if current_player == human:
                print("You win!")
            else:
                print("Computer wins!")
            break
        elif is_draw():
            display_board()
            print("Game Draw!")
            break

        current_player = computer if current_player == human else human


def start_game():
    #Main menu
    print("Welcome to Tic Tac Toe!")

    while True:
        print("\nSelect an option:")
        print("1. Play vs Player")
        print("2. Play vs Computer")
        print("3. Quit")

        choice = input("> ")

        if choice == "1":
            reset_board()
            play_pvp()
        elif choice == "2":
            reset_board()
            play_pvc()
        elif choice == "3":
            print("Thanks for playing! Goodbye.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        #  Rematch Logic
        print()
        again = input("Would you like to play again? (y/n): ").lower()
        if again == "y":
            reset_board()
            continue
        else:
            print("Thanks for playing! Goodbye.")
            break


if __name__ == "__main__":
    start_game()
