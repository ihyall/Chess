class Board():
    def __init__(self):
        let = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        for i in range(8):
            if 0 <= i <= 1:
                side = 'black'
            elif 6 <= i <= 7:
                side = 'white'
            for j in range(8):
                if i == 0 or i == 7:
                    if let[j] == 'r':
                        Rook(i, j, side)
                    elif let[j] == 'n':
                        Knight(i, j, side)
                    elif let[j] == 'b':
                        Bishop(i, j, side)
                    elif let[j] == 'q':
                        Queen(i, j, side)
                    elif let[j] == 'k':
                        King(i, j, side)
                elif i == 1 or i == 6:
                    if j == 2 or j == 5:
                        Lancer(i, j, side)
                    elif j == 1 or j == 6:
                        Stunner(i, j, side)
                    elif j == 3 or j == 4:
                        Minister(i, j, side)
                    else:
                        Pawn(i, j, side)
                else:
                    Empty(i, j)

    def printboard(self):
        let = [chr(i + 65) for i in range(8)]
        num = list(range(8, 0, -1))
        visboard = []
        fcoord = [(i.x, i.y) for i in Figure.figlist]
        for i in range(12):
            visboard.append([])
            if i == 1:
                visboard[i].append('    ________________________    ')
            elif i == 10:
                visboard[i].append('    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾    ')
            elif i == 0 or i == 11:
                for j in range(12):
                    if j == 0 or j == 10:
                        visboard[i].append('\x1B[1;49m     \x1B[0m')
                    elif j == 1 or j == 11:
                        visboard[i].append('')
                    else:
                        visboard[i].append(let[j - 2])
                        visboard[i].append('\x1B[1;49m  \x1B[0m')
            else:
                visboard[i].append(num[i - 2])
                visboard[i].append('  |')
                for j in range(8):
                    if (i - 2, j) in fcoord:
                        visboard[i].append(Figure.figlist[fcoord.index((i - 2, j))])
                visboard[i].append('|  ')
                visboard[i].append(num[i - 2])
        for i in range(len(visboard)):
            for j in range(len(visboard[i])):
                if 2 <= i <= 9 and 2 <= j <= 9:
                    if i % 2 != j % 2:
                        if visboard[i][j].hl == True:
                            print('\x1B[38;2;255;0;0;48;2;0;0;0m', visboard[i][j], '\x1B[0m', end='')
                        elif visboard[i][j].__class__.__name__ == 'Empty':
                            print('\x1B[38;2;0;0;0;48;2;0;0;0m', visboard[i][j], '\x1B[0m', end='')
                        else:
                            print('\x1B[38;2;255;255;255;48;2;0;0;0m', visboard[i][j], '\x1B[0m', end='')
                    elif i % 2 == j % 2:
                        if visboard[i][j].hl == True:
                            print('\x1B[38;2;200;0;0;48;2;200;200;200m', visboard[i][j], '\x1B[0m', end='')
                        elif visboard[i][j].__class__.__name__ == 'Empty':
                            print('\x1B[38;2;200;200;200;48;2;200;200;200m', visboard[i][j], '\x1B[0m', end='')
                        else:
                            print('\x1B[38;2;0;0;0;48;2;200;200;200m', visboard[i][j], '\x1B[0m', end='')
                else:
                    print(visboard[i][j], end='')
            else:
                print()
        print('\n', f'Move {counter}. {"Black" if counter % 2 == 0 else "White"} side chooses a move: ', end='')


class Figure():
    let = [chr(i + 97) for i in range(8)]
    figlist = []

    def __init__(self, x, y, side, hl=False, stunned=False):
        self.x = x
        self.y = y
        self.side = side
        self.hl = hl
        self.stunned = stunned
        Figure.figlist.append(self)

    @property
    def coord(self):
        return Figure.coords_to_key(self.x, self.y)

    @staticmethod
    def coords_to_key(x, y):
        return Figure.let[y] + str(8 - x)

    @staticmethod
    def key_to_coords(c2):
        try:
            q = 8 - int(c2[1]), Figure.let.index(c2[0])
            return q
        except:
            return False

    def move(self, c2):
        fcoord = [(i.x, i.y) for i in Figure.figlist]
        try:
            if (self.side == 'black' and counter % 2 != 0) or (self.side == 'white' and counter % 2 == 0):
                raise
            else:
                x2, y2 = Figure.key_to_coords(c2)
                self.x, Figure.figlist[fcoord.index((x2, y2))].x = x2, self.x
                self.y, Figure.figlist[fcoord.index((x2, y2))].y = y2, self.y

        except:
            print('You wrote wrong coordinates, try again', end=': ')
            return False

    def eat(self):
        self.__class__ = Empty

    @staticmethod
    def search(c):
        fkey = [i.coord for i in Figure.figlist]
        try:
            a = Figure.figlist[fkey.index(c)]
            return a
        except:
            print('You chose wrong figure, try again', end=': ')
            return False

    @staticmethod
    def search_by_coords(c1, c2):
        fcoord = [(i.x, i.y) for i in Figure.figlist]
        return Figure.figlist[fcoord.index((c1, c2))]

    @classmethod
    def reset_highlight(cls):
        for i in range(len(Figure.figlist)):
            Figure.figlist[i].hl = False

    def dir_check(self, c2):
        if self.__class__.__name__ == 'Knight' or self.__class__.__name__ == 'Lancer':
            return True
        q = self.delta(c2)
        if abs(q[0]) == abs(q[1]):
            for i in range(min(self.x, self.x + q[0]) + 1, max(self.x, self.x + q[0])):
                for j in range(min(self.y, self.y + q[1]) + 1, max(self.y, self.y + q[1])):
                    if abs(self.x - i) == abs(self.y - j):
                        if Figure.search_by_coords(i, j).__class__.__name__ != 'Empty' and Figure.search_by_coords(i,
                                                                                                                   j) != self:
                            return False
                        elif self.side == Figure.search(c2).side:
                            return False
            if Figure.search(c2).side == 'empty':
                return True
            else:
                return 'eat' if not self.__class__.__name__ == 'Stunner' else True
        elif q[0] and not (q[1]):
            for i in range(min(self.x, self.x + q[0]) + 1, max(self.x, self.x + q[0])):
                if Figure.search_by_coords(i, self.y).__class__.__name__ != 'Empty' and Figure.search_by_coords(i,
                                                                                                                self.y) != self:
                    return False
                elif self.side == Figure.search(c2).side:
                    return False
            if Figure.search(c2).side == 'empty':
                return True
            else:
                return 'eat' if not self.__class__.__name__ == 'Stunner' else True
        elif not (q[0]) and q[1]:
            for j in range(min(self.y, self.y + q[1]) + 1, max(self.y, self.y + q[1])):
                if Figure.search_by_coords(self.x, j).__class__.__name__ != 'Empty' and Figure.search_by_coords(self.x,
                                                                                                                j) != self:
                    return False
                elif self.side == Figure.search(c2).side:
                    return False
            if Figure.search(c2).side == 'empty':
                return True
            else:
                return 'eat' if not self.__class__.__name__ == 'Stunner' else True
        return False

    def delta(self, c2):
        try:
            return (Figure.key_to_coords(c2)[0] - self.x, Figure.key_to_coords(c2)[1] - self.y)
        except:
            return 0, 0

    @classmethod
    def checkmate(cls):
        k = []
        for i in range(len(Figure.figlist)):
            if Figure.figlist[i].__class__.__name__ == 'King':
                k.append(Figure.figlist[i].side)
        if not 'white' in k:
            return 'Black'
        elif not 'black' in k:
            return 'White'
        else:
            return False


class Rook(Figure):
    def __init__(self, x, y, side):
        super().__init__(x, y, side)
        super().coord

    def __str__(self):
        return 'r' if self.side == 'black' else 'R'

    def move_check(self, c2):
        if (abs(self.delta(c2)[0]) and not (self.delta(c2)[1])) or (
                abs(self.delta(c2)[1]) and not (self.delta(c2)[0])) and self.side != Figure.search(c2).side:
            return True
        else:
            return False


class Knight(Figure):
    def __init__(self, x, y, side):
        super().__init__(x, y, side)
        super().coord

    def __str__(self):
        return 'n' if self.side == 'black' else 'N'

    def move_check(self, c2):
        if ((abs(self.delta(c2)[0]) == 1 and abs(self.delta(c2)[1]) == 2) or (
                abs(self.delta(c2)[1]) == 1 and abs(self.delta(c2)[0]) == 2)) and self.side != Figure.search(c2).side:
            return True
        else:
            return False


class Bishop(Figure):
    def __init__(self, x, y, side):
        super().__init__(x, y, side)
        super().coord

    def __str__(self):
        return 'b' if self.side == 'black' else 'B'

    def move_check(self, c2):
        if abs(self.delta(c2)[0]) == abs(self.delta(c2)[1]) != 0:
            return True
        else:
            return False


class Queen(Figure):
    def __init__(self, x, y, side):
        super().__init__(x, y, side)
        super().coord

    def __str__(self):
        return 'q' if self.side == 'black' else 'Q'

    def move_check(self, c2):
        if (abs(self.delta(c2)[0]) and not (self.delta(c2)[1])) or (
                abs(self.delta(c2)[1]) and not (self.delta(c2)[0])) or abs(self.delta(c2)[0]) == abs(
                self.delta(c2)[1]) != 0:
            return True
        else:
            return False


class King(Figure):
    def __init__(self, x, y, side):
        super().__init__(x, y, side)
        super().coord

    def __str__(self):
        return 'k' if self.side == 'black' else 'K'

    def move_check(self, c2):
        if 0 < (abs(self.delta(c2)[0]) + abs(self.delta(c2)[1])) <= 2:
            return True
        else:
            return False


class Pawn(Figure):
    def __init__(self, x, y, side):
        super().__init__(x, y, side)
        super().coord

    def __str__(self):
        return 'p' if self.side == 'black' else 'P'

    def move_check(self, c2):
        if self.side == 'black' and counter % 2 == 0:
            if self.x == 1:
                if 1 <= self.delta(c2)[0] <= 2 and self.delta(c2)[1] == 0:
                    return True
                else:
                    return False
            elif self.delta(c2)[0] == 1 and self.delta(c2)[1] == 0 and Figure.search(c2).side != 'white':
                return True
            elif self.delta(c2)[0] == 1 and abs(self.delta(c2)[1]) == 1 and Figure.search(c2).side == 'white':
                return True
            else:
                return False
        elif self.side == 'white' and counter % 2 == 1:
            if self.x == 6:
                if -1 >= self.delta(c2)[0] >= -2 and self.delta(c2)[1] == 0:
                    return True
                else:
                    return False
            elif self.delta(c2)[0] == -1 and abs(self.delta(c2)[1]) == 0 and Figure.search(c2).side != 'black':
                return True
            elif self.delta(c2)[0] == -1 and abs(self.delta(c2)[1]) == 1 and Figure.search(c2).side == 'black':
                return True
            else:
                return False


class Lancer(Figure):
    def __init__(self, x, y, side):
        super().__init__(x, y, side)
        super().coord

    def __str__(self):
        return 'l' if self.side == 'black' else 'L'

    def move_check(self, c2):
        if self.side == 'black' and 'counter%2 == 0':
            if abs(self.delta(c2)[1]) in [0, 1] and Figure.search(c2).side != 'black':
                if self.delta(c2)[0] == 1 and Figure.search(c2).side != 'white':
                    return True
                elif self.delta(c2)[0] == 2 and Figure.search(c2).side == 'white':
                    return 'eat'
                else:
                    return False
        elif self.side == 'white' and 'counter%2 == 1' and Figure.search(c2).side != 'white':
            if abs(self.delta(c2)[1]) in [0, 1]:
                if self.delta(c2)[0] == -1 and Figure.search(c2).side != 'black':
                    return True
                elif self.delta(c2)[0] == -2 and Figure.search(c2).side == 'black':
                    return 'eat'
                else:
                    return False


class Stunner(Figure):
    def __init__(self, x, y, side):
        super().__init__(x, y, side)
        super().coord

    def __str__(self):
        return 's' if self.side == 'black' else 'S'

    def move_check(self, c2):
        if Figure.search(c2).side != 'empty' and Figure.search(c2).side != self.side:
            return 'stun'
        elif abs(self.delta(c2)[0]) == abs(self.delta(c2)[1]) != 0:
            return True
        else:
            return False


class Minister(Figure):
    def __init__(self, x, y, side):
        super().__init__(x, y, side)
        super().coord

    def __str__(self):
        return 'm' if self.side == 'black' else 'M'

    def move_check(self, c2):
        if abs(self.delta(c2)[0]) == abs(self.delta(c2)[1]) == 1:
            return True
        else:
            return False


class Empty(Figure):
    def __init__(self, x, y, hl=False):
        self.x = x
        self.y = y
        self.side = 'empty'
        self.hl = hl
        Figure.figlist.append(self)

    def __str__(self):
        return '•'

    @property
    def coord(self):
        return Figure.coords_to_key(self.x, self.y)


board = Board()
counter = 1
board.printboard()
while True:
    if Figure.checkmate():
        print('they are not')
        print(f'{Figure.checkmate()} won!')
        break
    m = input()
    if m == 'stop':
        break
    f = 'P'
    for i in ['K', 'Q', 'R', 'N', 'B', 'S', 'L', 'M']:
        if i in m:
            f = i
            m = m.replace(i, '', 1)
            break
    m = m.split('-')
    if len(m) == 2:
        if Figure.search(m[0]) and Figure.search(m[1]):
            if not Figure.search(m[0]) or Figure.search(m[0]).side == 'empty':
                print('You wrote wrong coordinates, try again', end=': ')
                continue
            elif Figure.search(m[0]).stunned == True:
                print('This figure is stunned. Try choosing another one', end=': ')
                continue
            else:
                fig = Figure.search(m[0])
            if fig.__class__.__name__ != 'Stunner' and not (fig.dir_check(m[1]) and fig.move_check(m[1])) or str(
                    fig).upper() != f:
                print('You wrote wrong coordinates, try again', end=': ')
                continue
            elif fig.move_check(m[1]) == 'stun':
                Figure.search(m[1]).stunned = True
                counter += 1
                print(f'Figure on {m[1]} was stunned', '\n')
                for i in range(len(Figure.figlist)):
                    if Figure.figlist[i].side == fig.side:
                        Figure.figlist[i].stunned = False
                board.printboard()
                continue
            elif fig.dir_check(m[1]) and fig.move_check(m[1]):
                if (fig.side == 'black' and counter % 2 != 0) or (fig.side == 'white' and counter % 2 == 0):
                    print('Wait for other side to make a move: ', end='')
                    continue
                elif fig.dir_check(m[1]) == 'eat' and fig.move_check(m[1]):
                    Figure.search(m[0]).move(m[1])
                    Figure.search(m[0]).eat()
                    counter += 1
                    print()
                    for i in range(len(Figure.figlist)):
                        if Figure.figlist[i].side == fig.side:
                            Figure.figlist[i].stunned = False
                    board.printboard()
                    continue
                elif fig.move_check(m[1]) == 'eat':
                    Figure.search(m[1]).eat()
                    counter += 1
                    print()
                    for i in range(len(Figure.figlist)):
                        if Figure.figlist[i].side == fig.side:
                            Figure.figlist[i].stunned = False
                    board.printboard()
                    continue
                else:
                    Figure.search(m[0]).move(m[1])
                    counter += 1
                    print()
                    for i in range(len(Figure.figlist)):
                        if Figure.figlist[i].side == fig.side:
                            Figure.figlist[i].stunned = False
                    board.printboard()
                    continue
    elif len(m) == 1:
        if not Figure.search(m[0]) or Figure.search(m[0]).side == 'empty':
            print('You wrote wrong coordinates, try again', end=': ')
            continue
        elif Figure.search(m[0]).stunned == True:
            print('This figure is stunned. Try choosing another one', end=': ')
            continue
        else:
            fig = Figure.search(m[0])
            if (fig.side == 'black' and counter % 2 != 0) or (fig.side == 'white' and counter % 2 == 0):
                print('Wait for other side to make a move: ', end='')
                continue
            for i in range(8):
                for j in range(8):
                    fig1 = Figure.search_by_coords(i, j)
                    if fig.move_check(fig1.coord) and fig.dir_check(fig1.coord) and fig.side != fig1.side:
                        fig1.hl = True
                    elif fig.move_check(fig1.coord) == 'stun':
                        fig1.hl = True
            print('\n' + 'Places you can make a move are marked red.')
            board.printboard()
            Figure.reset_highlight()
            continue
    else:
        continue