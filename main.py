from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from datetime import date
import bcrypt

# Importaciones locales
import models
import schemas
import logic
from database import SessionLocal, engine

# Creación de las tablas
models.Base.metadata.create_all(bind=engine)

# ====================== FUNCIÓN PARA CARGAR EMPLEADO INICIAL ======================
def cargar_empleados_iniciales():
    db = SessionLocal()
    try:
        # Buscamos si el empleado ya está registrado para no duplicarlo cada vez que se reinicie el servidor
        empleado = db.query(models.Usuario).filter(models.Usuario.email == "empleado1@tfg.com").first()
        if not empleado:
            # Encriptamos la contraseña "empleado123" usando la misma lógica de tu endpoint
            salt = bcrypt.gensalt()
            password_encriptada = bcrypt.hashpw("empleado123".encode('utf-8'), salt).decode('utf-8')
            
            nuevo_emp = models.Usuario(
                nombre="Carlos Gómez",
                email="empleado1@tfg.com",
                contraseña=password_encriptada, # Manteniendo tu atributo 'contraseña' con Ñ
                rol="empleado"                # Rol exacto según tu memoria
            )
            db.add(nuevo_emp)
            db.commit()
            print("¡Usuario Empleado creado y encriptado con éxito en DigitalOcean!")
    except Exception as e:
        db.rollback()
        print(f"Error al cargar empleados iniciales: {e}")
    finally:
        db.close()

# Ejecutamos la carga del usuario justo aquí, antes de arrancar la API
cargar_empleados_iniciales()


# ====================== FASTAPI APP ======================
app = FastAPI(title="API Simulador Solar TFG")

# Montar archivos estáticos (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Dependencia para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ====================== RUTA PRINCIPAL (Frontend) ======================
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Sirve el archivo index.html cuando entres a la URL principal"""
    try:
        with open("static/index.html", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <h1>Error: No se encontró el archivo static/index.html</h1>
        <p>Verifica que el archivo esté en la carpeta 'static'.</p>
        """


# ====================== ENDPOINTS DE LA API ======================

# --- AUTENTICACIÓN Y USUARIOS ---
@app.post("/usuarios", response_model=schemas.UsuarioOut)
def crear_usuario(usuario_data: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    salt = bcrypt.gensalt()
    password_encriptada = bcrypt.hashpw(usuario_data.password.encode('utf-8'), salt).decode('utf-8')
    
    nuevo_usuario = models.Usuario(
        nombre=usuario_data.nombre, 
        email=usuario_data.email, 
        contraseña=password_encriptada, 
        rol=usuario_data.rol
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@app.post("/login")
def login(datos: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == datos.email).first()
    
    if not usuario or not bcrypt.checkpw(datos.password.encode('utf-8'), usuario.contraseña.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
    return {
        "usuario": {
            "id_usuario": usuario.id_usuario, 
            "nombre": usuario.nombre, 
            "rol": usuario.rol
        }
    }


# --- GESTIÓN DE CLIENTES ---
@app.get("/clientes-detallados")
def listar_clientes(db: Session = Depends(get_db)):
    resultados = db.query(models.Cliente, models.Usuario.nombre).join(
        models.Usuario, models.Cliente.id_usuario == models.Usuario.id_usuario
    ).all()
    
    return [{**c.__dict__, "asignado_a": n} for c, n in resultados]


@app.post("/clientes")
def crear_o_obtener_cliente(c: schemas.ClienteCreate, db: Session = Depends(get_db)):
    existente = db.query(models.Cliente).filter(models.Cliente.dni_cif == c.dni_cif).first()
    if existente: 
        return existente
        
    nuevo = models.Cliente(**c.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@app.delete("/clientes/{id}")
def borrar_cliente(id: int, db: Session = Depends(get_db)):
    db.query(models.Presupuesto).filter(models.Presupuesto.id_cliente == id).delete()
    db.query(models.Cliente).filter(models.Cliente.id_cliente == id).delete()
    db.commit()
    return {"ok": True}


# --- SIMULACIÓN Y PRESUPUESTOS ---
@app.post("/simular-presupuesto")
def simular(datos: schemas.SimulacionInput, db: Session = Depends(get_db)):
    config = db.query(models.Configuracion).first()
    p_inst = config.precio_instalacion if config else 1000.0   # ← Cambiado a 1000
    h_sol = config.horas_sol_media if config else 5.0
    
    res = logic.calcular_presupuesto_solar(datos.consumo_anual_kwh, datos.precio_kwh, h_sol, p_inst)
    
    nuevo_consumo = models.Consumo(consumo_anual_kwh=datos.consumo_anual_kwh, precio_kwh=datos.precio_kwh)
    db.add(nuevo_consumo)
    db.commit()
    db.refresh(nuevo_consumo)

    nuevo_p = models.Presupuesto(
        fecha=date.today(), 
        kw_instalados=res["kw_instalados"], 
        coste_estimado=res["coste_estimado"],
        ahorro_estimado=res["ahorro_estimado"], 
        tiempo_amortizacion=res["tiempo_amortizacion"],
        id_usuario=datos.id_usuario, 
        id_cliente=datos.id_cliente, 
        id_consumo=nuevo_consumo.id_consumo,
        id_configuracion=config.id_configuracion if config else None
    )
    db.add(nuevo_p)
    db.commit()
    return res


@app.get("/presupuestos/cliente/{id}")
def historial_por_cliente(id: int, db: Session = Depends(get_db)):
    return db.query(models.Presupuesto).filter(models.Presupuesto.id_cliente == id).all()


@app.delete("/presupuestos/{id}")
def borrar_presupuesto(id: int, db: Session = Depends(get_db)):
    db.query(models.Presupuesto).filter(models.Presupuesto.id_presupuesto == id).delete()
    db.commit()
    return {"ok": True}


# --- ACTUALIZACIÓN DE PRESUPUESTOS ---
class PresupuestoUpdate(schemas.BaseModel):
    kw_instalados: float
    coste_estimado: float
    ahorro_estimado: float
    tiempo_amortizacion: float


@app.put("/presupuestos/{id_presupuesto}")
def actualizar_presupuesto(id_presupuesto: int, datos: PresupuestoUpdate, db: Session = Depends(get_db)):
    presu = db.query(models.Presupuesto).filter(models.Presupuesto.id_presupuesto == id_presupuesto).first()
    
    if not presu:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    
    presu.kw_instalados = datos.kw_instalados
    presu.coste_estimado = datos.coste_estimado
    presu.ahorro_estimado = datos.ahorro_estimado
    presu.tiempo_amortizacion = datos.tiempo_amortizacion
    
    db.commit()
    db.refresh(presu)
    return {"mensaje": "Presupuesto actualizado correctamente", "id": id_presupuesto}