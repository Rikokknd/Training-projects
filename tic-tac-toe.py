import random
import numpy


class Player:
    def __init__(self, mark: str) -> None:
        self.human = None
        self.random = None
        self.master = None
        self.mark = mark
        self.opponent = "X" if self.mark == "O" else "O"
        self.choose_controller()

    def return_mark(self):
        return self.mark

    def choose_controller(self):
        response = input("Please decide who controlls this player - (H)uman, (C)omputer or (M)aster : ").upper()
        while response not in ["H", "C", "M"]:
            response = input("Please respond with H, C or M : ").upper()
        if response == "H":
            self.human = True
        elif response == "C":
            self.random = True
        elif response == "M":
            self.master = True
        else:
            exit("Something went wrong...")

    def make_turn(self, board: numpy.ndarray):
        if self.human:
            return self.make_human_turn(board)
        elif self.random:
            return self.make_random_turn(board)
        elif self.master:
            return self.make_master_turn(board)

    def make_human_turn(self, _board: numpy.ndarray):
        def get_digit():
            choice = input("Please choose a cell to mark [1-9] : ")
            while not choice.isdigit() or int(choice) < 1 or int(choice) > 9:
                choice = input("Please use digits [1-9] : ")
            return int(choice)
        
        flat_board = _board.ravel()
        while True:
            c = get_digit() - 1
            if flat_board[c] == 0:
                return (c, self.return_mark())
            else:
                print("This cell is unavailable.")

    def make_random_turn(self, _board: numpy.ndarray):
        board = _board.ravel()
        possible_cells = []
        for pos, mark in enumerate(board):
            if mark == 0:
                possible_cells.append(pos)
        choice = random.choice(possible_cells)
        print(f"Computer '{self.mark}' marks a cell.")
        return (choice, self.return_mark())

    def make_master_turn(self, __board: numpy.ndarray):

        def minmaxer(_board: numpy.ndarray, my_turn=True):
            """Определяет, какая из свободных клеток самая выгодная. Возвращает [оценка клетки, номер клетки]."""

            def worsest_cell(list_of_worst_cells: list):
                """Определяет наихудшую клетку из списка. Наихудшая - клетка, которая встречается чаще всего.
                Если таких клеток больше 1, то худшая из них - нечетная (определено опытным путем)."""

                score = list_of_worst_cells[0][0]

                # убираем оценки, превращаем список в одномерный
                clean_list = [cell[1] for cell in worst_cells]

                cell, counts = numpy.unique(numpy.array(clean_list), return_counts=True)

                most_occurent_worst_cells = []

                # отбираем в список номера клеток, которые встречаются чаще всего
                for i in range(len(counts)):
                    if counts[i] == max(counts):
                        most_occurent_worst_cells.append(cell[i])

                if len(most_occurent_worst_cells) == 1:
                    # если такая клетка всего одна
                    return [score, most_occurent_worst_cells[0]]
                else:
                    # отбираем из списка нечетные клетки
                    odd_cells = [num for num in most_occurent_worst_cells if num % 2 == 1]

                    if odd_cells:
                        # если такие есть, возвращаем первую попавшуюся нечетную
                        return [score, odd_cells[0]]
                    else:
                        # иначе возвращаем первую попавшуюся
                        return [score, most_occurent_worst_cells[0]]
            
            possible_cells = []
            for pos, fill in enumerate(_board.ravel().tolist()): # собираем список свободных клеток
                if fill == 0:
                    possible_cells.append([0, pos + 1]) # 0 - score, pos - cell position
            if [0, 5] in possible_cells: # если центр свободен, ставим метку туда
                return [0, 5]
            if len(possible_cells) >= 8: # если на доске стоит только одна марка и она в центре - занимаем случайную нечетную ячейку 
                return random.choice([cell for cell in possible_cells if cell[1] % 2 == 1])

            # в результате работы этого цикла собирается информация, 
            # за какое кол-во ходов игрок, совершающий ход, сможет закончить игру.
            for cell in range(len(possible_cells)):
                # Создаем копию поля и пытаемся ставить нашу метку в разные доступные клетки
                new_board = _board.copy()
                new_board[(possible_cells[cell][1] - 1) // 3, (possible_cells[cell][1] - 1) % 3] = self.mark if my_turn == True else self.opponent

                result = Game.check_board(new_board)
                if result != 0 and result is not None:
                    # если в результате последней установки марки в ячейку один из игроков побеждает
                    # этой ячейке назначается оценка. Если это наш игрок то оценка положительная
                    # если оппонент то отрицательная. Величина оценки исходит из того, сколько
                    # свободных клеток остается на доске - чем больше свободных клеток, 
                    # тем раньше завершилась игра, тем выше оценка
                    score = len(possible_cells) * (-1 if my_turn == False else 1)
                    possible_cells[cell][0] = score
                elif result == 0:
                    # Если в результате последней установки марки в ячейку игра завершается ничьей - оценка 0
                    possible_cells[cell][0] = 0
                else:
                    # наполняем possible_cells всеми вариантами завершения игры, позже отберем самые лучшие и худшие
                    possible_cells.append(minmaxer(new_board, my_turn=(False if my_turn == True else True)))

            
            best_cells = []
            worst_cells = []
            best_option = None

            # отбираем лучшие и худшие варианты развития событий 
            for cell in possible_cells:
                if cell[0] == max(possible_cells)[0]:
                    best_cells.append(cell)
                elif cell[0] == min(possible_cells)[0]:
                    worst_cells.append(cell)

            # Выбираем самый лучший вариант хода:

            if not worst_cells: 
                # если все варианты развития имеют одинаковую оценку - функция min() не возвращает значений, 
                # поэтому этот лист может быть пустым. Возвращаем любой из них
                best_option = random.choice(best_cells)

            elif best_cells[0][0] < abs(worst_cells[0][0]):
                # если оценка(а с ней и вероятность завершения игры) у противника выше чем у нас - 
                # отбираем самый худший вариант развития событий и блокируем его
                best_option = worsest_cell(worst_cells)

            elif len(worst_cells) > len(best_cells):
                # если плохих вариантов развития игры больше чем хороших - 
                # отбираем самый худший вариант развития событий и блокируем его
                best_option = worsest_cell(worst_cells)

            else:
                # в остальных случаях выбираем любой из наилучших вариантов
                best_option = random.choice(best_cells)
            
            return best_option

        master_turn = minmaxer(__board)
        return (master_turn[1]-1, self.return_mark())


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
        
        def drw(content):
            return ' ' if content == 0 else content

        brd = self.board

        print("\n")
        print(f" {drw(brd[0, 0])} | {drw(brd[0, 1])} | {drw(brd[0, 2])} ")
        print(f"---|---|---")
        print(f" {drw(brd[1, 0])} | {drw(brd[1, 1])} | {drw(brd[1, 2])} ")
        print(f"---|---|---")
        print(f" {drw(brd[2, 0])} | {drw(brd[2, 1])} | {drw(brd[2, 2])} ")
        
    def check_board(board):
        """Возвращает марку победителя если находит 3 одинаковых марки на линии. Возвращает 0 при ничьей. None если игра продолжается."""
        # собираем в список все отрезки, которые нужно проверить - ряды, столбцы, диагонали
        rows_cols_diags = board.tolist() + board.transpose().tolist() + [board.diagonal().tolist()] + [numpy.fliplr(board).diagonal().tolist()]

        for line in rows_cols_diags:
            if len(set(line)) == 1 and set(line).pop() != 0:
                # если в линии все марки одинаковые и это не пустые места - конец игры, возвращаем марку победителя
                return set(line).pop()
        
        if 0 not in board.ravel().tolist():
            # если на поле не осталось свободных ячеек - это ничья
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

            if Game.check_board(self.board) is not None:
                return self.game_end(Game.check_board(self.board))

            while player_one_move is False:
                self.draw_board()
                print(f"Player {self.player2.return_mark()}:")
                cell, mark = self.player2.make_turn(self.board)
                self.board[cell // 3, cell % 3] = mark
                player_one_move = True

            if Game.check_board(self.board) is not None:
                return self.game_end(Game.check_board(self.board))

    def game_end(self, result):
        self.draw_board()

        if result == 0:
            print("It's a tie!")

        elif result == self.player1.return_mark():
            print("Player 1 wins!")
            self.player1_score += 1

        elif result == self.player2.return_mark():
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
