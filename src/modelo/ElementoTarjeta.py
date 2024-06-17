from sqlalchemy import Column, String, Integer, Date, ForeignKey
from src.modelo.Elemento import Elemento
from sqlalchemy.orm import relationship

from src.modelo.Elemento import Elemento
from src.modelo.TipoElemento import TipoElemento


class ElementoTarjeta(Elemento):    
    __tablename__ = 'elemento_tarjeta' 
    id = Column(Integer, ForeignKey('elemento.id'), primary_key = True)
    numero = Column(String)
    titular = Column(String)
    fechaVencimiento = Column(Date)
    codigoSeguridad = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    clave_id = Column(Integer, ForeignKey('clave_favorita.id'))
    clave = relationship("ClaveFavorita")

    __mapper_args__ = {
        'polymorphic_identity': TipoElemento.TARJETA.value,
    }