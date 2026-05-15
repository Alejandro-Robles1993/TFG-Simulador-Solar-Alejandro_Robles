# SolarEnergy CRM - Simulador Fotovoltaico

Este proyecto es una solución integral diseñada para empresas instaladoras de energía solar, desarrollada como **Proyecto de Fin de Grado (TFG)**. La herramienta permite digitalizar el ciclo de venta, gestionando clientes y generando presupuestos técnicos y económicos de forma automatizada y profesional.

La aplicación se encuentra completamente desplegada y operativa en entorno de producción.

## Funcionalidades Principales

* **Autenticación Segura:** Sistema de acceso para comerciales con protección de credenciales mediante hashing criptográfico (`bcrypt`).
* **Gestión de Cartera (CRM):** Registro completo de clientes potenciales, incluyendo datos de contacto, DNI/CIF y direcciones de obra.
* **Simulador Solar Inteligente:** Motor de cálculo técnico-económico que estima:
    * Potencia fotovoltaica necesaria (kWp).
    * Inversión total estimada del proyecto.
    * Ahorro energético y económico anual.
    * Periodo de retorno de la inversión (Amortización).
* **Historial de Ofertas:** Persistencia y trazabilidad de todos los presupuestos generados y vinculados a cada cliente de forma relacional.
* **Editor de Presupuestos:** Interfaz interactiva que permite ajustar valores y recalcular el estudio en tiempo real.

## Stack Tecnológico e Infraestructura

* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.9+) - Desplegado en **DigitalOcean App Platform**.
* **Frontend:** HTML5, CSS3 ([Bootstrap 5](https://getbootstrap.com/)), JavaScript Moderno (Async/Await & Fetch API).
* **Base de Datos:** [MySQL](https://www.mysql.com/) en entorno *Cloud* gestionado (**DigitalOcean Managed Databases**) a través de SQLAlchemy ORM.
* **Seguridad:** Cifrado de conexiones en tránsito mediante **SSL/TLS** y hashing de contraseñas con Bcrypt.

## Instalación y Uso en Local

Si deseas replicar o ejecutar el proyecto de manera local para desarrollo:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/Alejandro-Robles1993/TFG-Simulador-Solar-Alejandro_Robles.git](https://github.com/Alejandro-Robles1993/TFG-Simulador-Solar-Alejandro_Robles.git)
   cd nombre-del-repo
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

    pip install fastapi uvicorn sqlalchemy bcrypt pymysql cryptography

    ```



4.  **Lanzar el servidor API:**

    ```bash

    uvicorn main:app --reload

    ```



5.  **Acceder a la aplicación:**

    Abre tu navegador web e introduce la dirección local: https://tfg-simulador-solar-4hiul.ondigitalocean.app/
    Para testear de forma aislada los endpoints, puedes acceder a la documentación interactiva en https://tfg-simulador-solar-4hiul.ondigitalocean.app/docs

    Usuario para las pruebas:
    empleado@hotmail.com
    1234

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