# Sistema de Chat tipo "RAG"

## Descripción general

Este repositorio ya incluye una base funcional en Python para una app de escritorio con interfaz PySide6, persistencia en PostgreSQL y exportacion de conversaciones en JSON y XML.

La aplicacion implementa:

- Login basico por usuario y password.
- Vista principal tipo chat (usuario/sistema).
- Carga de archivos (txt, pdf, json, xml).
- Guardado de conversaciones y mensajes en PostgreSQL.
- Lectura de documentos JSON y XML.
- Exportacion de una conversacion a JSON y XML.

## Estructura del proyecto

```text
proyecto/
├── README.md
├── .gitignore
├── diagrams/
├── docs/
└── src/
```

### `diagrams/`
Carpeta para diagramas del proyecto y de analisis.

```text
diagrams/
├── actividades/
├── casos_uso/
├── clases/
├── componentes/
├── comunicacion/
├── estados/
├── nodos/
└── secuencia/
```

- `actividades/`: flujos de trabajo y procesos.
- `casos_uso/`: actores, objetivos e interacciones del sistema.
- `clases/`: modelo de clases y relaciones entre entidades.
- `componentes/`: division de componentes y dependencias.
- `comunicacion/`: interaccion entre objetos o elementos del sistema.
- `estados/`: estados posibles y transiciones del sistema.
- `nodos/`: distribucion fisica, despliegue o infraestructura.
- `secuencia/`: orden temporal de mensajes y operaciones.

### `docs/`
Carpeta para documentacion formal del proyecto.

```text
docs/
├── SRS/
├── administracion/
├── arquitectura/
├── estimacion/
└── metricas/
```

- `SRS/`: especificacion de requisitos del software.
- `administracion/`: planeacion, seguimiento y materiales de gestion.
- `arquitectura/`: decisiones, vistas y descripcion arquitectonica.
- `estimacion/`: calculos de tiempo, esfuerzo o alcance.
- `metricas/`: indicadores, mediciones y resultados del proyecto.

### `src/`
Carpeta reservada para el codigo fuente y la implementacion del proyecto.

```text
src/
├── main.py
└── chat_rag/
	├── __init__.py
	├── config.py
	├── assets/
	│   └── elementos gráficos...
	├── controllers/
	│   ├── __init__.py
	│   ├── archivo.py
	│   ├── autorizacion.py
	│   ├── chat.py
	│   ├── conversacion.py
	│   ├── manejador_archivo.py
	│   ├── modelo_ia.py
	│   └── usuario.py
	├── db/
	│   ├── __init__.py
	│   ├── connection.py
	│   └── models/
	│       ├── archivo_model.py
	│       ├── conversacion_model.py
	│       ├── mensaje_model.py
	│       ├── model_base.py
	│       └── usuario_model.py
	├── ui/
	│   ├── __init__.py
	│   ├── main_window.py
	│   └── views/
	│       ├── __init__.py
	│       ├── chat_view.py
	│       └── login_view.py
	└── tests/
		└── test_autorizacion.py
```

## Requisitos

- Python 3.11 o superior
- PostgreSQL 14 o superior

Instala dependencias con:

```bash
pip install -r requirements.txt
```

## Configuracion

1. Crea un archivo `.env` en la raiz del proyecto (puedes copiar `.env.example`).
2. Ajusta credenciales de app y conexion a base de datos.

Variables esperadas:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=chat_rag
DB_USER=postgres
DB_PASSWORD=postgres
```

## Preparar PostgreSQL

1. Crea la base de datos (ejemplo):

```sql
CREATE DATABASE chat_rag;
```

2. Ejecuta la app. Las tablas se crean automaticamente al iniciar.

## Ejecucion

Desde la raiz del proyecto:

```bash
python src/main.py
```

## Notas tecnicas

- PostgreSQL: se usa la libreria `psycopg`.
- JSON: se usa el modulo estandar `json` para lectura y escritura.
- XML: se usa el modulo estandar `xml.etree.ElementTree` para lectura y escritura.

## Siguiente paso sugerido

Integrar una API de IA real (si disponen de una gratuita) en `chat_service.py` para reemplazar la respuesta simulada.

## Enlaces a diagramas de los RFs

- **RF-01 – Inicio de sesión**: [Diagrama RF-01 - Inicio de sesión](https://drive.google.com/file/d/1SKOCEcRLtfP-OEyp4_uAb0Jltc6QRiYc/view?usp=sharing)
- **RF-02 – Visualización de conversación**: [Diagrama RF-02 - Visualización de conversación](https://drive.google.com/file/d/1sx8RVY0V05mLj_lU_4GSe92SlhyoklKl/view?usp=sharing)
- **RF-03 – Envío de mensajes**: [Diagrama RF-03 - Envío de mensajes](https://drive.google.com/file/d/1TyAh7FPSdb8rpm5NtIaodfFEdWg4Q6D1/view?usp=sharing)
- **RF-04 – Carga de archivo**: [Diagrama RF-04 - Carga de archivo](https://drive.google.com/file/d/1MmnXDCEEch1MB2cZj0W9nnxxGQFeubW6/view?usp=sharing)
- **RF-05 – Respuesta simulada (modo alternativo)**: [Diagrama RF-05 - Respuesta simulada](https://drive.google.com/file/d/1Dbhku1yzauZEfyPsq6GUT5UaiHnI_Dm_/view?usp=drive_link)
- **RF-06 – Registro de conversaciones**: [Diagrama RF-06 - Registro de conversaciones](https://drive.google.com/file/d/1zX8SOsCdEU1-eWTd9Gbs6hsf7mrwx8DR/view?usp=drive_link)
- **RF-07 – Asociación de archivo**: [Diagrama RF-07 - Asociación de archivo](https://drive.google.com/file/d/1TgYOe2qjp3OMqCtol_DVoxLcN13xwS-Q/view?usp=drive_link)
- **RF-08 – Exportación a JSON o XML**: [Diagrama RF-08 - Exportación](https://drive.google.com/file/d/1opCgBX0q2nF936ZUhOKfy7LLuHOGqfsx/view?usp=drive_link)
