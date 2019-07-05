import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use("ggplot") #This is to show the training graph at the end

SIZE = 10
HOW_MANY_EPISODES = 50000
MOVE_PENALTY = 1
ENEMY_PENALTY = 300
FOOD_REWARD = 25
epsilon = 0.9
EPS_DECAY = 0.9998
SHOW_EVERY = 10000

LEARNING_RATE = 0.1
DISCOUNT = 0.95

PLAYER_COLOUR = 1
FOOD_COLOUR = 2
ENEMY_COLOUR = 3

colours = {1: (255, 175, 0),
     2: (0, 255, 0),
     3: (0, 0, 255)}
#In BGR due to opencv

class Blob:
    '''A generic class for a game object with a position in the game'''
    def __init__(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)

    def __str__(self):
        '''Used during testing for object position'''
        return f"{self.x}, {self.y}"

    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)

    def action(self, choice):
        if choice == 0:
            self.move(x=1, y=1)
        if choice == 1:
            self.move(x=-1, y=-1)
        if choice == 2:
            self.move(x=1, y=-1)
        if choice == 3:
            self.move(x=-1, y=1)

    def move(self, x=False, y=False):
        if not x:
            self.x += np.random.randint(-1, 2)
        else:
            self.x += x

        if not y:
            self.y += np.random.randint(-1, 2)
        else:
            self.y += y

        ### Wall detection ###
        if self.x < 0:
            self.x = 0
        elif self.x > SIZE-1:
            self.x = SIZE-1

        if self.y < 0:
            self.y = 0
        elif self.y > SIZE-1:
            self.y = SIZE-1


class Player(Blob):
    def __init__(self, start_q_table=None):
        super().__init__()

        if start_q_table is None:
            self.q_table = {}

            for x1 in range(-SIZE+1, SIZE):
                for y1 in range(-SIZE+1, SIZE):
                    for x2 in range(-SIZE+1, SIZE):
                        for y2 in range(-SIZE+1, SIZE):
                            self.q_table[((x1,y1), (x2,y2))] = [np.random.uniform(-5, 0) for i in range(4)]
        else:
            with open(start_q_table, "rb") as f:
                self.q_table = pickle.load(f)

        self._obs = None
        self._reward = 0
        self._action = 0

    def max_q(self, obs):
        return np.max(self.q_table[obs])

    def best_action(self):
        return np.argmax(self.q_table[self._obs])

    def update_observation(self, food, enemy):
        food_obs = self - food
        enemy_obs = self - enemy
        self._obs = (food_obs, enemy_obs)

    def update_reward(self, food, enemy):
        if self.x == enemy.x and self.y == enemy.y:
            self._reward = -ENEMY_PENALTY
        elif self.x == food.x and self.y == food.y:
            self._reward = FOOD_REWARD
        else:
            self._reward = -MOVE_PENALTY

    def update_q_table(self, food, enemy):
        new_obs = (self-food, self-enemy)
        max_future_q = self.max_q(new_obs)
        current_q = self.q_table[self._obs][self._action]

        if self._reward == FOOD_REWARD:
            new_q = FOOD_REWARD
        elif self._reward == -ENEMY_PENALTY:
            new_q = -ENEMY_PENALTY
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT + max_future_q)

        self.q_table[self._obs][self._action] = new_q

    def get_reward(self):
        return self._reward


class Enemy(Blob):
    def __init__(self, start_q_table=None):
        super().__init__()

        if start_q_table is None:
            self.q_table = {}

            for x1 in range(-SIZE+1, SIZE):
                for y1 in range(-SIZE+1, SIZE):
                    self.q_table[(x1,y1)] = [np.random.uniform(-5, 0) for i in range(4)]
        else:
            with open(start_q_table, "rb") as f:
                self.q_table = pickle.load(f)

        self._obs = None
        self._reward = 0
        self._action = 0

    def max_q(self, obs):
        return np.max(self.q_table[obs])

    def best_action(self):
        return np.argmax(self.q_table[self._obs])

    def update_observation(self, food):
        food_obs = self - food
        self._obs = food_obs

    def update_reward(self, food):
        if self.x == food.x and self.y == food.y:
            self._reward = FOOD_REWARD
        else:
            self._reward = -MOVE_PENALTY

    def update_q_table(self, food, enemy):
        new_obs = self - food
        max_future_q = self.max_q(new_obs)
        current_q = self.q_table[self._obs][self._action]

        if self._reward == FOOD_REWARD:
            new_q = FOOD_REWARD
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT + max_future_q)

        self.q_table[self._obs][self._action] = new_q

    def get_reward(self):
        return self._reward


player_episode_rewards = []
enemy_episode_rewards = []

for episode in range(HOW_MANY_EPISODES):
    player = Player()
    food = Blob()
    enemy = Enemy()

    if episode%SHOW_EVERY==0 and episode>0:
        print(f"on # {episode}, epsilon: {epsilon}")
        print(f"{SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}")
        show = True
    else:
        show = False

    player_episode_reward = 0
    enemy_episode_reward = 0

    for i in range(200):
        player.update_observation(food, enemy)

        if np.random.random() > epsilon:
            player_action = player.best_action()
            enemy_action = enemy.best_action()
        else:
            player_action = np.random.randint(0,4)
            enemy_action = np.random.randint(0,4)

        player.action(player_action)
        enemy.action(enemy_action)

        food.move()

        player.update_reward(food, enemy)
        player.update_q_table(food, enemy)

        enemy.update_reward(player)
        enemy.update_q_table(player)

        if show:
            env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
            env[food.y][food.x] = colours[FOOD_COLOUR]
            env[player.y][player.x] = colours[PLAYER_COLOUR]
            env[enemy.y][enemy.x] = colours[ENEMY_COLOUR]

            img = Image.fromarray(env, "RGB") #Actually opencv interprets colour in BGR
            img = img.resize((300, 300))
            cv2.imshow("", np.array(img))

            if player.get_reward()==FOOD_REWARD or player.get_reward==-ENEMY_PENALTY:
                if cv2.waitKey(500) & 0xFF == ord("q"):
                    break
            else:
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        player_episode_reward += player.get_reward()
        enemy_episode_reward += enemy.get_reward()

        if player.get_reward==FOOD_REWARD or player.get_reward()==-ENEMY_PENALTY:
            break

    player_episode_rewards.append(player_episode_reward)
    enemy_episode_rewards.append(enemy_episode_reward)

    epsilon *= EPS_DECAY

player_moving_avg = np.convolve(player_episode_rewards, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode="valid")
enemy_moving_avg = np.convolve(enemy_episode_rewards, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode="valid")

plt.figure(1)
plt.subplot(211)
plt.plot([i for i in range(len(player_moving_avg))], player_moving_avg)
plt.ylabel(f"Reward ({SHOW_EVERY} player moving average)")
plt.xlabel("Episode #")

plt.subplot(212)
plt.plot([i for i in range(len(enemy_moving_avg))], enemy_moving_avg)
plt.ylabel(f"Reward ({SHOW_EVERY} enemy moving average)")
plt.xlabel("Episode #")
plt.show()

with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
    pickle.dump(q_table, f)