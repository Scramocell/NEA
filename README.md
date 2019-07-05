# NEA
This is my NEA A level project to develop an AI that can play Chinese Checkers against 5 other entities. Originally the game will be 1v1 with two agents this will slowly scale to 6v6. The final plan is to be able to play a 6v6 game without having 5 other people to play with.

# Reinforcement 1
This is my first prototype of reinforcement learning, it is copied from a tutorial by 'Sentdex', a great youtube programming tutorial channel, as part of his reinforcement learning course. I claim no ownership of the code except for a few variable name changes to improve readability.

The idea was to get an understanding of Q learning before I started my project to see if it was feasible. I was mainly focusing on building my own environment, rather using prebuilt ones, as I would have to do in my final project.

Youtube video: https://www.youtube.com/watch?v=G92TF4xYQcU

# Reinforcement 2
This is a continuation of reinforcement one to check I understand the underlying methods and how they operate. I split the algorithm into the smallest reasonable sections and placed them into the class rather than outside. This now allows the enemy to also use reinforcement learning.

Now we have a dynamic environment where the enemy and player learn of each other and the random nature of the food. The enemy is concerned with eating the player and does not care about the food, the player is concerned about both. This can create situations where the enemy can learn that the player must go to the food and thus stick around the food.

One possible next step is to save Blob actions in a file, this way specific games can be replayed back rather than waiting a fix amount of episodes and also not being able to replay them
