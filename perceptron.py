import numpy as np
import math

def threshold(net, treshold=0.0):
	return 1 if net >= treshold else 0

def sigmoid(net, slope=1.0):
	np.seterr('ignore')
	return 1/(1+np.exp(-net*slope))

def step(net):
	if(net <= 0):
		return 0
	elif(net > 0):
		return 1

def linear(net, slope=1.0):
	return net

class Perceptron:
	def __init__(self, inp_size, activation=step, activ_params=None, weights=[]):
		self.activation = activation

		self.activ_params = None

		if(len(weights) == 0):
			self.weights = np.random.uniform(-100.0, 100.0, inp_size)
		else:
			self.weights = weights

		#print('weights', self.weights)
		#print('activ params',self.activ_params,'\n')

	def decide(self, inp_data):
		#faz a combinacao linear dos parametros pelos pesos
		net = sum(list(map(lambda x, y: x*y, inp_data, self.weights)))
		#print('net', net)
		#aplica a funcao de ativacao
		f_net = self.activation(net)
		return f_net

	def to_genotype(self, score):
		indiv = {}
		indiv['features'] = self.weights
		indiv['score'] = score
		return indiv

def perceptrons_to_genotype(perceptrons, scores):
	population = []
	for i in range(0, len(perceptrons)):
		population.append(perceptrons[i].to_genotype(scores[i]))

	return population

def slnns_to_genotype(slnns, scores):
	population = []
	for i in range(0, len(slnns)):
		population.append(slnns[i].to_genotype(scores[i]))
	return population

def genotypes_to_slnns(genotypes, inp_size, out_size, activation=linear):
	nns = []
	for indiv in genotypes:
		nn = SingleLayerNN(inp_size=inp_size, out_size=out_size, weights=indiv['features'], 
			activation=activation)
		nns.append(nn)
	return nns

class SingleLayerNN:
	def __init__(self, inp_size=3, out_size=2, activation=step, weights=[]):
		self.ps = []
		self.p_qtt = out_size

		j = 0
		for i in range(0, self.p_qtt):
			p = None
			if(len(weights) > 0):
				#print('recebeu weights de parametro')
				p_weights = []
				while(len(p_weights) < inp_size):
					#print('colocando peso',weights[j],'no perceptron')
					p_weights.append(weights[j])
					j = j+1
				p = Perceptron(inp_size=inp_size, weights=p_weights, activation=activation)
			else:
				p= Perceptron(inp_size=inp_size, activation=activation)

			self.ps.append(p)

	def decide(self, inp_data):
		out = []
		for p in self.ps:
			out.append(p.decide(inp_data))
		return out

	def to_genotype(self, score):
		indiv = {}
		indiv['features'] = []
		for i in range(0, len(self.ps)):
			for j in range(0, len(self.ps[i].weights)):
				indiv['features'].append(self.ps[i].weights[j])
		indiv['score'] = score
		return indiv

	def print(self):
		for i in range(0, len(self.ps)):
			print('perceptron',i,'weights', self.ps[i].weights)
		return 0

def main():
	test_info = np.random.randint(0, 2, 3)
	
	scores = list(range(0,3))
	print('scores', scores)

	indivs = []
	for i in range(0, 3):
		sl_nn = SingleLayerNN(inp_size=4, out_size=3, activation=linear)
		for j in range(0, sl_nn.p_qtt):
			print('slnn',i, 'p=',j,'weights', sl_nn.ps[j].weights)
		random_data = np.random.uniform(-10, 10, 4)
		print('random data to be input into the NN', random_data)
		print('nn decision', sl_nn.decide(random_data))
		print('\n')

	return 0

main()
