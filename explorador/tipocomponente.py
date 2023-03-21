from enum import Enum, auto

"""
En esta clase TipoComponente estan todos los tipos de componentes 
y los diferentes errores que se pueden encontrar en un archivo .
"""
class TipoComponente(Enum):
	COMENTARIO = auto()
	ESPACIO_BLANCO = auto()
	PUNTUACION = auto()
	DECLARACION = auto()
	IDENTIFICADOR = auto()
	IMPRIMIR = auto()
	PALABRA_CLAVE = auto()
	CONDICIONAL = auto()
	CONDICION = auto()
	REPETICION = auto()
	ASIGNACION = auto()
	OPERADOR = auto()
	COMPARADOR = auto()
	VALOR_LOGICO = auto()
	ENTERO = auto()
	FLOTANTE = auto()
	TEXTO = auto()
	ERROR = auto()
	ERROR_MAYUSCULA_ID = auto()
	ERROR_FLOTANTE_LETRA = auto()
	TEXTO_SIN_CIERRE = auto()