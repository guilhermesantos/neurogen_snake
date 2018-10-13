#Autor: Guilherme Milan Santos
#Baseado no jogo de snake em https://github.com/korolvs/snake_nn/

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

class Direction(Enum):
	UP = 0
	LEFT = 1
	RIGHT = 2
	DOWN = 3

class InputMode(Enum):
	KEYBOARD = 0
	NEURAL_NET	 = 1

class SnakeState:
	def __init__(self, bw=20, bh = 20, param_dir=Direction.DOWN, steering_type=SteeringType.ABSOLUTE):
		self.direction = param_dir
		self.steering_type = steering_type
		self.food = {}
		self.num = 0
		self.score = 50
		self.game_state = GameState.PLAYING
		self.board = {'width': bw, 'height': bh}
		self.snake = []
		self.size = 3

		starting_x = int(np.random.uniform(5,bw-5))
		starting_y = int(np.random.uniform(5,bh-5))

		for i in range(0,3):
			part = {}
			if(self.direction == Direction.UP):
				part['x'] = starting_x
				part['y'] = starting_y+i
			elif(self.direction == Direction.DOWN):
				part['x'] = starting_x
				part['y'] = starting_y-i
			elif(self.direction == Direction.LEFT):
				part['x'] = starting_x+i
				part['y'] = starting_y
			elif(self.direction == Direction.RIGHT):
				part['x'] = starting_x-i
				part['y'] = starting_y

			self.snake.append(part)

		self.create_food()

	def get_game_state(self):
		return self.game_state

	def end_game(self):
		self.game_state = GameState.CLOSING

	def create_food(self):
		self.food['x'] = randint(1, self.board['width']-2)
		self.food['y'] = randint(1, self.board['height']-2)
		return 0

	def grow_snake(self):
		new_part = {}
		new_part['x'] = self.snake[-1]['x']
		new_part['y'] = self.snake[-1]['y']
		if(self.direction == Direction.UP):
			new_part['y'] += 1
		elif(self.direction == Direction.DOWN):
			new_part['y'] -= 1
		elif(self.direction == Direction.LEFT):
			new_part['x'] += 1
		elif(self.direction == Direction.RIGHT):
			new_part['x'] -= 1
		self.snake.append(new_part)
		self.size += 1
		self.create_food()

	def collision_detection(self):
		if(self.snake[0]['x'] == self.food['x'] and self.snake[0]['y'] == self.food['y']):
			self.grow_snake()
			self.score += 10
		elif(self.snake[0]['x'] == 0 or self.snake[0]['x'] == self.board['width']-1):
			#colisao em x
			self.game_state = GameState.GAME_OVER
		elif(self.snake[0]['y'] == 0 or self.snake[0]['y'] == self.board['height']):
			#colisao em y
			self.game_state = GameState.GAME_OVER
		else:
			i = 1
			while(i < len(self.snake)):
				if(self.snake[0]['x'] == self.snake[i]['x'] and
					self.snake[0]['y'] == self.snake[i]['y']):
					self.game_state = GameState.GAME_OVER
				i = i+1

	def set_direction(self, new_direction):
		if(self.game_state == GameState.PLAYING):
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
		if(self.game_state == GameState.PLAYING):
			self.score -= 1
			new_part = {}
			new_part['x'] = self.snake[0]['x']
			new_part['y'] = self.snake[0]['y']
			if(self.direction == Direction.UP):
				new_part['y'] = new_part['y']-1
			elif(self.direction == Direction.DOWN):
				new_part['y'] = new_part['y']+1
			elif(self.direction == Direction.LEFT):
				new_part['x'] = new_part['x']-1
			elif(self.direction == Direction.RIGHT):
				new_part['x'] = new_part['x']+1

			removed_part = self.snake.pop()#tira ultimo ponto da cobra
			self.snake.insert(0, new_part)#cria novo ponto da cobra no comeco
			self.collision_detection()
			if(self.score < 0):
				self.game_state = GameState.GAME_OVER

	def get_game_info(self):
		obstacle_ahead = ((self.direction == Direction.RIGHT and self.snake[0]['x']+1 == self.board['width']-1)
			or (self.direction == Direction.LEFT and self.snake[0]['x']-1 == 0) 
			or (self.direction == Direction.UP and self.snake[0]['y']-1 == 0)
			or (self.direction == Direction.DOWN and self.snake[0]['y']+1 == self.board['height']))
		
		obstacle_to_the_left =  ((self.direction == Direction.RIGHT and self.snake[0]['y']-1 == 0)
			or (self.direction == Direction.LEFT and self.snake[0]['y']+1 == self.board['height'])
			or (self.direction == Direction.UP and self.snake[0]['x']-1 == 0)
			or (self.direction == Direction.DOWN and self.snake[0]['x']+1 == self.board['width']-1))

		obstacle_to_the_right = ((self.direction == Direction.RIGHT and self.snake[0]['y']+1 == self.board['height'])
			or (self.direction == Direction.LEFT and self.snake[0]['y']-1 == 0)
			or (self.direction == Direction.UP and self.snake[0]['x']+1 == self.board['width']-1)
			or (self.direction == Direction.DOWN and self.snake[0]['x']-1 == 0))

		food_to_the_left = ((self.direction == Direction.RIGHT and self.snake[0]['y'] > self.food['y'])
			or (self.direction == Direction.LEFT and self.snake[0]['y'] < self.food['y'])
			or (self.direction == Direction.UP and self.snake[0]['x'] > self.food['x'])
			or (self.direction == Direction.DOWN and self.snake[0]['x'] < self.food['x']))

		food_to_the_right = ((self.direction == Direction.RIGHT and self.snake[0]['y'] < self.food['y'])
			or (self.direction == Direction.LEFT and self.snake[0]['y'] > self.food['y'])
			or (self.direction == Direction.UP and self.snake[0]['x'] < self.food['x'])
			or (self.direction == Direction.DOWN and self.snake[0]['x'] > self.food['x']))

		return (obstacle_ahead, obstacle_to_the_left, obstacle_to_the_right, 
			food_to_the_left, food_to_the_right)

#class snake_nn_input:	
#	def read_input(self, state):
#		game_info = state.get_game_info()
#		parsed_nn_decision = self.parse_nn_decision(self.nn.decide(game_info))
#		self.state.set_direction(new_direction=parsed_nn_decision)
#		return 0

#	def parse_nn_decision(self, decision):
#		chosen = decision.index(max(decision))
#		return Direction(chosen)

#class snake_kb_input:
#	def read_game_input():
#		if(self.keypress == curses.KEY_UP):
#			self.state.set_direction(Direction.UP)
#		elif(self.keypress == curses.KEY_DOWN):
#			self.state.set_direction(Direction.DOWN)
#		elif(self.keypress == curses.KEY_RIGHT):
#			self.state.set_direction(Direction.RIGHT)
#		elif(self.keypress == curses.KEY_LEFT):
#			self.state.set_direction(Direction.LEFT)
#		return 0

class SnakeUI:
	def __init__(self, snake_state=None, nn=None, stdscr=None, debug='t', bh=20, bw=20,
		steering_type=SteeringType.ABSOLUTE):
		self.steering_type = steering_type
		self.state = snake_state
		self.bh = bh
		self.bw = bw

		self.keypress = None
		self.nn = None

		self.stdscr = curses.initscr()
		self.window = curses.newwin(bh+1, bw, 0, 0)		
		self.window.nodelay(1)
		self.window.keypad(1)
		
		if(nn == None):
			self.input = InputMode.KEYBOARD
		else:
			self.input = InputMode.NEURAL_NET
			self.nn = nn

		self.debug = debug
		self.debug_window = None
		self.debug_message = None
		if(self.debug == 't'):
			self.debug_window = curses.newwin(500, 100, bh+1, 0)
			self.debug_window.nodelay(1)
			self.debug_msg = ''

		curses.curs_set(0)
		curses.noecho()
		curses.cbreak()

	def start_game(self, nn=None):
		self.state = SnakeState(param_dir=Direction.DOWN, bw=self.bw, bh=self.bh, 
			steering_type=self.steering_type)

		if(nn == None):
			self.input = InputMode.KEYBOARD
		else:
			self.nn = nn
			self.input = InputMode.NEURAL_NET

	def render(self):
		if(self.debug == 't'):
			self.render_debug_window()		
		self.window.clear()
		self.window.border(0)
		
		#Cobra, alimento e pontuacao
		for snake_part in self.state.snake:
			self.window.addch(snake_part['y'], snake_part['x'], '*')
		self.window.addch(self.state.food['y'], self.state.food['x'], 'A')
		self.window.addstr(0, self.state.board['width']-5, str(self.state.score))
		
		if(self.state.game_state == GameState.PLAYING):
			game_info = self.state.get_game_info()
		#elif(self.state.game_state == GameState.GAME_OVER):
		#	self.debug_msg = 'dead. up to restart, down to quit'

		self.read_keyboard_input()

		if(self.input == InputMode.NEURAL_NET):
			self.read_nn_input()

	def read_nn_input(self):
		game_info = self.state.get_game_info()
		nn_output = self.nn.decide(game_info)
		#self.debug_msg += 'nn_output '+str(nn_output)
		chosen_direction = nn_output.index(max(nn_output))
		#self.debug_msg += 'chosen'+str(chosen_direction)+'\n'
		self.state.set_direction(new_direction=Direction(chosen_direction))
		return 0

	def render_debug_window(self):
		self.debug_window.clear()
		self.debug_window.border(0)
		self.debug_window.addstr(1, 1, self.debug_msg)
		self.debug_window.refresh()

	def read_keyboard_input(self):
		self.keypress = self.window.getch()
		curses.flushinp()		
		if(self.input == InputMode.KEYBOARD):
			if(self.state.game_state == GameState.GAME_OVER):
				if(self.keypress == curses.KEY_UP):
					self.start_game()
				if(self.keypress == curses.KEY_DOWN):
					self.state.end_game()
			else:
				if(self.keypress == curses.KEY_UP):
					self.state.set_direction(Direction.UP)
				elif(self.keypress == curses.KEY_DOWN):
					self.state.set_direction(Direction.DOWN)
				elif(self.keypress == curses.KEY_RIGHT):
					self.state.set_direction(Direction.RIGHT)
				elif(self.keypress == curses.KEY_LEFT):
					self.state.set_direction(Direction.LEFT)		
				
	def get_snake_state(self):
		return self.state

	def kill_ui(self):
		if(self.input == InputMode.KEYBOARD):
			self.window.keypad(False)
		curses.nocbreak()
		curses.echo()
		curses.endwin()

def init_perceptrons(qtt, inp_size):
	perceptrons = []
	for i in range(0, qtt):
		perceptron = Perceptron(inp_size=inp_size)
		perceptrons.append(perceptron)
	return perceptrons

def init_nns(qtt, inp_size, out_size):
	nns = []
	for nn in range(0, qtt):
		nn = SingleLayerNN(inp_size=inp_size, out_size=out_size, activation=linear)
		nns.append(nn)
	return nns

def ai_game_loop(param_dir=Direction.DOWN, update_freq=10000, render_freq=10000, bw=20, bh=20, 
	steering_type=SteeringType.ABSOLUTE):

	if(param_dir == None):
		param_dir = Direction.DOWN
	if(update_freq == None):
		update_freq = 30
	if(render_freq == None):
		render_freq = 30
	if(bw == None):
		bw = 20
	if(bh == None):
		bh = 20

	inp_size = 5
	out_size = 3
	nns = init_nns(qtt=5, inp_size=inp_size, out_size=out_size)

	time_between_updates = 1/update_freq
	time_between_renders = 1/render_freq

	last_update_time = time.time()
	last_render_time = time.time()

	snake_ui = SnakeUI(snake_state=None, steering_type=steering_type, bw=bw, bh=bh)
	best_score = 0
	for generation in range(0, 5000):
		scores = []
		for nn in nns:
			snake_ui.start_game(nn)
			
			while(snake_ui.state.game_state != GameState.GAME_OVER):
				current_time = time.time()
				if(abs(current_time - last_update_time) > time_between_updates):
					snake_ui.state.step()
					last_update_time = time.time()

				if(abs(current_time - last_render_time) > time_between_renders):
					snake_ui.render()
					last_render_time = time.time()

			scores.append(snake_ui.state.size)
		
		if(max(scores)>best_score):
			best_score = max(scores)

		snake_ui.debug_msg = 'best {} gen {}'.format(str(best_score), str(generation))
		indivs = slnns_to_genotype(nns, scores)
		new_gen = breed_new_gen(indivs)
		nns = genotypes_to_slnns(new_gen, inp_size=inp_size, out_size=out_size)

	snake_ui.kill_ui()

def game_loop(param_dir=None, update_freq=None, render_freq=None, bw=None, bh=None, 
	steering_type=SteeringType.ABSOLUTE):

	if(param_dir == None):
		param_dir = Direction.DOWN
	if(update_freq == None):
		update_freq = 20
	if(render_freq == None):
		render_freq = 20
	if(bw == None):
		bw = 20
	if(bh == None):
		bh = 20

	snake_ui = SnakeUI(bw=bw, bh=bh, steering_type=steering_type)
	snake_ui.start_game()

	time_between_updates = 1/update_freq
	time_between_renders = 1/render_freq

	last_update_time = time.time()
	last_render_time = time.time()

	while(snake_ui.state.game_state != GameState.CLOSING):
		current_time = time.time()
		if(abs(current_time - last_update_time) > time_between_updates):
			snake_ui.state.step()
			last_update_time = time.time()

		if(abs(current_time - last_render_time) > time_between_renders):
			snake_ui.render()
			last_render_time = time.time()

	snake_ui.kill_ui()
	return 0

def parse_cl_args():
	arguments = sys.argv
	args = {}
	for i in range(1, len(sys.argv), 2):
		if(arguments[i] == '-dir'):
			args['dir'] = arguments[i+1]
		elif(arguments[i] == '-ui'):
			args['ui'] = arguments[i+1]
		elif(arguments[i] == '-uf'):
			args['uf'] = int(arguments[i+1])
		elif(arguments[i] == '-rf'):
			args['rf'] = int(arguments[i+1])
		elif(arguments[i] == '-kb'):
			args['inp'] = InputMode.KEYBOARD
		elif(arguments[i] == '-nn'):
			args['inp'] = InputMode.NEURAL_NET
		elif(arguments[i] == '-bw'):
			args['bw'] = int(arguments[i+1])
		elif(arguments[i] == '-bh'):
			args['bh'] = int(arguments[i+1])
		elif(arguments[i] == '-rs'):
			args['st'] = SteeringType.RELATIVE
		elif(arguments[i] == '-as'):
			args['st'] = SteeringType.ABSOLUTE
	#IMPLEMENTAR ARG BW E BH

	if('dir' not in args.keys()):
		args['dir'] = None
	if('ui' not in args.keys()):
		args['ui'] = 't'
	if('uf' not in args.keys()):
		args['uf'] = None
	if('rf' not in args.keys()):
		args['rf'] = None
	if('inp' not in args.keys()):
		args['inp'] = InputMode.KEYBOARD
	if('bw' not in args.keys()):
		args['bw'] = None
	if('bh' not in args.keys()):
		args['bh'] = None
	if('st' not in args.keys()):
		args['st'] = SteeringType.RELATIVE

	return args
		

def main():
	args = parse_cl_args()

	if(args['ui'] == 't'):
		if(args['inp'] == InputMode.KEYBOARD):
			game_loop(param_dir=args['dir'], 
				update_freq=args['uf'], render_freq=args['rf'], bw=args['bw'], bh=args['bh'],
				steering_type=args['st'])
		else:
			ai_game_loop(param_dir=args['dir'], 
				update_freq=args['uf'], render_freq=args['rf'], bw=args['bw'], bh=args['bh'],
				steering_type=args['st'])

main()