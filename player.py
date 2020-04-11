import random
from marble import Marble

class Player:
    def __init__(self, data, colour, locations, triangles):
        '''Initialises a Player object:
            Sets the direction, type
            Creates 10 marbles with locations and colour'''

        self._direction = data[0]
        self._locations = locations
        marble_locations = data[1]
        self._marbles = [Marble(location, colour) for location in marble_locations]
        self._type = 'Generic'

    def _move(self, location, marble_index):
        '''Moves a marble to the given location'''

        marble = self._marbles[marble_index]
        marble.move(location)

    def update(self, marble_locations):
        '''A generic player will complete a random move'''
        found = False

        while not found:
            random_marble = random.choice(self._marbles)
            available_moves = self.get_available_moves(marble_locations, marble=random_marble)

            try:
                random_location = random.choice(available_moves)
                random_marble.move(random_location)
                found = True
            except:
                found = False

    def get_available_moves(self, marble_locations, marble=None):
        '''Returns the available locations for all marbles or a specific marble'''

        moves = []

        ###Retrieving all moves or those for a specific marble###
        if marble is not None:
            marbles = [marble]
        else:
            marbles = self._marbles

        for marble in marbles:
            marble_moves = []

            ###~~~Retrieving each marble's rolls and hops~~~###
            for location in marble.check_rolls(marble_locations):
                if location in self._locations:
                    marble_moves.append(location)
            for location in marble.check_hops(marble_locations, self._locations):
                if location in self._locations:
                    marble_moves.append(location)
            ###~~~                                      ~~~###

            if len(marbles) == 1: #If only one marble was passed
                moves = marble_moves
            else:
                moves.append(marble_moves)

        return moves

    def get_marbles(self):
        return self._marbles

    def get_direction(self):
        return self._direction

    def get_type(self):
        return self._type

def main():
    pass

if __name__ == '__main__':
    main()
