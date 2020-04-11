class Marble:
    def __init__(self, location, colour):
        '''Initialises a Marble object:
            Sets location and colour'''

        self.__location = location
        self.__colour = colour

    def move(self, location):
        '''Changes the location of the marble'''

        self.set_location(location)

    def check_rolls(self, marble_locations, hop_location=None, hoppable=False):
        '''Returns the possible locations the marble can roll to
        If hoppable is true the inverse is returned, it is only used in check hops
        By default the method checks this marble's hops, a different location can be used'''

        if hop_location is None:
            hop_location = self.__location

        possible_locations = []

        ###~~~Checking surrounding neighbours~~~###
        for extra in [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, 1), (1, -1)]: #[(+x), (-x), (+y), (-y), (+z), (-z)]
            x, y = hop_location

            extra_x, extra_y = extra
            neighbour_location = (x + extra_x, y + extra_y)
            #Checks the all possible rolls to see if a marble occupies that space

            if neighbour_location not in marble_locations and not hoppable:
                possible_locations.append(neighbour_location)
            if neighbour_location in marble_locations and hoppable:
                possible_locations.append((x + 2*extra_x, y + 2*extra_y)) #Hopped location
        ###~~~                               ~~~###

        return possible_locations

    def check_hops(self, marble_locations, locations, hop_location=None):
        '''Returns the possible locations the marble can hop to
        By default it checks for this marble but it can check a generic locations'''

        if hop_location is None:
            hop_location = self.__location

        x, y = self.get_location()
        mask_locations = self.__mask_locations(x, y, locations)
        allowed_locations = []

        ###~~~Remove locations with marbles~~~###
        for location in mask_locations:
            if location not in marble_locations:
                allowed_locations.append(location)
        ###~~~                             ~~~###

        possible_locations = []

        ###~~~The locations one hop away~~~###
        new_locations = self.check_rolls(marble_locations, hop_location=hop_location, hoppable=True)

        ###~~~Removes locations with marbles in them~~~###
        for location in new_locations:
            if location in allowed_locations:
                possible_locations.append(location)
        ###~~~                                      ~~~###

        ###~~~Repeat process for each new location added~~~###
        for location in possible_locations:
            new_locations = self.check_rolls(marble_locations, hop_location=location, hoppable=True)

            for new_location in new_locations:
                if new_location in allowed_locations and new_location not in possible_locations:
                    possible_locations.append(new_location)
        ###~~~                                          ~~~###
        #This terminates when no new locations are added
        #It works by adding to the array that is being looped so will continue until no more are added

        return possible_locations

    def __mask_locations(self, x_coord, y_coord, locations):
        '''Returns the locations that could be hopped to'''

        mask_locations = []

        #The locations are every second space
        #This extends from the marble location to the edges of the board

        for mask_x in range(x_coord-16, 17+x_coord, 2):
            for mask_y in range(y_coord-16, 17+y_coord, 2):
                masked = (mask_x, mask_y)

                if masked in locations:
                    mask_locations.append(masked)

        return mask_locations

    def get_colour(self):
        return self.__colour

    def get_location(self):
        return self.__location

    def set_location(self, location):
        self.__location = location

def main():
    pass

if __name__ == '__main__':
    main()
