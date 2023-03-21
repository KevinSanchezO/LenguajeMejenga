from utilitarios.arbolsintaxisabstracta import ASA
from utilitarios.tiponodo import TipoNodo
from utilitarios.tipodatos import TipoDatos

class Visitante:

	def __init__(self, nueva_tabla_simbolos):
		self.tabla_simbolos = nueva_tabla_simbolos
		self.lista_errores = []

	"""
	El corazon del patron visitante
	recorrera todo el arbol identificando cada uno de los nodos
	encontrando variables e identificando tipos
	"""
	def visitar(self, nodo):
		if nodo.tipo is TipoNodo.PROGRAMA:
			self.__visitar_programa(nodo)
		
		elif nodo.tipo is TipoNodo.ASIGNACIÓN:
			self.__visitar_asignacion(nodo)
		
		elif nodo.tipo is TipoNodo.EXPRESIÓN_MATEMÁTICA:
			self.__visitar_expresion_matematica(nodo)
		
		elif nodo.tipo is TipoNodo.EXPRESIÓN:
			self.__visitar_expresion(nodo)
		
		elif nodo.tipo is TipoNodo.FUNCIÓN:
			self.__visitar_funcion(nodo)
		
		elif nodo.tipo is TipoNodo.INVOCACIÓN:
			self.__visitar_invocacion(nodo)
		
		elif nodo.tipo is TipoNodo.PARÁMETROS:
			self.__visitar_parametros(nodo)
		
		elif nodo.tipo is TipoNodo.INSTRUCCIÓN:
			self.__visitar_instruccion(nodo)
		
		elif nodo.tipo is TipoNodo.REPETICIÓN:
			self.__visitar_repeticion(nodo)

		elif nodo.tipo is TipoNodo.BIFURCACIÓN:
			self.__visitar_bifurcacion(nodo)

		elif nodo.tipo is TipoNodo.ANTIANARQUÍA:
			self.__visitar_antianarquia(nodo)

		elif nodo.tipo is TipoNodo.CONDICIÓN:
			self.__visitar_condicion(nodo)

		elif nodo.tipo is TipoNodo.COMPARACIÓN:
			self.__visitar_comparacion(nodo)

		elif nodo.tipo is TipoNodo.RETORNO:
			self.__visitar_retorno(nodo)

		elif nodo.tipo is TipoNodo.PRINCIPAL:
			self.__visitar_principal(nodo)

		elif nodo.tipo is TipoNodo.OPERADOR:
			self.__visitar_operador(nodo)

		elif nodo.tipo is TipoNodo.VALOR_LOGICO:
			self.__visitar_valor_logico(nodo)

		elif nodo.tipo is TipoNodo.COMPARADOR:
			self.__visitar_comparador(nodo)

		elif nodo.tipo is TipoNodo.TEXTO:
			self.__visitar_texto(nodo)

		elif nodo.tipo is TipoNodo.ENTERO:
			self.__visitar_entero(nodo)

		elif nodo.tipo is TipoNodo.FLOTANTE:
			self.__visitar_flotante(nodo)

		elif nodo.tipo is TipoNodo.IDENTIFICADOR:
			self.__visitar_identificador(nodo)

		elif nodo.tipo is TipoNodo.VALOR:
			self.__visitar_valor(nodo)


	def __visitar_programa(self, nodo_actual):
		"""
		Programa ::= ( Asignación | Función | Comentario ) * Principal
		"""
		for nodo in nodo_actual.nodos:
			nodo.visitar(self)



	def __visitar_parametros(self, nodo_actual):
		"""
		Parametros ::= identificador ( , identificador )*
		"""
		for nodo in nodo_actual.nodos:
			self.tabla_simbolos.nuevo_registro(nodo)
			nodo.visitar(self)
			self.tabla_simbolos.encontrar_registro(nodo.contenido, nodo.atributos['tipo'])



	def __visitar_asignacion(self, nodo_actual):
		"""
		Asignación ::= ( Declaración ) pase ( Literal | Expresión Matemática | Identificador )
		""" 
		self.tabla_simbolos.nuevo_registro(nodo_actual.nodos[0])
		for nodo in nodo_actual.nodos:
			nodo.visitar(self)

		nodo_actual.atributos['tipo'] = nodo_actual.nodos[1].atributos['tipo']
		nodo_actual.nodos[0].atributos['tipo'] = nodo_actual.nodos[1].atributos['tipo']

		self.tabla_simbolos.encontrar_registro(nodo_actual.nodos[0].contenido, nodo_actual.nodos[1].atributos['tipo'])



	def __visitar_expresion_matematica(self, nodo_actual):
		"""
		ExpresiónMatemática ::= (Expresión) | Número | Identificador
		"""
		for nodo in nodo_actual.nodos:
			if nodo.tipo == TipoNodo.IDENTIFICADOR:
				registro = self.tabla_simbolos.verificar_existencia_bool(nodo.contenido)
				if not(registro):
					self.lista_errores.append("Error, no existe la variable " + nodo.contenido + " para la expresion matematica")
				else:
					registro_dentro = self.tabla_simbolos.verificar_existencia(nodo.contenido)
					if not(registro_dentro['tipodato'] == TipoDatos.NUMERO or registro_dentro['tipodato'] == TipoDatos.CUALQUIERA):
						self.lista_errores.append("Error, la variable " + nodo.contenido + " no se puede operar en la expresion matematica, no es un numero")
			nodo.visitar(self)
		nodo_actual.atributos['tipo'] = TipoDatos.NUMERO


	def __visitar_expresion(self, nodo_actual):
		"""
		Expresión ::= Expresión Matemática Operador Expresión Matemática
		"""
		for nodo in nodo_actual.nodos:
			nodo.visitar(self)

		nodo_actual.atributos['tipo'] = TipoDatos.NUMERO



	def __visitar_funcion(self, nodo_actual):
		"""
		Funcion ::= (Comentario)? jugada Identificador ( Parametros ) [ Instrucción + ]
		"""

		self.tabla_simbolos.nuevo_registro(nodo_actual)

		self.tabla_simbolos.abrir_bloque()

		for nodo in nodo_actual.nodos:
			nodo.visitar(self)

		#print(self.tabla_simbolos)
		self.tabla_simbolos.cerrar_bloque()

		nodo_actual.atributos['tipo'] = nodo_actual.nodos[2].atributos['tipo']



	def __visitar_bifurcacion(self, nodo_actual):
		"""
		TiempoExtra ::= tiempoExtra ( (Condicion | ValorLogico | Identificador) ) [ Instrucción+ ]
		Penales ::= penales [ Instrucción + ]
		"""
		self.tabla_simbolos.abrir_bloque()

		for nodo in nodo_actual.nodos:
			nodo.visitar(self)

		#print(self.tabla_simbolos)
		self.tabla_simbolos.cerrar_bloque()
		nodo_actual.atributos['tipo'] = nodo_actual.nodos[0].atributos['tipo']



	def __visitar_antianarquia(self, nodo_actual):
		"""
		AntiAnarquía ::= tiempoRegular ( (Condicion|ValorLogico|Identificador) ) [ Instrucción + ] (TiempoExtra )* (Penales)? 
		"""
		self.tabla_simbolos.abrir_bloque()

		for nodo in nodo_actual.nodos:
			nodo.visitar(self)

		#print(self.tabla_simbolos)
		self.tabla_simbolos.cerrar_bloque()
		nodo_actual.atributos['tipo'] = nodo_actual.nodos[0].atributos['tipo']



	def __visitar_invocacion(self, nodo_actual):
		"""
		Invocación ::= invo Identificador ( Parametros* )
		"""
		if (self.tabla_simbolos.verificar_existencia_bool(nodo_actual.contenido)):
			registro = self.tabla_simbolos.verificar_existencia(nodo_actual.nodos[0].contenido)

			if registro['referencia'].tipo is not TipoNodo.FUNCIÓN:
				self.lista_errores.append("Error de invocacion en la funcion " + nodo_actual.contenido)

			for nodo in nodo_actual.nodos:
				if nodo.tipo == TipoNodo.PARÁMETROS:
					for i in nodo.nodos:
						registro_dentro = self.tabla_simbolos.verificar_existencia_bool(i.contenido)
						if not(registro_dentro):
							self.lista_errores.append("Error de variable parametro de invocacion innexistente " + i.contenido)
				nodo.visitar(self)

			nodo_actual.atributos['tipo'] = registro['referencia'].atributos['tipo']
		else:
			self.lista_errores.append("Error, invocacion a funcion innexistente " + nodo_actual.contenido)



	def __visitar_instruccion(self, nodo_actual):
		"""
		Instrucción ::= (Repetición | Bifurcación | (Asignación | Invocación) | Retorno | Error | Comentario )
		"""

		for nodo in nodo_actual.nodos:
			nodo.visitar(self)
			nodo_actual.atributos['tipo'] = nodo.atributos['tipo']

		#nodo_actual.nodos[0].visitar(self)



	def __visitar_principal(self, nodo_actual):
		"""
		Principal ::= (Comentario)? pitido_Inicial () [ Instrucción + ] 
		"""
		self.tabla_simbolos.abrir_bloque()

		for nodo in nodo_actual.nodos:
			nodo.visitar(self)

		#print(self.tabla_simbolos)
		self.tabla_simbolos.cerrar_bloque()

		# nodo_actual.nodos[0].visitar(self)
		if nodo_actual.nodos != []:
			nodo_actual.atributos['tipo'] = nodo_actual.nodos[0].atributos['tipo']



	def __visitar_retorno(self, nodo_actual):
		"""
		Retorno ::= resultado Valor
		"""
		for nodo in nodo_actual.nodos:
			nodo.visitar(self)

			for nodo_dentro in nodo.nodos:
				if nodo_dentro.tipo == TipoNodo.IDENTIFICADOR:
					if self.tabla_simbolos.verificar_existencia_bool(nodo_dentro.contenido):
						registro = self.tabla_simbolos.verificar_existencia(nodo_dentro.contenido)
						nodo_actual.atributos['tipo'] = registro['referencia'].atributos['tipo']
					else:
						self.lista_errores.append("Error, no se puede retornar la variable que no existe " + nodo_actual.contenido)
				else:
					nodo_actual.atributos['tipo'] = nodo_dentro.atributos['tipo']


	def __visitar_repeticion(self, nodo_actual):
		"""
		Repetición ::= series ( Condicion | ValorLogico | Identificador ) [ Instrucción +]
		"""
		self.tabla_simbolos.abrir_bloque()
		for nodo in nodo_actual.nodos:
			nodo.visitar(self)

		# nodo_actual.nodos[0].visitar(self)
		#print(self.tabla_simbolos)
		self.tabla_simbolos.cerrar_bloque()
		nodo_actual.atributos['tipo'] = nodo_actual.nodos[1].atributos['tipo']



	def __visitar_operador(self, nodo_actual):
		"""
		Operador ::= ( aFavor | enContra | golVisita | balonDividido | cambioExtra)
		"""
		nodo_actual.atributos['tipo'] = TipoDatos.NUMERO



	def __visitar_condicion(self, nodo_actual):
		"""
		Condición ::= Comparación ( condicionLogica Comparación )*
		"""
		for nodo in nodo_actual.nodos:
			nodo.visitar(self)

		nodo_actual.atributos['tipo'] = TipoDatos.VALOR_VERDAD



	def __visitar_comparacion(self, nodo_actual):
		"""
		Comparación ::= Valor Comparador Valor
		"""
		for nodo in nodo_actual.nodos:
			if nodo.tipo == TipoNodo.IDENTIFICADOR:
				registro = self.tabla_simbolos.verificar_existencia_bool(nodo.contenido)
				if not(registro):
					self.lista_errores.append("Error de comparacion en la variable " + nodo.contenido)
			nodo.visitar(self)

		valor_izquierda = nodo_actual.nodos[0].nodos[0]
		comparador = nodo_actual.nodos[1]
		valor_derecha = nodo_actual.nodos[2].nodos[0]

		#este caso es si se compara un numero con un tipo cualquiera Y EL COMPARADOR es de tipo numero
		if (valor_izquierda.atributos['tipo'] == TipoDatos.NUMERO and valor_derecha.atributos['tipo'] == TipoDatos.CUALQUIERA) or (valor_derecha.atributos['tipo'] == TipoDatos.NUMERO and valor_izquierda.atributos['tipo'] == TipoDatos.CUALQUIERA):
			nodo_actual.atributos['tipo'] = TipoDatos.VALOR_VERDAD

		#este caso es si las variables de la comparacion son de tipo cualquiera pero el operador es de tipo numero
		elif ((valor_izquierda.atributos['tipo'] == TipoDatos.CUALQUIERA or valor_derecha.atributos['tipo'] == TipoDatos.CUALQUIERA) and comparador.atributos['tipo'] is not TipoDatos.NUMERO):
			nodo_actual.atributos['tipo'] = TipoDatos.VALOR_VERDAD	
		
		#Y este es si todos son iguales
		elif valor_izquierda.atributos['tipo'] == valor_derecha.atributos['tipo'] and valor_izquierda.atributos['tipo'] == comparador.atributos['tipo']:
			
			if ((valor_izquierda.atributos['tipo'] is not TipoDatos.NUMERO or valor_izquierda.atributos['tipo'] is not TipoDatos.CUALQUIERA) and comparador.atributos['tipo'] is TipoDatos.NUMERO):
				self.lista_errores.append("Error de comparacion, conflicto de tipos con " + valor_izquierda.contenido + " y " + valor_derecha.contenido)
			
			else:
				nodo_actual.atributos['tipo'] = TipoDatos.VALOR_VERDAD

		else:
			self.lista_errores.append("Error de comparacion, conflicto de tipos con " + valor_izquierda.contenido + " y " + valor_derecha.contenido)



	def __visitar_comparador(self, nodo_actual):
		"""
		Comparador ::= (mundialMayor, mundialMenor, mundialMixto, mundialMayor_Mixto, mundialMenor_Mixto, mundialSimple )
		"""
		if nodo_actual.contenido not in ['mundialMixto', 'mundialSimple']:
			nodo_actual.atributos['tipo'] = TipoDatos.NUMERO
		else:
			nodo_actual.atributos['tipo'] == TipoDatos.CUALQUIERA


	def __visitar_valor(self, nodo_actual):
		"""
		Valor ::= ( Identificador | Literal | Expresión Matemática )
		"""
		for nodo in nodo_actual.nodos:
			nodo.visitar(self)


	def __visitar_valor_logico(self, nodo_actual):
		"""
		ValorLogico ::= gol|fuera
		"""
		nodo_actual.atributos['tipo'] = TipoDatos.VALOR_VERDAD


	def __visitar_texto(self, nodo_actual):
		"""
		Texto ::= ~ [0-9a-zA-Z\W]+ ~
		"""
		nodo_actual.atributos['tipo'] = TipoDatos.TEXTO



	def __visitar_entero(self, nodo_actual):
		"""
		Entero ::= -?[0-9]+
		"""
		nodo_actual.atributos['tipo'] = TipoDatos.NUMERO



	def __visitar_flotante(self, nodo_actual):
		"""
		Flotante ::= -?[0-9]+.[0-9]+
		"""
		nodo_actual.atributos['tipo'] = TipoDatos.NUMERO



	def __visitar_identificador(self, nodo_actual):
		"""
		Identificador ::= [a-z][a-zA-Z0-9\W]+
		"""
		nodo_actual.atributos['tipo'] = TipoDatos.CUALQUIERA

