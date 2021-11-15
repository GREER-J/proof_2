from controller import Controller
from view import Pygame_view
from Model.simulation import Simulation


def main():
    c = Controller(Simulation(), Pygame_view())
    c.start()


if(__name__ == '__main__'):
    main()
