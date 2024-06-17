import datetime

from src.modelo.ElementoSecreto import ElementoSecreto
from src.modelo.ElementoTarjeta import ElementoTarjeta
from src.modelo.Elemento import Elemento
from src.modelo.ClaveFavorita import ClaveFavorita
from src.modelo.ElementoLogin import ElementoLogin
from src.modelo.declarative_base import Session, engine, Base
from src.modelo.ElementoIdentificacion import ElementoIdentificacion
from sqlalchemy import desc, Date



class ElememtoRepository:

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def crear_secreto(self, nombre, secreto, clave, notas):
        clave_maestra = self.session.query(ClaveFavorita).filter(ClaveFavorita.nombre == clave).first()
        elemento_secreto = ElementoSecreto(secreto=secreto, clave=clave_maestra, notas=notas, nombre_elemento=nombre)
        self.session.add(elemento_secreto)
        self.session.commit()
        return elemento_secreto

    def dar_elementos(self):
        return self.session.query(Elemento).order_by(desc(Elemento.id)).all()
    
    def dar_elemento_nombre_tipo(self, nombre, tipo):
        return self.session.query(Elemento).filter(Elemento.nombre_elemento == nombre, Elemento.tipo == tipo).first()
    
    def crear_login(self, nombre, email, usuario, password, url, notas):
         
        claveFavorita = self.session.query(ClaveFavorita).filter(ClaveFavorita.nombre == password).limit(1).first()
  
        elementoLogin = ElementoLogin(nombre_elemento = nombre, email = email, usuario = usuario, clave = claveFavorita, url = url, notas = notas)
        self.session.add(elementoLogin)
        self.session.commit()
        
        return elementoLogin

    def dar_todos_elementos_por_tipo(self, tipo):
        return self.session.query(Elemento).filter(Elemento.tipo == tipo).all()

    def dar_todos_elementos_identificacion(self):
        return self.session.query(ElementoIdentificacion).all()

    def dar_todos_elementos_tarjeta(self):
        return self.session.query(ElementoTarjeta).all()

    def dar_elemento_por_id(self, id):
        return self.session.query(Elemento).filter(Elemento.id == id).first()

    def crear_identificacion(self, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion, fvencimiento, notas):
        elemIdentificacion = ElementoIdentificacion(
            nombre_elemento=nombre_elemento,
            nombre=nombre_completo,
            numero=numero,
            fecha_venc=datetime.datetime.strptime(fvencimiento, '%Y-%m-%d').date(),
            fecha_nacimiento=datetime.datetime.strptime(fnacimiento, '%Y-%m-%d').date(),
            fecha_exp=datetime.datetime.strptime(fexpedicion, '%Y-%m-%d').date(),
            notas=notas
        )
        self.session.add(elemIdentificacion)
        self.session.commit()
        return elemIdentificacion
    
    def editar_login(self, id, nombre, email, usuario, password, url, notas):
         
        claveFavorita = self.session.query(ClaveFavorita).filter(ClaveFavorita.nombre == password).limit(1).first()
  
        elementoLogin = self.dar_elemento_por_id(id)
        
        elementoLogin.nombre_elemento= nombre
        elementoLogin.email = email
        elementoLogin.usuario= usuario
        elementoLogin.url=url
        elementoLogin.clave=claveFavorita
        elementoLogin.notas = notas

        self.session.commit()        
        return elementoLogin

    def eliminar_elemento(self, id):
        elemento = self.session.query(Elemento).filter(Elemento.id == id).first()
        if elemento is not None:
            self.session.delete(elemento)
            self.session.commit()
        return elemento

    def editar_elemento_identificacion(self, id, nombre_elemento, numero, nombre_completo, fnacimiento, fexpedicion,
                                       fvencimiento, notas):
        identificacion = self.dar_elemento_por_id(id)
        if identificacion is not None:
            identificacion.nombre_elemento = nombre_elemento
            identificacion.nombre = nombre_completo
            identificacion.numero = numero
            identificacion.fecha_nacimiento = datetime.datetime.strptime(fnacimiento, '%Y-%m-%d').date()
            identificacion.fecha_exp = datetime.datetime.strptime(fexpedicion, '%Y-%m-%d').date()
            identificacion.fecha_venc = datetime.datetime.strptime(fvencimiento, '%Y-%m-%d').date()
            identificacion.notas = notas
            self.session.commit()
        return identificacion
