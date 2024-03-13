from engine.main import Game
import scriptblue
import scriptred

if __name__ == "__main__":
    G = Game((40, 40), scriptred, scriptblue)
    G.run_game()