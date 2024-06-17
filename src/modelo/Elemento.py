from sqlalchemy import Column, Integer, String, DateTime, func
from .declarative_base import Base


class Elemento(Base):    
    __tablename__ = 'elemento'    
    id = Column(Integer, primary_key=True)
    nombre_elemento = Column(String)
    tipo = Column(String)
    fecha_creacion = Column(DateTime, default=func.now())
    notas = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'ELEMENTO',
        'polymorphic_on': tipo
    }
    