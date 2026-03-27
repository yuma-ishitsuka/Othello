import numpy as np

WHITE = 1
BLACK = -1
BLANK = 0
BOARD_SIZE = 8
DIRECTION_LIST = [-1, 0, 1]

class Board:
    # 初期設定
    def __init__(self):
        self.cell = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.cell = self.cell.astype(int)
        self.cell[3][3] = self.cell[4][4] = 1
        self.cell[3][4] = self.cell[4][3] = -1
        self.current = BLACK
        self.pass_count = 0
        self.turn = 1

    # ターンチェンジ
    def turnchange(self):
        self.current *= -1
    def stonenumber(self):
        return self.stones
    
    # その座標が範囲内かチェック
    def rangecheck(self, x, y):
        if x == None: x = -1
        if y == None: y = -1
        if x < 0 or BOARD_SIZE <= x or y < 0 or BOARD_SIZE <= y:
            return False
        return True
    
    # その場所に置けるかどうかチェック
    def check_can_put(self, x, y):
        if not self.rangecheck(x, y):
            return False
        if not self.cell[x][y] == BLANK:
            return False
        elif not self.can_reverse_stone(x, y):
            return False
        else: return True

    # (dx, dy)方向にひっくり返せる石があるかどうか
    def can_reverse(self, dx, dy, x, y):
        if not self.rangecheck(x+dx, y+dy):
            return False
        length = 0
        while self.cell[x+dx][y+dy] == -self.current:
            x += dx
            y += dy
            length += 1
            if self.cell[x+dx][y+dy] == self.current:
                return length
        else:
            return False

    def can_reverse_stone(self, x, y):
        for dx in DIRECTION_LIST:
            for dy in DIRECTION_LIST:
                if dx == dy == 0:
                    continue
                elif not self.rangecheck(x+dx, y+dy):
                    continue
                elif not self.can_reverse(dx, dy, x, y):
                    continue
                else: return True

    def reverse_stone(self, x, y):
        for dx in DIRECTION_LIST:
            for dy in DIRECTION_LIST:
                length = self.can_reverse(dx, dy, x, y)
                if length == False:
                    length = 0
                if length > 0:
                    for j in range(length):
                        k = j + 1
                        self.cell[x+k*dx][y+k*dy] *= -1
    
    def display(self):
        print("---"*10)
        print("\n", end=" ")
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.cell[x][y] == WHITE:
                    print("W", end=" ")
                elif self.cell[x][y] == BLACK:
                    print("B", end=" ")
                else:
                    print("*", end=" ")
            print("\n", end=" ")
        print("\n", end=" ")

    def put_stone(self, x, y):
        if self.check_can_put(x, y):
            self.pass_count = 0
            self.cell[x][y] = self.current
            self.reverse_stone(x, y)
            self.turnchange()
            return True
        else:
            return False
        
    def check_put_place(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.check_can_put(x, y):
                    return True
                else:
                    continue
        return False