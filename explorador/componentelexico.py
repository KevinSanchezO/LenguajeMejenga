"""
Clase que servira como estructura de datos para los componentes lexicos encontrados
"""
class ComponenteLexico:

	def __init__(self, nuevoTipoComponente, nuevoTexto, linea):
		self.tipoComponente = nuevoTipoComponente
		self.texto = nuevoTexto
		self.linea = linea

	"""
	Ejemplo de representacion:
	ENTERO <420>, linea = 5
	"""
	def representarInstancia(self):
		return f'{self.tipoComponente} <{self.texto}>, linea = {self.linea}'