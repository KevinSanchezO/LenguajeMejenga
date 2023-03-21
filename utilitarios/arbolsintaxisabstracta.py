class ASA:
	def __init__(self):
		self.raiz = None

	def imprimir_preorden(self):
		self.__preorden(self.raiz, 0)

	def __preorden(self, nodo, tabs):
		if nodo is not None:
			print('')
			for i in range(tabs):
				print('\t', end = ' ')
			print("<" + str(nodo.tipo) + " | " + nodo.contenido + " | " + str(nodo.atributos['tipo']) + ">", end = ' ')
			for nodo in nodo.nodos:
				self.__preorden(nodo, tabs + 1)