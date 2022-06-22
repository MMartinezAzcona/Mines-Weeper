import random
import re


class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # Create board & plant the bombs
        self.board = self.make_new_board()
        self.assig_values_to_boad()

        # Initialize a set to keep track of uncovered locations
        self.dug = set()

    def make_new_board(self):
        # Construct new board based on dim_size and num_bombs
        # We should construct the list of lists here

        # Generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # Plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                continue

            board[row][col] = '*'

    def assig_values_to_boad(self):
        # Assigns how many neighbouring bombs are in each location
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # If it's a bomb we don´t want to calculate anything
                    continue
                self.board[r][c] = self.get_neighboring_bombs(r, c)

    def get_neighboring_bombs(self, row, col):
        # Iterate over each neighbor location and sum up the number of bombs
        num_neighbor_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size, (row+1)+1)):
            for c in range(max(0, col-1), min(self.dim_size, (col+1)+1)):
                if r == row and c == col:
                    continue
                elif self.board[r][c] == '*':
                    num_neighbor_bombs += 1

    def dig(self, row, col):
        # Returns TRUE if successful dig and FALSE if there is a bomb
        """
        Scenarios:
            - hit a bomb --> game over
            - dig a location with neighboring bombs -> finish dig
            - dig a location with no neighboring bombs -> recursive dig
        """
        self.dug.add((row, col)) # Keep track where we dug
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row-1), min(self.dim_size, (row+1)+1)):
            for c in range(max(0, col-1), min(self.dim_size, (col+1)+1)):
                if (r, c) in self.dug:
                    continue  # Dont dig where you've already dug
                self.dig(r, c)

        return True

    def __str__(self):
        # Returns a string that displays the board
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        string_rep = ''
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % col)
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep


def play(dim_size=10, num_bombs=10):
    # Step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # Step 2: show the user the board and ask for where they want to dig
    # Step 3a: if location is a bomb --> GAME OVER
    # Step 3a: if location not a bomb --> dig recursively until each square is at next to a bomb
    # Step 4: Repeat steps 2 & 3 until no more places to  dig

    safe = Tr

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Dig! (input as row,column): "))
        row, col = int(user_input[0]), int(user_input[-1])

        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Invalid location. Try again")
            continue

        safe = board.dig(row, col)

        if not safe:
            # Dug a boom! Game Over
            break

    if safe:
        print("Congrats! You won!")
    else:
        print("GAME OVER...")

    # reveal the board
    board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
    print(board)


if __name__ == '__main__':

    play()