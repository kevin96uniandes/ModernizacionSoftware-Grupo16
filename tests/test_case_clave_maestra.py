import unittest
from faker import Faker

from src.modelo.declarative_base import Base, engine
from src.logica.FachadaCajaDeSeguridad import FachadaCajaDeSeguridad
from src.repositorios.ClaveMaestraRepositorio import ClaveMaestraRepository


class TestCaseClaveFavorita(unittest.TestCase):
        
    def setUp(self):
        self.claveMaestraRepository = ClaveMaestraRepository()
        self.fachada = FachadaCajaDeSeguridad()
        self.fake = Faker()

    def tearDown(self):
        Base.metadata.drop_all(bind=engine)
        
    def test_validar_existe_clave_maestra(self):
        clave_maestra = self.fake.text()
        self.claveMaestraRepository.crear_clave_maestra(clave_maestra)
        
        claveMaestra = self.fachada.dar_claveMaestra()
        self.assertEqual(claveMaestra, clave_maestra)
