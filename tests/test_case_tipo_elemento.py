import unittest
from src.modelo.TipoElemento import TipoElemento


class TestCaseTipoElemento(unittest.TestCase):
    def test_validar_valor_de_retorno(self):
        self.assertEqual('Login', TipoElemento.LOGIN.value)
        self.assertEqual('Identificacion', TipoElemento.IDENTIFICACION.value)
        self.assertEqual('Secreto', TipoElemento.SECRETO.value)
        self.assertEqual('Tarjeta', TipoElemento.TARJETA.value)
