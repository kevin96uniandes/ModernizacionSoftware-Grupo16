from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.modelo.Elemento import Elemento
from src.modelo.TipoElemento import TipoElemento


class ElementoLogin(Elemento):    
    __tablename__ = 'elemento_login' 
    id = Column(Integer, ForeignKey('elemento.id'), primary_key = True)
    usuario = Column(String)
    url = Column(String)
    email = Column(String)
    clave_id = Column(Integer, ForeignKey('clave_favorita.id'))
    clave = relationship("ClaveFavorita")


    __mapper_args__ = {
        'polymorphic_identity': TipoElemento.LOGIN.value,
    }
    
    def __getitem__(self, indice):
        if indice == 'nombre_elemento':
            return self.nombre_elemento
        if indice == 'email':
            return self.email
        if indice == 'usuario':
            return self.usuario
        if indice == 'url':
            return self.url
        if indice == 'clave':
            return self.clave
        if indice == 'nombre_elemento':
            return self.nombre_elemento
        if indice == 'tipo':
            return self.tipo
        if indice == 'fecha_creacion':
            return self.fecha_creacion
        if indice == 'notas':
            return self.notas
        raise IndexError("Índice fuera de rango")