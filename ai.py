import numpy
import random
from player import Player

class AI(Player):
    def __init__(self, data, colour, locations, triangles):
        '''Intialises an AI object:
            Super calls the Player constructor
            Sets type
            Sets weights, evaluations and tree depth'''

        super().__init__(data, colour, locations, triangles)
        self._type = 'AI'
        self.__triangles = triangles

        self.__k_depth = 2  # fairly shallow becuase the number of board states increases by x10^6 each depth
        self.__INFINITY = 1000000000

        self.__weights = [random.randint(1, 100), random.randint(1, 100)]
        self.__weight_matrix = []
        self.__new_features = []
        self.__feature_matrix = []

        self.__learning_rate = 0.1

    def update(self, marble_locations):
        '''Updates the AI by choosing the best moving and making it'''

        ###~~~Choosing the best move~~~###
        available_moves = self.get_available_moves(marble_locations)
        marble_index = 0
        first_run = True

        for i in range(10):
            for move in available_moves[i]:
                marble_position_array = self.__split_locations(marble_locations)
                marble_position_array[self._direction][i] = move

                evaluation = self.__alphabeta(marble_locations, marble_position_array, 0, -self.__INFINITY, self.__INFINITY, True)

                if first_run:
                    best_score = evaluation
                    best_move = move
                    marble_index = i
                    feature = self.__new_features[-1]  # Get the latest feature
                    first_run = False
                elif evaluation > best_score:
                    best_score = evaluation
                    best_move = move
                    marble_index = i
                    feature = self.__new_features[-1]

        self._move(best_move, marble_index)
        ###~~~                ~~~###

        ###~~~Updating matrices~~~###
        self.__weight_matrix.append(self.__weights)
        self.__feature_matrix.append(feature)
        self.__new_features = []
        ###~~~                 ~~~###

        self.__weight_tuning()

    def __weight_tuning(self):
        '''Changes the weights values so that they increase success'''
        weight_a = numpy.array([weights[0] for weights in self.__weight_matrix])
        weight_b = numpy.array([weights[1] for weights in self.__weight_matrix])
        feature_a = numpy.array([features[0] for features in self.__feature_matrix])
        feature_b = numpy.array([features[1] for features in self.__feature_matrix])
        weights = [weight_a, weight_b]
        features = [feature_a, feature_b]

        for i in range(len(weights)):
            weight = weights[i]
            feature = features[i]

            X = numpy.vstack([weight, numpy.ones(len(weight))]).T  # This is done to allow a square matrix to be created
            # ^ This adds a second row of ones to make a 2 x n matrix

            try:
                ###This is the least_squares matrix algorithm,
                ###however it has issues with floating point approximation error
                ###so does not always work

                square_matrix_X = numpy.dot(X.T, X)  # Becuase of above this becomes a n x n matrix
                new_Y = numpy.dot(X.T, feature)  # Converts the y (feature values) becuase we changed X

                ###Find vector b, for (X.T . X)b = (X.T . y)###
                ###ie. vector [m, c] to create equation y = mx+c
                least_square = numpy.linalg.solve(square_matrix_X, new_Y)
            except:
                least_square = numpy.linalg.lstsq(X, feature)[
                    0]  # This is the built in function which avoids floating error

            new_weight, c = least_square  # The new_weight will be the gradient, this slowly shifts the weight to the optimal value

            self.__weights[i] += self.__learning_rate * (new_weight - self.__weights[i])

    def __alphabeta(self, marble_locations, marble_position_array, depth, alpha, beta, maximising_player):
        '''Algorithm determines the evaluation of a certain move given future moves'''

        ###~~~Retrieves the evaluation of the board~~~###
        if depth >= self.__k_depth:
            opponent_position_matrix, AI_position_vector = self.__matrices_from_array(marble_position_array)
            new_marble_positions = marble_position_array[self._direction]

            return self.__evaluation(opponent_position_matrix, AI_position_vector, new_marble_positions)
        ###~~~                                     ~~~###

        ###~~~Maximising players chooses the maximum value~~~###
        if maximising_player:
            best_value = -self.__INFINITY

            ###~~~Completing all of this AIs possible moves~~~###
            generic_marble = self._marbles[0]  # So that we can access hop and roll checks (no other significance)

            ###~~~Trying each marble's rolls and hops~~~###
            available_moves = []

            for i in range(len(marble_position_array[self._direction])):
                check_location = marble_position_array[self._direction][i]

                ###Checking hops###
                for location in generic_marble.check_hops(marble_locations, self._locations,
                                                          hop_location=check_location):
                    if location in self._locations:
                        if location not in available_moves:  # Prevents double checking a move
                            available_moves.append((i, location))  # Save marble number and it's new location

                ###Checking rolls###
                for location in generic_marble.check_rolls(marble_locations, hop_location=check_location):
                    if location in self._locations:
                        if location not in available_moves:
                            available_moves.append((i, location))
            ###~~~                                   ~~~###

            ###~~~Creating an updated copy of marble positions~~~###
            for new_location in available_moves:
                i, move = new_location

                new_marble_position_array = marble_position_array[:]
                new_marble_position_array[self._direction][i] = move
                new_marble_locations = []

                for marble_array in new_marble_position_array:
                    new_marble_locations += marble_array

                value = self.__alphabeta(new_marble_locations, new_marble_position_array, depth + 1, alpha, beta, False)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)

                if alpha >= beta:
                    break #beta cut off
            ###~~~             ~~~##

            ###~~~                                     ~~~###

            return best_value
        ###~~~                                            ~~~###

        ###~~~Minimising player chooses the minimum value~~~###
        else:
            best_value = self.__INFINITY

            ###~~~Completing opponent players possible moves~~~###
            ###Everything is very similar; differences:
            ###Looking at multiple players not just one
            ###Minimises the value not maximising it

            generic_marble = self._marbles[0]

            available_moves = []

            for direction in range(len(marble_position_array)):  # Cycle through every players possible moves
                if direction != self._direction:  # Except for this AI

                    for i in range(len(marble_position_array[direction])):
                        check_location = marble_position_array[direction][i]

                        for location in generic_marble.check_hops(marble_locations, self._locations,
                                                                  hop_location=check_location):
                            if location in self._locations:
                                if location not in available_moves:
                                    available_moves.append((direction, i, location))

                        for location in generic_marble.check_rolls(marble_locations, hop_location=check_location):
                            if location in self._locations:
                                if location not in available_moves:
                                    available_moves.append((direction, i, location))

            for new_move in available_moves:
                direction, i, move = new_move

                new_marble_position_array = marble_position_array[:]
                new_marble_position_array[direction][i] = move
                new_marble_locations = []

                for marble_array in new_marble_position_array:
                    new_marble_locations += marble_array

                value = self.__alphabeta(new_marble_locations, new_marble_position_array, depth + 1, alpha, beta, True)
                best_value = min(best_value, value)
                beta = min(beta, best_value)

                if alpha >= beta:
                    break #alpha cut off
            ###~~~                                          ~~~###

            return best_value
        ###~~~                                           ~~~###

    def __evaluation(self, opponent_position_matrix, AI_position_vector, new_marble_positions):
        '''Evaluates the state of the board returning a single float'''

        ###~~~Features are created from the matrix~~~###
        AI_feature_vector = self.__get_features(AI_position_vector, 1)
        opponent_feature_matrix = self.__get_features(opponent_position_matrix, 5)

        ###~~~Calculate rewards~~~###
        reward = 0

        for i in range(len(new_marble_positions)):
            for triangle in self.__triangles:
                if new_marble_positions[i] in self.__triangles:
                    reward -= 100000

        for i in range(len(new_marble_positions)):
            if new_marble_positions[i] in self.__triangles[self._direction]:
                reward += 2 * 100000
        ###~~~                  ~~~###

        ###~~~Create the two vectors~~~###
        feature_vector = numpy.subtract(AI_feature_vector, opponent_feature_matrix)
        weight_vector = numpy.array(self.__weights)

        self.__new_features.append(feature_vector)

        evaluation = reward + numpy.dot(weight_vector, feature_vector)

        return evaluation

    def __matrices_from_array(self, marble_position_array):
        '''returns matrices from an array'''

        position_matrix = []
        position_vector = numpy.array([])

        ###~~~Retrieve the appropriate coordinate for each players marbles~~~###
        for i in range(len(marble_position_array)):
            if i == 0 or i == 1:
                vector = [coord[1] for coord in marble_position_array[i]]
            elif i == 2:
                vector = [coord[0] for coord in marble_position_array[i]]
            elif i == 3 or i == 4:
                vector = [-coord[1] for coord in marble_position_array[i]]
            elif i == 5:
                vector = [-coord[0] for coord in marble_position_array[i]]
            ###~~~                                                            ~~~###

            ###~~~Add opponent's vectors to matrix~~~###
            if i != self._direction:
                position_matrix.append(vector)
            else:
                position_vector = numpy.array(vector)
        ###~~~                                ~~~###

        ###~~~Return the matrix and vector~~~###
        return numpy.array(position_matrix), position_vector

    def __get_features(self, matrix, players):
        '''Calculates the feature vector from a position matrix'''

        ###~~~Calculate the mean from the position matrix~~~###
        average_distances = numpy.add(10, matrix)  # correction factor
        average_distances = numpy.mean(average_distances)
        ###~~~                                           ~~~###

        total_distances = numpy.subtract(8, matrix)  # correction factor

        total_distances = numpy.sum(total_distances) / players

        ###~~~Return a vector of the values~~~###
        return numpy.array([average_distances, total_distances])

    def __split_locations(self, marble_locations):
        '''splits marble locations into individual players'''

        split = []

        for n in range(6):
            split.append(marble_locations[10 * n:10 * (n + 1)])

        return split

    def set_weights(self, weight_array):
        self.__weights = weight_array

    def get_weights(self):
        return self.__weights

    def get_weight_matrix(self):
        return self.__weight_matrix


def main():
    pass


if __name__ == '__main__':
    main()
