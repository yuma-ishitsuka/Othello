from othello import Board
from game import Game
from versus import Versus

def modechange():
    try:
        mode = int(input("一人遊びは0、CPU対戦は1を入力してください。>> "))
    except:
        print("入力が間違っています。")
        return modechange()
    if mode == 0:
        game.gameplay()
    elif mode == 1:
        versus.versus()
    else:
        print("0または1を入力してください。")
        return modechange()


if __name__ == "__main__":
    board = Board()
    game = Game()
    versus = Versus()
    modechange()
