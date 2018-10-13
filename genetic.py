import perceptron
from perceptron import Perceptron
from perceptron import SingleLayerNN
import numpy as np
from operator import itemgetter

def init_nns(qtt, inp_size, out_size):
	nns = []
	for nn in range(0, qtt):
		nn = SingleLayerNN(inp_size=inp_size, out_size=out_size)
		nns.append(nn)
	return nns

def init_perceptrons(qtt, inp_size):
	perceptrons = []
	for i in range(0, qtt):
		perceptron = Perceptron(inp_size=inp_size)
		perceptrons.append(perceptron)
	return perceptrons

def breed_new_gen(unsorted_old_gen):
	sorted_old_gen = sorted(unsorted_old_gen, key=itemgetter('score'))	

	best_indiv_index = len(sorted_old_gen)-1
	best_indiv = sorted_old_gen[best_indiv_index]
	
	new_gen = []
	for i in range(0, len(sorted_old_gen)-1):
		father = roulette(sorted_old_gen)
		#print('will mate father index',father,'indiv',sorted_old_gen[father])
		mother = roulette(sorted_old_gen)
		#print('will mate mother index',mother,'indiv',sorted_old_gen[mother])
		new_indiv = mate(sorted_old_gen[father], sorted_old_gen[mother])
		#print('child index',i,'indiv',new_indiv)
		new_indiv = mutate(new_indiv)
		new_gen.append(new_indiv)

	new_gen.append(best_indiv)


	return new_gen

def roulette(indivs):
	total_score = sum(indiv['score'] for indiv in indivs)
	acum_pctg = 0

	chosen_range = np.random.uniform(0, 100)
	chosen_ind = 0
	
	for i in range(0, len(indivs)):
		cur_ind_range = int((indivs[i]['score']/total_score)*100)

		if(i < len(indivs)-1 and chosen_range >= acum_pctg and chosen_range <= acum_pctg+cur_ind_range):
			chosen_ind = i
		elif(i == len(indivs)-1 and chosen_range >= acum_pctg and 
			chosen_range <= acum_pctg+cur_ind_range + (100-acum_pctg+cur_ind_range)):
			chosen_ind = i
		acum_pctg += cur_ind_range


	return chosen_ind

def mutate(indiv):
	mutation_chance = np.random.uniform(0, 1)
	#print('mutation chance', mutation_chance)
	if(mutation_chance <= 0.4):
		#print('will mutate')
		mutation_index = np.random.randint(0,len(indiv['features']))
		#print('mutation index', mutation_index)
		mutation_type = 2
		#print('original value', indiv['features'][mutation_index])
		if(mutation_type == 0):
			#print('mutation type multiplic')
			indiv['features'][mutation_index] = indiv['features'][mutation_index]*4
		elif(mutation_type == 1):
			#print('mutation type division')
			indiv['features'][mutation_index] = indiv['features'][mutation_index]/4
		else:
			#print('mutation type sign change')
			indiv['features'][mutation_index] = np.random.uniform(-50, 50)
		#print('new value', indiv['features'][mutation_index])

	print('\n')

	return indiv

def mate(father, mother):
	new_indiv = {}
	new_indiv['features'] = []
	for i in range(0, len(father['features'])):
		new_indiv['features'].append((father['features'][i]+mother['features'][i])/2)

	return new_indiv

def main():
	#cria scores aleatorios
	random_scores = []
	for i in range(0,10):
		random_scores.append(int(np.random.uniform(0, 500)))
	
	#inicializa nns aleatorias
	nns = init_nns(qtt=10, inp_size=3, out_size=3)
	
	#cria genotipos pra todas as nns
	old_gen = []
	for i in range(0, len(nns)):
		print('nn',i)
		#printa todos os perceptrons de cada nn
		for percep in nns[i].ps:
			print('perceptron weights', percep.weights)
		print('\n')
		
		#cria genotipo
		indiv = nns[i].to_genotype(random_scores[i])
		old_gen.append(indiv)
		#printa genotipo criado
		print('individual', indiv)

	new_gen = breed_new_gen(old_gen)
	print('new gen',new_gen)

	#exibe e imprime as nns criadas
	print('\n\n')
	for i in range(0, len(new_gen)):
		print('individual used to create a nn', new_gen[i])
		nn = SingleLayerNN(inp_size=3, out_size=3, weights=new_gen[i]['features'])
		print('nn',i)
		nn.print()

	return 0

#main()