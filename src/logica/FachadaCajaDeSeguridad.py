import re
import string
import random
from dateutil.relativedelta import relativedelta
from sqlalchemy.exc import IntegrityError
from urllib.parse import urlparse
from datetime import datetime

from src.repositorios import ClaveRepositorio, ElementoRepositorio, ClaveMaestraRepositorio
from src.modelo.ClaveFavorita import ClaveFavorita

from src.modelo.TipoElemento import TipoElemento
from src.modelo.ElementoLogin import ElementoLogin
from src.modelo.ElementoSecreto import ElementoSecreto
from src.modelo.ClaveMaestra import ClaveMaestra

'''
Esta clase es la fachada con los métodos a implementar en la lógica
'''


class FachadaCajaDeSeguridad:

    def __init__(self):
        self.claveRepository = ClaveRepositorio.ClaveRepository()
        self.elementoRepository = ElementoRepositorio.ElememtoRepository()
        self.claveMaestraRepository = ClaveMaestraRepositorio.ClaveMaestraRepository()

        try:
            self.claves_favoritas = list()
            self.claves_favoritas = self.dar_claves_favoritas()
            self.elementos = list()
            self.elementos = self.dar_elementos()
        except Exception as e:
            print('Error para obtener los datos', e)

    def dar_elementos(self):
        ''' Retorna la lista de elementos de la caja de seguridad
        Retorna:
            (list): La lista con los dict o los objetos de los elementos
        '''
        return self.elementoRepository.dar_elementos()

    def dar_elemento(self, id_elemento):
        ''' Retorna un elemento de la caja de seguridad
        Parámetros:
            id_elemento (int): El identificador del elemento a retornar
        Retorna:
            (dict): El elemento identificado con id_elemento
        '''        
        elemento = self.elementoRepository.dar_elemento_por_id(id_elemento)
        if elemento is not None:
            if elemento.tipo == TipoElemento.LOGIN.value:
                print(elemento.email)
                print(elemento.clave)
            if elemento.tipo == TipoElemento.IDENTIFICACION.value:
                print(elemento.numero)
            return elemento.__dict__
        else:
            return None

    def dar_claves_favoritas(self):
        ''' Retorna la lita de claves favoritas
        Retorna:
            (list): La lista con los dict o los objetos de las claves favoritas
        '''
        return self.claveRepository.dar_claves_favoritas()

    def dar_clave_favorita(self, id_clave):
        ''' Retorna una clave favoritas
        Parámetros:
            id_clave (int): El identificador de la clave favorita a retornar
        Retorna:
            (dict): La clave favorita identificada con id_clave
        '''
        raise NotImplementedError("Método no implementado")

    def dar_clave(self, nombre_clave):
        ''' Retorna la clave asignada a una clave favorita
        Parámetros:
            nombre_clave (string): El nombre de la clave favorita
        Retorna:
            (string): La clave asignada a la clave favorita del parámetro
        '''
        clave = self.claveRepository.dar_clave_por_nombre(nombre_clave)
        if clave is None:
            return 'La clave favorita a buscar no existe en el sistema'
        return clave.clave

    def eliminar_elemento(self, id):
        ''' Elimina un elemento de la lista de elementos
        Parámetros:
            id (int): El id del elemento a eliminar_clave
        '''
        elemento = self.elementoRepository.eliminar_elemento(id)
        if elemento is None:
            return 'El elemento a eliminar no existe en el sistema'
        return elemento
    def dar_claveMaestra(self):
        ''' Retorna la clave maestra de la caja de seguridad
        Rertorna:
            (string): La clave maestra de la caja de seguridad
        '''
        clave_maestra = self.claveMaestraRepository.dar_clave_maestra()
        if clave_maestra is None:
            clave_maestra = ClaveMaestra(clave='clave')
        return clave_maestra.clave

    def crear_login(self, nombre, email, usuario, password, url, notas):
        ''' Crea un elemento login
        Parámetros:
            nombre (string): El nombre del elemento
            email (string): El email del elemento
            usuario (string): El usuario del login
            password (string): El nombre de clave favorita del elemento
            url (string): El URL del login
            notas (string): Las notas del elemento
        '''
        try:
            elementoLogin = self.elementoRepository.crear_login(nombre, email, usuario, password, url, notas)
            self.elementos.append(elementoLogin)
        except Exception as e:
            raise Exception("Error a la hora de guardar el elemento login en la base de datos ", e)

    def validar_crear_editar_login(self, id, nombre, email, usuario, password, url, notas):
        patron = r'^[\w]+[\.\w-]*@[\w]+[\.\w]+[a-zA-Z]$'
        ''' Valida que un login se pueda crear o editar
        Parámetros:
            nombre (string): El nombre del elemento
            email (string): El email del elemento
            usuario (string): El usuario del login
            password (string): El nombre de clave favorita del elemento
            url (string): El URL del login
            notas (string): Las notas del elemento
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la 
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        if nombre == '' or nombre == None:
            return 'El campo nombre es obligatorio'
        if email == '' or email == None:
            return 'El campo email es obligatorio'
        if re.match(patron, email) == None:
            return 'El campo email debe tener una estructura valida (xxxxx@xxx.com)'
        if usuario == '' or usuario == None:
            return 'El campo usuario debe ser obligatorio'
        if password == '' or password == None:
            return 'El campo password es obligatorio'
        if url == '' or url == None:
            return 'El campo url debe ser obligatorio'
        else:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return 'El campo url debe tener una estructura valida (https://xxxxx.xxx)'
        if notas == '' or notas == None:
            return 'El campo notas es obligatorio'
        if len(notas) < 3:
            return 'El campo notas debe tener minimo 3 caracteres'
        if len(notas) > 512:
            return 'El campo notas debe tener maximo 512 caracteres'
        elemento = self.elementoRepository.dar_elemento_nombre_tipo(nombre, TipoElemento.LOGIN.value)
        if elemento != None:
            if id != None and id != -1:
                if elemento.nombre_elemento != nombre:
                    return 'El elemento ya fue creado en el sistema'
            else:
                return 'El elemento ya fue creado en el sistema'

        if id != None and id != -1:
            if id > len(self.elementos) or id < 0:
                return 'El id enviado no representa un elemento en el sistema'
        return ''

    def editar_login(self, id, nombre, email, usuario, password, url, notas):
        ''' Edita un elemento login
        Parámetros:
            nombre (string): El nombre del elemento
            email (string): El email del elemento
            usuario (string): El usuario del login
            password (string): El nombre de clave favorita del elemento
            url (string): El URL del login
            notas (string): Las notas del elemento
        '''
        self.elementoRepository.editar_login(id, nombre, email, usuario, password, url, notas)

    def crear_id(self, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion, fvencimiento, notas):
        ''' Crea un elemento identificación
        Parámetros:
            nombre_elemento (string): El nombre del elemento
            numero (string): El número del elemento
            nombre_completo (string): El nombre completo de la persona en la identificación
            fnacimiento (string): La fecha de nacimiento de la persona en la identificación
            fexpedicion (string): La fecha de expedición en la identificación
            fvencimiento (string): La feha de vencimiento en la identificación
            notas (string): Las notas del elemento
        '''
        elemIdentificacion = self.elementoRepository.crear_identificacion(nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion, fvencimiento, notas)
        self.elementos.append(elemIdentificacion)

    def validar_crear_editar_id(self, id, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion,
                                fvencimiento, notas):
        ''' Valida que una identificación se pueda crear o editar
        Parámetros:
            nombre_elemento (string): El nombre del elemento
            numero (string): El número del elemento
            nombre_completo (string): El nombre completo de la persona en la identificación
            fnacimiento (string): La fecha de nacimiento de la persona en la identificación
            fexpedicion (string): La fecha de expedición en la identificación
            fvencimiento (string): La feha de vencimiento en la identificación
            notas (string): Las notas del elemento
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la 
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        if nombre_elemento == '' or nombre_elemento is None:
            return 'El nombre del elemento identificación no puede ser vacío'
        if len(nombre_elemento) < 3 or len(nombre_elemento) > 512:
            return 'El campo nombre elemento debe tener minimo 3 y máximo 512 caracteres'
        if numero == '' or numero is None:
            return 'El numero del elemento identificación no puede ser vacío'
        if nombre_completo == '' or nombre_completo is None:
            return 'El nombre completo del cliente del elemento identificación no puede ser vacío'
        if len(nombre_completo) < 3 or len(nombre_completo) > 512:
            return 'El campo nombre completo debe tener minimo 3 y máximo 512 caracteres'
        if fnacimiento == '' or fnacimiento is None:
            return 'La fecha de nacimiento del elemento identificación no puede ser vacía'
        if fexpedicion == '' or fexpedicion is None:
            return 'La fecha de expedición del elemento identificación no puede ser vacía'
        if fvencimiento == '' or fvencimiento is None:
            return 'La fecha de vencimiento del elemento identificación no puede ser vacía'
        if notas == '' or notas is None:
            return 'Las notas del elemento identificación no puede ser vacía'
        if len(numero) > 20:
            return 'El número no puede tener mas de 20 caracteres'
        fecha_expedicion = datetime.strptime(fexpedicion, "%Y-%m-%d")
        fecha_nacimiento = datetime.strptime(fnacimiento, "%Y-%m-%d")
        fecha_vencimiento = datetime.strptime(fvencimiento, "%Y-%m-%d")
        if fecha_nacimiento > fecha_expedicion:
            return 'La fecha de nacimiento no puede ser mayor a la fecha de expedición'
        if fecha_nacimiento > datetime.today():
            return 'La fecha de nacimiento no puede ser mayor a la fecha actual'
        if fecha_expedicion > datetime.today():
            return 'La fecha de expedición no puede ser mayor a la fecha actual'
        if fecha_vencimiento < datetime.today():
            return 'La fecha de vencimiento no puede ser menor a la fecha actual'
        return ''

    def editar_id(self, id, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion, fvencimiento, notas):
        ''' Edita un elemento identificación
        Parámetros:
            nombre_elemento (string): El nombre del elemento
            numero (string): El número del elemento
            nombre_completo (string): El nombre completo de la persona en la identificación
            fnacimiento (string): La fecha de nacimiento de la persona en la identificación
            fexpedicion (string): La fecha de expedición en la identificación
            fvencimiento (string): La feha de vencimiento en la identificación
            notas (string): Las notas del elemento
        '''
        validacion = self.validar_crear_editar_id (None, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion,
                                fvencimiento, notas)
        if len(validacion) == 0:
            identificacion = self.elementoRepository.editar_elemento_identificacion(id, nombre_elemento, numero,
                                                                                    nombre_completo, fnacimiento,
                                                                                    fexpedicion, fvencimiento, notas)
            if identificacion is None:
                return 'El elemento a eliminar no existe en el sistema'
            return identificacion
        return validacion

    def crear_tarjeta(self, nombre_elemento, numero, titular, fvencimiento, ccv, clave, direccion, telefono, notas):
        ''' Crea un elemento tarjeta
        Parámetros:
            nombre_elemento (string): El nombre del elemento
            numero (string): El número del elemento
            titular (string): El nombre del titular de la tarjeta
            fvencimiento (string): La feha de vencimiento en la tarjeta
            ccv (string): El código de seguridad en la tarjeta
            clave (string): El nombre de clave favorita del elemento
            direccion (string): La dirección del titular de la tarjeta
            telefono (string): El número de teléfono del titular de la tarjeta
            notas (string): Las notas del elemento
        '''
        raise NotImplementedError("Método no implementado")

    def validar_crear_editar_tarjeta(self, id, nombre_elemento, numero, titular, fvencimiento, ccv, clave, direccion,
                                     telefono, notas):
        ''' Valida que una tarjeta se pueda crear o editar
        Parámetros:
            nombre_elemento (string): El nombre del elemento
            numero (string): El número del elemento
            titular (string): El nombre del titular de la tarjeta
            fvencimiento (string): La feha de vencimiento en la tarjeta
            ccv (string): El código de seguridad en la tarjeta
            clave (string): El nombre de clave favorita del elemento
            direccion (string): La dirección del titular de la tarjeta
            telefono (string): El número de teléfono del titular de la tarjeta
            notas (string): Las notas del elemento
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la 
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        raise NotImplementedError("Método no implementado")

    def editar_tarjeta(self, id, nombre_elemento, numero, titular, fvencimiento, ccv, clave, direccion, telefono,
                       notas):
        ''' Edita un elemento tarjeta
        Parámetros:
            nombre_elemento (string): El nombre del elemento
            numero (string): El número del elemento
            titular (string): El nombre del titular de la tarjeta
            fvencimiento (string): La feha de vencimiento en la tarjeta
            ccv (string): El código de seguridad en la tarjeta
            clave (string): El nombre de clave favorita del elemento
            direccion (string): La dirección del titular de la tarjeta
            telefono (string): El número de teléfono del titular de la tarjeta
            notas (string): Las notas del elemento
        '''
        raise NotImplementedError("Método no implementado")

    def crear_secreto(self, nombre, secreto, clave, notas):
        ''' Crea un elemento secreto
        Parámetros:
            nombre (string): El nombre del elemento
            secreto (string): El secreto del elemento
            clave (string): El nombre de clave favorita del elemento
            notas (string): Las notas del elemento
        '''
        try:
            elementoSecreto = self.elementoRepository.crear_secreto(nombre, secreto, clave, notas)
            self.elementos.append(elementoSecreto)
            return elementoSecreto
        except Exception as e:
            raise Exception("Error a la hora de guardar el elemento secreto en la base de datos ", e)

    def validar_crear_editar_secreto(self, id, nombre, secreto, clave, notas):
        ''' Valida que se pueda crear o editar un elemento secreto
        Parámetros:
            nombre (string): El nombre del elemento
            secreto (string): El secreto del elemento
            clave (string): El nombre de clave favorita del elemento
            notas (string): Las notas del elemento
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la 
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        raise NotImplementedError("Método no implementado")

    def editar_secreto(self, id, nombre, secreto, clave, notas):
        ''' Edita un elemento secreto
        Parámetros:
            nombre (string): El nombre del elemento
            secreto (string): El secreto del elemento
            clave (string): El nombre de clave favorita del elemento
            notas (string): Las notas del elemento
        '''
        raise NotImplementedError("Método no implementado")

    def crear_clave(self, nombre, clave, pista):
        ''' Crea una clave favorita
        Parámetros:
            nombre (string): El nombre de la clave favorita
            clave (string): El password o clae de la clave favorita
            pista (string): La pista para recordar la clave favorita
        '''
        try:
            clave = self.claveRepository.crear_clave(clave, nombre, pista)
            self.claves_favoritas.append(clave)
        except IntegrityError as e:
            raise IntegrityError("El nombre de la clave ya existe", None, None)
        except Exception as e:
            raise Exception("Error a la hora de guardar la clave en la base de datos ", e)

    def validar_crear_editar_clave(self, nombre, clave, pista):

        ''' Valida que se pueda crear o editar una clave favorita
        Parámetros:
            nombre (string): El nombre de la clave favorita
            clave (string): El password o clae de la clave favorita
            pista (string): La pista para recordar la clave favorita
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la
            validación o una cadena de caracteres vacía si no hay errores.
        '''

        patron = "^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[$@#%&()*.;:,]).+$"
        if nombre == '' or nombre is None:
            return 'El campo nombre es obligatorio'
        if clave == '' or clave is None:
            return 'El campo clave es obligatorio'
        if len(clave) > 255:
            return 'La longitud de la clave sobrepasa los 255 caracteres'
        if (clave.count(' ') >= 1):
            return 'La clave no debe contener espacios en blanco'
        if pista == '' or pista is None:
            return 'El campo pista es obligatorio'
        if len(nombre) > 255:
            return "La longitud del nombre sobrepasa los 255 caracteres"
        if len(pista) > 255:
            return "La longitud de la pista sobrepasa los 255 caracteres"
        if len(clave) < 8:
            return "La longitud de la clave debe ser mayor o igual a 8"
        if re.match(patron, clave) == None:
            return '''
        La clave no cumple con los requisitos de seguridad
        - Debe contener al menos 1 mayúscula
        - Debe contener al menos 1 minúscula
        - Debe contener al menos 1 caractér especial (#?!@$%^&*-)
        - Debe contener mínimo 8 caracteres
        '''
        return ''

    def editar_clave(self, id, nombre, clave, pista):
        ''' Edita una clave favorita
        Parámetros:
            nombre (string): El nombre de la clave favorita
            clave (string): El password o clae de la clave favorita
            pista (string): La pista para recordar la clave favorita
        '''
        try:
            self.claveRepository.editar_clave(id, nombre, clave, pista)
            self.claves_favoritas = self.dar_claves_favoritas()
        except IntegrityError as e:
            raise IntegrityError("Nombre de la clave ya existe en el sistema", None, None)
        except Exception as e:
            raise Exception("Error a la hora de actualizar la clave en la base de datos ", e)

    def generar_clave(self):
        ''' Genera una clave para una clave favorita
        Retorna:
            (string): La clave generada
        '''
        longitud = 4
        simbolos_permitidos = ''.join(random.choice('$%&()*.;:,') for i in range(longitud))
        minusculas = ''.join(random.choice(string.ascii_lowercase) for i in range(longitud))
        mayusculas = ''.join(random.choice(string.ascii_uppercase) for i in range(longitud))
        digitos = ''.join(random.choice(string.digits) for i in range(longitud))
        clave_insegura = list(mayusculas + minusculas + digitos + simbolos_permitidos)

        random.shuffle(clave_insegura)
        clave = ''.join(clave_insegura)
        return clave

    def eliminar_clave(self, id):
        ''' Elimina una clave favorita
        Parámetros:
            id (int): El id de la clave favorita a borrar
        '''
        self.claves_favoritas = self.dar_claves_favoritas()
        clave = self.claves_favoritas[id]
        self.claveRepository.eliminar_clave(clave)
        del self.claves_favoritas[id]


    def dar_reporte_seguridad(self):
        ''' Genera la información para el reporte de seguridad
        Retorna:
            (dict): Un mapa con los valores numéricos para las llaves logins, ids, tarjetas,
            secretos, inseguras, avencer, masdeuna y nivel que conforman el reporte
        '''
        claves = self.claveRepository.dar_claves_favoritas()
        return {
            'inseguras': self.__retornar_cantidad_claves_inseguras(claves),
            'masdeuna': self.__retornar_cantidad_claves_usadas_masdeunavez(claves),
            'logins': len(self.elementoRepository.dar_todos_elementos_por_tipo(TipoElemento.LOGIN.value)),
            'secretos': len(self.elementoRepository.dar_todos_elementos_por_tipo(TipoElemento.SECRETO.value)),
            'tarjetas': len(self.elementoRepository.dar_todos_elementos_por_tipo(TipoElemento.TARJETA.value)),
            'avencer': '',
            'ids': len(
                self.elementoRepository.dar_todos_elementos_por_tipo(TipoElemento.IDENTIFICACION.value)),
            'nivel': self.__retornar_nivel_seguridad(),

        }

    def __retornar_cantidad_claves_inseguras(self, claves_favoritas: list[ClaveFavorita]) -> int:
        inseguras = 0
        for clave in claves_favoritas:
            if self.validar_crear_editar_clave(clave.nombre, clave.clave, clave.pista) != '':
                inseguras += 1
        return inseguras

    def __retornar_cantidad_claves_usadas_masdeunavez(self, claves_favoritas: list[ClaveFavorita]) -> int:
        masdeuna = 0
        for clave in claves_favoritas:
            if (len(clave.elementosLogin) > 1) or (len(clave.elementosSecretos) > 1) or (
                    len(clave.elementosTarjeta) > 1):
                masdeuna += 1
        return masdeuna

    def __retornar_nivel_seguridad(self):
        clavesFavoritas = self.dar_claves_favoritas()

        clavesUsadasReporteR = self.__retornar_cantidad_claves_usadas_reporte(clavesFavoritas)
        clavesSegurasSC = self.__retornar_cantidad_claves_seguras(clavesFavoritas)
        porcentajeElementosV = self.__retornar_proporcion_fechas_lejos_de_vencer()

        return (clavesSegurasSC * 0.5) + (porcentajeElementosV * 0.2) + (clavesUsadasReporteR * 0.3)

    def __retornar_cantidad_claves_usadas_reporte(self, claves_favoritas: list[ClaveFavorita]) -> int:
        porcentaje = 100
        for clave in claves_favoritas:
            if (len(clave.elementosLogin) >= 3) or (len(clave.elementosSecretos) >= 3) or (
                    len(clave.elementosTarjeta) >= 3):
                porcentaje = 0
            elif (len(clave.elementosLogin) > 1) or (len(clave.elementosSecretos) == 1) or (
                    len(clave.elementosTarjeta) > 1):
                porcentaje = 50

        return porcentaje

    def __retornar_cantidad_claves_seguras(self, claves_favoritas: list[ClaveFavorita]) -> int:
        seguras = 0
        for clave in claves_favoritas:
            if self.validar_crear_editar_clave(clave.nombre, clave.clave, clave.pista) == '':
                seguras += 1
        return seguras

    def __retornar_proporcion_fechas_lejos_de_vencer(self):
        identificaciones = self.elementoRepository.dar_todos_elementos_identificacion()
        tarjetas = self.elementoRepository.dar_todos_elementos_tarjeta()
        elementos_lejos_de_vencer = 0
        fecha_actual = datetime.today()
        for identificacion in identificaciones:
            diferencia_meses = relativedelta(fecha_actual, datetime.combine(identificacion.fecha_venc,
                                                                                     datetime.now().time())).months
            if diferencia_meses > 3:
                elementos_lejos_de_vencer += 1
        for tarjeta in tarjetas:
            diferencia_meses = relativedelta(fecha_actual, datetime.combine(tarjeta.fechaVencimiento,
                                                                                     datetime.now().time())).months
            if diferencia_meses > 3:
                elementos_lejos_de_vencer += 1
        try:
            return ((elementos_lejos_de_vencer * 100) / (len(identificaciones) + len(tarjetas)))
        except ZeroDivisionError as e:
            return 0
