from utilitarios.arbolsintaxisabstracta import ASA
from utilitarios.nodoarbol import NodoÁrbol
from utilitarios.tiponodo import TipoNodo
from utilitarios.tipodatos import TipoDatos

class TablaSimbolos:

	def __init__(self):
		self.profundidad = 0
		self.simbolos = []
		self.registro_avance = []


	def abrir_bloque(self):
		self.profundidad += 1


	def cerrar_bloque(self):
		for registro in self.simbolos:
			if registro["profundidad"] == self.profundidad:
				self.registro_avance += [registro]
				self.simbolos.remove(registro)
		self.profundidad -= 1

	# Esto es para ir guardando los bloques que eliminamos, asi los podemos mostrar
	# Al terminar y que no parezca que hicimos magia negra
	def mostrar_avance(self):
		for avance in self.registro_avance:
			print(avance)


	def nuevo_registro(self, nodo, nombre_registro = ''):
		diccionario = {}
		diccionario['nombre'] = nodo.contenido
		diccionario['tipodato'] = '' # Esto nos salvo la vida para poder trabajar las expresiones matematicas
		diccionario['profundidad'] = self.profundidad
		diccionario['referencia'] = nodo

		self.simbolos.append(diccionario)


	#retorna directamente el registro que estamos preguntando si existe
	def verificar_existencia(self, nombre):
		for registro in self.simbolos:
			if registro['nombre'] == nombre and registro['profundidad'] <= self.profundidad:
				return registro

	#este por el otro lado solo nos da un booleano en caso de que exista o no, fue una salvada en el patron
	def verificar_existencia_bool(self, nombre):
		for registro in self.simbolos:
			if registro['nombre'] == nombre and registro['profundidad'] <= self.profundidad:
				return True
		return False


	def encontrar_registro(self, nombre, tipo_dato):
		for i in self.simbolos:
			if i['nombre'] == nombre:
				i['tipodato'] = tipo_dato


	def __str__(self):
		resultado = "\n\nTABLA DE SIMBOLOS\n"
		resultado += "profundidad: " + str(self.profundidad) + '\n'
		for registro in self.simbolos:
			resultado += str(registro) + '\n'

		return resultado
