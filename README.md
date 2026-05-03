# Sistema de Chat tipo "RAG"

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

## Enlaces a diagramas de los RFs

- **RF-01 – Inicio de sesión**: [Diagrama RF-01 - Inicio de sesión](https://drive.google.com/file/d/1SKOCEcRLtfP-OEyp4_uAb0Jltc6QRiYc/view?usp=sharing)
- **RF-02 – Visualización de conversación**: [Diagrama RF-02 - Visualización de conversación](https://drive.google.com/file/d/1sx8RVY0V05mLj_lU_4GSe92SlhyoklKl/view?usp=sharing)
- **RF-03 – Envío de mensajes**: [Diagrama RF-03 - Envío de mensajes](https://drive.google.com/file/d/1TyAh7FPSdb8rpm5NtIaodfFEdWg4Q6D1/view?usp=sharing)
- **RF-04 – Carga de archivo**: [Diagrama RF-04 - Carga de archivo](https://drive.google.com/file/d/1MmnXDCEEch1MB2cZj0W9nnxxGQFeubW6/view?usp=sharing)
- **RF-05 – Respuesta simulada (modo alternativo)**: [Diagrama RF-05 - Respuesta simulada](diagrams/estados/RF-05-respuesta_simulada.png)
- **RF-06 – Registro de conversaciones**: [Diagrama RF-06 - Registro de conversaciones](diagrams/clases/RF-06-registro_conversaciones.png)
- **RF-07 – Asociación de archivo**: [Diagrama RF-07 - Asociación de archivo](diagrams/comunicacion/RF-07-asociacion_archivo.png)
- **RF-08 – Exportación a JSON o XML**: [Diagrama RF-08 - Exportación](diagrams/actividades/RF-08-exportacion_json_xml.png)