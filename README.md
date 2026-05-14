# SolarEnergy CRM - Simulador Fotovoltaico

Este proyecto es una solución integral diseñada para empresas instaladoras de energía solar, desarrollada como **Proyecto de Fin de Grado (TFG)**. La herramienta permite digitalizar el ciclo de venta, gestionando clientes y generando presupuestos técnicos y económicos de forma automatizada y profesional.

## Funcionalidades Principales

* **Autenticación Segura:** Sistema de acceso para comerciales con cifrado de contraseñas mediante la librería `bcrypt`.
* **Gestión de Cartera (CRM):** Registro completo de clientes potenciales, incluyendo datos de contacto, DNI/CIF y direcciones de obra.
* **Simulador Solar Inteligente:** Motor de cálculo técnico-económico que estima:
    * Potencia fotovoltaica necesaria (kWp).
    * Inversión total estimada del proyecto.
    * Ahorro energético y económico anual.
    * Periodo de retorno de la inversión (Amortización).
* **Historial de Ofertas:** Persistencia de todos los presupuestos generados vinculados a cada cliente.
* **Editor de Presupuestos:** Interfaz interactiva que permite ajustar valores y recalcular el estudio en tiempo real.

## Stack Tecnológico

* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.9+)
* **Frontend:** HTML5, CSS3 (Bootstrap 5), JavaScript (Fetch API)
* **Base de Datos:** SQLite gestionado a través de SQLAlchemy ORM
* **Seguridad:** Hashing de credenciales con Bcrypt

## Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/nombre-del-repo.git](https://github.com/tu-usuario/nombre-del-repo.git)
    cd nombre-del-repo
    ```

2.  **Preparar el entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install fastapi uvicorn sqlalchemy bcrypt
    ```

4.  **Lanzar el servidor API:**
    ```bash
    uvicorn main:app --reload
    ```

5.  **Acceder a la aplicación:**
    Abre el archivo `index.html` en cualquier navegador moderno.

## Estructura del Proyecto

* `main.py`: Punto de entrada de la aplicación y definición de rutas REST.
* `models.py`: Estructura de las tablas de la base de datos.
* `schemas.py`: Modelos de validación de datos para la API.
* `logic.py`: Motor de cálculo de la simulación solar.
* `database.py`: Configuración de la conexión SQLAlchemy.
* `index.html`: Interfaz de usuario y lógica del frontend.

---
**Desarrollado por:** Alejandro Argimiro Robles Moya 
**Tutor:** Damian Sulea  
**Grado:** Desarrollo de Aplicaciones Multiplataforma (DAM)