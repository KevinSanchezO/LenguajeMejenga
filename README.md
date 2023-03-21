# Lenguaje Mejenga :soccer:

## Especificación

Este proyecto es un compilador hecho en Python para el curso de Compiladores e interpretes para el lenguaje de programación "Mejenga" diseñado en el curso por Jordi Segura Madrigal y Kevin Sánchez Obando. El proyecto presenta todas las partes que conforman a un compilador (explorador, analizador, generador y verificador).

El lenguaje de programación “Mejenga” está diseñado para todos aquellos
amantes del fútbol en Costa Rica. Está compuesto por reglas y palabras reservadas
que hacen referencia a la jerga comúnmente utilizada en partidos no profesionales
de fútbol practicados en este país conocido como “mejengas” y que es el origen del
nombre del lenguaje.

Vemos en la gramática palabras como “pase” siendo una asignación a una
variable que esperamos que se lea como “a esta variable pasale este valor”,
“aFavor”, “enContra”, “gol”, “fuera”, “series”, entre otros, esto para hacer una
referencia a estas palabras en las cuales nos basamos en sus significados para de
cierta forma relacionarlas con su funcionalidad. Por ejemplo las estructuras de
bifurcación que serían if-elif-else, las cuales están basadas en el lenguaje de
programación Python; las vemos como tiempoRegular, tiempoExtra y penales
respectivamente, siendo estos los 3 tiempos que hay posibles en un partido de
fútbol, haciendo referencia a que si no se gana en el primer tiempoRegular se gana
en el tiempoExtra y en todo caso si no pasa ninguna de las anteriores se gana en
los penales.

## Gramática EBNF

Programa ::= ( Asignación | Función | Comentario ) * Principal <br>
nstrucción ::= ( Funcion = Invocación | Asignación | AntiAnarquía | Repetición |
Retorno ) <br>
Asignación ::= ( Declaración ) pase ( Literal | Expresión Matemática | Identificador ) <br>
Declaración ::= ( visita | local ) Identificador <br>
Funcion ::= (Comentario)? jugada Identificador ( Parametros ) [ Instrucción + ] <br>
ExpresiónMatemática ::= (Expresión) | Número | Identificador <br>
Expresión ::= Expresión Matemática Operador Expresión Matemática <br>
Operador ::= ( aFavor | enContra | golVisita | balonDividido | cambioExtra) <br>
Invocación ::= invo Identificador ( Parametros* ) <br>
Parametros ::= identificador ( , identificador )* <br>
Literal ::= ( Texto | Numero | ValorLógico ) <br>
Repetición ::= series ( Condicion | ValorLogico | Identificador ) [ Instrucción +] <br>
Principal ::= (Comentario)? pitido_Inicial () [ Instrucción + ] <br>
Comentario ::= piloObando: (\w ( \s\w ) * )? <br>
Condición ::= Comparación ( condicionLogica Comparación )* <br>
condicionLogica ::= ( leyVentaja | falta ) <br>
Comparación ::= Valor Comparador Valor <br>
AntiAnarquía ::= tiempoRegular ( (Condicion|ValorLogico|Identificador) ) [ Instrucción+ ] (TiempoExtra )* (Penales)? <br>
TiempoExtra ::= tiempoExtra ( (Condicion | ValorLogico | Identificador) ) [
Instrucción+ ] <br>
Penales ::= penales [ Instrucción + ] <br>
Retorno ::= resultado Valor <br>
Imprimir ::= marcador ( Valor | Identificador ) <br>
Valor ::= ( Identificador | Literal | Expresión Matemática ) <br>
Comparador ::= (mundialMayor, mundialMenor, mundialMixto,
mundialMayor_Mixto, mundialMenor_Mixto, mundialSimple ) <br>
ValorLógico ::= gol | fuera <br>
Numero ::= ( Entero | Flotante) <br>
Entero ::= -?[0-9]+ <br>
Flotante ::= -?[0-9]+.[0-9]+ <br>
Texto ::= ~ [0-9a-zA-Z\W]+ ~ <br>
Identificador ::= [a-z][a-zA-Z0-9\W]+ <br>

## Ambiente de programación

Python 3.10.3 <br>
Sistema operativo Ubuntu

