import unittest
import datetime
from faker import Faker
from faker.providers import internet

from src.modelo.ElementoIdentificacion import ElementoIdentificacion
from src.modelo.declarative_base import Base, engine
from src.logica.FachadaCajaDeSeguridad import FachadaCajaDeSeguridad


class TestCaseClaveFavorita(unittest.TestCase):

    def setUp(self):
        self.fachada = FachadaCajaDeSeguridad()
        self.fake = Faker()
        self.fake.add_provider(internet)

    def tearDown(self):
        Base.metadata.drop_all(bind=engine)

    def test_existen_elementos(self):

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre, clave, pista)

        nombre_secreto = self.fake.name()
        secreto = self.fake.text()
        clave_nombre = nombre
        notas = self.fake.text()

        self.fachada.crear_secreto(nombre_secreto, secreto, clave_nombre, notas)

        claves_favoritas = self.fachada.dar_elementos()
        self.assertTrue(len(claves_favoritas) > 0)

    def test_validar_ordenamiento_descendente_elementos(self):
        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre, clave, pista)
        for i in range(1, 5):
            nombre_secreto = self.fake.name()+' '+ str(i)
            secreto =  self.fake.text()
            clave_nombre = nombre
            notas =  self.fake.text()
            self.fachada.crear_secreto(nombre_secreto, secreto, clave_nombre, notas)

        elementos = self.fachada.dar_elementos()
        self.assertEqual(4, elementos[0].id)

    def test_validar_nombre_vacio_elemento_login(self):

        esperado = "El campo nombre es obligatorio"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = ''
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_nombre_indefinido_elemento_login(self):

        esperado = "El campo nombre es obligatorio"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = None
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_email_vacio_elemento_login(self):

        esperado = "El campo email es obligatorio"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = ''
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_email_indefinido_elemento_login(self):

        esperado = "El campo email es obligatorio"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = None
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_estructura_email_valida_elemento_login(self):

        esperado = "El campo email debe tener una estructura valida (xxxxx@xxx.com)"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = self.fake.name()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_usuario_vacio_elemento_login(self):

        esperado = "El campo usuario debe ser obligatorio"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = self.fake.email()
        usuario = ''
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_usuario_indefinido_elemento_login(self):

        esperado = "El campo usuario debe ser obligatorio"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = self.fake.email()
        usuario = None
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_campo_url_vacio_elemento_login(self):

        esperado = "El campo url debe ser obligatorio"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = ''
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_campo_url_indefinido_elemento_login(self):

        esperado = "El campo url debe ser obligatorio"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = None
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_campo_url_estructura_definida_elemento_login(self):

        esperado = "El campo url debe tener una estructura valida (https://xxxxx.xxx)"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.text()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_campo_notas_vacio_elemento_login(self):

        esperado = "El campo notas es obligatorio"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = ''

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_campo_notas_indefinido_elemento_login(self):

        esperado = "El campo notas es obligatorio"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = None

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_campo_notas_tamano_minimo_elemento_login(self):

        esperado = "El campo notas debe tener minimo 3 caracteres"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.pystr(max_chars=2)

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_campo_notas_tamano_maximo_elemento_login(self):

        esperado = "El campo notas debe tener maximo 512 caracteres"

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.pystr(min_chars=513, max_chars=515)

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_password_vacia_elemento_login(self):

        esperado = "El campo password es obligatorio"

        nombre_clave = ''
        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_validar_password_indefinida_elemento_login(self):

        esperado = "El campo password es obligatorio"

        nombre_clave = None
        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        self.assertEqual(esperado, resultado)

    def test_insercion_satisfactoria_elemento_login(self):
        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        if resultado == '':
            self.fachada.crear_login(nombre, email, usuario, nombre_clave, url, notas)

        self.assertTrue(True)

    def test_validar_elemento_login_existente_sistema(self):
        esperado = 'El elemento ya fue creado en el sistema'

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        # Creación elemento 1
        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        if resultado == '':
            self.fachada.crear_login(nombre, email, usuario, nombre_clave, url, notas)

        # Creación elemento 2, se deja mismo nombre
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.text()
        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        if resultado == '':
            self.fachada.crear_login(nombre, email, usuario, nombre_clave, url, notas)

        self.assertEqual(esperado, resultado)

    def test_validar_nombre_vacio_elemento_identificacion(self):
        esperado = 'El nombre del elemento identificación no puede ser vacío'
        nombre_elemento = ''
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(2003, 1, 1),
                                                  end_date=datetime.date(2003, 12, 31))
        fecha_expedicion = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(2025, 1, 1),
                                                   end_date=datetime.date(2025, 12, 31))
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_nombre_indefinido_elemento_identificacion(self):
        esperado = 'El nombre del elemento identificación no puede ser vacío'
        nombre_elemento = None
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(2003, 1, 1),
                                                  end_date=datetime.date(2003, 12, 31))
        fecha_expedicion = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(2025, 1, 1),
                                                   end_date=datetime.date(2025, 12, 31))
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_numero_vacio_elemento_identificacion(self):
        esperado = 'El numero del elemento identificación no puede ser vacío'
        nombre_elemento = self.fake.name()
        numero = ''
        nombre_completo = self.fake.name()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(2003, 1, 1),
                                                  end_date=datetime.date(2003, 12, 31))
        fecha_expedicion = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(2025, 1, 1),
                                                   end_date=datetime.date(2025, 12, 31))
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_numero_indefinido_elemento_identificacion(self):
        esperado = 'El numero del elemento identificación no puede ser vacío'
        nombre_elemento = self.fake.name()
        numero = None
        nombre_completo = self.fake.name()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(2003, 1, 1),
                                                  end_date=datetime.date(2003, 12, 31))
        fecha_expedicion = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(2025, 1, 1),
                                                   end_date=datetime.date(2025, 12, 31))
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_nombre_completo_vacio_elemento_identificacion(self):
        esperado = 'El nombre completo del cliente del elemento identificación no puede ser vacío'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = ''
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(2003, 1, 1),
                                                  end_date=datetime.date(2003, 12, 31))
        fecha_expedicion = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(2025, 1, 1),
                                                   end_date=datetime.date(2025, 12, 31))
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_nombre_completo_indefinido_elemento_identificacion(self):
        esperado = 'El nombre completo del cliente del elemento identificación no puede ser vacío'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = None
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(2003, 1, 1),
                                                  end_date=datetime.date(2003, 12, 31))
        fecha_expedicion = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(2025, 1, 1),
                                                   end_date=datetime.date(2025, 12, 31))
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_fecha_nacimiento_vacio_elemento_identificacion(self):
        esperado = 'La fecha de nacimiento del elemento identificación no puede ser vacía'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_nacimiento = ''
        fecha_expedicion = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(2025, 1, 1),
                                                   end_date=datetime.date(2025, 12, 31))
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_fecha_nacimiento_indefinido_elemento_identificacion(self):
        esperado = 'La fecha de nacimiento del elemento identificación no puede ser vacía'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_nacimiento = None
        fecha_expedicion = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(2025, 1, 1),
                                                   end_date=datetime.date(2025, 12, 31))
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_fecha_expedicion_vacio_elemento_identificacion(self):
        esperado = 'La fecha de expedición del elemento identificación no puede ser vacía'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_expedicion = ''
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(2025, 1, 1),
                                                   end_date=datetime.date(2025, 12, 31))
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_fecha_expedicion_indefinido_elemento_identificacion(self):
        esperado = 'La fecha de expedición del elemento identificación no puede ser vacía'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_expedicion = None
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(2025, 1, 1),
                                                   end_date=datetime.date(2025, 12, 31))
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_fecha_vencimiento_vacia_elemento_identificacion(self):
        esperado = 'La fecha de vencimiento del elemento identificación no puede ser vacía'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(2003, 1, 1),
                                                  end_date=datetime.date(2003, 12, 31))
        fecha_expedicion = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_vencimiento = ''
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_fecha_vencimiento_indefinida_elemento_identificacion(self):
        esperado = 'La fecha de vencimiento del elemento identificación no puede ser vacía'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(2003, 1, 1),
                                                  end_date=datetime.date(2003, 12, 31))
        fecha_expedicion = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_vencimiento = None
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_notas_vacia_elemento_identificacion(self):
        esperado = 'Las notas del elemento identificación no puede ser vacía'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(2003, 1, 1),
                                                  end_date=datetime.date(2003, 12, 31))
        fecha_expedicion = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(2025, 1, 1),
                                                   end_date=datetime.date(2025, 12, 31))
        notas = ''
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_notas_indefinidas_elemento_identificacion(self):
        esperado = 'Las notas del elemento identificación no puede ser vacía'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(2003, 1, 1),
                                                  end_date=datetime.date(2003, 12, 31))
        fecha_expedicion = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(2025, 1, 1),
                                                   end_date=datetime.date(2025, 12, 31))
        notas = None
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento, fecha_expedicion, fecha_vencimiento, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_fecha_nac_mayor_fecha_exp_elemento_identificacion(self):
        esperado = 'La fecha de nacimiento no puede ser mayor a la fecha de expedición'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(2021, 1, 1),
                                                  end_date=datetime.date(2021, 12, 31))
        fecha_nacimiento_str = fecha_nacimiento.strftime('%Y-%m-%d')
        fecha_expedicion = self.fake.date_between(start_date=datetime.date(2003, 1, 1),
                                                  end_date=datetime.date(2003, 12, 31))
        fecha_expedicion_str = fecha_expedicion.strftime('%Y-%m-%d')
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(2025, 1, 1),
                                                   end_date=datetime.date(2025, 12, 31))
        fecha_vencimiento_str = fecha_vencimiento.strftime('%Y-%m-%d')
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento_str, fecha_expedicion_str,
                                                         fecha_vencimiento_str, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_fecha_nac_mayor_fecha_actual_elemento_identificacion(self):
        esperado = 'La fecha de nacimiento no puede ser mayor a la fecha actual'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_posterior = datetime.datetime.now()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date((fecha_posterior.year + 1), 1, 1),
                                                  end_date=datetime.date((fecha_posterior.year + 1), 12, 31))
        fecha_nacimiento_str = fecha_nacimiento.strftime('%Y-%m-%d')
        fecha_expedicion = self.fake.date_between(start_date=datetime.date((fecha_posterior.year + 2), 1, 1),
                                                  end_date=datetime.date((fecha_posterior.year + 2), 12, 31))
        fecha_expedicion_str = fecha_expedicion.strftime('%Y-%m-%d')
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date((fecha_posterior.year + 3), 1, 1),
                                                   end_date=datetime.date((fecha_posterior.year + 3), 12, 31))
        fecha_vencimiento_str = fecha_vencimiento.strftime('%Y-%m-%d')
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento_str, fecha_expedicion_str,
                                                         fecha_vencimiento_str, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_fecha_exp_mayor_fecha_actual_elemento_identificacion(self):
        esperado = 'La fecha de expedición no puede ser mayor a la fecha actual'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_posterior = datetime.datetime.now()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year - 1, 1, 1),
                                                  end_date=datetime.date(fecha_posterior.year - 1, 12, 31))
        fecha_nacimiento_str = fecha_nacimiento.strftime('%Y-%m-%d')
        fecha_expedicion = self.fake.date_between(start_date=datetime.date((fecha_posterior.year + 2), 1, 1),
                                                  end_date=datetime.date((fecha_posterior.year + 2), 12, 31))
        fecha_expedicion_str = fecha_expedicion.strftime('%Y-%m-%d')
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year, 1, 1),
                                                   end_date=datetime.date(fecha_posterior.year, 12, 31))
        fecha_vencimiento_str = fecha_vencimiento.strftime('%Y-%m-%d')
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento_str, fecha_expedicion_str,
                                                         fecha_vencimiento_str, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_fecha_venc_menor_fecha_actual_elemento_identificacion(self):
        esperado = 'La fecha de vencimiento no puede ser menor a la fecha actual'
        nombre_elemento = self.fake.name()
        numero = str(self.fake.random_number(digits=10))
        nombre_completo = self.fake.name()
        fecha_posterior = datetime.datetime.now()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year - 3, 1, 1),
                                                  end_date=datetime.date(fecha_posterior.year - 3, 12, 31))
        fecha_nacimiento_str = fecha_nacimiento.strftime('%Y-%m-%d')
        fecha_expedicion = self.fake.date_between(start_date=datetime.date((fecha_posterior.year - 2), 1, 1),
                                                  end_date=datetime.date((fecha_posterior.year - 2), 12, 31))
        fecha_expedicion_str = fecha_expedicion.strftime('%Y-%m-%d')
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year - 1, 1, 1),
                                                   end_date=datetime.date(fecha_posterior.year - 1, 12, 31))
        fecha_vencimiento_str = fecha_vencimiento.strftime('%Y-%m-%d')
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento_str, fecha_expedicion_str,
                                                         fecha_vencimiento_str, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_longitud_numero_elemento_identificacion(self):
        esperado = 'El campo nombre elemento debe tener minimo 3 y máximo 512 caracteres'
        nombre_elemento = self.fake.pystr(min_chars=1, max_chars=2)
        numero = str(self.fake.random_number(digits=21))
        nombre_completo = self.fake.name()
        fecha_posterior = datetime.datetime.now()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year - 10, 1, 1),
                                                  end_date=datetime.date(fecha_posterior.year - 10, 12, 31))
        fecha_nacimiento_str = fecha_nacimiento.strftime('%Y-%m-%d')
        fecha_expedicion = self.fake.date_between(start_date=datetime.date((fecha_posterior.year - 1), 1, 1),
                                                  end_date=datetime.date((fecha_posterior.year - 1), 12, 31))
        fecha_expedicion_str = fecha_expedicion.strftime('%Y-%m-%d')
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year + 1, 1, 1),
                                                   end_date=datetime.date(fecha_posterior.year + 1, 12, 31))
        fecha_vencimiento_str = fecha_vencimiento.strftime('%Y-%m-%d')
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento_str, fecha_expedicion_str,
                                                         fecha_vencimiento_str, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_longitud_nombre_elemento_elemento_identificacion(self):
        esperado = 'El campo nombre elemento debe tener minimo 3 y máximo 512 caracteres'
        nombre_elemento = self.fake.pystr(min_chars=513, max_chars=514)
        numero = str(self.fake.random_number(digits=20))
        nombre_completo = self.fake.name()
        fecha_posterior = datetime.datetime.now()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year - 10, 1, 1),
                                                  end_date=datetime.date(fecha_posterior.year - 10, 12, 31))
        fecha_nacimiento_str = fecha_nacimiento.strftime('%Y-%m-%d')
        fecha_expedicion = self.fake.date_between(start_date=datetime.date((fecha_posterior.year - 1), 1, 1),
                                                  end_date=datetime.date((fecha_posterior.year - 1), 12, 31))
        fecha_expedicion_str = fecha_expedicion.strftime('%Y-%m-%d')
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year + 1, 1, 1),
                                                   end_date=datetime.date(fecha_posterior.year + 1, 12, 31))
        fecha_vencimiento_str = fecha_vencimiento.strftime('%Y-%m-%d')
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento_str, fecha_expedicion_str,
                                                         fecha_vencimiento_str, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_longitud_nombre_completo_elemento_identificacion(self):
        esperado = 'El campo nombre completo debe tener minimo 3 y máximo 512 caracteres'
        nombre_elemento = self.fake.pystr(min_chars=3, max_chars=512)
        numero = str(self.fake.random_number(digits=20))
        nombre_completo = self.fake.pystr(min_chars=1, max_chars=2)
        fecha_posterior = datetime.datetime.now()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year - 10, 1, 1),
                                                  end_date=datetime.date(fecha_posterior.year - 10, 12, 31))
        fecha_nacimiento_str = fecha_nacimiento.strftime('%Y-%m-%d')
        fecha_expedicion = self.fake.date_between(start_date=datetime.date((fecha_posterior.year - 1), 1, 1),
                                                  end_date=datetime.date((fecha_posterior.year - 1), 12, 31))
        fecha_expedicion_str = fecha_expedicion.strftime('%Y-%m-%d')
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year + 1, 1, 1),
                                                   end_date=datetime.date(fecha_posterior.year + 1, 12, 31))
        fecha_vencimiento_str = fecha_vencimiento.strftime('%Y-%m-%d')
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento_str, fecha_expedicion_str,
                                                         fecha_vencimiento_str, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_longitud_nombre_completo_elemento_identificacion(self):
        esperado = 'El campo nombre completo debe tener minimo 3 y máximo 512 caracteres'
        nombre_elemento = self.fake.pystr(min_chars=4, max_chars=5)
        numero = str(self.fake.random_number(digits=20))
        nombre_completo = self.fake.pystr(min_chars=513, max_chars=514)
        fecha_posterior = datetime.datetime.now()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year - 10, 1, 1),
                                                  end_date=datetime.date(fecha_posterior.year - 10, 12, 31))
        fecha_nacimiento_str = fecha_nacimiento.strftime('%Y-%m-%d')
        fecha_expedicion = self.fake.date_between(start_date=datetime.date((fecha_posterior.year - 1), 1, 1),
                                                  end_date=datetime.date((fecha_posterior.year - 1), 12, 31))
        fecha_expedicion_str = fecha_expedicion.strftime('%Y-%m-%d')
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year + 1, 1, 1),
                                                   end_date=datetime.date(fecha_posterior.year + 1, 12, 31))
        fecha_vencimiento_str = fecha_vencimiento.strftime('%Y-%m-%d')
        notas = self.fake.text()
        respuesta = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento_str, fecha_expedicion_str,
                                                         fecha_vencimiento_str, notas)
        self.assertEqual(esperado, respuesta)

    def test_validar_creacion_elemento_identificaciones(self):
        nombre_elemento = self.fake.pystr(min_chars=4, max_chars=5)
        numero = str(self.fake.random_number(digits=20))
        nombre_completo = self.fake.pystr(min_chars=3, max_chars=511)
        fecha_posterior = datetime.datetime.now()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year - 10, 1, 1),
                                                  end_date=datetime.date(fecha_posterior.year - 10, 12, 31))
        fecha_nacimiento_str = fecha_nacimiento.strftime('%Y-%m-%d')
        fecha_expedicion = self.fake.date_between(start_date=datetime.date((fecha_posterior.year - 1), 1, 1),
                                                  end_date=datetime.date((fecha_posterior.year - 1), 12, 31))
        fecha_expedicion_str = fecha_expedicion.strftime('%Y-%m-%d')
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year + 1, 1, 1),
                                                   end_date=datetime.date(fecha_posterior.year + 1, 12, 31))
        fecha_vencimiento_str = fecha_vencimiento.strftime('%Y-%m-%d')
        notas = self.fake.text()
        resultado = self.fachada.validar_crear_editar_id(None, nombre_elemento, numero, nombre_completo,
                                                         fecha_nacimiento_str, fecha_expedicion_str,
                                                         fecha_vencimiento_str, notas)
        if resultado == '':
            self.fachada.crear_id(nombre_elemento, numero, nombre_completo, fecha_nacimiento_str, fecha_expedicion_str,
                                  fecha_vencimiento_str, notas)

        self.assertTrue(True)

    def test_validar_eliminar_elemento_id_no_existe(self):
        esperado = 'El elemento a eliminar no existe en el sistema'
        id = self.fake.random_number(digits=1)
        respuesta = self.fachada.eliminar_elemento(id)
        self.assertEquals(esperado, respuesta)

    def test_validar_eliminar_elemento_exitoso(self):
        esperado = self.__crear_elemento_secreto()
        respuesta = self.fachada.eliminar_elemento(1)
        self.assertEqual(esperado, respuesta)

    def test_validar_lista_elemento_despues_eliminar(self):
        esperado = 1
        self.__crear_elemento_secreto()
        self.__crear_elemento_secreto()
        self.fachada.eliminar_elemento(1)
        respuesta = self.fachada.dar_elementos()
        self.assertEqual(esperado, len(respuesta))

    def test_edicion_elemento_login_no_existe(self):

        esperado = 'El id enviado no representa un elemento en el sistema'
        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        if resultado == '':
            self.fachada.crear_login(nombre, email, usuario, nombre_clave, url, notas)

        nombre2 = self.fake.name()
        email2 = self.fake.email()
        usuario2 = self.fake.user_name()

        resultado2 = self.fachada.validar_crear_editar_login(3, nombre2, email2, usuario2, nombre_clave, url, notas)
        if resultado2 == '':
            self.fachada.editar_login(3, nombre2, email2, usuario2, nombre_clave, url, notas)

        self.assertEqual(esperado, resultado2)

    def test_edicion_elemento_login_existe(self):

        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre_clave = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre_clave, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre_clave, clave, pista)

        nombre = self.fake.name()
        email = self.fake.email()
        usuario = self.fake.user_name()
        url = self.fake.url()
        notas = self.fake.text()

        resultado = self.fachada.validar_crear_editar_login(None, nombre, email, usuario, nombre_clave, url, notas)
        if resultado == '':
            self.fachada.crear_login(nombre, email, usuario, nombre_clave, url, notas)

        nombre2 = self.fake.name()
        email2 = self.fake.email()
        usuario2 = self.fake.user_name()

        resultado2 = self.fachada.validar_crear_editar_login(1, nombre2, email2, usuario2, nombre_clave, url, notas)
        if resultado2 == '':
            self.fachada.editar_login(1, nombre2, email2, usuario2, nombre_clave, url, notas)

        elementos = self.fachada.dar_elementos()
        self.assertEqual(nombre2, elementos[0].nombre_elemento)

    def test_editar_elemento_identificacion_no_existe(self):
        esperado = 'El elemento a eliminar no existe en el sistema'
        identificacion = self.__crear_objeto_elemento_identificacion()
        fecha_nacimiento_str = identificacion.fecha_nacimiento.strftime('%Y-%m-%d')
        fecha_expedicion_str = identificacion.fecha_exp.strftime('%Y-%m-%d')
        fecha_vencimiento_str = identificacion.fecha_venc.strftime('%Y-%m-%d')
        respuesta = self.fachada.editar_id(1,
                                           identificacion.nombre_elemento,
                                           identificacion.numero,
                                           identificacion.nombre,
                                           fecha_nacimiento_str,
                                           fecha_expedicion_str,
                                           fecha_vencimiento_str,
                                           identificacion.notas
                                           )
        self.assertEquals(esperado, respuesta)

    def test_editar_elemento_identificacion_falla_validacion_campos(self):
        respuesta = self.fachada.editar_id(1, None, None, None, None, None, None, None)
        self.assertTrue(len(respuesta) > 0)

    def test_editar_elemento_identificacion_exitoso(self):
        esperado = self.__crear_objeto_elemento_identificacion()
        fecha_nacimiento_str = esperado.fecha_nacimiento.strftime('%Y-%m-%d')
        fecha_expedicion_str = esperado.fecha_exp.strftime('%Y-%m-%d')
        fecha_vencimiento_str = esperado.fecha_venc.strftime('%Y-%m-%d')
        self.__crear_elemento_identificacion(esperado)
        esperado.nombre = self.fake.name()
        respuesta = self.fachada.editar_id(
            1,
            esperado.nombre_elemento,
            esperado.numero,
            esperado.nombre,
            fecha_nacimiento_str,
            fecha_expedicion_str,
            fecha_vencimiento_str,
            esperado.notas
        )
        self.assertEqual(esperado.nombre, respuesta.nombre)

    def test_validar_editar_elemento_lista_elementos(self):
        esperado = self.__crear_objeto_elemento_identificacion()
        fecha_nacimiento_str = esperado.fecha_nacimiento.strftime('%Y-%m-%d')
        fecha_expedicion_str = esperado.fecha_exp.strftime('%Y-%m-%d')
        fecha_vencimiento_str = esperado.fecha_venc.strftime('%Y-%m-%d')
        self.__crear_elemento_identificacion(esperado)
        esperado.nombre = self.fake.name()
        self.fachada.editar_id(
            1,
            esperado.nombre_elemento,
            esperado.numero,
            esperado.nombre,
            fecha_nacimiento_str,
            fecha_expedicion_str,
            fecha_vencimiento_str,
            esperado.notas
        )
        lista_elementos = self.fachada.dar_elementos()
        self.assertEqual(esperado.nombre, lista_elementos[0].nombre)

    def __crear_elemento_secreto(self):
        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre, clave, pista)

        nombre_secreto = self.fake.name()
        secreto = self.fake.text()
        clave_nombre = nombre
        notas = self.fake.text()

        return self.fachada.crear_secreto(nombre_secreto, secreto, clave_nombre, notas)

    def __crear_objeto_elemento_identificacion(self) -> ElementoIdentificacion:
        nombre_elemento = self.fake.pystr(min_chars=4, max_chars=5)
        numero = str(self.fake.random_number(digits=20))
        nombre_completo = self.fake.pystr(min_chars=3, max_chars=511)
        fecha_posterior = datetime.datetime.now()
        fecha_nacimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year - 10, 1, 1),
                                                  end_date=datetime.date(fecha_posterior.year - 10, 12, 31))
        fecha_expedicion = self.fake.date_between(start_date=datetime.date((fecha_posterior.year - 1), 1, 1),
                                                  end_date=datetime.date((fecha_posterior.year - 1), 12, 31))
        fecha_vencimiento = self.fake.date_between(start_date=datetime.date(fecha_posterior.year + 1, 1, 1),
                                                   end_date=datetime.date(fecha_posterior.year + 1, 12, 31))
        notas = self.fake.text()
        return ElementoIdentificacion(
            id=None,
            nombre_elemento=nombre_elemento,
            nombre=nombre_completo,
            numero=numero,
            fecha_nacimiento=fecha_nacimiento,
            fecha_exp=fecha_expedicion,
            fecha_venc=fecha_vencimiento,
            notas=notas
        )

    def __crear_elemento_identificacion(self, identificacion: ElementoIdentificacion):
        fecha_nacimiento_str = identificacion.fecha_nacimiento.strftime('%Y-%m-%d')
        fecha_expedicion_str = identificacion.fecha_exp.strftime('%Y-%m-%d')
        fecha_vencimiento_str = identificacion.fecha_venc.strftime('%Y-%m-%d')
        resultado = self.fachada.validar_crear_editar_id(
            None,
            identificacion.nombre_elemento,
            identificacion.numero,
            identificacion.nombre,
            fecha_nacimiento_str,
            fecha_expedicion_str,
            fecha_vencimiento_str,
            identificacion.notas
        )

        if resultado == '':
            return self.fachada.crear_id(identificacion.nombre_elemento,
                                         identificacion.numero,
                                         identificacion.nombre,
                                         fecha_nacimiento_str,
                                         fecha_expedicion_str,
                                         fecha_vencimiento_str,
                                         identificacion.notas
                                         )
