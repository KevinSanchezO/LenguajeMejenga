import copy
from verificador.visitante import Visitante
from generador.visitantegenerador import VistanteGenerador

class NodoÁrbol:
	def __init__(self, tipo, contenido = None, nodos = [], atributos = {}):
		self.tipo = tipo
		self.contenido = contenido
		self.nodos = nodos
		diccionario = {}
		diccionario['tipo'] = ''
		self.atributos = diccionario


	def visitar(self, visitador):
		return visitador.visitar(self)


	def visitar_generador(self, generador):
		return generador.visitar_generador(self)
