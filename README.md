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
	├── models.py
	├── db/
	│   ├── __init__.py
	│   ├── connection.py
	│   └── repository.py
	├── services/
	│   ├── __init__.py
	│   ├── chat_service.py
	│   ├── export_service.py
	│   └── file_service.py
	├── ui/
	│   ├── __init__.py
	│   ├── login_dialog.py
	│   └── main_window.py
	└── utils/
		├── __init__.py
		├── json_utils.py
		└── xml_utils.py
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
APP_USERNAME=admin
APP_PASSWORD=admin123
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

Credenciales por defecto (si no cambias `.env`):

- Usuario: `admin`
- Password: `admin123`

## Notas tecnicas

- PostgreSQL: se usa la libreria `psycopg`.
- JSON: se usa el modulo estandar `json` para lectura y escritura.
- XML: se usa el modulo estandar `xml.etree.ElementTree` para lectura y escritura.

## Siguiente paso sugerido

Integrar una API de IA real (si disponen de una gratuita) en `chat_service.py` para reemplazar la respuesta simulada.