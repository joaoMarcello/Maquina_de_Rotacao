'''
	===========   ATIVIDADE DE INTRODUCAO A CRIPTOGRAFIA :: MAQUINA DE ROTACA0   =====================
		Implementar a cifra de maquina de rotacao com tres cilindros, considerando o alfabeto com 
	26 letras maiusculas.

	Joao Marcello, 2021
	==================================================================================================
'''

# Constantes utilizadas para transformar letras em numeros e vice-versa.
ALFA = {
	'A' : 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'G' : 6, 'H' : 7, 'I' : 8, 'J' : 9, 'K' : 10, 'L' : 11, 'M' : 12, 'N' : 13, 'O' : 14, 'P' : 15,
	'Q' : 16, 'R' : 17, 'S' : 18, 'T' : 19, 'U' : 20, 'V' : 21, 'W' : 22, 'X' : 23, 'Y' : 24, 'Z' : 25
}

V_ALFA = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']#'''


''' Carrega um arquivo de texto em uma string.
	Recebe:
		- filepath: caminho para o arquivo.
	Retorna:
		- uma string com o texto do arquivo informado.
'''
def carregarArquivoTexto(filepath = './claro.txt'):
	f = open(filepath, 'r')   # abrindo o arquivo
	s = f.read().replace('\n', '') # atribuido o texto a s, e removendo as quebras de linha
	s = s.replace(' ', '') # removendo os espacos em branco
	return s

#==========================================================================================================================================
''' Implementacao do cilindro usado na maquina de rotacao. 
'''
class Cilindro:
	''' Construtor.
		Recebe:
			- v: o vetor que representa o lado direito do cilindro
	'''
	def __init__(self, v):
		self.left = [i for i in range(1,27)]  # o lado esquerdo tera os numeros de 1 ate 26 em ordem crescente
		self.right = v
		self.prox = None  # o proximo cilindro
		self.prev = None  # cilindro anterior
		self.rotateCount = 0   # quant. de rotacoes que o cilindro fez


	''' Imprime os vetores left e right do cilindro (Usada para debug).
	'''
	def print(self):
		print('Right: ', self.right)
		print('Left: ', self.left)


	''' Funcao utilizada quando se pressiona um botao da maquina.
		Recebe:
			- c: o caractere que foi pressionado
			- mode: 0 se deseja cifrar ou qualquer outro valor caso se deseje decifrar
		Retorna:
			- um inteiro que representa a letra para a cifragem/decifragem (dependendo do valor de mode) 
	'''
	def press(self, c, mode=0):
		ent = self.left if mode == 0 else self.right
		sai = self.right if mode == 0 else self.left
		prox = self.prox if mode == 0 else self.prev

		# transformando o caractere informado em um numero e utilizando esse numero para definir o valor de entrada 
		t = ent[ALFA[c]]
		
		# procurando no vetor de saida o mesmo valor da entrada
		for i in range(len(sai)):
			if t == sai[i]:
				# se este eh o ultimo cilindro, retorna o valor encontrado
				if prox is None:
					return i
				else:   # senao, chama a funcao press do proximo cilindro, passando o  valor encontrado
					return prox.press(V_ALFA[i], mode)
				

	''' Simula a rotacao do cilindro no sentido horario. Se este cilindro completar uma volta e estiver conectado com um proximo cilindro,
		faz o proximo cilindro rotacionar em uma unidade.
		Recebe:
			- quant: a quantidade de rotacoes desejada (valores inteiros positivos)
	'''
	def rotate(self, quant=1):
		# se a quant. for menor ou igual a zero, a funcao nao faz nada
		if quant <= 0:
			return

		# rotacionando o vetor direito
		temp = [self.right[-1]]
		self.right = temp + self.right[:-1]
		self.rotateCount += 1

		# rotacionando o vetor esquerdo
		temp = [self.left[-1]]
		self.left = temp + self.left[:-1]

		# se completou um ciclo...
		if self.rotateCount >= 26:
			# zera a quant. de rotacoes que ja fez
			self.rotateCount = 0
			# faz o proximo cilindro rotacionar uma unidade, se existir
			if self.prox is not None: self.prox.rotate()

		# usando recursao para completar a quant.de rotacoes
		self.rotate(quant-1)


	''' Simula a rotacao anti-horaria do cilindro.
		Recebe:
			-quant: a quantidade de rotacoes desejada (valores inteiros positivos)
	'''
	def rotateAntiClockWise(self, quant=1):
		# se a quant. de rotacoes for menor ou igual a zero, nao faz nada
		if quant <= 0:
			return

		# rotacionando o vetor esquerdo
		temp = [self.left[0]]   # armazenando o primeiro elemento do vetor em uma lista
		self.left = self.left[1:] + temp     # concatenando a lista temp com a lista left (menos o primeiro elemento)
		self.rotateCount -= 1  # decrementando a quant. de rotacoes

		# rotacionando o vetor direito
		temp = [self.right[0]]
		self.right = self.right[1:] + temp

		# se completou um ciclo...
		if self.rotateCount < 0:
			# coloca a quant. de rotacoes no valor maximo
			self.rotateCount = 25
			# faz o proximo cilindro rotacionar em uma unidade no sentido anti-horario, se existir
			if self.prox is not None: self.prox.rotateAntiClockWise()

		# usando a recursao para completar a quant. de rotacoes
		self.rotateAntiClockWise(quant-1)
#====================================================================================================================================================


''' Implementacao da maquina de rotacao. Armazena os cilindros como uma lista duplamente encadeada (cada cilindro conhece o
	proximo e o anterior).
'''
class MaquinaRotacao:
	''' Construtor.
		Recebe:
			- c1, c2, c3: sao objetos do tipo Cilindro e representam os cilindros 1, 2 e 3 respectivamente
			- p1, p2, p3: inteiros que indicam a posicao inicial de cada cilindro
	'''
	def __init__(self, c1, c2=None, c3=None, p1=0, p2=0, p3=0):
		# indica se a maquina esta cifrando (0) ou decifrando (1)
		self.mode = 0  
		# armazenando a posicao inicial em uma lista
		self.posInicial = [p1 % 26, p2 % 26, p3 % 26]
		# o primeiro cilindro
		self.first = c1
		# rotacionando o primeiro cilindro
		self.first.rotate(self.posInicial[0])
		# o ultimo cilindro
		self.last = c1

		# se c2 foi informado
		if c2 is not None:
			# rotacionando o segundo cilindro
			c2.rotate(self.posInicial[1])
			# fazendo c2 apontar para c1
			c2.prev = c1
			# fazendo c1 apontar para c2
			self.first.prox = c2
			# atualizando qual eh o ultimo cilindro
			self.last = c2

		# se c3 foi informado
		if c3 is not None:
			# rotacionando o terceiro cilindro
			c3.rotate(self.posInicial[2])
			# fazendo c3 apontar para c2
			c3.prev = c2
			# fazendo c2 apontar para c3
			if c2 is not None: self.first.prox.prox = c3
			# atualizando qual eh o ultimo cilindro
			self.last = c3


	''' Simula p pressionar de um botao da maquina. Apertar um botao implica em fazer os cilindros rotacionarem.
		Essa rotacao vai depender do modo em que a maquina esta: se mode (0), os cilindros irao girar no sentido horario, senao
		no sentido anti-horario.
		Recebe:
			- c: o caractere que foi pressionado
		Retorna:
			- um inteiro que representa o caractere cifrado/decifrado, dependendo do modo em que maquina esta
	'''
	def press(self, c):
		if self.mode == 0:
			r = self.first.press(c)
			self.first.rotate()
			return r
		else:
			r = self.last.press(c, mode=1)
			self.first.rotateAntiClockWise()
			return r


	''' Coloca a maquina em um determinado estado.
		Recebe:
			- p1, p2, p3: a quant. de rotacoes inicial de cada cilindro
	'''
	def setPosition(self, p1=0, p2=0, p3=0):
		# armazenando temporariamente os cilindros c2 e c3
		c2 = self.first.prox
		c3 = c2.prox if c2 is not None else None

		# rotacionando o primeiro cilindro no sentido anti-horario rotateCount vezes, para coloca-lo na sua posicao inicial
		self.first.rotateAntiClockWise(self.first.rotateCount)
		# rotacionando o primeiro cilindro p1 vezes
		self.first.rotate(p1)


		# se o cilindro 2 existe...
		if c2 is not None:
			# rotacionando o segundo cilindro no sentido anti-horario rotateCount vezes, para coloca-lo na sua posicao inicial
			c2.rotateAntiClockWise(c2.rotateCount)
			# rotacionando o segundo cilindro p2 vezes
			c2.rotate(p2)

		if c3 is not None:
			# rotacionando o terceiro cilindro no sentido anti-horario rotateCount vezes, para coloca-lo na sua posicao inicial
			c3.rotateAntiClockWise(c3.rotateCount)
			# rotacionando o terceiro cilindro p3 vezes
			c3.rotate(p3)


	''' Rotaciona o primeiro cilindro da maquina (ocasionalmente, rotacionara tambem os outros cilindros, caso o primeiro complete
		um ciclo).
		Recebe:
			- quant: a quantidade de rotacoes que deve ser feita. Se o valor for positivo, rotacionara no sentido horario, senao
				rotacionara no sentido anti-horario.
	'''
	def rotate(self,quant=0):
		if quant > 0:
			for i in range(quant):
				self.first.rotate()
		else:
			for i in range(quant*-1):
				self.first.rotateAntiClockWise()


	''' Criptografa uma mensagem.
		Recebe:
			- texto: uma string que representa a mensagem a ser cifrada.
		Retorna:
			- uma string com o resultado da cifragem.
	'''
	def criptografar(self, texto):
		# transformando os caracteres da mensagem em maiusculas
		texto = texto.upper()

		# colocando a maquina no modo cifragem
		self.mode = 0

		# colocando a maquina na posicao inicial
		self.setPosition(self.posInicial[0], self.posInicial[1], self.posInicial[2])

		# string para armazenar a mensagem cifrada
		s = ''
		# iterando sobre os caracteres da mensagem
		for i in range(len(texto)):
			# armazenando o resultado da cifragem para o caractere atual
			r = self.press(texto[i])
			# transformando o numero retornado em um caractere e concatenado o resultado a string s
			s += V_ALFA[r]

		return s


	''' Decifra uma mensagem.
		Recebe:
			- texto: uma string que representa o texto a ser decifrado.
		Retorna:
			- uma string com o resultado da decifragem
	'''
	def descriptografar(self, texto):
		# colocando a maquina no modo decifragem
		self.mode = 1
		self.setPosition(self.posInicial[0], self.posInicial[1], self.posInicial[2])
		
		# tamanho do texto cifrado		
		t_size = len(texto)

		# fazendo a maquina rotacionar o primeiro cilindro t_size vezes
		self.rotate(len(texto)-1)

		# string para armazenar o resultado da decifragem
		s = ''
		# iterando sobre os caracteres da mensagem de tras pra frente
		for i in range(t_size):
			# o caractere atual
			c = texto[t_size-1-i]
			# armazenando o resultado da decifragem para o caractere atual
			r = self.press(c)
			# transformando o numero retornado em um caractere e concatenando com a string s
			s = V_ALFA[r] + s

		return s
#============================================================================================================================================


''' Imprime um menu para o usuario.
'''
def printMenu():
	print('--> +---------------------+')
	print('--> |       MENU          |')
	print('--> +---------------------+')
	print('--> |    1:  Cifrar       |')
	print('--> |    2:  Decifrar     |')
	print('--> |    3:  Sair         |')
	print('--> +---------------------+', end='')


''' Funcao principal: Le a opcao do usuario e executa a acao correspondente.
'''
def main():
	# criando os cilindros para a maquina de rotacao
	c1 = Cilindro( [4,5,10,1,11,15,2,6,17,20,16,8,21,7,23,25,12,22,13,24,9,18,3,19,26,14] )
	c2 = Cilindro( [23,4,14,17,6,3,2,21,24,8,20,9,13,10,11,18,25,1,16,19,15,22,7,5,12,26] )
	c3 = Cilindro( [20,17,15,3,5,4,13,18,22,24,6,9,12,8,1,25,19,11,2,16,10,21,14,26,7,23] )

	# criando a maquina de rotacao, passando os cilindros e suas posicoes iniciais
	maq = MaquinaRotacao(c1, c2, c3, 0, 0, 0)

	# variavel para armazenar a opcao do usuario
	option = -1

	# enquanto a opcao nao eh 'Sair'
	while(option != 3):
		# mostra o menu
		printMenu()

		# le a opcao do usuario
		option = int(input('\n--> Informe sua opcao: '))
		r = True

		if option == 1:  # se opcao eh 1 == Cifrar
			try:
				texto = carregarArquivoTexto('claro.txt')  # carrega o texto no arquivo e armazena em uma variavel
				r = maq.criptografar(texto)   # criptografando o texto
				f = open('cifrado.txt', 'w')  
				f.write(r)
				f.close()
				print("--> Texto cifrado foi salvo no arquivo 'cifrado.txt'.\n--> Pressione 'Enter' para continuar.", end='')
				input()
			except:
				print("--> Erro! Nao existe um texto para cifrar!\n--> Crie um arquivo chamado 'claro.txt' no diretorio do programa.", end='')
				input()
		else:
			if option == 2:  # se opcao eh 2 == Decifrar
				try:
					texto = carregarArquivoTexto('cifrado.txt') # carrega o texto no arquivo e armazena em uma variavel
					r = maq.descriptografar(texto)   # descriptografando o texto
					f = open('decifrado.txt', 'w')
					f.write(r)
					f.close()
					print("--> Texto decifrado foi salvo no arquivo 'decifrado.txt'.\n--> Pressione 'Enter' para continuar.", end='')
					input()
				except:
					print("--> Erro! Nao existe um texto para decifrar!\n--> Utilize antes o comando '1' para cifrar.", end='')
					input()
			else:  
				if option != 3:   # opcao invalida
					print('--> Opcao invalida!!!', end='')
					input()

	print('--> Programa finalizado.')
#============================================================================================================================================


if __name__ == '__main__':
	main()





