from game import Game
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

game = Game()
game.run()