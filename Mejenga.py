"""
En este archivo se encuentra el main del compilador, el cual se encarga de cargar el archivo
y llamar a las funciones del explorador y futuros componentes, para identificar los errores y componentes lexicos existentes. 
"""
from explorador.explorador import Explorador
from analizador.analizador_gramatica import Analizador
from verificador.verificador import Verificador
from generador.generador import Generador
from utilitarios.archivo import *
import argparse

parser = argparse.ArgumentParser(description = 'Compilador del lenguaje Mejenga')

parser.add_argument('--explorador', dest = 'explorador', action = 'store_true',
	help = 'ejecuta unicamente el explorador y retorna una lista con los componentes lexicos')

parser.add_argument('--analizador-gramatica', dest = 'analizador_gramatica', action = 'store_true',
	help = 'ejecuta unicamente el analizador y retorna el ASA')

parser.add_argument('--verificador', dest = 'verificador', action = 'store_true',
	help = 'ejecuta unicamente el verificador')

parser.add_argument('--generar', dest='generador', action='store_true', 
        help='''Genera código python''')


parser.add_argument('archivo', help = 'Archivo')

def mejenga():
	args = parser.parse_args()

	if args.explorador is True:
		texto = cargarArchivo(args.archivo)
		
		explorador = Explorador(texto)
		explorador.explorar()
		
		explorador.imprimirComponentes()
	elif args.analizador_gramatica is True:
		texto = cargarArchivo(args.archivo)
		
		explorador = Explorador(texto)
		explorador.explorar()

		analizador = Analizador(explorador.componentes)
		analizador.analizar()
		analizador.imprimir_arbol()
		analizador.imprimir_errores()
	elif args.verificador is True:
		texto = cargarArchivo(args.archivo)
		
		explorador = Explorador(texto)
		explorador.explorar()

		analizador = Analizador(explorador.componentes)
		analizador.analizar()
		

		verificador = Verificador(analizador.asa)
		verificador.verificar()

		verificador.imprimir_arbol()

		print('\nPROFUNDIDADES RECORRIDAS')
		verificador.tabla_simbolos.mostrar_avance()

		print(verificador.tabla_simbolos)
		verificador.mostrar_errores_lista_simbolos()
	elif args.generador is True:
		texto = cargarArchivo(args.archivo)
		
		explorador = Explorador(texto)
		explorador.explorar()

		analizador = Analizador(explorador.componentes)
		analizador.analizar()
		

		verificador = Verificador(analizador.asa)
		verificador.verificar()
		verificador.mostrar_errores_lista_simbolos()

		verificador.imprimir_arbol()
		print("\n")
		generador = Generador(verificador.asa)
		generador.generar()


		
	else:
		parser.print_help()


if __name__ == "__main__":
    mejenga()
