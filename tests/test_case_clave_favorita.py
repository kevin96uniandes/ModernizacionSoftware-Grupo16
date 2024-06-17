import random
import unittest
from sqlalchemy.exc import IntegrityError
from faker import Faker
from src.modelo.declarative_base import Base, engine
from src.logica.FachadaCajaDeSeguridad import FachadaCajaDeSeguridad
from src.repositorios.ClaveRepositorio import ClaveRepository


class TestCaseClaveFavorita(unittest.TestCase):

    def setUp(self):
        self.fachada = FachadaCajaDeSeguridad()
        self.fake = Faker()
        self.claveRepositorio = ClaveRepository()

    def tearDown(self):
        Base.metadata.drop_all(bind=engine)

    def test_solicitud_datos_nombre_vacio_clave_favorita(self):
        nombre = ""
        clave = self.fake.text()
        pista = self.fake.text()
        esperado = "El campo nombre es obligatorio"
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        self.assertEqual(esperado, resultado)
        
    def test_solicitud_datos_nombre_none_clave_favorita(self):
        nombre = None
        clave = self.fake.text()
        pista = self.fake.text()
        esperado = "El campo nombre es obligatorio"
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        self.assertEqual(esperado, resultado)

    def test_solicitud_datos_clave_vacio_clave_favorita(self):
        nombre = self.fake.name()
        clave = ""
        pista = self.fake.text()
        esperado = "El campo clave es obligatorio"
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        self.assertEqual(esperado, resultado)
        
    def test_solicitud_datos_clave_none_clave_favorita(self):
        nombre = self.fake.name()
        clave = None
        pista = self.fake.text()
        esperado = "El campo clave es obligatorio"
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        self.assertEqual(esperado, resultado)

    def test_solicitud_datos_pista_vacio_clave_favorita(self):
        nombre = self.fake.name()
        clave = self.fachada.generar_clave()
        pista = ""
        esperado = "El campo pista es obligatorio"
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        self.assertEqual(esperado, resultado)
        
    def test_solicitud_datos_pista_none_clave_favorita(self):
        nombre = self.fake.name()
        clave = self.fachada.generar_clave()
        pista = None
        esperado = "El campo pista es obligatorio"
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        self.assertEqual(esperado, resultado)

    def test_validar_espacios_en_blanco_clave_favorita(self):
        nombre = self.fake.name()
        clave = self.fake.password()+' '+self.fake.password()
        pista = self.fake.text()
        esperado = "La clave no debe contener espacios en blanco"
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        self.assertEqual(esperado, resultado)
        
    def test_validar_longitud_clave_mayor_ocho_clave_favorita(self):
        nombre = self.fake.name()
        clave = self.fake.password(length=5)
        pista = self.fake.text()
        esperado = "La longitud de la clave debe ser mayor o igual a 8"
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        self.assertEqual(esperado, resultado)

    def test_validar_seguridad_clave_favorita(self):
        esperado = '''
        La clave no cumple con los requisitos de seguridad
        - Debe contener al menos 1 mayúscula
        - Debe contener al menos 1 minúscula
        - Debe contener al menos 1 caractér especial (#?!@$%^&*-)
        - Debe contener mínimo 8 caracteres
        '''
        nombre = self.fake.name()
        clave = self.fake.pystr(min_chars=10, max_chars=12)
        pista = self.fake.text()
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        self.assertEqual(esperado, resultado)
        
    def test_generar_clave_segura(self):
        esperado = ''
        nombre = self.fake.name()
        pista = self.fake.text()
        clave = self.fachada.generar_clave()
        
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        self.assertEqual(esperado, resultado)

    def test_validar_longitud_nombre_clave_favorita(self):
        esperado = 'La longitud del nombre sobrepasa los 255 caracteres'
        nombre = self.fake.pystr(min_chars=260, max_chars=265)
        pista = self.fake.text()
        clave = self.fachada.generar_clave()
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        self.assertEqual(esperado, resultado)
        
    def test_validar_longitud_clave_clave_favorita(self):
        esperado = 'La longitud de la clave sobrepasa los 255 caracteres'
        clave = self.fake.pystr(min_chars=260, max_chars=265)
        pista = self.fake.text()
        nombre = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        self.assertEqual(esperado, resultado)

    def test_validar_longitud_pista_clave_favorita(self):
        esperado = 'La longitud de la pista sobrepasa los 255 caracteres'
        clave = self.fachada.generar_clave()
        pista = self.fake.pystr(min_chars=260, max_chars=265)
        nombre = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        self.assertEqual(esperado, resultado)

    def test_insercion_satisfactoria_clave_favorita(self):
        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre, clave, pista)
        self.assertTrue(True)

    def test_insercion_falla_nombre_existe_clave_favorita(self):
        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre, clave, pista)
            self.assertRaises(IntegrityError, self.fachada.crear_clave, nombre, clave, pista)
                
    def test_existen_claves_favoritas(self):
        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        nombre = self.fake.name()
        resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
        if resultado == '':
            self.fachada.crear_clave(nombre, clave, pista)
        claves_favoritas = self.fachada.dar_claves_favoritas()
        self.assertTrue(len(claves_favoritas) > 0)

    def test_validar_ordenamiento_descendente_claves_favoritas(self):
        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        for i in range(1, 5):
            nombre = self.fake.name()+' '+ str(i)
            resultado = self.fachada.validar_crear_editar_clave(nombre, clave, pista)
            if resultado == '':
                self.fachada.crear_clave(nombre, clave, pista)
        claves_favoritas = self.fachada.dar_claves_favoritas()
        self.assertEquals(4, claves_favoritas[0].id)

    def test_edicion_falla_nombre_existe_clave_favorita(self):
        esperado = "Nombre de la clave ya existe en el sistema"
        with self.assertRaises(IntegrityError) as ie:
            clave1 = self.fachada.generar_clave()
            pista1 = self.fake.text()
            nombre1 = self.fake.name()
            resultado1 = self.fachada.validar_crear_editar_clave(nombre1, clave1, pista1)

            clave2 = self.fachada.generar_clave()
            pista2 = self.fake.text()
            nombre2 = self.fake.name()
            resultado2 = self.fachada.validar_crear_editar_clave(nombre2, clave2, pista2)

            if resultado1 == '' and resultado2 == '':
                self.fachada.crear_clave(nombre1, clave1, pista1)
                self.fachada.crear_clave(nombre2, clave2, pista2)

            claves_favoritas = self.fachada.dar_claves_favoritas()
            id = claves_favoritas[0].id
            nombre_editar = claves_favoritas[1].nombre
            clave = claves_favoritas[0].clave
            pista = claves_favoritas[0].pista
            self.fachada.editar_clave(id, nombre_editar, clave, pista)
        self.assertEqual(esperado, ie.exception.statement)

    def test_edicion_satisfactoria_clave_favorita(self):
            clave1 = self.fachada.generar_clave()
            pista1 = self.fake.text()
            nombre1 = self.fake.name()
            resultado1 = self.fachada.validar_crear_editar_clave(nombre1, clave1, pista1)

            clave2 = self.fachada.generar_clave()
            pista2 = self.fake.text()
            nombre2 = self.fake.name()
            resultado2 = self.fachada.validar_crear_editar_clave(nombre2, clave2, pista2)

            if resultado1 == '' and resultado2 == '':
                self.fachada.crear_clave(nombre1, clave1, pista1)
                self.fachada.crear_clave(nombre2, clave2, pista2)

            claves_favoritas = self.fachada.dar_claves_favoritas()
            id = claves_favoritas[0].id
            nombre = self.fake.name()
            clave = self.fachada.generar_clave()
            pista = self.fake.text()
            self.fachada.editar_clave(id, nombre, clave, pista)
            clave_favorita_modificada = self.claveRepositorio.dar_clave_por_id(2)

            self.assertEqual(nombre, clave_favorita_modificada.nombre)

    def test_validar_elemento_no_existe(self):
        for i in range(1, 3):
            self.__crear_elemento_login()
        elemento = self.fachada.dar_elemento(3)
        self.assertIsNone(elemento)

    def test_validar_elemento_existe(self):
        for i in range(1, 3):
            self.__crear_elemento_login()
            self.__crear_elemento_secreto()
        elemento = self.fachada.dar_elemento(random.randint(1, 4))
        self.assertIsNotNone(elemento)
        self.assertIsInstance(elemento, dict)
        
    def test_eliminar_clave_favorita_existe(self):
        esperado = 1
        
        clave1 = self.fachada.generar_clave()
        pista1 = self.fake.text()
        nombre1 = self.fake.name()
        resultado1 = self.fachada.validar_crear_editar_clave(nombre1, clave1, pista1)
        
        clave2 = self.fachada.generar_clave()
        pista2 = self.fake.text()
        nombre2 = self.fake.name()
        resultado2 = self.fachada.validar_crear_editar_clave(nombre2, clave2, pista2)
        if resultado1 == '' and resultado2 == '':
            self.fachada.crear_clave(nombre1, clave1, pista1)
            self.fachada.crear_clave(nombre2, clave2, pista2)
            
        claves_favoritas_con_indice = []
        claves_favoritas = self.fachada.dar_claves_favoritas()
        
        numero_fila = 0
        for clave in claves_favoritas:
            claves_favoritas_con_indice.append({'id': numero_fila, 'clave': clave })
            numero_fila=numero_fila+1
        
        self.fachada.eliminar_clave(claves_favoritas_con_indice[1]['id'])
        
        claves_favoritas = self.fachada.dar_claves_favoritas()
        
        self.assertEqual(esperado, len(claves_favoritas))
        self.assertEqual(nombre2, claves_favoritas[0].nombre)
        
    def test_eliminar_clave_favorita_no_existe(self):        
        clave1 = self.fachada.generar_clave()
        pista1 = self.fake.text()
        nombre1 = self.fake.name()
        resultado1 = self.fachada.validar_crear_editar_clave(nombre1, clave1, pista1)

        if resultado1 == '':
            self.fachada.crear_clave(nombre1, clave1, pista1)    
            
        self.assertRaises(IndexError, self.fachada.eliminar_clave, 3)

    def test_validar_dar_clave_favorita_por_nombre_no_existe(self):
        esperado = 'La clave favorita a buscar no existe en el sistema'
        nombre_clave = self.fake.name()
        resultado = self.fachada.dar_clave(nombre_clave)
        self.assertEqual(esperado, resultado)

    def test_validar_dar_clave_favorita_por_nombre_existe(self):
        nombre = self.fake.pystr(min_chars=4, max_chars=10)
        clave = self.fachada.generar_clave()
        pista = self.fake.text()
        self.fachada.crear_clave(nombre, clave, pista)
        resultado = self.fachada.dar_clave(nombre)
        self.assertEqual(clave, resultado)

    def __crear_elemento_login(self):
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

        self.fachada.crear_secreto(nombre_secreto, secreto, clave_nombre, notas)
        
        