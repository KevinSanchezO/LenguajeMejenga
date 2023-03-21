# Tipo de datos disponibles para anotaciones
from enum import Enum, auto

class TipoDatos(Enum):

    TEXTO        = auto()
    NUMERO       = auto()
    ENTERO       = auto()
    FLOTANTE     = auto()
    VALOR_VERDAD = auto()
    CUALQUIERA   = auto()
    NINGUNO      = auto()
