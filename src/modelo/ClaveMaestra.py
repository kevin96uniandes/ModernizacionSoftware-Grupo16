from sqlalchemy import Column, Integer, String
from .declarative_base import Base


class ClaveMaestra(Base):
    __tablename__ = 'clave_maestra'
    id = Column(Integer, primary_key=True)
    clave = Column(String)

    def __getitem__(self, indice):
        if indice == 'clave':
            return self.clave
        else:
            raise IndexError("Índice fuera de rango")