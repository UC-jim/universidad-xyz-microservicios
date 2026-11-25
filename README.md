# Sistema de Gestión Universitaria - Arquitectura de Microservicios (PA3)

Sistema desarrollado con Python 3.13, FastAPI, Programación Orientada a Objetos (POO) y MySQL bajo una arquitectura desacoplada de microservicios (`estudiantes-service` y `cursos-service`).

## Estructura del Proyecto
- `database/`: Scripts SQL con creación de esquemas, índices y procedimientos almacenados.
- `estudiantes-service/`: Microservicio independiente para la gestión de estudiantes (Puerto 8001).
- `cursos-service/`: Microservicio independiente para la gestión de cursos (Puerto 8002).

## Ejecución Local
1. Activar entorno virtual e instalar dependencias:
   `pip install -r requirements.txt`
2. Importar `database/db_estudiantes.sql` y `database/db_cursos.sql` en MySQL.
3. Iniciar microservicios:
   - `uvicorn main:app --reload --port 8001` (dentro de `estudiantes-service`)
   - `uvicorn main:app --reload --port 8002` (dentro de `cursos-service`)
4. Ejecutar pruebas automatizadas:
   - `pytest estudiantes-service/test_estudiantes.py -v`
   - `pytest cursos-service/test_cursos.py -v`