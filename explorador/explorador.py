"""
La clase Explorardor primeramente inicializa todos los tipos de componentes,
luego se procesa el archivo linea por linea para identificar los errores u 
componentes lexicos que puedan existir, ademas de poseer la funcion que imprime 
los componentes u errores que se identificaron.
"""
import re
from enum import Enum, auto
from utilitarios.archivo import separar_palabras, verificar_Comentario, verificar_Texto
from explorador.tipocomponente import TipoComponente
from explorador.componentelexico import ComponenteLexico

class Explorador():

	def __init__(self, archivoTexto):
		self.texto = archivoTexto
		self.componentes = []
		self.descriptores_componentes = [(TipoComponente.COMENTARIO, r'^piloObando:.*'),
									 (TipoComponente.ESPACIO_BLANCO, r'^(\s)*'),
									 (TipoComponente.PUNTUACION, r'^([[\](),])'),
                                     (TipoComponente.DECLARACION, r'^(visita|local)'),
                                     (TipoComponente.IMPRIMIR, r'^(marcador)'),
                                     (TipoComponente.PALABRA_CLAVE, r'^(jugada|pitido_Inicial|resultado)'),
                                     (TipoComponente.CONDICIONAL, r'^(tiempoRegular|tiempoExtra|penales)'),
                                     (TipoComponente.CONDICION, r'^(leyVentaja|falta)'),
                                     (TipoComponente.REPETICION, r'^series'),
                                     (TipoComponente.ASIGNACION, r'^pase'),
                                     (TipoComponente.OPERADOR, r'^(aFavor|enContra|golVisita|balonDividido|cambioExtra)'),
                                     (TipoComponente.COMPARADOR, r'^(mundialMayor|mundialMenor|mundialMixto|mundialMayor_Mixto|mundialMenor_Mixto|mundialSimple)'),
                                     (TipoComponente.VALOR_LOGICO, r'^(gol|fuera)'),
                                     (TipoComponente.TEXTO, r'^(~.?[^~]*)~'),                                                                     
                                     (TipoComponente.FLOTANTE, r'^(-?[0-9]+\.[0-9]+)'),
                                     (TipoComponente.ENTERO, r'^(-?[0-9]+)'),
                                     (TipoComponente.IDENTIFICADOR, r'^([a-zA-Z0-9]+)')]

	"""
    Metodo que sera llamado para inciar el proceso de exploracion
	"""
	def explorar(self):
		numero_linea = 1
		for linea in self.texto:
			palabras = separar_palabras(linea)
			resultado = self.procesarLinea(verificar_Texto(verificar_Comentario(palabras)), numero_linea)
			self.componentes += resultado
			numero_linea += 1

	"""
	Permite imprimir todos los componentes encontrados en pantalla
	"""
	def imprimirComponentes(self):
		for componente in self.componentes:
			print (componente.representarInstancia())

	"""
	Realiza el proceso de procesar toda la linea del codigo y determinar los componentes que presenta
	ademas de identificar errores lexicos
	al finalizar devuelve una lista con todos los componentes y errores encontrados en la linea
	"""
	def procesarLinea(self, palabras, numero_linea):
		componentes = [] #almacenador de los componentes encontrados
		for i in palabras:
			bandera = False
			for tipoComponente, regex in self.descriptores_componentes:
				respuesta = re.fullmatch(regex, i) #guarda el match encontrado

				if respuesta is not None and not bandera:
					if tipoComponente is not TipoComponente.ESPACIO_BLANCO:
						nuevoComponente = ComponenteLexico(tipoComponente, respuesta.group(), numero_linea) #el explorador no toma en cuenta los comentarios
						componentes.append(nuevoComponente)
						bandera = True
				else:
					if re.fullmatch(r'^(~.?[^~]*)', i) != None and not bandera:
						error = ComponenteLexico(TipoComponente.TEXTO_SIN_CIERRE, 'Error de sintaxis texto sin cierre ~: '+i+' linea: '+(str(numero_linea)), numero_linea)
						componentes.append(error)
						bandera = True
					elif re.fullmatch(r'^([A-Z][a-zA-Z0-9]+)', i) != None and not bandera:
						error = ComponenteLexico(TipoComponente.ERROR_MAYUSCULA_ID, 'Error de sintaxis mayuscula id: '+i+' linea: '+(str(numero_linea)), numero_linea)
						componentes.append(error)
						bandera = True
					else:
						if tipoComponente == tipoComponente.IDENTIFICADOR and not bandera:
							error = ComponenteLexico(TipoComponente.ERROR, 'Error de sintaxis: '+i+' en linea: '+ (str(numero_linea)), numero_linea)
							componentes.append(error)
							bandera = True
		return componentes

