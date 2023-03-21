from explorador.explorador import TipoComponente
from utilitarios.arbolsintaxisabstracta import ASA
from utilitarios.nodoarbol import NodoÁrbol
from utilitarios.tiponodo import TipoNodo

import colorama
from colorama import Fore

class Analizador:

    def __init__(self, lista_componentes):

        self.componentes_léxicos = lista_componentes
        self.cantidad_componentes = len(lista_componentes)
        self.posición_componente_actual = 0
        self.componente_actual = lista_componentes[0]
        self.asa = ASA()
        self.errores = []
        self.bandera_error = False
        self.respaldo_pos = 0


    #metodo que se encarga de solicitar la impresion del ASA
    def imprimir_arbol(self):
        print("")
        self.asa.imprimir_preorden()
        print("")


    #metodo que se encarga de invocar el proceso de crear el ASA
    def analizar(self):
        """
        Método principal que inicia el análisis siguiendo el esquema de
        análisis por descenso recursivo
        """
        self.asa.raiz = self.__analizar_programa()

    #metodo que se encarga de mostrar en pantalla todos los errores encontrados en el proceso del analizador
    def imprimir_errores(self):
        for item in self.errores:
            print(Fore.YELLOW + item)


    #metodo que crea el ASA encontrando asignaciones globales, funciones y sus instrucciones
    def __analizar_programa(self):
        """
        Programa ::= ( Asignación | Función ) * Principal
        """

        #Obviamos los comentarios 
        #pueden venir múltiples asignaciones o funciones
        nodos_nuevos = []


        while (True):

            if self.componente_actual.tipoComponente == TipoComponente.COMENTARIO:
                self.__pasar_siguiente_componente()
            # Si es asignación
            if self.componente_actual.texto == 'visita' : #seccion de asignaciones globales
                self.respaldo_pos = self.posición_componente_actual + 1
                nodo_temporal = self.__analizar_asignación()
                if self.bandera_error:
                    self.componente_actual = self.componentes_léxicos[self.respaldo_pos]
                    self.posición_componente_actual = self.respaldo_pos
                    self.__buscar_siguiente_seguro()
                else:
                    nodos_nuevos += [nodo_temporal]

            # Si es función
            elif (self.componente_actual.texto == 'jugada'): #seccion de funciones
                self.respaldo_pos = self.posición_componente_actual + 1
                nodo_temporal = self.__analizar_función()
                if self.bandera_error:
                    self.componente_actual = self.componentes_léxicos[self.respaldo_pos]
                    self.posición_componente_actual = self.respaldo_pos
                    self.__buscar_siguiente_seguro()
                else:
                    nodos_nuevos += [nodo_temporal]
            else:
                break;
        if (self.componente_actual.texto == 'pitidoInicial'): #seccion de funcion principal
            nodos_nuevos += [self.__analizar_principal()]
        else:
            nodos_nuevos += [self.__analizar_error_pitidoIncial()]
        return NodoÁrbol(TipoNodo.PROGRAMA, nodos=nodos_nuevos, contenido = "Programa")


    #metodo que administra el error de no encontrar la funcion principal en el codigo en el proceso del analizador
    def __analizar_error_pitidoIncial(self):
        self.errores += ["ERROR, No existe instancia a pitidoInicial"]
        return NodoÁrbol(TipoNodo.ERROR_FALTA_INICIALIZADOR, nodos=[], contenido = "Error pitidoIncial")


    #analiza la funcion principal del codigo y sus instrucciones
    def __analizar_principal(self):
        """
        Principal ::= (Comentario)? pitido_Inicial () [ Instrucción + ]
        """
        nodos_nuevos = []

        #Esta seccion es obligatoria en este orden
        self.__verificar('pitidoInicial')
        self.__verificar('(')
        self.__verificar(')')
        self.__verificar('[')
        while (self.componente_actual.texto != ']'):
            nodos_nuevos += [self.__analizar_instrucción()]
        self.__verificar(']')
        return NodoÁrbol(TipoNodo.PRINCIPAL, nodos=nodos_nuevos, contenido = "pitidoInicial")


##################################################################################################
######################################## FUNCIÓN #################################################
##################################################################################################


    #metodo que genera la rama del ASA de una funcion junto a los nodos de sus instrucciones
    def __analizar_función(self):
        """
        Función ::= (Comentario)? jugada Identificador (ParámetrosFunción) BloqueInstrucciones
                    (Comentario)? jugada Identificador ( Parametros ) [ Instrucción + ] <------ Cambiar en la gramática
        Parametros ::= identificador ( , identificador )* <------ Cambiar en la gramática

        """

        nodos_nuevos = []

        # Esta sección es obligatoria en este orden
        self.__verificar('jugada')

        nodos_nuevos += [self.__verificar_identificador()]
        self.__verificar('(')
        nodos_nuevos += [self.__analizar_parámetros()]
        self.__verificar(')')
        self.__verificar('[')
        while (self.componente_actual.texto != ']'):
            nodos_nuevos += [self.__analizar_instrucción()]
        self.__verificar(']')

        # La función lleva el nombre del identificador
        return NodoÁrbol(TipoNodo.FUNCIÓN, contenido=nodos_nuevos[0].contenido, nodos=nodos_nuevos)


    #metodo para identificar los parametros de funciones
    def __analizar_parámetros(self):
        """
        Parametros ::= Identificador ( , Identificador)+
        """
        nodos_nuevos = []

        # Fijo un valor tiene que haber
        nodos_nuevos += [self.__verificar_identificador()]


        while( self.componente_actual.texto == ','):
            self.__verificar(',')
            nodos_nuevos += [self.__verificar_identificador()]

        # Esto funciona con lógica al verrís... Si no revienta con error
        # asumimos que todo bien y seguimos.

        return NodoÁrbol(TipoNodo.PARÁMETROS , nodos=nodos_nuevos, contenido = "Parametros")


    def __analizar_instrucción(self):
        """
        Instrucción ::= ( Invocación | Asignación | AntiAnarquía | Repetición | Retorno )
        """

        nodos_nuevos = []        
        if self.componente_actual.texto == 'series':
            nodos_nuevos += [self.__analizar_repetición()]
        elif self.componente_actual.texto == 'invo':
            nodos_nuevos += [self.__analizar_invocación()]
        elif self.componente_actual.texto == 'tiempoRegular':
            nodos_nuevos += [self.__analizar_antianarquía()]
        elif self.componente_actual.texto == 'local':
            nodos_nuevos += [self.__analizar_asignación()]
        elif self.componente_actual.texto == 'resultado':
            nodos_nuevos += [self.__analizar_retorno()]
        else: # Muy apropiado el chiste de ir a revisar si tiene error al último.
            nodos_nuevos += [self.__analizar_error()]
        # Acá yo debería volarme el nivel Intrucción por que no aporta nada
        return NodoÁrbol(TipoNodo.INSTRUCCIÓN, nodos=nodos_nuevos, contenido = "Instrucciones")


################################################ Error ######################################


    def __analizar_error(self):
        nodos_nuevos = []
        self.__pasar_siguiente_componente()
        if not(self.bandera_error):
            self.errores += ["Error en la linea " + str(self.componente_actual.linea) + ", Debido a que se esperaba una instruccion"]
        self.bandera_error = True
        return NodoÁrbol(TipoNodo.ERROR, nodos=nodos_nuevos, contenido = "Error")


################################################ Retorno ####################################

    def __analizar_retorno(self):
        """
        resultado Valor
        """
        nodos_nuevos = []
        self.__verificar('resultado')

        nodos_nuevos += [self.__analizar_valor()]
        return NodoÁrbol(TipoNodo.RETORNO, nodos=nodos_nuevos, contenido = nodos_nuevos[0].contenido)

############################################### Antianarquía ################################

    def __analizar_antianarquía(self):
        """
         tiempoRegular ( (Condicion | ValorLogico | Identificador) ) [ Instrucción + ] (TiempoExtra )*
          (Penales)?
        """

        nodos_nuevos = []
        self.__verificar('tiempoRegular')
        self.__verificar('(')
        ### condicion verdadera o falsa
        if self.componente_actual.tipoComponente == TipoComponente.VALOR_LOGICO:
            nodos_nuevos += [self.__verificar_valor_logico()]
        elif self.componente_actual.tipoComponente == TipoComponente.IDENTIFICADOR and (self.componentes_léxicos[self.posición_componente_actual + 1].tipoComponente != TipoComponente.COMPARADOR):
            nodos_nuevos += [self.__verificar_identificador()]
        else:
            nodos_nuevos += [self.__verificar_condición()]
        self.__verificar(')') 
        ## bloque de instrucciones 
        self.__verificar('[')
        while (self.componente_actual.texto != ']'):
            nodos_nuevos += [self.__analizar_instrucción()]
        self.__verificar(']') 

        ### si hay elif o else
        while (self.componente_actual.texto == 'tiempoExtra'):
            nodos_nuevos += [self.__verificar_tiempoExtra()]
        if self.componente_actual.texto == 'penales':
            nodos_nuevos += [self.__verificar_penales()]
        return NodoÁrbol(TipoNodo.ANTIANARQUÍA, nodos=nodos_nuevos, contenido = "tiempoRegular")


    def __verificar_tiempoExtra(self):
        """
        TiempoExtra ::= tiempoExtra ( (Condicion | ValorLogico | Identificador) ) [ Instrucción+ ] <-- cambio gramatica
        """
        nodos_nuevos = []
        self.__verificar_tipo_componente(TipoComponente.CONDICIONAL)
        self.__verificar('(')
        if self.componente_actual.tipoComponente == TipoComponente.VALOR_LOGICO:
            nodos_nuevos += [self.__verificar_valor_logico()]
        elif self.componente_actual.tipoComponente == TipoComponente.IDENTIFICADOR and (self.componentes_léxicos[self.posición_componente_actual + 1].tipoComponente != TipoComponente.COMPARADOR):
            nodos_nuevos += [self.__verificar_identificador()]
        else:
            nodos_nuevos += [self.__verificar_condición()]
        self.__verificar(')')
        self.__verificar('[')
        while (self.componente_actual.texto != ']'):
            nodos_nuevos += [self.__analizar_instrucción()]
        self.__verificar(']') 
        return NodoÁrbol(TipoNodo.BIFURCACIÓN, nodos=nodos_nuevos, contenido = "tiempoExtra")


    def __verificar_penales(self):
        """
        Penales ::= penales [ Instrucción + ]
        """
        nodos_nuevos = []
        self.__verificar_tipo_componente(TipoComponente.CONDICIONAL)
        self.__verificar('[') 
        while (self.componente_actual.texto != ']'):
            nodos_nuevos += [self.__analizar_instrucción()]
        self.__verificar(']') 
        return NodoÁrbol(TipoNodo.BIFURCACIÓN, nodos=nodos_nuevos, contenido = "penales")


############################################### Invocación ######################################

    def __analizar_invocación(self):
        """
        Invocación ::= invo Identificador ( Parametros* ) <-- Cambiar gramatica
        """
        nodos_nuevos = []
        self.__verificar('invo')
        nodos_nuevos += [self.__verificar_identificador()]
        self.__verificar('(')
        if self.componente_actual.texto != ')':
            nodos_nuevos += [self.__analizar_parámetros()]
        self.__verificar(')')
        return NodoÁrbol(TipoNodo.INVOCACIÓN, nodos=nodos_nuevos, contenido = nodos_nuevos[0].contenido)



############################################### Repetición ######################################

    def __analizar_repetición(self):
        """
        Repetición ::= series ( Condicion | ValorLogico | Identificador  ) [ Instrucción +] <--- Cambio se agregó identificador
        """
        nodos_nuevos = []

        # Todos presentes en ese orden... sin opciones
        self.__verificar('series')
        self.__verificar('(')
        if self.componente_actual.tipoComponente == TipoComponente.VALOR_LOGICO:
            nodos_nuevos += [self.__verificar_valor_logico()]
        elif (self.componente_actual.tipoComponente == TipoComponente.IDENTIFICADOR) and (self.componentes_léxicos[self.posición_componente_actual + 1].tipoComponente  != TipoComponente.COMPARADOR):
            nodos_nuevos += [self.__verificar_identificador()]
        else:
            nodos_nuevos += [self.__verificar_condición()]
        self.__verificar(')')
        self.__verificar('[')
        nodos_nuevos += [self.__analizar_instrucción()]
        self.__verificar(']')
        return NodoÁrbol(TipoNodo.REPETICIÓN, nodos=nodos_nuevos, contenido = "series")

    def __verificar_condición(self):
        """
        Condición ::= Comparación ( condicionLogica Comparación )*
        """
        nodos_nuevos = []

        # La primera sección obligatoria la comparación
        nodos_nuevos += [self.__analizar_comparación()]

        while( self.componente_actual.tipoComponente == TipoComponente.CONDICION):
            nodos_nuevos += [self.__verificar_condicionLogica()]
            nodos_nuevos += [self.__analizar_comparación()]        
        return NodoÁrbol(TipoNodo.CONDICIÓN, nodos=nodos_nuevos, contenido = "Condicion")

    def __verificar_condicionLogica(self):
        """
        CondicionLogica ::= ( leyVentaja | falta ) or and
        """
        texto_contenido = componente_actual.texto
        self.__verificar_tipo_componente(TipoComponente.CONDICION)
        return NodoÁrbol(TipoNodo.CONDICIÓN, nodos=nodos_nuevos, contenido = texto_contenido)


    def __analizar_comparación(self):
        """
        Comparación ::=  Valor Comparador Valor 
        """
        nodos_nuevos = []
        nodos_nuevos += [self.__analizar_valor()]
        nodos_nuevos += [self.__verificar_comparador()]
        nodos_nuevos += [self.__analizar_valor()]
        return NodoÁrbol(TipoNodo.COMPARACIÓN, nodos=nodos_nuevos, contenido="Comparación")

    def __analizar_valor(self):
        """
        Valor ::= ( Identificador | Literal | Expresión Matemática ) <--- cambio
        """
        nodos_nuevos = []
        estado_valor = False
        if self.componente_actual.tipoComponente in [TipoComponente.ENTERO, TipoComponente.FLOTANTE, TipoComponente.VALOR_LOGICO, TipoComponente.TEXTO]:
            nodos_nuevos += [self.__analizar_literal()]
        elif self.componente_actual.tipoComponente == TipoComponente.IDENTIFICADOR:
            nodos_nuevos += [self.__verificar_identificador()]
        else:
            estado_valor = True
            nodos_nuevos += [self.__analizar_expresión_matemática()]
        if estado_valor:
            return NodoÁrbol(TipoNodo.VALOR, nodos=nodos_nuevos, contenido="expresion matematica")
        else:
            return NodoÁrbol(TipoNodo.VALOR, nodos=nodos_nuevos, contenido=nodos_nuevos[0].contenido)  


    def __verificar_comparador(self):
        """
        Comparador ::= (mundialMayor, mundialMenor, mundialMixto, mundialMayor_Mixto, mundialMenor_Mixto, mundialSimple )
        """
        texto_contenido = self.componente_actual.texto
        self.__verificar_tipo_componente(TipoComponente.COMPARADOR)
        nodo = NodoÁrbol(TipoNodo.COMPARADOR, contenido = texto_contenido)
        return nodo

###############################################################################################
################################### ASIGNACIÓN ################################################
###############################################################################################

    def __analizar_asignación(self):
        """
        Asignación ::= ( Declaración ) pase ( Literal | Expresión Matemática | Identificador )
        Declaración ::= ( visita | local )-> se revisa antes de la asignación Identificador
        """
        self.__pasar_siguiente_componente()
        nodos_nuevos = []
        # La declaración en esta posición es obligatorio
        nodos_nuevos += [self.__verificar_identificador()]

        # Igual el pase
        self.__verificar('pase')


        # El siguiente bloque es de opcionales
        if self.componente_actual.tipoComponente in [TipoComponente.ENTERO, TipoComponente.FLOTANTE, TipoComponente.VALOR_LOGICO, TipoComponente.TEXTO] :
            nodos_nuevos += [self.__analizar_literal()]

        # los paréntesis obligatorios (es un poco feo)
        elif self.componente_actual.texto == '(': 
            nodos_nuevos += [self.__analizar_expresión_matemática()]

        elif self.componente_actual.tipoComponente is TipoComponente.IDENTIFICADOR:
            nodos_nuevos += [self.__verificar_identificador()]

        return NodoÁrbol(TipoNodo.ASIGNACIÓN, nodos=nodos_nuevos, contenido = "Asignacion")
        

#####################################literal################################

    def __analizar_literal(self):
        """
        Literal ::= (Número | Texto | ValorVerdad)
        """

        if self.componente_actual.tipoComponente is TipoComponente.TEXTO:
            nodo = self.__verificar_texto()

        elif self.componente_actual.tipoComponente is TipoComponente.VALOR_LOGICO:
            nodo = self.__verificar_valor_logico()

        else:
            nodo = self.__analizar_número()

        return nodo


    def __verificar_texto(self):
        """
        Verifica si el tipo del componente léxico actuales de tipo TEXTO

        Texto ::= ~.?[^~]*)~
        """
        texto_contenido = self.componente_actual.texto
        self.__verificar_tipo_componente(TipoComponente.TEXTO)

        nodo = NodoÁrbol(TipoNodo.TEXTO, contenido = texto_contenido)
        return nodo


    def __analizar_número(self):
        """
        Número ::= (Entero | Flotante)
        """
        if self.componente_actual.tipoComponente == TipoComponente.ENTERO:
            nodo = self.__verificar_entero()
        else:
            nodo = self.__verificar_flotante()
        return nodo


    def __verificar_entero(self):
        """
        Verifica si el tipo del componente léxico actuales de tipo ENTERO

        Entero ::= (-)?\d+
        """
        texto_contenido = self.componente_actual.texto
        self.__verificar_tipo_componente(TipoComponente.ENTERO)
        nodo = NodoÁrbol(TipoNodo.ENTERO, contenido = texto_contenido)
        return nodo


    def __verificar_flotante(self):
        """
        Verifica si el tipo del componente léxico actuales de tipo FLOTANTE

        Flotante ::= (-)?\d+.(-)?\d+
        """
        texto_contenido = self.componente_actual.texto
        self.__verificar_tipo_componente(TipoComponente.FLOTANTE)
        nodo = NodoÁrbol(TipoNodo.FLOTANTE, contenido = texto_contenido)
        return nodo

    def __verificar_valor_logico(self):
        """
        ValorVerdad ::= (True | False)
        """
        texto_contenido = self.componente_actual.texto
        self.__verificar_tipo_componente(TipoComponente.VALOR_LOGICO)
        nodo = NodoÁrbol(TipoNodo.VALOR_LOGICO, contenido = texto_contenido)
        return nodo

#################################################################################################
####################################Expresión Matemática ########################################

    def __analizar_expresión_matemática(self):
        """
        ExpresiónMatemática ::= (Expresión) | Número | Identificador <--- Cambiar gramatica
        """
        nodos_nuevos = [] 
        # Primera opción
        if self.componente_actual.texto == '(':
            # Los verificar no se incluyen por que son para forzar cierta
            # forma de escribir... pero no aportan nada a la semántica
            self.__verificar('(')
            nodos_nuevos += [self.__analizar_expresión()]
            self.__verificar(')')
        # Acá yo se que estan bien formados por que eso lo hizo el
        # explorador... es nada más revisar las posiciones.
        elif self.componente_actual.tipoComponente == TipoComponente.ENTERO:
            nodos_nuevos += [self.__verificar_entero()]
        elif self.componente_actual.tipoComponente == TipoComponente.FLOTANTE:
            nodos_nuevos += [self.__verificar_flotante()]
        # Este código se simplifica si invierto la opción anterior y esta
        else:
            nodos_nuevos += [self.__verificar_identificador()]
        return NodoÁrbol(TipoNodo.EXPRESIÓN_MATEMÁTICA, nodos = nodos_nuevos, contenido = "Expresion matematica")


    def __analizar_expresión(self):

        nodos_nuevos = []
        # Acá no hay nada que hacer todas son obligatorias en esas
        # posiciones

        nodos_nuevos += [self.__analizar_expresión_matemática()]

        nodos_nuevos += [self.__verificar_operador()]

        nodos_nuevos += [self.__analizar_expresión_matemática()]

        return NodoÁrbol(TipoNodo.EXPRESIÓN , nodos=nodos_nuevos, contenido = "expresion")

    def __verificar_operador(self):
        """
        Operador ::= ( aFavor | enContra | golVisita | balonDividido | cambioExtra )
        """
        texto_contenido = self.componente_actual.texto
        self.__verificar_tipo_componente(TipoComponente.OPERADOR)
        nodo = NodoÁrbol(TipoNodo.OPERADOR, contenido = texto_contenido)
        return nodo

##################################################################################################

    def __verificar_identificador(self):
        """
        Verifica si el tipo del componente léxico actuales de tipo
        IDENTIFICADOR
        Identificador ::= [a-z][a-zA-Z0-9]+
        """
        nodo = NodoÁrbol(TipoNodo.IDENTIFICADOR, contenido = self.componente_actual.texto)
        self.__verificar_tipo_componente(TipoComponente.IDENTIFICADOR)
        return nodo


    def __verificar_tipo_componente(self, tipo_esperado ):
        if self.componente_actual.tipoComponente is not tipo_esperado:
            self.errores += ["Error en la linea: "+(str)(self.componente_actual.linea)+" debido a que no cumple con el tipo esperado"]
            self.bandera_error = True
        self.__pasar_siguiente_componente()


    def __verificar(self, texto_esperado):
        """
        Verifica si el texto del componente léxico actual corresponde con
        el esperado cómo argumento
        """
        if self.componente_actual.texto != texto_esperado:
            self.errores += ["Error en la linea: "+(str)(self.componente_actual.linea)+" debido a que no es la palabra esperada, pruebe con " + texto_esperado]
            self.bandera_error = True
        self.__pasar_siguiente_componente()


    #Se salta al siguiente componente que podemos garantizar no presentara un error como una funcion, asignacion global o funcion principal
    def __buscar_siguiente_seguro(self):
            while (not(self.componente_actual.texto in ["pitidoInicial", "jugada", "visita"])):
                self.__pasar_siguiente_componente()
            self.bandera_error = False


    def __pasar_siguiente_componente(self):
        """
        Pasa al siguiente componente léxico
        """
        if self.posición_componente_actual + 1 < len(self.componentes_léxicos) :
            self.posición_componente_actual += 1
            self.componente_actual = self.componentes_léxicos[self.posición_componente_actual]
