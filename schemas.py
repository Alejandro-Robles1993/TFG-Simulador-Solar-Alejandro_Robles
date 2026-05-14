from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date

# --- USUARIOS ---
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: str

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioOut(UsuarioBase):
    id_usuario: int
    model_config = ConfigDict(from_attributes=True)


# --- CLIENTES ---
class ClienteBase(BaseModel):
    nombre: str
    dni_cif: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    id_usuario: int

class ClienteOut(ClienteBase):
    id_cliente: int
    id_usuario: int
    model_config = ConfigDict(from_attributes=True)


# --- CONSUMO Y CÁLCULOS ---
class ConsumoCreate(BaseModel):
    consumo_anual_kwh: float
    precio_kwh: float

class ConsumoOut(ConsumoCreate):
    id_consumo: int
    model_config = ConfigDict(from_attributes=True)

class SimulacionInput(BaseModel):
    consumo_anual_kwh: float
    precio_kwh: float
    id_cliente: int
    id_usuario: int


# --- PRESUPUESTOS ---
class PresupuestoRead(BaseModel):
    id_presupuesto: int
    fecha: date
    kw_instalados: float
    coste_estimado: float
    ahorro_estimado: float
    tiempo_amortizacion: float
    id_cliente: int
    id_usuario: int
    model_config = ConfigDict(from_attributes=True)