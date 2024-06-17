from src.modelo.ClaveFavorita import ClaveFavorita
from src.modelo.declarative_base import Session, engine, Base
from sqlalchemy import desc


class ClaveRepository:

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def crear_clave(self, clave, nombre, pista):
        claveMaestra = ClaveFavorita(clave=clave, nombre=nombre, pista=pista)
        self.session.add(claveMaestra)
        self.session.commit()
        return claveMaestra

    def orderById(element):
        return element.id

    def dar_claves_favoritas(self):
        return self.session.query(ClaveFavorita).order_by(desc(ClaveFavorita.id)).all()

    def editar_clave(self, id, nombre, clave, pista):
        clave_favorita = self.session.query(ClaveFavorita).filter(ClaveFavorita.id == id).first()
        if clave_favorita is not None:
            clave_favorita.nombre = nombre
            clave_favorita.clave = clave
            clave_favorita.pista = pista
            self.session.add(clave_favorita)
            self.session.commit()
        return clave_favorita

    def dar_clave_por_id(self, id):
        return self.session.query(ClaveFavorita).filter(ClaveFavorita.id == id).first()
    
    def eliminar_clave(self, clave):
        self.session.delete(clave)
        self.session.commit()

    def dar_clave_por_nombre(self, nombre):
        return self.session.query(ClaveFavorita).filter(ClaveFavorita.nombre == nombre).first()