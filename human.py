from player import Player

class Human(Player):
    def __init__(self, data, colour, locations, triangles):
        '''Initialises a Human object:
            Super calls the Player constructor
            Sets type
            Initialises selected marble and moves'''

        super().__init__(data, colour, locations, triangles)
        self._type = 'Human'
        self.__selected_marble = None
        self.__moves = []
        self.__next_turn = True #This is so that the game only moves onto the next player once the user places a marble

    def update(self, mouse_location, marble_locations):
        '''Allows the user to select and move marbles'''

        self.__next_turn = False

        if mouse_location is not None:

            ###~~~Choosing a marble~~~###
            for marble in self.get_marbles():
                marble_location = marble.get_location()

                if marble_location == mouse_location:
                    self.__selected_marble = marble
                    self.__moves = self.get_available_moves(marble_locations, marble)
            ###~~~                 ~~~###

            ###~~~Choosing a location~~~###
            if mouse_location in self.__moves:
                self.__selected_marble.move(mouse_location)
                self.__moves = []
                self.__selected_marble = None
                self.__next_turn = True #Now the game can move to the next player
            ###~~~                   ~~~###

    def reset(self):
        '''removes highlights and selected marbles'''
        self.__moves = []
        self.__selected_marble = None

    def is_next_turn(self):
        return self.__next_turn

    def get_moves(self):
        return self.__moves

    def get_selected_marble(self):
        return self.__selected_marble


def main():
    pass

if __name__ == '__main__':
    main()
