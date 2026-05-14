from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "Usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre     = Column(String(255), nullable=False)
    email      = Column(String(255), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    rol        = Column(String(255), nullable=False)

    # Relaciones
    clientes     = relationship("Cliente", back_populates="usuario_creador")
    presupuestos = relationship("Presupuesto", back_populates="usuario_creador")


class Cliente(Base):
    __tablename__ = "Cliente"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre     = Column(String(255), nullable=False)
    dni_cif    = Column(String(255), unique=True, nullable=False)
    telefono   = Column(String(255))
    email      = Column(String(255))
    direccion  = Column(String(255))
    id_usuario = Column(Integer, ForeignKey("Usuario.id_usuario"), nullable=False)

    # Relaciones
    usuario_creador = relationship("Usuario", back_populates="clientes")
    presupuestos    = relationship("Presupuesto", back_populates="cliente_rel")


class Consumo(Base):
    __tablename__ = "Consumo"

    id_consumo        = Column(Integer, primary_key=True, index=True)
    consumo_anual_kwh = Column(Float, nullable=False)
    precio_kwh        = Column(Float, nullable=False)


class Configuracion(Base):
    __tablename__ = "Configuracion"

    id_configuracion   = Column(Integer, primary_key=True, index=True)
    precio_instalacion = Column(Float, nullable=False)
    horas_sol_media    = Column(Float, nullable=False)


class Presupuesto(Base):
    __tablename__ = "Presupuesto"

    id_presupuesto      = Column(Integer, primary_key=True, index=True)
    fecha               = Column(Date, nullable=False)
    kw_instalados       = Column(Float, nullable=False)
    coste_estimado      = Column(Float, nullable=False)
    ahorro_estimado     = Column(Float, nullable=False)
    tiempo_amortizacion = Column(Float, nullable=False)
    
    # Claves Ajenas (Foreign Keys)
    id_usuario       = Column(Integer, ForeignKey("Usuario.id_usuario"))
    id_cliente       = Column(Integer, ForeignKey("Cliente.id_cliente"))
    id_consumo       = Column(Integer, ForeignKey("Consumo.id_consumo"))
    id_configuracion = Column(Integer, ForeignKey("Configuracion.id_configuracion"))

    # Relaciones
    usuario_creador = relationship("Usuario", back_populates="presupuestos")
    cliente_rel     = relationship("Cliente", back_populates="presupuestos")