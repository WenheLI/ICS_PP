class base:
    def __init__(self):
        self.m = [[0 for i in range(8)] for x in range(8)]

    def set_it(self, ele, x_pos, y_pos):
        if not self.is_on_board(x_pos, y_pos) or self.m[x_pos][y_pos] != 0:
            return False

        self.m[x_pos][y_pos] = ele

        otherTile = -1 * ele

        tot_flip = []
        for x_delta, y_delta in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = x_pos, y_pos
            x += x_delta
            y += y_delta
            if self.is_on_board(x, y) and self.m[x][y] == otherTile:
                x += x_delta
                y += y_delta
                if not self.is_on_board(x, y):
                    continue
                while self.m[x][y] == otherTile:
                    x += x_delta
                    y += y_delta
                    if not self.is_on_board(x, y):
                        break
                if not self.is_on_board(x, y):
                    continue
                if self.m[x][y] == ele:
                    while True:
                        x -= x_delta
                        y -= y_delta
                        if x == x_pos and y == y_pos:
                            break
                        tot_flip.append([x, y])
        self.m[x_pos][y_pos] = 0

        if len(tot_flip) == 0:
            return False
        else:

            return tot_flip

    def is_on_board(self, x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    def init(self):
        self.m[3][3] = -1
        self.m[4][3] = 1
        self.m[3][4] = 1
        self.m[4][4] = -1

    def flap(self, ele, x, y):
        ans = self.set_it(ele, x, y)
        r = -1 * ans
        if ans:
            print(ans)
            self.m[x][y] = ele
            for point in ans:
                print(point)
                self.m[point[0]][point[1]] = ele
            return True
        else:
            return False





            # def flap(self):

            # state = False
            # con = []
            # for x in range(1, 8):
            #     for y in range(1, 8):
            #         color = self.m[x][y]
            #         if color != 0:
            #             for i in range(-1, 2):
            #                 for n in range(-1, 2):
            #                     if i == n == 0:
            #                         continue
            #                     else:
            #                         if self.m[x+i][y+n] != color and self.m[x+i][y+n] != 0:
            #                             x = x+i
            #                             y = y+n
            #                             con.append([x, y])
            #                             if self.m[x][y] == color:
            #                                 state = True
            #                             while 0 < x < 7 and 0 < y < 7 and (self.m[x][y] != 0 or self.m[x][y] != color):
            #                                 x += i
            #                                 y += n
            #                                 con.append([x, y])
            #                         if state:
            #                             for pos in con:
            #                                 self.m[pos[0]][pos[1]] = color
            #                                 state = False
            #                                 con = []

    def show(self):
        for i in range(8):
            if i == 0:
                print('         ', i + 1, '|    ', end='', sep='')
            else:
                print(i + 1, '|    ', end='')
        print()
        for x in range(8):
            for y in range(8):
                if y == 0:
                    print(x+1, '|     ',  self.m[x][y], end='|     ')
                else:
                    print(self.m[x][y], end='|     ')
            print()
            print()


if __name__ == '__main__':
    a = base()
    count = 0
    a.init()
    while True:

        if count % 2 == 0:
            ele = 1
        else:
            ele = -1
        a.show()
        x = int(input()) - 1
        y = int(input()) - 1
        if a.flap(ele, y, x):
            count += 1
            # a.show()

        # a.flap()
