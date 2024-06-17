import enum


class TipoElemento(enum.Enum):
    LOGIN = 'Login'
    IDENTIFICACION = 'Identificacion'
    SECRETO = 'Secreto'
    TARJETA = 'Tarjeta'