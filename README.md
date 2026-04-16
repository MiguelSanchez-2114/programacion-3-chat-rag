# programacion-3-chat-rag

## Descripción general

Este proyecto consiste en una aplicación de escritorio desarrollada en Python con una interfaz gráfica tipo chat. La idea es que una persona pueda iniciar sesión, cargar un archivo de datos y hacer preguntas sobre ese contenido desde una conversación visual sencilla.

A nivel técnico, la aplicación se apoya en una capa de interfaz para capturar mensajes, mostrar respuestas y administrar opciones del sistema. También incluye manejo de archivos para reconocer la fuente de información cargada, una base de datos relacional para guardar las conversaciones y un mecanismo de exportación para recuperar esos datos en formatos JSON y XML.

Cuando se use una API de IA, el sistema consultará el modelo para generar respuestas con base en el archivo cargado. Si no hay una API gratuita disponible, la aplicación puede simular ese comportamiento sin romper el flujo principal, manteniendo la lógica de conversación y almacenamiento.

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