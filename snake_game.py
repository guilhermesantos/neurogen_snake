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
import snake as snk

class InputMode(Enum):
	KEYBOARD = 0
	NEURAL_NET	 = 1

class SnakeUI:
	def __init__(self, snake_state=None, nn=None, stdscr=None, debug='t', bh=20, bw=20,
		steering_type=snk.SteeringType.ABSOLUTE):
		self.update_freq = 50
		self.render_freq = self.update_freq

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
			self.debug_window = curses.newwin(5, 20, bh+1, 0)
			self.debug_window.nodelay(1)
			self.debug_msg = ''

		curses.curs_set(0)
		curses.noecho()
		curses.cbreak()
		
		self.part_ahead = 0
		self.part_right = 0
		self.part_left = 0
		self.display_ui = True

	def start_game(self, nn=None):
		self.state = snk.SnakeBoard(width=self.bw, height=self.bh, 
			steering_type=self.steering_type)

		if(nn == None):
			self.input = InputMode.KEYBOARD
		else:
			self.nn = nn
			self.input = InputMode.NEURAL_NET

	def render(self):
		if(self.display_ui):
			self.window.clear()
			self.window.border(0)
		
		self.read_keyboard_input()


		if(self.state.game_state == snk.GameState.PLAYING):
		
			if(self.input == InputMode.NEURAL_NET):
				self.read_nn_input()

			self.state.step()
			
			#Cobra, alimento e pontuacao
			if(self.display_ui):
				for snake in self.state.snakes:
					if(snake.state == snk.SnakeState.ALIVE):
						self.window.addstr(0, self.state.width-5, str(self.state.snakes[0].hunger))
						for snake_part in snake.parts:
							self.window.addch(snake_part[1], snake_part[0], '*')


				self.window.addch(self.state.food[1], self.state.food[0], 'A')


		if(self.debug == 't' and self.display_ui):
			self.render_debug_window()

		if(self.display_ui):
			self.window.refresh()

	def update(self):

		return 0


	def read_nn_input(self):
		game_info = self.state.snakes[0].get_game_info()
		nn_output = self.nn.decide(game_info)
		chosen_direction = nn_output.index(max(nn_output))
		part_ahead = game_info[3]
		part_left = game_info[4]
		part_right = game_info[5]
		if(part_ahead):
			self.part_ahead += 1
		if(part_left):
			self.part_left += 1
		if(part_right):
			self.part_right += 1
		#self.debug_msg = ' ahead {} left {} right {}'.format(self.part_ahead, self.part_left, self.part_right)
		self.state.snakes[0].set_direction(new_direction=snk.Direction(chosen_direction))
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
			if(self.state.game_state == snk.GameState.GAME_OVER):
				if(self.keypress == curses.KEY_UP):
					self.start_game()
				if(self.keypress == curses.KEY_DOWN):
					self.state.end_game()
			else:
				if(self.keypress == curses.KEY_UP):
					self.state.snakes[0].set_direction(snk.Direction.UP)
				elif(self.keypress == curses.KEY_DOWN):
					self.state.snakes[0].set_direction(snk.Direction.DOWN)
				elif(self.keypress == curses.KEY_RIGHT):
					self.state.snakes[0].set_direction(snk.Direction.RIGHT)
				elif(self.keypress == curses.KEY_LEFT):
					self.state.snakes[0].set_direction(snk.Direction.LEFT)
		else:
			if(self.keypress == curses.KEY_DOWN):
				self.state.end_game()
				self.kill_ui()
				exit()
			elif(self.keypress == curses.KEY_RIGHT):
				self.update_freq += 25
				self.render_freq = self.update_freq
			elif(self.keypress == curses.KEY_LEFT):
				if(self.update_freq - 25 > 0):
					self.update_freq -= 25
					self.render_freq = self.update_freq
			elif(self.keypress == curses.KEY_UP):
				self.display_ui = not self.display_ui

	def kill_ui(self):
		if(self.input == InputMode.KEYBOARD):
			self.window.keypad(False)
		curses.nocbreak()
		curses.echo()
		curses.endwin()

class NeuralNetSnake():
	def __init__(self):
		self.snake = None
		self.nns = []
		self.scores = []
		self.active_nn = None

	def set_score(self, nn):
		return 0

	def predict(self):
		return 0

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

def ai_game_loop(param_dir=snk.Direction.DOWN, update_freq=10000, render_freq=10000, bw=20, bh=20, 
	steering_type=snk.SteeringType.ABSOLUTE):

	if(param_dir == None):
		param_dir = snk.Direction.DOWN
	if(update_freq == None):
		update_freq = 30
	if(render_freq == None):
		render_freq = 30
	if(bw == None):
		bw = 20
	if(bh == None):
		bh = 20

	snake_qtt = 2

	snake_ui = SnakeUI(snake_state=None, steering_type=steering_type, bw=bw, bh=bh)
	best_size = 0
	generation = 0

	inp_size = 7
	out_size = 3

	nns = init_nns(qtt=5, inp_size=inp_size, out_size=out_size)

	time_between_updates = 1/10
	time_between_renders = 1/10

	last_update_time = time.time()
	last_render_time = time.time()

	memory = dict()

	while(generation < 500000 and (snake_ui.state == None or snake_ui.state.game_state != snk.GameState.CLOSING)):
		scores = []
		sizes = []
		for nn in nns:
			snake_ui.start_game(nn)
			
			while(snake_ui.state.game_state != snk.GameState.GAME_OVER):
				current_time = time.time()
				if(snake_ui.display_ui):
					if(abs(current_time - last_update_time) > 1/snake_ui.update_freq):
						snake_ui.update()
						snake_ui.render()
						last_update_time = time.time()
				else:
					snake_ui.update()
					snake_ui.render()
					last_update_time = time.time()
				#if(abs(current_time - last_render_time) > 1/snake_ui.render_freq):
				#	snake_ui.render()
				#	last_render_time = time.time()

			scores.append(snake_ui.state.snakes[0].score())
			sizes.append(snake_ui.state.snakes[0].size)
		
		if(max(sizes)>best_size):
			best_size = max(sizes)

		snake_ui.debug_msg = 'best {} gen {}'.format(str(best_size), str(generation))
		indivs = slnns_to_genotype(nns, scores)
		new_gen = breed_new_gen(indivs, memory)
		nns = genotypes_to_slnns(new_gen, inp_size=inp_size, out_size=out_size)
		generation += 1

	return 0

def game_loop(param_dir=None, update_freq=None, render_freq=None, bw=None, bh=None, 
	steering_type=snk.SteeringType.ABSOLUTE):

	if(param_dir == None):
		param_dir = snk.Direction.DOWN
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

	while(snake_ui.state.game_state != snk.GameState.CLOSING):
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
			args['st'] = snk.SteeringType.RELATIVE
		elif(arguments[i] == '-as'):
			args['st'] = snk.SteeringType.ABSOLUTE

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
		args['st'] = snk.SteeringType.RELATIVE

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