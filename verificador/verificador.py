from utilitarios.arbolsintaxisabstracta import ASA
from utilitarios.nodoarbol import NodoÁrbol
from utilitarios.tiponodo import TipoNodo
from utilitarios.tipodatos import TipoDatos
from verificador.tablasimbolos import TablaSimbolos
from verificador.visitante import Visitante

import colorama
from colorama import Fore

class Verificador:

	def __init__(self, nuevo_asa):
		self.asa = nuevo_asa
		self.tabla_simbolos = TablaSimbolos()
		self.__cargar_ambiente_estandar()
		self.visitador = Visitante(self.tabla_simbolos)


	def imprimir_arbol(self):
		if self.asa is None:
			print([])
		else:
			self.asa.imprimir_preorden()


	def __cargar_ambiente_estandar(self):
		funciones_estandar = [ ('marcador', TipoDatos.TEXTO),
							   ('seleccionNacional', TipoDatos.TEXTO),
							   ('rematesRealizados', TipoDatos.NUMERO),
							   ('entrevista', TipoDatos.CUALQUIERA),
							   ('posicionJugador', TipoDatos.TEXTO)]
		for nombre, tipo in funciones_estandar:
			nodo = NodoÁrbol(TipoNodo.FUNCIÓN, contenido = nombre)
			self.tabla_simbolos.nuevo_registro(nodo)


	def verificar(self):
		self.visitador.visitar(self.asa.raiz)
		

	def mostrar_errores_lista_simbolos(self):
		for mensaje in self.visitador.lista_errores:
			print(Fore.YELLOW + mensaje)
