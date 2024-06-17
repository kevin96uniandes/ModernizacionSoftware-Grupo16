from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .declarative_base import Base


class ClaveFavorita(Base):    
    __tablename__ = 'clave_favorita'    
    id = Column(Integer, primary_key=True)
    clave = Column(String)
    nombre = Column(String, unique=True)
    pista = Column(String)
    elementosSecretos = relationship("ElementoSecreto")
    elementosLogin = relationship("ElementoLogin")
    elementosTarjeta = relationship("ElementoTarjeta")
    
    def __getitem__(self, indice):
        if indice == 'nombre':
            return self.nombre
        if indice == 'clave':
            return self.clave
        if indice == 'pista':
            return self.pista
        else:
            raise IndexError("Índice fuera de rango")
    