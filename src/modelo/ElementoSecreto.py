from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.modelo.Elemento import Elemento
from src.modelo.TipoElemento import TipoElemento


class ElementoSecreto(Elemento):    
    __tablename__ = 'elemento_secreto' 
    id = Column(Integer, ForeignKey('elemento.id'), primary_key = True)
    secreto = Column(String)
    clave_id = Column(Integer, ForeignKey('clave_favorita.id'))
    clave = relationship("ClaveFavorita")

    __mapper_args__ = {
        'polymorphic_identity': TipoElemento.SECRETO.value,
    }