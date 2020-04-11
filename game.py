from human import Human
from ai import AI
from handler import Handler

class Game:
    def __init__(self):
        '''Initialises the game object:
            Creates game window
            Creates game locations
            Creates player objects
            Sets current player'''

        self.__training = False

        ###~~~Creating a file handler~~~###
        self.__handler = Handler()

        ###~~~Settings up the game~~~###
        center = [(x, y) for x in range(-4, 5) for y in range(-4, 5)]
        triangle1 = [(x-4, y+5) for x in range(0, 5) for y in range(4-x)]
        triangle3 = [(x+5, y-4) for x in range(0, 5) for y in range(4-x)]
        triangle5 = [(x-4, y-4) for x in range(0, 5) for y in range(4-x)]
        triangle2 = [(-x+4, y+1) for x in range(0, 4) for y in range(x, 4)]
        triangle4 = [(-x+4, y-8) for x in range(0, 4) for y in range(x, 4)]
        triangle6 = [(-x-5, y+1) for x in range(0, 4) for y in range(x, 4)]
        self.__locations = center + triangle1 + triangle3 + triangle4 + triangle6 #Triangles 2 and 5 are contained in the centre

        self.__ending_triangles = [triangle4, triangle5, triangle6, triangle1, triangle2, triangle3] #Triangle 1 aims for triangle 4 and so on
        self.__triangle_order = [triangle1, triangle2, triangle3, triangle4, triangle5, triangle6]

        self.__mouse_location = None

    def start(self):
        '''Start the game'''

        ###~~~Setting up variables'''~~~###
        game_file = ''
        players = 0
        message = 'Input game file name'
        message_coordinates = (41, 50)
        ###~~~                       ~~~###

        while True:
            #Important note: gameloops will occur within this loop
            #Therefore finished or closed games return the menu

            ###~~~Retrieving events~~~###
            events = self.__handler.get_events()

            if events['quit']:
                self.__handler.quit()
                exit()

            ###~~~Retrieving the game file name~~~###
            if events['ready'] and game_file == '':
                game_file = self.__handler.get_text()
                self.__handler.set_files(game_file)

                message = 'Input number of players'
                message_coordinates = (26, 50)
            ###~~~                             ~~~###

            ###~~~Retrieving the number of players~~~###
            elif events['ready'] and game_file != '':
                text = self.__handler.get_text()
                num_humans = None

                try:
                    num_humans = int(text)

                    if 0 <= num_humans < 7:
                        self.__initialise(num_humans)
                    else:
                        raise ValueError

                    ###Reset Variables###
                    game_file = ''
                    message = 'Input game file name'
                    message_coordinates = (41, 50)
                except:
                    message = 'Input an integer'
                    message_coordinates = (67, 50)
            ###~~~                                ~~~###

            elif events['quit']:
                break
            ###~~~                ~~~###

            self.__handler.display_menu(message, message_coordinates)

    def train(self, game_file, sessions):
        self.__training = True

        for session in range(sessions):
            print(session, end='\n\n')

            self.__handler.set_files(game_file)
            self.__initialise(0)

            for player in self.__players:
                print(player.get_weight_matrix())
                print(player.get_weights(), end='\n\n')

        self.__handler.quit()
        quit()

    def __initialise(self, players):
        '''Starts the game by creating players with relevant locations'''

        colour_order = ['Red', 'Black', 'Blue', 'Green', 'White', 'Yellow']
        self.__players = []

        ###~~~Get the starting positions of marbles~~~###
        game_data = self.__handler.load()
        if game_data:
            starting_locations = []

            for key, value in game_data.items():

                ###Testing if it is locations or the counter varaible###
                try:
                    locations = []
                    for _, location in value.items():
                        locations.append(tuple(location))
                except:
                    self.__counter = value

                starting_locations.append(locations)
        else:
            starting_locations = self.__triangle_order
        ###~~~                                     ~~~###

        ###~~~Setup the relevent players and AIs with marble locations~~~###
        for i in range(players):
            triangle = starting_locations[i]
            colour = colour_order[i]
            self.__players.append(Human([i, triangle], colour, self.__locations, self.__ending_triangles))

        for i in range(6-players):
            triangle = starting_locations[i+players]
            colour = colour_order[i+players]
            self.__players.append(AI([i+players, triangle], colour, self.__locations, self.__ending_triangles))
        ###~~~                                                        ~~~###

        ###~~~Get configured weights~~~###
        weight_data = self.__handler.load('Weights')
        if weight_data != None:
            for i in range(len(self.__players)):
                if self.__players[i].get_type() == 'AI':
                    weights = weight_data[str(i)]

                    if weights is not None:
                        self.__players[i].set_weights(weights)
        ###~~~                     ~~~###

        self.__current_player = self.__players[0]
        self.__counter = 0
        self.__running = True
        self.__last_saved_player = None
        self.__save() #Save the starting state to return to it
        self.__run()

    def __run(self):
        '''Runs the gameloop and checks if the previous play just played a winning move'''

        while self.__running:
            self.__update()

            ###~~~Check if the last player won~~~###
            last_player = self.__players[(self.__counter-1) % len(self.__players)]

            if self.__has_won(last_player):
                if self.__training: #Closes the game session allowing another to be created
                    self.__running = False
                    break

                self.__handler.display_board()
                self.__finished(last_player)
            ###~~~                            ~~~###

            self.__current_player = self.__players[self.__counter % len(self.__players)]

            ###For training purposes, so that games come to a close without a winner###
            if self.__counter > 1200: #Limits the number of moves to 100 for AI training
                self.__running = False

                ready = False
                while not ready:
                    self.__handler.display_menu('AI session complete', (42, 50))
                    events = self.__handler.get_events()
                    ready = events['ready']

                    if events['quit']:
                        self.__handler.quit()
                        quit()
            ###                                                                     ###

    def __update(self):
        '''updates the individual players and marble location array, keeps track of mouse movements'''

        ###~~~Updating the marble locations~~~###
        self.__marble_locations = []

        for player in self.__players:
            for marble in player.get_marbles():
                self.__marble_locations.append(marble.get_location())
        ###~~~                             ~~~###

        if not self.__training:
            ###~~~Deal with events that occur~~~###
            self.__handler.display_board(self.__players, self.__current_player)
            events = self.__handler.get_events()

            if events['mouse_location'] is not None:
                self.__mouse_location = events['mouse_location']
            if events['redo'] is True:
                self.__redo()
            if events['quit'] is True:
                self.__handler.end_game()
                self.__running = False
            ###~~~                           ~~~###

        ###~~~Updating the player with the relevant information~~~###
        if self.__current_player.get_type() == 'Human':

            ###Only save once at the start of their go###
            if self.__last_saved_player is not self.__current_player:
                self.__save()
                self.__last_saved_player = self.__current_player

            self.__current_player.update(self.__mouse_location, self.__marble_locations)

            ###Only move on when the user has completed their go###
            if self.__current_player.is_next_turn():
                self.__last_saved_player = None
                self.__counter += 1

        elif self.__current_player.get_type() == 'AI':
            self.__save()
            self.__current_player.update(self.__marble_locations)
            print(self.__counter)
            self.__counter += 1

        elif self.__current_player.get_type() == 'Generic':
            self.__current_player.update(self.__marble_locations)
            self.__counter += 1

        else:
            self.__counter += 1 #Move on to the next player
        ###~~~                                                 ~~~###

    def __save(self):
        '''Saves the game state into a file'''

        ###~~~Saving the Game~~~###
        weight_data = {}
        game_data = {}

        for i in range(len(self.__players)):
            player = self.__players[i]

            ###Only get weights from AI
            if player.get_type() == 'AI':
                weight_data[i] = player.get_weights()
            else:
                weight_data[i] = None

            ###~~~Save the whole game only if a human just played~~~###
            ### This is so we can redo back to the last human
            if self.__current_player.get_type() == 'Human':
                marble_data = {}
                marbles = player.get_marbles()

                for j in range(10):
                    marble = marbles[j]
                    marble_data[j] = marble.get_location()

                game_data[i] = marble_data
            ###~~~                                             ~~~###

        if game_data != {}: #Only if there is data to save
            game_data['counter'] = self.__counter
            self.__handler.save(game_data)

        self.__handler.save(weight_data, 'Weights')
        ###~~~               ~~~###

    def __redo(self):
        '''Resets the game to the humans last turn'''

        game_data = self.__handler.redo(2) #Go back to the start of the previous player not this player

        ###~~~Retrieve the previous locations~~~###
        previous_locations = []
        for key, value in game_data.items():

            try:
                locations = []
                for _, location in value.items():
                    locations.append(tuple(location))
            except:
                self.__counter = value

            previous_locations.append(locations)
        ###~~~                               ~~~###

        ###~~~Moving each of the marbles to their respective positions~~~###
        for i in range(len(self.__players)):
            player = self.__players[i]
            locations = previous_locations[i]
            marbles = player.get_marbles()

            for j in range(len(marbles)):
                marble = marbles[j]
                location = locations[j]
                marble.move(location)

            if player.get_type() == 'Human':
                player.reset()
        ###~~~                                                        ~~~###

        self.__save() #Rewrite the current file

    def __has_won(self, player):
        '''Determines if a player has won the game'''

        won = True
        direction = player.get_direction()
        locations = self.__ending_triangles[direction]

        ###~~~Check that each marble is in the right location~~~###
        for marble in player.get_marbles():
            if marble.get_location() not in locations:
                won = False
        ###~~~                                               ~~~###

        return won

    def __finished(self, player):
        '''If a player wins the game displays the winner'''

        self.__running = False

        ###~~~Displaying the message and waiting for response~~~###
        ready = False
        while not ready:
            self.__handler.display_menu('Game Over! Player', player.get_direction(), 'has won!', (75, 50))
            events = self.__handler.get_events()
            ready = events['ready']

            if events['quit']:
                self.__handler.quit()
                quit()
        ###~~~                                               ~~~###

def main():
    game = Game()
    game.start()

if __name__ == '__main__':
    main()
