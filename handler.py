import json
import os
import pygame

display_locations = {(-8, 4): (51, 94),
                    (-7, 3): (60, 108),
                    (-7, 4): (68, 94),
                    (-6, 2): (68, 123),
                    (-6, 3): (77, 108),
                    (-6, 4): (85, 94),
                    (-5, 1): (77, 137),
                    (-5, 2): (85, 123),
                    (-5, 3): (94, 108),
                    (-5, 4): (102, 94),
                    (-4, -4): (51, 210),
                    (-4, -3): (60, 196),
                    (-4, -2): (68, 181),
                    (-4, -1): (77, 167),
                    (-4, 0): (85, 153),
                    (-4, 1): (94, 139),
                    (-4, 2): (102, 124),
                    (-4, 3): (111, 110),
                    (-4, 4): (119, 95),
                    (-4, 5): (128, 79),
                    (-4, 6): (136, 65),
                    (-4, 7): (144, 50),
                    (-4, 8): (153, 35),
                    (-3, -4): (68, 210),
                    (-3, -3): (77, 196),
                    (-3, -2): (85, 181),
                    (-3, -1): (94, 167),
                    (-3, 0): (102, 153),
                    (-3, 1): (111, 139),
                    (-3, 2): (119, 124),
                    (-3, 3): (128, 110),
                    (-3, 4): (136, 95),
                    (-3, 5): (144, 79),
                    (-3, 6): (153, 65),
                    (-3, 7): (161, 50),
                    (-2, -4): (85, 210),
                    (-2, -3): (94, 196),
                    (-2, -2): (102, 181),
                    (-2, -1): (111, 167),
                    (-2, 0): (119, 153),
                    (-2, 1): (128, 139),
                    (-2, 2): (136, 124),
                    (-2, 3): (144, 110),
                    (-2, 4): (153, 95),
                    (-2, 5): (161, 79),
                    (-2, 6): (170, 65),
                    (-1, -4): (102, 210),
                    (-1, -3): (111, 196),
                    (-1, -2): (119, 181),
                    (-1, -1): (128, 167),
                    (-1, 0): (136, 153),
                    (-1, 1): (144, 139),
                    (-1, 2): (153, 124),
                    (-1, 3): (161, 110),
                    (-1, 4): (170, 95),
                    (-1, 5): (178, 79),
                    (0, -4): (119, 210),
                    (0, -3): (128, 196),
                    (0, -2): (136, 181),
                    (0, -1): (144, 167),
                    (0, 0): (153, 153),
                    (0, 1): (161, 139),
                    (0, 2): (170, 124),
                    (0, 3): (178, 110),
                    (0, 4): (187, 95),
                    (1, -5): (127, 225),
                    (1, -4): (136, 210),
                    (1, -3): (144, 196),
                    (1, -2): (153, 181),
                    (1, -1): (161, 167),
                    (1, 0): (170, 153),
                    (1, 1): (178, 139),
                    (1, 2): (187, 124),
                    (1, 3): (195, 110),
                    (1, 4): (203, 94),
                    (2, -6): (136, 239),
                    (2, -5): (144, 225),
                    (2, -4): (153, 210),
                    (2, -3): (161, 196),
                    (2, -2): (170, 181),
                    (2, -1): (178, 167),
                    (2, 0): (187, 153),
                    (2, 1): (195, 139),
                    (2, 2): (203, 124),
                    (2, 3): (212, 108),
                    (2, 4): (220, 94),
                    (3, -7): (144, 254),
                    (3, -6): (153, 239),
                    (3, -5): (161, 225),
                    (3, -4): (170, 210),
                    (3, -3): (178, 196),
                    (3, -2): (187, 181),
                    (3, -1): (195, 167),
                    (3, 0): (203, 153),
                    (3, 1): (212, 139),
                    (3, 2): (220, 124),
                    (3, 3): (229, 108),
                    (3, 4): (237, 94),
                    (4, -8): (153, 268),
                    (4, -7): (161, 254),
                    (4, -6): (170, 239),
                    (4, -5): (178, 225),
                    (4, -4): (187, 210),
                    (4, -3): (195, 196),
                    (4, -2): (203, 181),
                    (4, -1): (212, 167),
                    (4, 0): (220, 153),
                    (4, 1): (229, 139),
                    (4, 2): (237, 124),
                    (4, 3): (245, 108),
                    (4, 4): (254, 94),
                    (5, -4): (203, 210),
                    (5, -3): (212, 196),
                    (5, -2): (220, 181),
                    (5, -1): (229, 167),
                    (6, -4): (220, 210),
                    (6, -3): (229, 196),
                    (6, -2): (237, 181),
                    (7, -4): (237, 210),
                    (7, -3): (245, 196),
                    (8, -4): (254, 210)}

colours = {'Red': (255, 0, 0),
            'Green': (0, 255, 0),
            'Blue': (0, 0, 255),
            'Black': (0, 0, 0),
            'White': (200, 200, 200),
            'Yellow': (255, 255, 0)}

class Handler:
    def __init__(self):
        '''Initialises Handler Object
        This object deals with the display, input and files'''

        ###~~~Initialise Pygame~~~###
        pygame.init()
        icon = pygame.image.load('icon.jpg')
        pygame.display.set_caption('Chinese Checkers Engine')
        pygame.display.set_icon(icon)

        ###~~~Setting up text input~~~###
        self.__text_width = 0
        self.__default_text = 'Type...'
        self.__text = self.__default_text
        ###~~~                     ~~~###

        ###~~~Setting up the window~~~##
        self.__size = 300
        self.__size = 300
        self.__window = pygame.display.set_mode((self.__size, self.__size), pygame.RESIZABLE)
        self.__image = pygame.image.load('chinesecheckers.png')
        ###~~~###~~~         ~~~###~~~###

        ###~~~Setting up input boxes and buttons~~~###
        self.__redo_button = pygame.Rect(225, 10, 75, 32)
        ###~~~                                  ~~~###

    def set_files(self, game_file):
        '''Loads or create game files'''

        ###~~~Initialises all the files~~~###
        self.__game_file = game_file
        self.__weight_file = game_file + 'weights'
        self.__counter = 0
        ###~~~                         ~~~###

        ###~~~Creates a new Game directory~~~###
        try:
            os.mkdir(game_file)

            return True
        except:
            #The directory already exists
            return False
        ###~~~                            ~~~###

    def save(self, data, location='Game'):
        '''Saves the data provided into the game files'''

        ###~~~Choosing the appropriate file~~~###
        if location == 'Game':
            file = self.__game_file + '\\' + self.__game_file + str(self.__counter) + '.json'
            self.__counter += 1
        elif location == 'Weights':
            file = self.__game_file + '\\' + self.__weight_file + '.json'
        else:
            return False
        ###~~~                             ~~~###

        ###~~~Convert to JSON and save~~~###
        json_data = json.dumps(data, indent=2)

        with open(file, 'w') as json_file:
            json_file.write(json_data)

        return True
        ###~~~                        ~~~###

    def load(self, location='Game'):
        '''Returns data from the latest game file'''

        ###~~~Choosing the appropriate game file~~~###
        if location == 'Game':
            file = self.__game_file + '\\' + self.__game_file + str(self.__counter) + '.json'
        elif location == 'Weights':
            file = self.__game_file + '\\' + self.__weight_file + '.json'
        else:
            return None
        ###~~~                                  ~~~###

        ###~~~Try to load data from the given file~~~###
        try:
            json_file = open(file, 'r')
            json_data = json_file.read()
            data = json.loads(json_data)
            json_file.close()
            return data
        except:
            ###~~~The file doesn't exist and will be created when saving
            return None
        ###~~~                                    ~~~###

    def display_menu(self, message, coordinates):
        '''displays all the main menu elements'''

        input_box = pygame.Rect(50, (2/3) * self.__size, self.__size - 100, self.__size / 10)
        font = pygame.font.Font(None, int(self.__size / 10))
        small_font = pygame.font.Font(None, int(self.__size / 20))

        self.__window.fill((255, 255, 255))

        ###~~~Setting up and displaying text~~~###
        input_text_surface = font.render(self.__text, True, (0, 0, 0))
        self.__text_width = input_text_surface.get_width()

        display_text_surface = font.render(message, True, (0, 0, 0))
        prompt_surface = small_font.render('Enter to continue', True, (50, 50, 50))

        self.__window.blit(input_text_surface, (input_box.x+5, input_box.y+5))
        self.__window.blit(display_text_surface, coordinates)
        self.__window.blit(prompt_surface, (153, (24/30) * self.__size))

        pygame.draw.rect(self.__window, (0, 0, 0), input_box, 2)
        ###~~~                              ~~~###

        pygame.display.flip()

    def display_board(self, players, current_player):
        '''Displays all the elements on the board'''

        background = pygame.transform.scale(self.__image, (self.__size, self.__size))
        self.__window.blit(background, (0, 0))

        ###~~~Displaying individual player marbles~~~###
        for player in players:
            for marble in player.get_marbles():
                location = marble.get_location()
                colour = marble.get_colour()
                pygame.draw.circle(self.__window, colours[colour], display_locations[location], 7)
        ###~~~                                    ~~~###

        ###~~~Displaying the highlights for the user~~~###
        if current_player.get_type() == 'Human':
            for location in current_player.get_moves():
                pygame.draw.circle(self.__window, (255, 165, 0), display_locations[location], 7)

            ###~~~Highlighting the selected marble~~~###
            try:
                marble = current_player.get_selected_marble()
                location = marble.get_location()
                pygame.draw.circle(self.__window, (255, 165, 0), display_locations[location], 7, 2)
            except:
                pass

            ###Only display redo button for humans###
            redo_text = self.__font.render('REDO', True, (0, 255, 0))
            self.__window.blit(redo_text, (225, 10))
            ###~~~                                ~~~###
        ###~~~                                      ~~~###

        pygame.display.flip()

    def get_events(self):
        '''Returns the pygame events that have occured'''
        events = {'ready': False,
                    'mouse_location': None,
                    'redo': False,
                    'quit': False}

        ###~~~Event handler~~~###
        for event in pygame.event.get():

            ###~~~Converts mouse's screen position into a game location~~~###
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                for location, position in display_locations.items():
                    x, y = position
                    if (x-mx)**2 + (y-my)**2 <= 49:
                        events['mouse_location'] = location
            ###~~~                                                     ~~~###

                if self.__redo_button.collidepoint(event.pos):
                    events['redo'] = True

            ###~~~Key press events~~~###
            if event.type == pygame.KEYDOWN:

                ###Enter to continue at menu phase###
                if event.key == pygame.K_RETURN:
                    events['ready'] = True

                ###Text entering###
                elif event.key == pygame.K_BACKSPACE:
                    self.__text = self.__text[:-1]
                elif self.__text_width <= 180: #Prevents run over in the input box
                    self.__text += event.unicode
                else:
                    pass
            ###~~~                ~~~###

            ###~~~Window resizing~~~###
            if event.type == pygame.VIDEORESIZE:
                if event.w < event.h:
                    self.__size = event.w
                else:
                    self.__size = event.h
                self.__window = pygame.display.set_mode((self.__size, self.__size), pygame.RESIZABLE)
            ###~~~               ~~~###

            ###Controlled exit~~~###
            if event.type == pygame.QUIT:
                events['quit'] = True
        ###~~~              ~~~###

        return events

    def quit(self):
        '''quits the display'''

        pygame.display.quit()

    def end_game(self):
        '''Deletes unecessary game files'''

        ###~~~Reducing game file to just the last state~~~###
        for count in range(self.__counter-1):
            os.remove(self.__game_file + '\\' + self.__game_file + str(count) + '.json')

        os.rename(self.__game_file + '\\' + self.__game_file + str(self.__counter-1) + '.json', self.__game_file + '\\' + self.__game_file + '0.json')
        ###~~~                                         ~~~###

        self.__counter = 0 #Resetting counter for next game

    def redo(self, count_adjustment):
        '''Returns the data from the move before'''

        ###~~~Delete Unecessary game files~~~###
        self.__counter -= count_adjustment
        os.remove(self.__game_file + '\\' + self.__game_file + str(self.__counter+1) + '.json')
        ###~~~                            ~~~###

        if self.__counter < 0:
            self.__counter = 0

        data = self.load()

        return(data)

    def get_text(self):
        '''Returns and resets the text entered by the user'''

        text = self.__text
        self.__text = ''
        return text

def main():
    pass

if __name__ == '__main__':
    main()
