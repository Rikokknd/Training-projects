import string
from typing import Tuple
import numpy

"""
из чего состоит игра
1. игровое поле 3 на 3
2. 2 игрока
3. игроки ходят по очереди, ставят в пустые клетки свою метку
   После каждого хода нужно отрисовывать состояние поля
4. игра заканчивается победой, когда на любой горизонтали, вертикали или диагонали образуется 3 метки от одного игрока
5. игра заканчивается ничьей, когда поле заполняется до конца

1. нужно сгенерировать поле - numpy массив 3 на 3?
2. добавить 2 игроков, которые ходит по очереди
3. после каждого хода нужно проверять поле на условия победы/ничьей
"""


class Player:
    """Класс игрока. Может контролироваться как человеком, так и компьютером.
    Должен получать состояние доски, и ставить свою метку в пустые клетки.
    Не может изменять уже заполненные клетки. 
    """

    def __init__(self, mark: str) -> None:
        self.human = None
        self.mark = mark
        self.choose_controller()

    def choose_controller(self):
        response = input("Please decide who controlls this player - (H)uman or (C)omputer : ").upper()
        while response != "H" and response != "C":
            response = input("Please respond with H or C : ").upper()
        if response == "H":
            self.human = True
        else:
            print(f"Sorry, AI is not supported right now.")
            exit()

    def make_turn(self, board: numpy.ndarray) -> tuple:
        def get_digit():
            choice = input("Please choose a cell to mark [1-9] : ")
            while not choice.isdigit() or int(choice) < 1 or int(choice) > 9:
                choice = input("Please use digits [1-9] : ")
            return int(choice)
        
        flat_board = board.ravel()
        while True:
            c = get_digit() - 1
            if flat_board[c] == 0:
                return (c, self.return_mark())
            else:
                print("This cell is unavailable.")

    def return_mark(self):
        return self.mark
        


class Game:
    def __init__(self) -> None:
        print("\n\nHello! This is Tic-Tac-Toe game. First, choose who controls players.")
        self.board = numpy.zeros((3, 3), dtype='b')
        self.player_one = None
        self.player_two = None
        # print(self.board)
        self.add_players()
        self.game_cycle()

    def add_players(self):
        print("\nPlayer one:")
        self.player_one = Player("X")
        print("\nPlayer two:")
        self.player_two = Player("O")

    def draw_board(self):
        print("\n")
        print(f" {' ' if self.board[0, 0] == '0' else self.board[0, 0]} | {' ' if self.board[0, 1] == '0' else self.board[0, 1]} | {' ' if self.board[0, 2] == '0' else self.board[0, 2]} ")
        print(f"---|---|---")
        print(f" {' ' if self.board[1, 0] == '0' else self.board[1, 0]} | {' ' if self.board[1, 1] == '0' else self.board[1, 1]} | {' ' if self.board[1, 2] == '0' else self.board[1, 2]} ")
        print(f"---|---|---")
        print(f" {' ' if self.board[2, 0] == '0' else self.board[2, 0]} | {' ' if self.board[2, 1] == '0' else self.board[2, 1]} | {' ' if self.board[2, 2] == '0' else self.board[2, 2]} ")

    def check_board(self):
        pass

    def game_cycle(self):
        print("\nGame start!")
        player_one_move = True
        while True:
            while player_one_move is True:
                self.draw_board()
                print(f"Player {self.player_one.return_mark()}:")
                cell, mark = self.player_one.make_turn(self.board)
                self.board[cell] = mark
                player_one_move = False

            self.check_board()

            while player_one_move is False:
                self.draw_board()
                print(f"Player {self.player_two.return_mark()}:")
                cell, mark = self.player_two.make_turn(self.board)
                self.board[cell] = mark
                player_one_move = True

            self.check_board()

if __name__ == "__main__":
    Game()
