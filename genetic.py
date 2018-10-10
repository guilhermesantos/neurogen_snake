from perceptron import Perceptron
import numpy as np
from operator import itemgetter

def init_perceptrons(qtt, inp_size):
	perceptrons = []
	for i in range(0, qtt):
		perceptron = Perceptron(inp_size=inp_size)
		perceptrons.append(perceptron)
	return perceptrons

def breed_new_gen(perceptrons, scores):
	indiv_qtt = len(perceptrons)
	indivs = []
	for i in range(0, indiv_qtt):
		indiv = {}
		#indiv['perc'] = perceptrons[i]
		indiv['activ_params'] = perceptrons[i].activ_params
		indiv['weights'] = perceptrons[i].weights
		indiv['score'] = scores[i]
		indivs.append(indiv)
		#print('individual')
		#print(indiv)

	#print('unsorted indivs')
	#print(indivs)
	#print('\n')

	sorted_indivs = sorted(indivs, key=itemgetter('score'))	
	print('sorted indivs')
	for indiv in sorted_indivs:
		print('weights', indiv['weights'])
	print('\n')

	best_indiv = len(sorted_indivs)-1
	#print('best indiv', best_indiv)
	
	new_gen = []
	for i in range(0, indiv_qtt):
		father = best_indiv
		mother = i
		new_indiv = mate(sorted_indivs[father], sorted_indivs[mother])
		new_indiv = mutate(new_indiv)
		#print('pai {} mae {} novo indice {}'.format(str(father), str(mother), str(i)))
		#print('father', sorted_indivs[father]['weights'])
		#print('mother', sorted_indivs[mother]['weights'])
		#print('child', new_indiv['weights'])
		#print('\n')
		new_gen.append(new_indiv)

	for indiv in new_gen:
		print('weights', indiv['weights'])		
	print('\n')

	return new_gen

def roulette(indivs):
	return 0

def mutate(indiv):
	for i in range(0, len(indiv['weights'])):
		mutation_chance = np.random.uniform(0, 1)
		if(mutation_chance <= 0.3):
			print('mutate index', i)
			sum_chance = np.random.uniform(0,1)
			if(sum_chance <= 0.5):
				print('sum')
				indiv['weights'][i] = indiv['weights'][i]+0.1*indiv['weights'][i]
			else:
				print('sub')
				indiv['weights'][i] = indiv['weights'][i]-0.1*indiv['weights'][i]
	
	return indiv

def mate(father, mother):
	new_indiv = {}
	new_indiv['weights'] = []
	for i in range(0, len(father['weights'])):
		new_indiv['weights'].append((father['weights'][i]+mother['weights'][i])/2)

	new_indiv['activ_params'] = []
	for i in range(0, len(father['activ_params'])):
		new_indiv['activ_params'].append((father['activ_params'][i]+mother['activ_params'][i])/2)
	#print('mate. new indiv')
	#print(new_indiv['weights'])
	#print('\n')
	return new_indiv

def main():
	random_scores = []
	for i in range(0,10):
		random_scores.append(int(np.random.uniform(0, 500)))
	perceptrons = init_perceptrons(qtt=10, inp_size=3)
	breed_new_gen(perceptrons, random_scores)
	return 0

main()