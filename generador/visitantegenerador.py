from utilitarios.tiponodo import TipoNodo

class VistanteGenerador():
	def __init__(self):
		self.tabuladores = 0

	def visitar_generador(self, nodo):
		resultado = ""

		if nodo.tipo is TipoNodo.PROGRAMA:
			resultado = self.__visitar_programa(nodo)

		elif nodo.tipo is TipoNodo.ASIGNACIÓN:
			resultado = self.__visitar_asignacion(nodo)
		
		elif nodo.tipo is TipoNodo.EXPRESIÓN_MATEMÁTICA:
			resultado = self.__visitar_expresion_matematica(nodo)
		
		elif nodo.tipo is TipoNodo.EXPRESIÓN:
			resultado = self.__visitar_expresion(nodo)
		
		elif nodo.tipo is TipoNodo.FUNCIÓN:
			resultado = self.__visitar_funcion(nodo)
		
		elif nodo.tipo is TipoNodo.INVOCACIÓN:
			resultado = self.__visitar_invocacion(nodo)
		
		elif nodo.tipo is TipoNodo.PARÁMETROS:
			resultado = self.__visitar_parametros(nodo)
		
		elif nodo.tipo is TipoNodo.INSTRUCCIÓN:
			resultado = self.__visitar_instruccion(nodo)
		
		elif nodo.tipo is TipoNodo.REPETICIÓN:
			resultado = self.__visitar_repeticion(nodo)

		elif nodo.tipo is TipoNodo.BIFURCACIÓN:
			resultado = self.__visitar_bifurcacion(nodo)

		elif nodo.tipo is TipoNodo.ANTIANARQUÍA:
			resultado = self.__visitar_antianarquia(nodo)

		elif nodo.tipo is TipoNodo.CONDICIÓN:
			resultado = self.__visitar_condicion(nodo)

		elif nodo.tipo is TipoNodo.COMPARACIÓN:
			resultado = self.__visitar_comparacion(nodo)

		elif nodo.tipo is TipoNodo.RETORNO:
			resultado = self.__visitar_retorno(nodo)

		elif nodo.tipo is TipoNodo.PRINCIPAL:
			resultado = self.__visitar_principal(nodo)

		elif nodo.tipo is TipoNodo.OPERADOR:
			resultado = self.__visitar_operador(nodo)

		elif nodo.tipo is TipoNodo.VALOR_LOGICO:
			resultado = self.__visitar_valor_logico(nodo)

		elif nodo.tipo is TipoNodo.COMPARADOR:
			resultado = self.__visitar_comparador(nodo)

		elif nodo.tipo is TipoNodo.TEXTO:
			resultado = self.__visitar_texto(nodo)

		elif nodo.tipo is TipoNodo.ENTERO:
			resultado = self.__visitar_entero(nodo)

		elif nodo.tipo is TipoNodo.FLOTANTE:
			resultado = self.__visitar_flotante(nodo)

		elif nodo.tipo is TipoNodo.IDENTIFICADOR:
			resultado = self.__visitar_identificador(nodo)

		elif nodo.tipo is TipoNodo.VALOR:
			resultado = self.__visitar_valor(nodo)

		return resultado


	def __visitar_programa(self, nodo_actual):
		"""
		Programa ::= ( Asignación | Función | Comentario ) * Principal
		"""
		instrucciones = []

		for nodo in nodo_actual.nodos:
			instrucciones.append(nodo.visitar_generador(self))

		return "\n".join(instrucciones)


	def __visitar_asignacion(self, nodo_actual):
		"""
		Asignación ::= ( Declaración ) pase ( Literal | Expresión Matemática | Identificador )
		"""
		resultado = self.__retornar_tabuladores() + "{} = {}"
		instrucciones = []

		for nodo in nodo_actual.nodos:
			instrucciones.append(nodo.visitar_generador(self))

		return resultado.format(instrucciones[0], instrucciones[1])


	def	__visitar_expresion_matematica(self, nodo_actual):
		"""
		ExpresiónMatemática ::= (Expresión) | Número | Identificador
		"""
		instrucciones = []

		for nodo in nodo_actual.nodos:
			instrucciones += [nodo.visitar_generador(self)]

		return " ".join(instrucciones)


	def __visitar_expresion(self, nodo_actual):
		"""
		Expresión ::= Expresión Matemática Operador Expresión Matemática
		""" 	
		instrucciones = []

		for nodo in nodo_actual.nodos:
			instrucciones += [nodo.visitar_generador(self)]

		return " ".join(instrucciones)


	def __visitar_funcion(self, nodo_actual):
		"""
		Funcion ::= (Comentario)? jugada Identificador ( Parametros ) [ Instrucción + ]
		"""
		resultado = """\ndef {}({}):\n{}"""
		encabezado = []
		instrucciones = []
		cont = 0

		self.tabuladores += 1

		for nodo in nodo_actual.nodos:
			if cont < 2:
				encabezado += [nodo.visitar_generador(self)]
			else:
				instrucciones +=[nodo.visitar_generador(self)]
			cont += 1

		self.tabuladores -= 1
		return resultado.format(encabezado[0],encabezado[1], '\n'.join(instrucciones))


	def __visitar_invocacion(self, nodo_actual):
		"""
		Invocación ::= invo Identificador ( Parametros* )
		"""

		resultado = self.__retornar_tabuladores() + "{}({})"
		instrucciones = []

		for nodo in nodo_actual.nodos:
			instrucciones += [nodo.visitar_generador(self)]

		return resultado.format(instrucciones[0], instrucciones[1])


	def __visitar_parametros(self, nodo_actual):
		"""
		Parametros ::= identificador ( , identificador )*
		"""
		parametros = []
		for nodo in nodo_actual.nodos:
			parametros.append(nodo.visitar_generador(self))

		if len(parametros) > 0:
			return ",".join(parametros)
		else:
			return ""


	def __visitar_instruccion(self, nodo_actual):
		"""
    	Instrucción ::= (Repetición | Bifurcación | (Asignación | Invocación) | Retorno | Error | Comentario )
		"""
		valor = ""

		for nodo in nodo_actual.nodos:
			valor += nodo.visitar_generador(self)

		return valor


	def __visitar_valor(self, nodo_actual):
		"""
		Valor ::= ( Identificador | Literal | Expresión Matemática )
		"""
		valor = ""

		for nodo in nodo_actual.nodos:
			valor += nodo.visitar_generador(self)

		return valor


	def __visitar_repeticion(self, nodo_actual):
		"""
		Repetición ::= series ( Condicion | ValorLogico | Identificador ) [ Instrucción +]
		"""

		resultado = self.__retornar_tabuladores() + "while {}:\n{}"
		encabezado = []
		instrucciones = []
		cont = 0

		self.tabuladores += 1

		for nodo in nodo_actual.nodos:
			if cont < 1:
				encabezado += [nodo.visitar_generador(self)]
			else:
				instrucciones +=[nodo.visitar_generador(self)]
			cont += 1

		self.tabuladores -= 1

		return resultado.format(encabezado[0], '\n'.join(instrucciones))


	def __visitar_bifurcacion(self, nodo_actual):
		"""
		TiempoExtra ::= tiempoExtra ( (Condicion | ValorLogico | Identificador) ) [ Instrucción+ ]
		Penales ::= penales [ Instrucción + ]
		"""
		self.tabuladores -= 1

		if nodo_actual.contenido == "tiempoExtra":
			return self.__generar_elif(nodo_actual)
		else:
			return self.__generar_else(nodo_actual)


	def __generar_elif(self, nodo_actual):
		resultado_elif = self.__retornar_tabuladores() + "elif {}:\n{}"

		encabezado = []
		instrucciones = []
		cont = 0

		self.tabuladores += 1

		for nodo in nodo_actual.nodos:
			if cont < 1:
				encabezado += [nodo.visitar_generador(self)]
			else:
				instrucciones +=[nodo.visitar_generador(self)]
			cont += 1

		return resultado_elif.format(encabezado[0], '\n'.join(instrucciones))


	def __generar_else(self, nodo_actual):
		resultado_else = self.__retornar_tabuladores() + "else:\n{}"
		instrucciones = []

		self.tabuladores += 1

		for nodo in nodo_actual.nodos:
			instrucciones.append(nodo.visitar_generador(self))

		return resultado_else.format("\n".join(instrucciones))


	def __visitar_antianarquia(self, nodo_actual):
		"""
		AntiAnarquía ::= tiempoRegular ( (Condicion|ValorLogico|Identificador) ) [ Instrucción + ] (TiempoExtra )* (Penales)? 
		"""
		resultado = self.__retornar_tabuladores() + """if {}:\n{}"""
		encabezado = []
		instrucciones = []
		cont = 0

		self.tabuladores += 1

		for nodo in nodo_actual.nodos:
			if cont < 1:
				encabezado += [nodo.visitar_generador(self)]
			else:
				instrucciones +=[nodo.visitar_generador(self)]
			cont += 1

		self.tabuladores -= 1
		return resultado.format(encabezado[0], '\n'.join(instrucciones))


	def __visitar_condicion(self, nodo_actual):
		"""
		Condición ::= Comparación ( condicionLogica Comparación )*
		"""

		instrucciones = []

		for nodo in nodo_actual.nodos:
			instrucciones += [nodo.visitar_generador(self)]

		return instrucciones[0]


	def __visitar_comparacion(self, nodo_actual):
		"""
		Comparación ::= Valor Comparador Valor
		"""	
		resultado = "{} {} {}"
		elementos = []

		for nodo in nodo_actual.nodos:
			elementos.append(nodo.visitar_generador(self))

		return resultado.format(elementos[0], elementos[1], elementos[2])


	def __visitar_retorno(self, nodo_actual):
		"""
		Retorno ::= resultado Valor
		"""
		resultado = self.__retornar_tabuladores() + "return {}"
		valor = ""

		for nodo in nodo_actual.nodos:
			valor += nodo.visitar_generador(self)

		return resultado.format(valor)


	def __visitar_principal(self, nodo_actual):
		"""
		Principal ::= (Comentario)? pitido_Inicial () [ Instrucción + ]
		"""
		resultado = """\ndef principal():\n{}\n
if __name__ == '__main__':
    principal()
"""

		self.tabuladores += 1	
		instrucciones = []
		for nodo in nodo_actual.nodos:
			instrucciones += [nodo.visitar_generador(self)]
		return resultado.format('\n'.join(instrucciones))


	def __visitar_operador(self, nodo_actual):
		"""
		Operador ::= ( aFavor | enContra | golVisita | balonDividido | cambioExtra)
		"""

		if nodo_actual.contenido == 'aFavor':
			return "+"

		elif nodo_actual.contenido == 'enContra':
			return "-"

		elif nodo_actual.contenido == 'golVisita':
			return "*"

		elif nodo_actual.contenido == 'balonDividido':
			return "/"

		elif nodo_actual.contenido == 'cambioExtra':
			return "%"


	def __visitar_valor_logico(self, nodo_actual):
		"""
		ValorLogico ::= gol|fuera
		"""
		if nodo_actual.contenido == 'gol':
			return 'True'
		else:
			return 'False'


	def __visitar_comparador(self, nodo_actual):
		"""
		Comparador ::= (mundialMayor, mundialMenor, mundialMixto, mundialMayor_Mixto, mundialMenor_Mixto, mundialSimple )
		"""

		if nodo_actual.contenido == 'mundialMayor':
			return '>'

		elif nodo_actual.contenido == 'mundialMenor':
			return '<'

		elif nodo_actual.contenido == 'mundialMixto':
			return '='

		elif nodo_actual.contenido == 'mundialMayor_Mixto':
			return '>='

		elif nodo_actual.contenido == 'mundialMenor_Mixto':
			return '<='

		elif nodo_actual.contenido == 'mundialSimple':
			return '!='


	def __visitar_texto(self, nodo_actual):
		"""
		Texto ::= ~ [0-9a-zA-Z\W]+ ~
		"""
		return nodo_actual.contenido.replace('~', '"')


	def __visitar_entero(self, nodo_actual):
		"""
		Entero ::= -?[0-9]+
		"""
		return nodo_actual.contenido


	def __visitar_flotante(self, nodo_actual):
		"""
		Flotante ::= -?[0-9]+.[0-9]+
		"""
		return nodo_actual.contenido


	def __visitar_identificador(self, nodo_actual):
		"""
		Identificador ::= [a-z][a-zA-Z0-9\W]+
		"""
		return nodo_actual.contenido


	def __retornar_tabuladores(self):
		return "    " * self.tabuladores
