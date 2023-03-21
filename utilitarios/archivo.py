"""
Este archivo posee las funciones auxiliares que son necesarias para
que el explorardor y futuras componentes, puedan procesar el archivo linea por linea 
"""


"""
Elimina los saltos de linea de una linea cargada desde un archivo
"""
def eliminar_salto(linea):
	linea = linea[0:-1]
	return linea

"""
Crea una lista con las lineas de texto de un archivo
obviando el salto de linea al final (\n)
"""
def creacion_lineas(lista_lineas):
	lineas = []
	for linea in lista_lineas:
		lineas += [eliminar_salto(linea)]
	return lineas

"""
Permite cargar un archivo por medio de una ruta y convierte
el texto en una lista con las lineas de texto del archivo cargado
"""
def cargarArchivo(ruta_archivo):
	archivo = open(ruta_archivo,"r")
	lista_lineas = archivo.readlines()

	lineas_archivo = creacion_lineas(lista_lineas)

	return lineas_archivo

"""
Separa las palabras de una linea de texto separadas por espacios
"""
def separar_palabras(linea):
	palabras = linea.split()
	return palabras

"""
verifica si un comentario cumple con la regla lexica propuesta
"""
def verificar_Comentario(lista_linea):
	if len(lista_linea) > 0:
		if lista_linea[0] == 'piloObando:':
			linea_Comentario = lista_linea[0]
			lista_linea = lista_linea[1:]
			for i in lista_linea:
				linea_Comentario += ' ' + i
			return [linea_Comentario]
		else:
			return lista_linea
	else:
		return []


"""
verifica si un comentario cumple con la regla lexica propuesta
"""
def verificar_Texto(lista_linea):
	nueva_lista = []
	bandera = False
	nuevo_texto = ''
	for i in lista_linea:
		if i[0] == '~' or bandera:
			if i[0] == '~':
				if bandera:
					nuevo_texto += ' ' + i
				else:
					nuevo_texto += i
				bandera = not bandera
			else:
				nuevo_texto += ' ' + i
			if i[0] == '~' and not bandera:
				nueva_lista += [nuevo_texto]
		else:
 			nueva_lista += [i]
	if bandera:
 		nueva_lista += [nuevo_texto]
	return nueva_lista

