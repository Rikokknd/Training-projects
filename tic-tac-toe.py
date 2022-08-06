import random
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

    def return_mark(self):
        return self.mark

    def choose_controller(self):
        response = input("Please decide who controlls this player - (H)uman or (C)omputer : ").upper()
        while response != "H" and response != "C":
            response = input("Please respond with H or C : ").upper()
        if response == "H":
            self.human = True
        else:
            self.human = False

    def make_turn(self, board: numpy.ndarray):
        def get_digit():
            choice = input("Please choose a cell to mark [1-9] : ")
            while not choice.isdigit() or int(choice) < 1 or int(choice) > 9:
                choice = input("Please use digits [1-9] : ")
            return int(choice)
        
        flat_board = board.ravel()
        if self.human == False:
            return self.make_turn_ai(flat_board)
        while True:
            c = get_digit() - 1
            if flat_board[c] == 0:
                return (c, self.return_mark())
            else:
                print("This cell is unavailable.")

    def make_turn_ai(self, board):
        possible_cells = []
        for pos, mark in enumerate(board):
            if mark == 0:
                possible_cells.append(pos)
        choice = random.choice(possible_cells)
        print(f"Computer marks a cell.")
        return (choice, self.return_mark())


class Game:
    def __init__(self) -> None:
        print("\n\nHello! This is Tic-Tac-Toe game. First, choose who controls players.")
        self.board = numpy.zeros((3, 3), dtype='O')
        self.player1 = None
        self.player2 = None
        self.player1_score = 0
        self.player2_score = 0
        self.add_players()
        self.game_cycle()

    def add_players(self):
        print("\nPlayer one:")
        self.player1 = Player("X")
        print("\nPlayer two:")
        self.player2 = Player("O")

    def draw_board(self):
        print("\n")
        print(f" {' ' if self.board[0, 0] == 0 else self.board[0, 0]} | {' ' if self.board[0, 1] == 0 else self.board[0, 1]} | {' ' if self.board[0, 2] == 0 else self.board[0, 2]} ")
        print(f"---|---|---")
        print(f" {' ' if self.board[1, 0] == 0 else self.board[1, 0]} | {' ' if self.board[1, 1] == 0 else self.board[1, 1]} | {' ' if self.board[1, 2] == 0 else self.board[1, 2]} ")
        print(f"---|---|---")
        print(f" {' ' if self.board[2, 0] == 0 else self.board[2, 0]} | {' ' if self.board[2, 1] == 0 else self.board[2, 1]} | {' ' if self.board[2, 2] == 0 else self.board[2, 2]} ")
        
    def check_board(self):
        rows_cols_diags = self.board.tolist() + self.board.transpose().tolist() + [self.board.diagonal().tolist()] + [numpy.fliplr(self.board).diagonal().tolist()]
        mark1 = self.player1.return_mark()
        mark2 = self.player2.return_mark()

        for line in rows_cols_diags:
            if len(set(line)) == 1 and set(line).pop() != 0:
                if set(line).pop() == mark1:
                    return 1
                elif set(line).pop() == mark2:
                    return 2
        
        if 0 not in self.board.ravel().tolist():
            return 0

        return None

    def game_cycle(self):
        print("\nGame start!")
        player_one_move = True
        while True:
            while player_one_move is True:
                self.draw_board()
                print(f"Player {self.player1.return_mark()}:")
                cell, mark = self.player1.make_turn(self.board)
                self.board[cell // 3, cell % 3] = mark
                player_one_move = False

            if self.check_board() is not None:
                return self.game_end(self.check_board())

            while player_one_move is False:
                self.draw_board()
                print(f"Player {self.player2.return_mark()}:")
                cell, mark = self.player2.make_turn(self.board)
                self.board[cell // 3, cell % 3] = mark
                player_one_move = True

            if self.check_board() is not None:
                return self.game_end(self.check_board())

    def game_end(self, result):
        self.draw_board()

        if result == 0:
            print("It's a tie!")
        elif result == 1:
            print("Player 1 wins!")
            self.player1_score += 1
        elif result == 2:
            print("Player 2 wins!")
            self.player2_score += 1
        else:
            print("Something went wrong!")

            
        print(f"Score: Player 1 - {str(self.player1_score)} wins, Player 2 - {str(self.player2_score)} wins.\n")

        if input("If you want to quit the game, type N : ").upper() == "N":
            exit("\nGoodbye!\n")
        else:
            self.board = numpy.zeros((3, 3), dtype='O')
            self.game_cycle()

        
if __name__ == "__main__":
    Game()
