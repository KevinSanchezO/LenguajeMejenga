from utilitarios.arbolsintaxisabstracta import ASA
from generador.visitantegenerador import VistanteGenerador

class Generador:

	def __init__(self, nuevo_asa):
		self.asa = nuevo_asa
		self.visitador = VistanteGenerador()

	def generar(self):
		resultado = """import sys

def seleccionNacional(texto1, texto2):
    return texto1 + texto2

def posicionJugador(texto, indice):
    return texto[indice]

def rematesRealizados(texto):
    return len(texto)

def marcador(texto):
    print(texto)

"""

		resultado += self.visitador.visitar_generador(self.asa.raiz)
		self.__generar_archivo(resultado)
		print("\nSE HA GENERADO EL ARCHIVO DE CODIGO\n")
		print(resultado)

	def __generar_archivo(self, texto):
		nombre_archivo = 'codigogenerado.py'

		with open(nombre_archivo, 'w') as f:
			f.write('{}'.format(texto))
