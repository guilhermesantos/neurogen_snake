import numpy as np
import math

def threshold(net, treshold=0.0):
	return 1 if net >= treshold else 0

def sigmoid(net, slope=1.0):
	return 1/(1+exp(-net*slope))

def piecewise(net, activ_params):
	cutoff_x1 = activ_params[0]
	cutoff_x2 = activ_params[1]
	cutoff_x3 = activ_params[2]

	if(net <= -1):
		return 0
	elif(net > -1 and net <= 0):
		return 1	
	elif(net > 0 and net <= 1):
		return 2
	return 3

class Perceptron:
	def __init__(self, inp_size, activ_funct=piecewise, activ_params=None, weights=None):
		self.activ_funct = activ_funct

		if(activ_params == None):
			self.activ_params = np.random.uniform(-10.0, 10.0, 3)
		else:
			self.activ_params = activ_params

		if(weights == None):
			self.weights = np.random.uniform(-10.0, 10.0, inp_size)
		else:
			self.weights = weights

		#print('weights', self.weights)
		#print('activ params',self.activ_params,'\n')

	def decide(self, inp_data):
		#faz a combinacao linear dos parametros pelos pesos
		net = sum(list(map(lambda x, y: x*y, inp_data, self.weights)))
		#print('net', net)
		#aplica a funcao de ativacao
		f_net = self.activ_funct(net, activ_params=self.activ_params)
		return f_net

def main():
	perceptron = Perceptron(inp_size=3)
	test_info = np.random.uniform(-1.0, 1.0, 3)
	print('weights', perceptron.weights)
	print('activ_params', perceptron.activ_params)
	print('test info', test_info)
	decision = perceptron.decide(test_info)
	print('decision', decision)
	return 0

#main()
