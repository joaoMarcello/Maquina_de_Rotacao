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
	s = f.read().replace('\n', ' ') # atribuido o texto a s, substituindo as quebras de linhas por espacos
	s = s.replace(' ', '')
	return s

class Cilindro:
	def __init__(self, v):
		self.v1 = [i for i in range(1,27)]
		self.v = v
		self.prox = None
		self.prev = None
		self.rotateCount = 0

	def press(self, c, mode=0):
		ent = self.v1 if mode == 0 else self.v
		sai = self.v if mode == 0 else self.v1
		prox = self.prox if mode == 0 else self.prev

		t = ent[ALFA[c]]
		
		for i in range(len(sai)):
			if t == sai[i]:
				if prox is None:
					return i
				else:
					return prox.press(V_ALFA[i], mode)
					

	def rotate(self, quant=1):
		if quant <= 0:
			return

		temp = [self.v[-1]]
		self.v = temp + self.v[:-1]
		self.rotateCount += 1

		temp = [self.v1[-1]]
		self.v1 = temp + self.v1[:-1]

		if self.rotateCount >= 26:
			self.rotateCount = 0
			if self.prox is not None: self.prox.rotate()

		self.rotate(quant-1)


	def rotateAntiClockWise(self, quant=1):
		if quant <= 0:
			return

		temp = [self.v1[0]]
		self.v1 = self.v1[1:] + temp
		self.rotateCount -= 1

		temp = [self.v[0]]
		self.v = self.v[1:] + temp

		if self.rotateCount < 0:
			self.rotateCount = 25
			if self.prox is not None: self.prox.rotateAntiClockWise()

		self.rotateAntiClockWise(quant-1)

class MaquinaRotacao:
	def __init__(self, c1, c2=None, c3=None, p1=0, p2=0, p3=0):
		self.mode = 0
		self.posInicial = [p1,p2,p3]
		self.c1 = c1
		self.c1.rotate(p1)
		self.last = c1

		if c2 is not None:
			c2.rotate(p2)
			c2.prev = c1
			self.c1.prox = c2
			self.last = c2

		if c3 is not None:
			c3.rotate(p3)
			c3.prev = c2
			if c2 is not None: self.c1.prox.prox = c3
			self.last = c3

	def press(self, c):
		if self.mode == 0:
			r = self.c1.press(c)
			self.c1.rotate()
			return r
		else:
			r = self.last.press(c, mode=1)
			self.c1.rotateAntiClockWise()
			return r

	def setInitialPos(self, p1=0,p2=0,p3=0):
		c2 = self.c1.prox
		c3 = c2.prox if c2 is not None else None

		self.c1.prox = None
		self.c1.rotateAntiClockWise(self.c1.rotateCount)
		self.c1.rotate(p1)


		if c2 is not None:
			c2.prox = None
			c2.rotateAntiClockWise(c2.rotateCount)
			c2.rotate(p2)
			c2.prox = c3

		if c3 is not None:
			c3.prox = None
			c3.rotateAntiClockWise(c3.rotateCount)
			c3.rotate(p3)

		self.c1.prox = c2



	def rotate(self,quant=0):
		if quant > 0:
			for i in range(quant):
				self.c1.rotate()
		else:
			for i in range(quant*-1):
				self.c1.rotateAntiClockWise()

	def criptografar(self, texto):
		self.mode = 0
		self.setInitialPos(self.posInicial[0], self.posInicial[1], self.posInicial[2])
		s = ''
		for i in range(len(texto)):
			r = self.press(texto[i])
			s += V_ALFA[r]

		return s

	def descriptografar(self, texto):
		self.mode = 1
		self.setInitialPos(self.posInicial[0], self.posInicial[1], self.posInicial[2])
		
		#print(self.c1.rotateCount, self.c1.prox.rotateCount, self.c1.prox.prox.rotateCount)

		t_size = len(texto)

		self.rotate(len(texto)-1)

		s = ''
		for i in range(t_size):
			c = texto[t_size-1-i]
			r = self.press(c)
			s = V_ALFA[r] + s

		return s


v1 = [1,19,10,14,26,20,8,16,7,22,4,11,5,17,9,12,23,18,2,25,6,24,13,21,3,15]
v2 = [1,6,4,15,3,14,12,23,5,16,2,22,19,11,18,25,24,13,7,10,8,21,9,26,17,20]
v3 = [8,18,26,17,20,22,10,3,13,11,4,23,5,24,9,12,25,16,19,6,15,21,2,7,1,14]

r1 = [4,5,10,1,11,15,2,6,17,20,16,8,21,7,23,25,12,22,13,24,9,18,3,19,26,14]   # 22 - 18
r2 = [22,25,13,16,5,3,2,20,23,7,19,8,12,9,10,17,24,1,15,18,14,21,6,4,11,26]   # 4 - 25
r3 = [20,17,15,3,5,4,13,18,22,24,6,9,12,8,1,25,19,11,2,16,10,21,14,26,7,23]

c3 = Cilindro(r3)

c2 = Cilindro(r2)

c1 = Cilindro(r1)

texto = carregarArquivoTexto('claro.txt')

maq = MaquinaRotacao(c1, c2, c3, 0, 0, 0)

r = maq.criptografar(texto)
f = open('cifrado.txt', 'w')
f.write(r)
f.close()

print('==================================================================================\n')

r = carregarArquivoTexto('cifrado.txt')
s = maq.descriptografar(r)
f = open('decifrado.txt', 'w')
f.write(s)
f.close()

'''
print('==================================================================================\n')
d3 = Cilindro(v3)

d2 = Cilindro(v2)

d1 = Cilindro(v1)

dec = MaquinaRotacao(d1,d2,d3, 0, 0, 0)
dec.mode = 1
s = dec.descriptografar(r)
print(s)
#'''




