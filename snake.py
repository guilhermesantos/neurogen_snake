#Baseado no jogo de snake em https://github.com/korolvs/snake_nn/

import curses
from curses import wrapper
from random import randint
import sys
import time
import tensorflow

class SnakeState:
	def __init__(self, board_width=20, board_height = 20, param_dir='left'):
		self.dirs = {'up':0, 'down':1, 'left':2, 'right':3}
		self.direction = self.dirs[param_dir]
		self.food = {}
		self.num = 0
		self.score = 0
		self.game_over = False
		self.board = {'width': board_width, 'height': board_height}
		self.snake = []
		#starting_x = randint(5, board_width-5)
		#starting_y = randint(5, board_height-5)
		starting_x = 5
		starting_y = 5

		for i in range(0,3):
			part = {}
			if(self.direction == self.dirs['up']):
				part['x'] = starting_x
				part['y'] = starting_y+i
			elif(self.direction == self.dirs['down']):
				part['x'] = starting_x
				part['y'] = starting_y-i
			elif(self.direction == self.dirs['left']):
				part['x'] = starting_x+i
				part['y'] = starting_y
			elif(self.direction == self.dirs['right']):
				part['x'] = starting_x-i
				part['y'] = starting_y

			self.snake.append(part)

		self.create_food()

	def create_food(self):
		self.food['x'] = randint(1, self.board['width']-2)
		self.food['y'] = randint(1, self.board['height']-2)
		return 0

	def grow_snake(self):
		new_part = {}
		new_part['x'] = self.snake[-1]['x']
		new_part['y'] = self.snake[-1]['y']
		if(self.direction == self.dirs['up']):
			new_part['y'] += 1
		elif(self.direction == self.dirs['down']):
			new_part['y'] -= 1
		elif(self.direction == self.dirs['left']):
			new_part['x'] += 1
		elif(self.direction == self.dirs['right']):
			new_part['x'] -= 1
		self.snake.append(new_part)
		self.create_food()

	def collision_detection(self):
		if(self.snake[0]['x'] == self.food['x'] and self.snake[0]['y'] == self.food['y']):
			self.grow_snake()
			self.score += 10
		elif(self.snake[0]['x'] == 0 or self.snake[0]['x'] == self.board['width']-1):
			#colisao em x
			self.game_over = True
		elif(self.snake[0]['y'] == 0 or self.snake[0]['y'] == self.board['height']):
			#colisao em y
			self.game_over = True
		else:
			i = 1
			while(i < len(self.snake) and self.game_over == False):
				if(self.snake[0]['x'] == self.snake[i]['x'] and
					self.snake[0]['y'] == self.snake[i]['y']):
					self.game_over = True
				i = i+1

	def set_direction(self, new_direction_str=None, new_direction_int=None):
		if(new_direction_int is None):
			new_direction = self.dirs[new_direction_str]
		else:
			new_direction = new_direction_int

		if(new_direction == self.dirs['up'] and self.direction != self.dirs['down']):
			self.direction = self.dirs['up']
		elif(new_direction == self.dirs['down'] and self.direction != self.dirs['up']):
			self.direction = self.dirs['down']
		elif(new_direction == self.dirs['left'] and self.direction != self.dirs['right']):
			self.direction = self.dirs['left']
		elif(new_direction == self.dirs['right'] and self.direction != self.dirs['left']):
			self.direction = self.dirs['right']

	def step(self):
		new_part = {}
		new_part['x'] = self.snake[0]['x']
		new_part['y'] = self.snake[0]['y']
		if(self.direction == self.dirs['up']):
			new_part['y'] = new_part['y']-1
		elif(self.direction == self.dirs['down']):
			new_part['y'] = new_part['y']+1
		elif(self.direction == self.dirs['left']):
			new_part['x'] = new_part['x']-1
		elif(self.direction == self.dirs['right']):
			new_part['x'] = new_part['x']+1

		removed_part = self.snake.pop()#tira ultimo ponto da cobra
		self.snake.insert(0, new_part)#cria novo ponto da cobra no comeco
		self.collision_detection()


class SnakeUI:
	def __init__(self, state, keyboard='t', stdscr=None):
		self.state = state
		self.keyboard = keyboard
		self.keypress = None
		self.stdscr = curses.initscr()

		self.window = curses.newwin(state.board['width'], state.board['height'], 0, 0)		
		#self.window.timeout(200)

		curses.curs_set(0)
		curses.noecho()
		curses.cbreak()
		curses.flushinp()

		#if(self.keyboard):
		if(keyboard == 't')
			self.window.nodelay(1)
			self.window.keypad(1)
			self.window.nodelay(True)
		#wrapper(self.set_stdscr)
		
		self.render()

	def render(self):
		self.window.clear()
		self.window.border(0)
		
		#colocar score
		for snake_part in self.state.snake:
			self.window.addch(snake_part['y'], snake_part['x'], '*')

		self.window.addstr(0, self.state.board['width']-5, str(self.state.score))

		self.window.addch(self.state.food['y'], self.state.food['x'], 'A')
		self.keypress = self.window.getch()
		curses.flushinp()
		

		if(self.keyboard == 't'):
			if(self.keypress == 259):
				self.state.set_direction(new_direction_str='up')
			elif(self.keypress == curses.KEY_DOWN):
				self.state.set_direction(new_direction_str='down')
			elif(self.keypress == curses.KEY_RIGHT):
				self.state.set_direction(new_direction_str='right')
			elif(self.keypress == curses.KEY_LEFT):
				self.state.set_direction(new_direction_str='left')

	def kill_ui(self):
		if(self.keyboard == 't'):
			self.window.keypad(False)
		curses.nocbreak()
		curses.echo()
		curses.endwin()
		return 0

	def new_state(self, state):
		#substitui state e renderiza janela de novo
		return 0

def ui_game_loop(param_dir='left', update_freq=10, render_freq=10):
	return 0

def invisible_game_loop(param_dir='left', update_freq=10, render_freq=10):
	return 0

def game_loop(param_dir='left', ui_mode='t', update_freq=10, render_freq=10, keyboard='t'):
	snake_state = SnakeState(param_dir=param_dir)
	
	if(ui_mode == 't'):
		snake_ui = SnakeUI(state=snake_state, keyboard=keyboard)
		#wrapper(snake_ui.set_stdscr)

		time_between_updates = 1/update_freq
		time_between_renders = 1/render_freq

		last_update_time = time.time()
		last_render_time = time.time()

		while(snake_state.game_over == False):
			current_time = time.time()
			if(abs(current_time - last_update_time) > time_between_updates):
				snake_state.step()
				last_update_time = time.time()

			if(abs(current_time - last_render_time) > time_between_renders):
				snake_ui.render()
				last_render_time = time.time()

		snake_ui.kill_ui()
	else:
		time_between_updates = 1/update_freq
		last_update_time = time.time()

		while(snake_state.game_over == False):
			current_time = time.time()
			if(abs(current_time - last_update_time) > time_between_updates):
				snake_state.step()
				last_update_time = time.time()
				print(snake_state.__dict__)
		
	#enquanto usuario quer continuar
		#para cada geracao ate o numero de geracoes especificado
			#tem cobra viva?
				#itera sobre todos os pares snake state/snake ui (se estiver em modo grafico) que estao vivas 
				#pega estado do jogo
					#joga na rede neural
					#joga saida da rede neural no jogo
					#step
					#render (se estiver em modo grafico)
					#pega estado do jogo
					#cobra morreu?
						#tira da lista de cobras vivas
			#nao tem cobra viva?
				#calcula fitness de todas as cobras da geração
				#cruza as melhores
				#cria as novas redes neurais
				#cria novos pares snake state/snake ui (se estiver em modo grafico)
				#comeca de novo
	#continua? 
	#quantas geracoes?
	#modo grafico? 

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
			args['kb'] = arguments[i+1]

	if('dir' not in args.keys()):
		args['dir'] = 'left'
	if('ui' not in args.keys()):
		args['ui'] = 't'
	if('uf' not in args.keys()):
		args['uf'] = 10
	if('rf' not in args.keys()):
		args['rf'] = 10
	if('kb' not in args.keys()):
		args['kb'] = 't'

	return args
		

def main():
	args = parse_cl_args()
	if(args['ui'] == 't'):
		ui_game_loop(param_dir=args['dir'], update_freq=args['uf'], render_freq=args['rf'])
	else:
		invisible_game_loop(param_dir=args['dir'], update_freq=args['uf'], render_freq=args['rf'])

	game_loop(param_dir=args['dir'], ui_mode=args['ui'], 
		update_freq=args['uf'], render_freq=args['rf'], keyboard=args['kb'])

main()