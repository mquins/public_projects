import re
from typing import List, Dict, Tuple


class Board:
    pieces: List[str] = ['#', '@']  # Pieces for player 1 and player 2
    blank_board: str = (
        "                "
        " ....|....|....|"
        " ....|....|....|"
        " ....|....|....|"
        " ....|....|....|"
        " ----+----+----+"
        " ....|....|....|"
        " ....|....|....|"
        " ....|....|....|"
        " ....|....|....|"
        " ----+----+----+"
        " ....|....|....|"
        " ....|....|....|"
        " ....|....|....|"
        " ....|....|....|"
        " ----+----+----+"
    )

    def __init__(self) -> None:
        self.game_board: List[List[str]] = [list(self.blank_board[i:i+16])
                                            for i in range(0, 256, 16)]

    def display(self) -> None:
        row: List[str]
        for row in self.game_board:
            print(' '.join(row))
        print()

    def pos_is_free(self, pos: List[int]) -> bool:
        x: int
        y: int
        x, y = pos
        return (self.game_board[x][y] != self.pieces[0]
                and self.game_board[x][y] != self.pieces[1])

    def add_piece(self, player: int, pos: List[int]) -> None:
        x: int
        y: int
        x, y = pos
        self.game_board[x][y] = self.pieces[player]

    def check_victory(self, player: int, pos: List[int]) -> bool:
        direction: Dict[str, Tuple[int, int]] = {
            'N': (-1, 0), 'S': (1, 0),
            'W': (0, -1), 'E': (0, 1),
            'NE': (-1, 1), 'NW': (-1, -1),
            'SE': (1, 1),  'SW': (1, -1)
        }
        count: Dict[str, int] = {
            'N': 0, 'S': 0, 'W': 0, 'E': 0,
            'NE': 0, 'NW': 0, 'SE': 0, 'SW': 0
        }

        d: str
        for d in direction:
            x: int
            y: int
            x, y = pos
            while (1 <= x <= 15 and 1 <= y <= 15
                    and self.game_board[x][y] == self.pieces[player]):
                count[d] += 1
                x += direction[d][0]
                y += direction[d][1]

        return (count['N'] + count['S'] == 6
                or count['W'] + count['E'] == 6
                or count['NE'] + count['SW'] == 6
                or count['NW'] + count['SE'] == 6)


def play_one_game() -> None:
    cur_board = Board()
    cur_board.display()
    player: int = 0

    while True:  # play until one player wins or quits
        while True:  # get and validate input from user for one move
            try:
                user_input: str = input(
                    f' Player {player + 1} "{Board.pieces[player]}", '
                    'please enter a position to place your piece, '
                    'or -1 to quit: ').strip()
                pos: List[int]
                pos = [int(i) for i in re.split(r"[\s,]+", user_input)]
                if len(pos) == 1 and pos[0] == -1:
                    return  # quit if -1 entered
                if len(pos) == 2 and 1 <= pos[0] <= 15 and 1 <= pos[1] <= 15:
                    if cur_board.pos_is_free(pos):
                        break  # position ok
                    else:
                        print(" That position is taken. Please enter another")
                else:
                    print(" Invalid number(s) entered. Please try again")
            except ValueError:
                print(" Please enter one or two integers, "
                      "separated by a comma and/or space")

        cur_board.add_piece(player, pos)
        cur_board.display()
        if (cur_board.check_victory(player, pos)):
            print(f" Congrats! Player {player + 1} wins!")
            break
        player = 1 - player


print("\n Welcome to gomoko!")
print(f' Player 1 Black is "{Board.pieces[0]}", and ')
print(f' Player 2 White is "{Board.pieces[1]}".')
print(" The top left position is 1, 1.")

while True:
    play_one_game()
    if input(" Do you want to play again? (y/n) ") == "n":
        break
