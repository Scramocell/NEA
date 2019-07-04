import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use("ggplot") #This is to show the training graph at the end

SIZE = 10 #This is the size of the game field
HM_EPISODES = 50000 #How many iterations occur
MOVE_PENALTY = 1 #Get to the food as quick as possible
ENEMY_PENALTY = 300 #Do not get eaten
FOOD_REWARD = 25 #Eat the food
epsilon = 0.9 #This is a control variable to allow learning at the start
EPS_DECAY = 0.9998 #How much it decreases by
SHOW_EVERY = 10000 #Every 3000th train is displayed

start_q_table = None #This will be the filename if continuing training

LEARNING_RATE = 0.1 #A weighting to multiple the result, can be changed
DISCOUNT = 0.95 #Again can be changed, this time a constant

PLAYER_COLOUR = 1 #dictionary indices for the colour of the objects
FOOD_COLOUR = 2
ENEMY_COLOUR = 3

d = {1: (255, 175, 0),
     2: (0, 255, 0),
     3: (0, 0, 255)} #Here is the dictionary in BGR as opencv uses this convention

class Blob: #Objects in the game
    def __init__(self):
        self.x = np.random.randint(0, SIZE) #Has a random position in the field
        self.y = np.random.randint(0, SIZE)

    def __str__(self): #Not used in final, it is for testing purposes
        return f"{self.x}, {self.y}" 

    def __sub__(self, other): #Find the tuple of x and y distance between objects
        return (self.x - other.x, self.y - other.y)

    def action(self, choice): #The agent moves diagonally, less to code no real reason
        if choice == 0:
            self.move(x=1, y=1)
        if choice == 1:
            self.move(x=-1, y=-1)
        if choice == 2:
            self.move(x=1, y=-1)
        if choice == 3:
            self.move(x=-1, y=1)

    def move(self, x=False, y=False): #Moves based on action
        if not x:
            self.x += np.random.randint(-1, 2)
        else:
            self.x += x

        if not y:
            self.y += np.random.randint(-1, 2)
        else:
            self.y += y

        if self.x < 0: #Wall detection
            self.x = 0
        elif self.x > SIZE-1:
            self.x = SIZE-1

        if self.y < 0:
            self.y = 0
        elif self.y > SIZE-1:
            self.y = SIZE-1

if start_q_table is None: #If no q_table was inputted
    q_table = {} #Create a new one, it is a dictionary of possible observations leading to possible actions

    '''There are four observations in two tuples:
        The x and y difference between player and food
        The x and y difference between player and enemey'''
    
    for x1 in range(-SIZE+1, SIZE): 
        for y1 in range(-SIZE+1, SIZE):
            for x2 in range(-SIZE+1, SIZE):
                for y2 in range(-SIZE+1, SIZE):
                    q_table[((x1, y1), (x2, y2))] = [np.random.uniform(-5, 0) for i in range(4)]
    #Gives a random weight value to each of the four options
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f) #Use the file specified

episode_rewards = [] #Later use for graphing training session
for episode in range(HM_EPISODES): #Loop through all episodes
    player = Blob()
    food = Blob()
    enemy = Blob() #Create 3 objects

    if episode % SHOW_EVERY == 0: #If we are showing this episode
        print(f"on # {episode}, epsilon: {epsilon}") #Show the epsilon value
        print(f"{SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}") #Mean rewards
        show = True #We want to see this episode
    else:
        show = False

    episode_reward = 0 #Individual episode reward
    for i in range(200): #Random value, the game goes for 200 player actions so it terminates
        obs = (player - food, player - enemy) #The observations as stated
        if np.random.random() > epsilon: #Originally this is 10% likely this reduces over time
            action = np.argmax(q_table[obs]) #Use the weighted action for given observations
        else:
            action = np.random.randint(0,4) #Use a random action

    #The AI works by giving random values and trying random actions at first
    #It chooses the next action based on experience saved in the Q table for given observations

        player.action(action) #Complete the specified action

        enemy.move()
        food.move()

        if player.x == enemy.x and player.y == enemy.y: #If player gets eaten
            reward = -ENEMY_PENALTY #Penalise heavily
        elif player.x == food.x and player.y == food.y: #If it finds food
            reward = FOOD_REWARD #Reward it
        else:
            reward = -MOVE_PENALTY #A move has occured and no outcome so penalise

        new_obs = (player-food, player-enemy) #Now check the environment
        max_future_q = np.max(q_table[new_obs]) #Find the max reward stored for this new scenario
        current_q = q_table[obs][action] #Find the reward stored for the past scenario

        if reward == FOOD_REWARD: #If it ate
            new_q = FOOD_REWARD #The reward to be stored will be the food reward
        elif reward == -ENEMY_PENALTY: #If it dies
            new_q = -ENEMY_PENALTY #The reward to be stored is a penalty
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT + max_future_q)

    #This is the important algorithm it calculates what the q value should be based on
    #the previous q value in this scenario and the result of the players action. This
    #is monitored through the Learning rate and discount constants'''
    
        q_table[obs][action] = new_q #Update the table (this is the reinforcement) 

        if show: #This is to show the game in action every 3000 episodes
            env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8) #blank field matrix
            env[food.y][food.x] = d[FOOD_COLOUR] 
            env[player.y][player.x] = d[PLAYER_COLOUR]
            env[enemy.y][enemy.x] = d[ENEMY_COLOUR] #the location where an object is at changes

            img = Image.fromarray(env, "RGB") #convert this to an image
            img = img.resize((300, 300)) #Make it visible
            cv2.imshow("", np.array(img)) #Display it on screen, can be done more complicated with tinker

            if reward == FOOD_REWARD or reward == -ENEMY_PENALTY: #If the game ended
                if cv2.waitKey(500) & 0xFF == ord("q"): #Wait a bit longer 
                    break

            else:
                if cv2.waitKey(1) & 0xFF == ord("q"): #Otherwise normal speed
                    break

        episode_reward += reward #Store this versions reward
        if reward == FOOD_REWARD or reward == -ENEMY_PENALTY: #End the game
            break

    episode_rewards.append(episode_reward) #Add this episodes reward
    epsilon *= EPS_DECAY #Decrease epsilon so it reduced randomness

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode="valid")
#This is to normalise the data for simpler display. In all honesty this is copy paste don't know
#exactly how it works, but have a good idea is it is matrices

plt.plot([i for i in range(len(moving_avg))], moving_avg) #create all the plots
plt.ylabel(f"reward {SHOW_EVERY}")
plt.xlabel("episode #")#Labels
plt.show() #Display the graph

with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
    pickle.dump(q_table, f) #Save the table for further use

#Using the table after training with a reset epsilon can help with overall training
#It reintroduces the randomness to prevent slumps or in the case of one traing test I
#did it starting getting worse'''
