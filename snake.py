#Autor: Guilherme Milan Santos 
#Numero USP: 9012966
#Instrucoes: executar python snake_game.py -nn
#Utiliza python 3, curses, numpy e math
#Para fechar, apertar a seta para baixo no teclado
#Para entrar no modo invisivel (treina mais rapidamente), apertar a seta para cima no teclado
#Para aumentar a velocidade no modo visivel, apertar a seta para a direita
#para diminuir a velocidade no modo visivel. apertar a seta para a esquerda

import curses
from random import randint
import sys
import time
from enum import Enum
from perceptron import *
from genetic import *
import numpy as np


class GameState(Enum):
	PLAYING = 0
	PAUSED = 1
	GAME_OVER = 2
	CLOSING = 3

class SteeringType(Enum):
	ABSOLUTE = 0
	RELATIVE = 1

class InputMode(Enum):
	KEYBOARD = 0
	NEURAL_NET	 = 1

class Direction(Enum):
	UP = 0
	LEFT = 1
	RIGHT = 2
	DOWN = 3

class SnakeState(Enum):
	DEAD = 0
	ALIVE = 1

class SnakeBoard:
	def __init__(self, width=20, height=20, steering_type=SteeringType.ABSOLUTE):
		self.dead_snakes = 0
		self.food = [0,0]
		self.width = 20
		self.height = 20
		self.steering_type = steering_type
		self.game_state = GameState.PLAYING
		self.snakes = []
		new_snake = Snake(steering_type=steering_type, bw=width, bh=height)
		self.snakes.append(new_snake)		
		self.create_food()

	def get_game_state(self):
		return self.game_state

	def end_game(self):
		self.game_state = GameState.CLOSING

	def create_food(self):
		self.food[0] = randint(1, self.width-2)
		self.food[1] = randint(1, self.height-2)
		while(self.food in self.snakes[0].parts):
			self.food[0] = randint(1, self.width-2)
			self.food[1] = randint(1, self.height-2)

		for snake in self.snakes:
			snake.food = self.food

	def collision_detection(self):
		for snake in self.snakes:
			if(snake.parts[0] == self.food):
				snake.grow_snake()
				self.create_food()
			elif(snake.parts[0][0] == 0 or snake.parts[0][0] == self.width-1):
				#colisao em x
				snake.state = SnakeState.DEAD
			elif(snake.parts[0][1] == 0 or snake.parts[0][1] == self.height-1):
				#colisao em y
				snake.state = SnakeState.DEAD
			elif(snake.parts[0] in snake.parts[1:]):
				#colisao consigo mesma
				snake.state = SnakeState.DEAD

	def step(self):
		for snake in self.snakes:
			snake.step()
			self.collision_detection()
			if(snake.state == SnakeState.DEAD):
				self.dead_snakes += 1

		if(self.dead_snakes == len(self.snakes)):
			self.game_state = GameState.GAME_OVER


class Snake:
	def __init__(self, param_dir=Direction.DOWN, steering_type=SteeringType.ABSOLUTE, bw=20, bh=20):
		self.state = SnakeState.ALIVE
		self.steering_type = SteeringType.RELATIVE
		self.parts = []
		self.hunger = 50
		self.size = 3
		self.time_alive = 0
		self.direction = param_dir
		self.bw = bw
		self.bh = bh
		starting_x = int(np.random.uniform(5,bw-5))
		starting_y = int(np.random.uniform(5,bh-5))
		
		for i in range(0,3):
			part = [0,0]
			if(self.direction == Direction.UP):
				part[0] = starting_x
				part[1] = starting_y+i
			elif(self.direction == Direction.DOWN):
				part[0] = starting_x
				part[1] = starting_y-i
			elif(self.direction == Direction.LEFT):
				part[0] = starting_x+i
				part[1] = starting_y
			elif(self.direction == Direction.RIGHT):
				part[0] = starting_x-i
				part[1] = starting_y

			self.parts.append(part)		

	def grow_snake(self):
		self.hunger += 30
		new_part = [0,0]
		new_part[0] = self.parts[-1][0]
		new_part[1] = self.parts[-1][1]
		if(self.direction == Direction.UP):
			new_part[1] += 1
		elif(self.direction == Direction.DOWN):
			new_part[1] -= 1
		elif(self.direction == Direction.LEFT):
			new_part[0] += 1
		elif(self.direction == Direction.RIGHT):
			new_part[0] -= 1
		self.parts.append(new_part)
		self.size += 1

	def set_direction(self, new_direction):
		if(self.state == SnakeState.ALIVE):
			if(self.steering_type == SteeringType.ABSOLUTE):
				if(new_direction == Direction.UP and self.direction != Direction.DOWN):
					self.direction = Direction.UP

				elif(new_direction == Direction.DOWN and self.direction != Direction.UP):
					self.direction = Direction.DOWN

				elif(new_direction == Direction.LEFT and self.direction != Direction.RIGHT):
					self.direction = Direction.LEFT

				elif(new_direction == Direction.RIGHT and self.direction != Direction.LEFT):
					self.direction = Direction.RIGHT
			
			elif(self.steering_type == SteeringType.RELATIVE):
				
				if(self.direction == Direction.UP):
					if(new_direction == Direction.LEFT):
						self.direction = Direction.LEFT
					elif(new_direction == Direction.RIGHT):
						self.direction = Direction.RIGHT

				elif(self.direction == Direction.DOWN):
					if(new_direction == Direction.LEFT):
						self.direction = Direction.RIGHT
					elif(new_direction == Direction.RIGHT):
						self.direction = Direction.LEFT

				elif(self.direction == Direction.LEFT):
					if(new_direction == Direction.LEFT):
						self.direction = Direction.DOWN
					elif(new_direction == Direction.RIGHT):
						self.direction = Direction.UP
				else:
					if(new_direction == Direction.LEFT):
						self.direction = Direction.UP
					elif(new_direction == Direction.RIGHT):
						self.direction = Direction.DOWN

	def step(self):
		if(self.state == SnakeState.ALIVE):
			self.time_alive += 1
			self.hunger -= 1
			new_part = [0,0]
			new_part[0] = self.parts[0][0]
			new_part[1] = self.parts[0][1]
			if(self.direction == Direction.UP):
				new_part[1] = new_part[1]-1
			elif(self.direction == Direction.DOWN):
				new_part[1] = new_part[1]+1
			elif(self.direction == Direction.LEFT):
				new_part[0] = new_part[0]-1
			elif(self.direction == Direction.RIGHT):
				new_part[0] = new_part[0]+1

			removed_part = self.parts.pop()#tira ultimo ponto da cobra
			self.parts.insert(0, new_part)#cria novo ponto da cobra no comeco
			if(self.hunger < 0):
				self.state = SnakeState.DEAD

	def score(self):
		return self.size*self.time_alive

	def get_game_info(self):
		head = self.parts[0]
		#obstacle_ahead = (
		#	(self.direction == Direction.RIGHT and (head[0]+1 == self.bw-1 or [head[0]+1, head[1]] in self.parts))
		#	or (self.direction == Direction.LEFT and (head[0]-1 == 0 or [head[0]-1, head[1]] in self.parts)) 
		#	or (self.direction == Direction.UP and (head[1]-1 == 0 or [head[0], head[1]-1] in self.parts))
		#	or (self.direction == Direction.DOWN and (head[1]+1 == self.bh or [head[0],head[1]+1] in self.parts)))

		#obstacle_to_the_left =  (
		#	(self.direction == Direction.RIGHT and (head[1]-1 == 0 or [head[0],head[1]-1] in self.parts))
		#	or (self.direction == Direction.LEFT and (head[1]+1 == self.bh or [head[0],head[1]+1] in self.parts))
		#	or (self.direction == Direction.UP and (head[0]-1 == 0 or [head[0]-1,head[1]] in self.parts))
		#	or (self.direction == Direction.DOWN and (head[0]+1 == self.bw-1 or [head[0]+1,head[1]] in self.parts)))

		#obstacle_to_the_right = (
		#	(self.direction == Direction.RIGHT and (head[1]+1 == self.bh or [head[0],head[1]+1] in self.parts))
		#	or (self.direction == Direction.LEFT and (head[1]-1 == 0 or [head[0],head[1]-1] in self.parts))
		#	or (self.direction == Direction.UP and (head[0]+1 == self.bw-1 or [head[0]+1,head[1]] in self.parts))
		#	or (self.direction == Direction.DOWN and (head[0]-1 == 0 or [head[0]-1,head[1]] in self.parts)))
		obstacle_ahead = ((self.direction == Direction.RIGHT and head[0]+1 == self.bw-1)
			or (self.direction == Direction.LEFT and head[0]-1 == 0)
			or (self.direction == Direction.UP and head[1]-1 == 0)
			or (self.direction == Direction.DOWN and head[1]+1 == self.bh))

		obstacle_to_the_left =  ((self.direction == Direction.RIGHT and (head[1]-1 == 0))
			or (self.direction == Direction.LEFT and (head[1]+1 == self.bh))
			or (self.direction == Direction.UP and (head[0]-1 == 0))
			or (self.direction == Direction.DOWN and (head[0]+1 == self.bw-1)))

		obstacle_to_the_right = ((self.direction == Direction.RIGHT and (head[1]+1 == self.bh))
			or (self.direction == Direction.LEFT and (head[1]-1 == 0))
			or (self.direction == Direction.UP and (head[0]+1 == self.bw-1))
			or (self.direction == Direction.DOWN and (head[0]-1 == 0)))
		

		for part in self.parts:
			if(obstacle_ahead == 1):
				break
			if(self.direction == Direction.RIGHT):
				if(part[0] == head[0]+1 and part[1] == head[1]):
					obstacle_ahead = 1
			elif(self.direction == Direction.LEFT):
				if(part[0] == head[0]-1 and part[1] == head[1]):
					obstacle_ahead = 1
			elif(self.direction == Direction.UP):
				if(part[0] == head[0] and part[1] == head[1]-1):
					obstacle_ahead = 1
			elif(self.direction == Direction.DOWN):
				if(part[0] == head[0] and part[1] == head[1]+1):
					obstacle_ahead = 1

		for part in self.parts:
			if(obstacle_to_the_left == 1):
				break
			if(self.direction == Direction.RIGHT):
				if(part[0] == head[0] and part[1] == head[1]-1):
					obstacle_to_the_left = 1
			elif(self.direction == Direction.LEFT):
				if(part[0] == head[0] and part[1] == head[1]+1):
					obstacle_to_the_left = 1			
			elif(self.direction == Direction.UP):
				if(part[0] == head[0]-1 and part[1] == head[1]):
					obstacle_to_the_left = 1
			elif(self.direction == Direction.DOWN):
				if(part[0] == head[0]+1 and part[1] == head[1]):
					obstacle_to_the_left = 1

		for part in self.parts:
			if(obstacle_to_the_right == 1):
				break
			if(self.direction == Direction.RIGHT):
				if(part[0] == head[0] and part[1] == head[1]+1):
					obstacle_to_the_right = 1
			elif(self.direction == Direction.LEFT):
				if(part[0] == head[0] and part[1] == head[1]-1):
					obstacle_to_the_right = 1
			elif(self.direction == Direction.UP):
				if(part[0] == head[0]+1 and part[1] == head[1]):
					obstacle_to_the_right = 1
			elif(self.direction == Direction.DOWN):
				if(part[0] == head[0]-1 and part[1] == head[1]):
					obstacle_to_the_right = 1
		#part_ahead = (
		#	(self.direction == Direction.RIGHT and ([head[0]+1, head[1]] in self.parts))
		#	or (self.direction == Direction.LEFT and ([head[0]-1, head[1]] in self.parts)) 
		#	or (self.direction == Direction.UP and ([head[0], head[1]-1] in self.parts))
		#	or (self.direction == Direction.DOWN and ([head[0],head[1]+1] in self.parts)))

		#part_to_the_left = (
		#	(self.direction == Direction.RIGHT and ([head[0],head[1]-1] in self.parts))
		#	or (self.direction == Direction.LEFT and ([head[0],head[1]+1] in self.parts))
		#	or (self.direction == Direction.UP and ([head[0]-1,head[1]] in self.parts))
		#	or (self.direction == Direction.DOWN and ([head[0]+1,head[1]] in self.parts)))

		#part_to_the_right = (
		#	(self.direction == Direction.RIGHT and ([head[0],head[1]+1] in self.parts))
		#	or (self.direction == Direction.LEFT and ([head[0],head[1]-1] in self.parts))
		#	or (self.direction == Direction.UP and ([head[0]+1,head[1]] in self.parts))
		#	or (self.direction == Direction.DOWN and ([head[0]-1,head[1]] in self.parts)))

		food_to_the_left = ((self.direction == Direction.RIGHT and head[1] > self.food[1])
			or (self.direction == Direction.LEFT and head[1] < self.food[1])
			or (self.direction == Direction.UP and head[0] > self.food[0])
			or (self.direction == Direction.DOWN and head[0] < self.food[0]))

		food_to_the_right = ((self.direction == Direction.RIGHT and head[1] < self.food[1])
			or (self.direction == Direction.LEFT and head[1] > self.food[1])
			or (self.direction == Direction.UP and head[0] < self.food[0])
			or (self.direction == Direction.DOWN and head[0] > self.food[0]))

		food_ahead = ((self.direction == Direction.RIGHT and head[0] < self.food[0])
			or (self.direction == Direction.LEFT and head[0] > self.food[0])
			or (self.direction == Direction.UP and head[1] > self.food[1])
			or (self.direction == Direction.DOWN and head[1] < self.food[1]))

		food_behind = ((self.direction == Direction.RIGHT and head[0] > self.food[0])
			or (self.direction == Direction.LEFT and head[0] < self.food[0])
			or (self.direction == Direction.UP and head[1] < self.food[1])
			or (self.direction == Direction.DOWN and head[1] > self.food[1]))

		return (obstacle_ahead, obstacle_to_the_left, obstacle_to_the_right,
			food_to_the_left, food_to_the_right, food_ahead, food_behind)		