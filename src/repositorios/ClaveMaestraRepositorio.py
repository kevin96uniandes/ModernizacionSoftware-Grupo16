from src.modelo.declarative_base import Session, engine, Base
from src.modelo.ClaveMaestra import ClaveMaestra


class ClaveMaestraRepository:

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def dar_clave_maestra(self):
        return self.session.query(ClaveMaestra).first()
    
    def crear_clave_maestra(self, clave):
        clave_maestra = ClaveMaestra(clave=clave)
        self.session.add(clave_maestra)
        self.session.commit()
