#Autor: Guilherme Milan Santos
#Baseado no jogo de snake em https://github.com/korolvs/snake_nn/

import curses
from random import randint
import sys
import time
from enum import Enum
from perceptron import Perceptron
import genetic

class GameState(Enum):
	PLAYING = 0
	PAUSED = 1
	GAME_OVER = 2
	CLOSING = 3

class Direction(Enum):
	UP = 0
	DOWN = 1
	LEFT = 2
	RIGHT = 3

class InputMode(Enum):
	KEYBOARD = 0
	NEURAL_NET	 = 1

class SnakeState:
	def __init__(self, bw=20, bh = 20, param_dir=Direction.DOWN):
		self.direction = param_dir
		self.food = {}
		self.num = 0
		self.score = 0
		self.game_state = GameState.PLAYING
		self.board = {'width': bw, 'height': bh}
		self.snake = []

		starting_x = 5
		starting_y = 5

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
			if(new_direction == Direction.UP and self.direction != Direction.DOWN):
				self.direction = Direction.UP

			elif(new_direction == Direction.DOWN and self.direction != Direction.UP):
				self.direction = Direction.DOWN

			elif(new_direction == Direction.LEFT and self.direction != Direction.RIGHT):
				self.direction = Direction.LEFT

			elif(new_direction == Direction.RIGHT and self.direction != Direction.LEFT):
				self.direction = Direction.RIGHT

	def step(self):
		if(self.game_state == GameState.PLAYING):
			self.score += 1
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

		return (obstacle_ahead, obstacle_to_the_left, obstacle_to_the_right)

class SnakeUI:
	def __init__(self, snake_state=None, perceptron=None, stdscr=None, debug='t', bh=20, bw=20):
		self.state = snake_state
		self.bh = bh
		self.bw = bw

		self.keypress = None
		self.perceptron = None

		self.stdscr = curses.initscr()
		self.window = curses.newwin(bh+1, bw, 0, 0)		
		self.window.nodelay(1)
		self.window.keypad(1)
		
		if(perceptron == None):
			self.input = InputMode.KEYBOARD
		else:
			self.input = InputMode.NEURAL_NET
			self.perceptron = perceptron

		self.debug = debug
		self.debug_window = None
		self.debug_message = None
		if(self.debug == 't'):
			self.debug_window = curses.newwin(5, bw, 
				bh+1, 0)
			self.debug_window.nodelay(1)
			self.debug_msg = ''

		curses.curs_set(0)
		curses.noecho()
		curses.cbreak()
		#self.render()

	def start_game(self, perceptron=None):
		self.state = SnakeState(param_dir=Direction.DOWN, bw=self.bw, bh=self.bh)
		if(perceptron == None):
			self.input = InputMode.KEYBOARD
		else:
			self.perceptron = perceptron
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
			#self.debug_msg = 'playing'
		elif(self.state.game_state == GameState.GAME_OVER):
			self.debug_msg = 'dead. up to quit, down to restart'

		self.read_keyboard_input()

		if(self.input == InputMode.NEURAL_NET):
			self.read_nn_input()

	def read_nn_input(self):
		game_info = self.state.get_game_info()
		nn_decision = self.perceptron.decide(game_info)
		self.state.set_direction(new_direction=Direction(nn_decision))
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
					self.state.end_game()
				if(self.keypress == curses.KEY_DOWN):
					self.restart_game()
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

	def restart_game(self, perceptron=None):
		self.state = SnakeState(param_dir=Direction.RIGHT, bh=self.bh, 
			bw=self.bw)
		if(perceptron != None):
			self.perceptron = perceptron
			self.input = InputMode.NEURAL_NET
		else:
			self.input = InputMode.KEYBOARD

def init_perceptrons(qtt, inp_size):
	perceptrons = []
	for i in range(0, qtt):
		perceptron = Perceptron(inp_size=inp_size)
		perceptrons.append(perceptron)
	return perceptrons

def ai_game_loop(param_dir=Direction.DOWN, update_freq=10000, render_freq=10000, bw=20, bh=20):
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

	perceptrons = init_perceptrons(qtt=10, inp_size=3)

	time_between_updates = 1/update_freq
	time_between_renders = 1/render_freq

	last_update_time = time.time()
	last_render_time = time.time()

	snake_ui = SnakeUI(snake_state=None)
	for generation in range(0, 5000):
		scores = []
		for perceptron in perceptrons:
			#snake_state = SnakeState(param_dir=param_dir, bw=bw, bh=bh)
			snake_ui.start_game(perceptron)
			snake_ui.debug_msg = 'geracao {} qtd percep {}'.format(str(generation), str(len(perceptrons)))
			
			while(snake_ui.state.game_state != GameState.GAME_OVER):
				current_time = time.time()
				if(abs(current_time - last_update_time) > time_between_updates):
					snake_ui.state.step()
					last_update_time = time.time()

				if(abs(current_time - last_render_time) > time_between_renders):
					snake_ui.render()
					last_render_time = time.time()

			scores.append(snake_ui.state.score)
		
		new_gen = genetic.breed_new_gen(perceptrons, scores)
		perceptrons = []
		for indiv in new_gen:
			perceptron = Perceptron(inp_size=len(indiv['weights']), weights=indiv['weights'])
			perceptrons.append(perceptron)

	snake_ui.kill_ui()

def game_loop(param_dir=None, update_freq=None, render_freq=None, bw=None, bh=None):
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

	snake_state = SnakeState(param_dir=param_dir, bw=bw, bh=bh)	
	snake_ui = SnakeUI(snake_state=snake_state)

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
	#else:
	#	time_between_updates = 1/update_freq
	#	last_update_time = time.time()

	#	while(snake_state.game_state != GameState.CLOSING):
	#		current_time = time.time()
	#		if(abs(current_time - last_update_time) > time_between_updates):
	#			snake_state.step()
	#			last_update_time = time.time()
	#			print(snake_state.__dict__)
		
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
			args['inp'] = InputMode.KEYBOARD
		elif(arguments[i] == '-nn'):
			args['inp'] = InputMode.NEURAL_NET
		elif(arguments[i] == '-bw'):
			args['bw'] = int(arguments[i+1])
		elif(arguments[i] == '-bh'):
			args['bh'] = int(arguments[i+1])

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

	return args
		

def main():
	args = parse_cl_args()

	if(args['ui'] == 't'):
		if(args['inp'] == InputMode.KEYBOARD):
			game_loop(param_dir=args['dir'], 
				update_freq=args['uf'], render_freq=args['rf'], bw=args['bw'], bh=args['bh'])
		else:
			ai_game_loop(param_dir=args['dir'], 
				update_freq=args['uf'], render_freq=args['rf'], bw=args['bw'], bh=args['bh'])

main()