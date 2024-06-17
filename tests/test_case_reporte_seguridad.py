import unittest
import datetime

from faker import Faker
from src.modelo.declarative_base import Base, Session, engine
from src.logica.FachadaCajaDeSeguridad import FachadaCajaDeSeguridad
from src.repositorios import ClaveRepositorio
from src.modelo.ElementoTarjeta import ElementoTarjeta
from src.modelo.ClaveFavorita import ClaveFavorita
from src.modelo.ElementoIdentificacion import ElementoIdentificacion


class ReporteSeguridadTestCase(unittest.TestCase):
    
    def setUp(self):
        self.claveRepository = ClaveRepositorio.ClaveRepository()
        self.fachada = FachadaCajaDeSeguridad()
        self.fake = Faker()
        self.session = Session()
        
    def tearDown(self):
        Base.metadata.drop_all(bind=engine)
        
    
    def test_mostrar_numero_claves_inseguras(self):
        
        esperado = 3
        
        self.fachada.crear_clave(self.fake.name(), '12345', self.fake.text())   
        self.fachada.crear_clave(self.fake.name(), 'abcde', self.fake.text()) 
        self.fachada.crear_clave(self.fake.name(), '123abc', self.fake.text())   
        self.fachada.crear_clave(self.fake.name(), self.fachada.generar_clave(), self.fake.text())   
        self.fachada.crear_clave(self.fake.name(), self.fachada.generar_clave(), self.fake.text())
        
        resultado = self.fachada.dar_reporte_seguridad()
        self.assertEqual(esperado, resultado['inseguras'])

    def test_mostrar_cantidad_claves_repetidas(self):
        '''Cantidad de claves repetidas mas de una vez'''

        esperado = 2

        self.fachada.crear_clave(self.fake.name(), self.fachada.generar_clave(), self.fake.text())
        self.fachada.crear_clave(self.fake.name(), self.fachada.generar_clave(), self.fake.text())
        self.fachada.crear_clave(self.fake.name(), self.fachada.generar_clave(), self.fake.text())

        claves = self.fachada.dar_claves_favoritas()

        self.__crear_elemento_login(claves[0].nombre)
        self.__crear_elemento_login(claves[0].nombre)
        self.__crear_elemento_login(claves[1].nombre)
        self.__crear_elemento_login(claves[1].nombre)
        self.__crear_elemento_login(claves[2].nombre)

        resultado = self.fachada.dar_reporte_seguridad()
        self.assertEqual(esperado, resultado['masdeuna'])
        
    def test_mostrar_cantidad_elementos_login(self):
        
        esperado = 5
        
        self.fachada.crear_clave(self.fake.name(), self.fachada.generar_clave(), self.fake.text())

        claves = self.fachada.dar_claves_favoritas()

        self.__crear_elemento_login(claves[0].nombre)
        self.__crear_elemento_login(claves[0].nombre)
        self.__crear_elemento_login(claves[0].nombre)
        self.__crear_elemento_login(claves[0].nombre)
        self.__crear_elemento_login(claves[0].nombre)
        
        resultado = self.fachada.dar_reporte_seguridad()
        self.assertEqual(esperado, resultado['logins'])

    def test_mostrar_cantidad_elementos_secreto(self):
        esperado = 4

        self.fachada.crear_clave(self.fake.name(), self.fachada.generar_clave(), self.fake.text())
        claves = self.fachada.dar_claves_favoritas()

        self.__crear_elemento_secreto(claves[0].nombre)
        self.__crear_elemento_secreto(claves[0].nombre)
        self.__crear_elemento_secreto(claves[0].nombre)
        self.__crear_elemento_secreto(claves[0].nombre)

        resultado = self.fachada.dar_reporte_seguridad()
        self.assertEqual(esperado, resultado['secretos'])


    def test_mostrar_cantidad_elementos_tarjeta(self):
        esperado = 6

        self.fachada.crear_clave(self.fake.name(), self.fachada.generar_clave(), self.fake.text())
        claves = self.fachada.dar_claves_favoritas()

        self.__crear_elemento_tarjeta(claves[0].nombre)
        self.__crear_elemento_tarjeta(claves[0].nombre)
        self.__crear_elemento_tarjeta(claves[0].nombre)
        self.__crear_elemento_tarjeta(claves[0].nombre)
        self.__crear_elemento_tarjeta(claves[0].nombre)
        self.__crear_elemento_tarjeta(claves[0].nombre)

        resultado = self.fachada.dar_reporte_seguridad()
        self.assertEqual(esperado, resultado['tarjetas'])

    def test_mostrar_cantidad_elementos_identificacion(self):
        esperado = 7

        self.__crear_elemento_identificacion()
        self.__crear_elemento_identificacion()
        self.__crear_elemento_identificacion()
        self.__crear_elemento_identificacion()
        self.__crear_elemento_identificacion()
        self.__crear_elemento_identificacion()
        self.__crear_elemento_identificacion()

        resultado = self.fachada.dar_reporte_seguridad()
        self.assertEqual(esperado, resultado['ids'])
        
    def test_mostrar_nivel_seguridad(self):
        esperado = 16.0

        self.fachada.crear_clave(self.fake.name(), 'abcde', self.fake.text()) 
        self.fachada.crear_clave(self.fake.name(), '123abc', self.fake.text())   
        self.fachada.crear_clave(self.fake.name(), self.fachada.generar_clave(), self.fake.text())   
        self.fachada.crear_clave(self.fake.name(), self.fachada.generar_clave(), self.fake.text())

        claves = self.fachada.dar_claves_favoritas()

        self.__crear_elemento_login(claves[0].nombre)
        self.__crear_elemento_login(claves[0].nombre)
        self.__crear_elemento_login(claves[1].nombre)
        
        self.__crear_elemento_secreto(claves[1].nombre)
        self.__crear_elemento_secreto(claves[2].nombre)
        
        self.__crear_elemento_tarjeta(claves[0].nombre)
        self.__crear_elemento_identificacion()


        resultado = self.fachada.dar_reporte_seguridad()
        self.assertEqual(esperado, resultado['nivel'])

    def __crear_elemento_login(self, nombre_clave):
        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        if resultado == '':
            self.fachada.crear_login(nombre, email, usuario, nombre_clave, url, notas)

    def __crear_elemento_secreto(self, nombre_clave):
        nombre_secreto = self.fake.name()
        secreto = self.fake.text()
        notas = self.fake.text()

        self.fachada.crear_secreto(nombre_secreto, secreto, nombre_clave, notas)
        
    def __crear_elemento_tarjeta(self, clave_nombre):
        nombre = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        titular = self.fake.name()
        fechaVencimiento = self.fake.name()
        notas = self.fake.text()
        direccion = self.fake.address()
        telefono =self.fake.phone_number()
        notaTexto = self.fake.text()
        ccv = str(self.fake.random_number(digits=3))
        
        claveFavorita = self.session.query(ClaveFavorita).filter(ClaveFavorita.nombre == clave_nombre).limit(1).first()
        
        elementoTarjeta = ElementoTarjeta(nombre_elemento = nombre, numero = numero, titular = titular, fechaVencimiento = self.fake.date_between(start_date=datetime.date(2023, 12, 30), end_date=datetime.date(2023, 12, 31)), direccion = direccion, telefono = telefono, clave = claveFavorita)

        self.session.add(elementoTarjeta)
        self.session.commit()
        
    def __crear_elemento_identificacion(self):
        nombreIdentificacion = self.fake.name()
        numero = self.fake.name()
        fechaNacimiento = self.fake.date_between(start_date=datetime.date(2003, 3, 3), end_date=datetime.date(2003, 12, 31))
        fechaExpedicion = self.fake.date_between(start_date=datetime.date(2022, 1, 1), end_date=datetime.date(2022, 12, 31))
        fechaVencimiento = self.fake.date_between(start_date=datetime.date(2023, 12, 30), end_date=datetime.date(2023, 12, 31))
        notaTexto = self.fake.name()

        elementoIdentificacion = ElementoIdentificacion(nombre=nombreIdentificacion, numero=numero, fecha_nacimiento=fechaNacimiento, fecha_exp=fechaExpedicion, fecha_venc=fechaVencimiento, notas=notaTexto)

        self.session.add(elementoIdentificacion)
        self.session.commit()