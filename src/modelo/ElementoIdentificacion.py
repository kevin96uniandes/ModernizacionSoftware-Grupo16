from sqlalchemy import Column, Integer, String, Date, ForeignKey

from src.modelo.Elemento import Elemento
from src.modelo.TipoElemento import TipoElemento



class ElementoIdentificacion(Elemento):    
    __tablename__ = 'elemento_Identificacion'
    id = Column(Integer, ForeignKey('elemento.id'), primary_key = True)
    nombre = Column(String)
    numero = Column(String)
    fecha_nacimiento = Column(Date)
    fecha_exp = Column(Date)
    fecha_venc = Column(Date)

    __mapper_args__ = {
        'polymorphic_identity': TipoElemento.IDENTIFICACION.value,
    }
    
     
    def __getitem__(self, indice):
        if indice == 'nombre':
            return self.nomnbre
        if indice == 'usuario':
            return self.usuario
        if indice == 'numero':
            return self.numero
        if indice == 'fecha_nacimiento':
            return self.fecha_nacimiento
        if indice == 'fecha_venc':
            return self.fecha_venc
        if indice == 'fecha_exp':
            return self.fecha_exp
        if indice == 'nombre_elemento':
            return self.nombre_elemento
        if indice == 'tipo':
            return self.tipo
        if indice == 'fecha_creacion':
            return self.fecha_creacion
        if indice == 'notas':
            return self.notas
        raise IndexError("Índice fuera de rango")