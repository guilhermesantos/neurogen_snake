#Autor: Guilherme Milan Santos 
#Numero USP: 9012966
#Instrucoes: executar python snake_game.py -nn
#Utiliza python 3, curses, numpy e math
#Para fechar, apertar a seta para baixo no teclado
#Para entrar no modo invisivel (treina mais rapidamente), apertar a seta para cima no teclado
#Para aumentar a velocidade no modo visivel, apertar a seta para a direita
#para diminuir a velocidade no modo visivel. apertar a seta para a esquerda

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

def breed_new_gen(unsorted_old_gen, memory):
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
		new_indiv = mutate(new_indiv, memory)
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

def mutate(indiv, memory):
	mutation_quantity = int(np.random.uniform(1,5))
	mutation_indexes = np.random.randint(0,len(indiv['features']), mutation_quantity-1)
	
	str_rep = geno_to_str(indiv)
	while(str_rep in memory.keys() and memory[str_rep] == 1):
		mutation_quantity = int(np.random.uniform(1,5))
		mutation_indexes = np.random.randint(0,len(indiv['features']), mutation_quantity-1)
		
		for mutation_index in mutation_indexes:
			indiv['features'][mutation_index] = int(np.random.uniform(low=-10,high=10))
		str_rep = geno_to_str(indiv)
	
	memory[str_rep] = 1

	return indiv

def mate(father, mother):
	new_indiv = {}
	new_indiv['features'] = []
	for i in range(0, len(father['features'])):
		new_indiv['features'].append(int((father['features'][i]+mother['features'][i])/2))

	return new_indiv

def geno_to_str(indiv):
	str_rep = ''
	for feature in indiv['features']:
		if(feature < 10):
			str_rep += str(feature)
		else:
			str_rep += 'A'
	return str_rep

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