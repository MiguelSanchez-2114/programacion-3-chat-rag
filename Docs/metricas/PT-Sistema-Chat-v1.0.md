# PLAN DE PRUEBAS
## Sistema de Chat Tipo RAG con Carga de Archivos
## Reponsable: Juan Emmanuel Sánchez Castañón
### Versión 1.0

---

## Hoja Resumen de Modificaciones

| Versión | Fecha | Cambios | Preparado por | Aprobado por |
|---------|-------|---------|---------------|--------------|
| 1.0 | 06/05/2026 | Versión Inicial | Juan Emmanuel Sánchez Castañón | Miguel de Jesus Sánchez Lopez |

---

## Índice

1. [Introducción](#1-introducción)
2. [Alcance de las Pruebas](#2-alcance-de-las-pruebas)
3. [Entorno y Configuración](#3-entorno-y-configuración-de-las-pruebas)
4. [Estrategia de Pruebas](#4-estrategia-de-pruebas)

---

## 1. Introducción

| Proyecto | Tipo de Proyecto |
|----------|-----------------|
| Sistema de Chat Tipo RAG con Carga de Archivos | Proyecto de Ingeniería de Software |

| Documentos relacionados |
|------------------------|
| RF001 – Iniciar de sesión |
| RF002 – Visualizar Conversación |
| RF003 – Enviar mensajes en el chat |
| RF004 – Cargar archivo |
| RF005 – Generar respuesta |
| RF006 – Registrar conversaciones |
| RF007 – Asociar archivo a la conversación |
| RF008 – Exportar chat (exportación) |

### 1.1 Objetivos del Plan de Pruebas

Este documento define la estrategia y las condiciones para llevar a cabo la validación del **Sistema de Chat Tipo RAG con Carga de Archivos**. El objetivo general es verificar el comportamiento del sistema ante condiciones anómalas o excepcionales, garantizando que responda de forma controlada y no genere errores críticos no manejados.
Las pruebas se enfocan exclusivamente en los casos de excepción definidos en cada requerimiento funcional, cubriendo errores de conexión, datos inválidos, errores de formato y fallos en los procesos internos del sistema.

### 1.2 Documentos Relacionados

| Nombre | Descripción |
|--------|-------------|
| TDCU001 drawio. | Requerimiento funcional 1 |
| TDCU002 drawio. | Requerimiento funcional 2 |
| TDCU003 drawio. | Requerimiento funcional 3 |
| TDCU004 drawio. | Requerimiento funcional 4 |
| TDCU005 drawio. | Requerimiento funcional 5 |
| TDCU006 drawio. | Requerimiento funcional 6 |
| TDCU007 drawio. | Requerimiento funcional 7 |
| TDCU008 drawio. | Requerimiento funcional 8 |

---

## 2. Alcance de las Pruebas

### 2.1 Cuadro Resumen de las Pruebas

| Módulos a probar | Tipo de prueba | Responsabilidad |
|-----------------|---------------|-----------------|
| RF001 – Iniciar sesión | Excepción / Negativa | Equipo de QA |
| RF002 – Visualizar Conversación | Excepción / Negativa | Equipo de QA |
| RF003 – Enviar mensajes en el chat | Excepción / Negativa | Equipo de QA |
| RF004 – Carga de archivo | Excepción / Negativa | Equipo de QA |
| RF005 – Generación de respuesta | Excepción / Negativa | Equipo de QA |
| RF006 – Registro de conversaciones | Excepción / Negativa | Equipo de QA |
| RF007 – Asociar archivo a la conversación | Excepción / Negativa | Equipo de QA |
| RF008 – Exportación de conversación | Excepción / Negativa | Equipo de QA |

**Objetivo de las pruebas:** Verificar que ante cada excepción definida en los RF, el sistema detecte el fallo, muestre un mensaje de error apropiado al usuario y mantenga la integridad y la estabilidad de la aplicación.

**Orden de ejecución:** Los módulos se ejecutan de forma secuencial siguiendo la dependencia entre requerimientos: RF001 → RF002 → RF003/RF004 → RF005 → RF006 → RF007 → RF008.

### 2.2 Requerimientos de Pruebas Excluidos

| Nombre | Descripción | Motivo |
|--------|-------------|--------|
| Flujos normales (FNE) | Casos de uso exitosos de cada RF | Fuera del alcance de este PT |
| Alternativas (CA) | Caminos alternativos definidos en cada RF | Fuera del alcance de este PT |
| Pruebas de rendimiento | Carga, estrés y concurrencia | No definidas en los RF actuales |


### 2.3 Casos de Prueba Incluidos

| # Excepciones por RF | RF | Módulo |
|---------------------|-----|--------|
| 2 | RF001 | Iniciar sesión |
| 2 | RF002 | Visualizar Conversación |
| 2 | RF003 | Enviar mensajes en el chat |
| 2 | RF004 | Carga de archivo |
| 2 | RF005 | Generación de respuesta |
| 2 | RF006 | Registro de conversaciones |
| 2 | RF007 | Asociar archivo a la conversación |
| 2 | RF008 | Exportación de conversación |
| **Total** | | **16 casos de excepción** |

### 2.4 Casos de Prueba Excluidos

| # Casos | Tipo | Módulo | Motivo |
|---------|------|--------|--------|
| N/A | Flujo normal | Todos los RF | Fuera del alcance |
| N/A | Alternativas (CA) | Todos los RF | Fuera del alcance |

---

## 3. Entorno y Configuración de las Pruebas

Para el proceso de pruebas se requiere la disponibilidad de los siguientes entornos:

**a. Servidor de Aplicación**
- Conexión con la aplicación del sistema de chat tipo RAG.
- Acceso a base de datos relacional configurada y operativa.
- Conectividad a internet habilitada.

**b. Equipos Cliente (Equipos de Prueba)**
- Aplicación de chat tipo RAG más reciente.
- Acceso a la aplicación chat RAG.
- Sistema operativo: Windows 10/11 o macOS reciente.

**c. Base de Datos de Pruebas**

| Parámetro | Valor |
|-----------|-------|
| Base de Datos | chat_rag_test |
| Servidor BD | aws-1-us-east-2.pooler.supabase.com |
| Datos de prueba | Cargados manualmente por el equipo de QA |

### 3.1 Criterios de Inicio

- **Aceptación del plan de pruebas:** Revisión y aceptación del presente documento por el Arquitecto responsable.
- **Aceptación del entorno:** Verificación de que el entorno de pruebas esté operativo, con acceso a BD y a la aplicación desplegada.
- **Aceptación de datos de prueba:** Validación de que los datos iniciales necesarios (usuarios registrados, conversaciones previas, archivos de prueba) estén disponibles.

### 3.2 Criterios de Aprobación / Rechazo

**Errores Graves:** El sistema no maneja la excepción, produce un crash, corrompe datos en BD, o expone información sensible. → **Rechazo inmediato del módulo afectado.**

**Errores Medios:** El sistema detecta el error pero el mensaje mostrado al usuario es incorrecto, ambiguo o no corresponde al RF. → **Se registra como defecto, requiere corrección.**

**Errores Leves:** El mensaje de error es correcto pero tiene problemas de presentación visual (tipografía, posición). → **Se registra, puede liberarse con corrección en siguiente sprint.**

| Criterio | Descripción |
|----------|-------------|
| Aprobación | 100% de las excepciones ejecutadas, con al menos 90% resueltas sin errores graves. El 10% restante puede contener únicamente errores leves. |
| Rechazo | Cualquier excepción que produzca un error grave pone en rechazo el módulo completo. |

---

## 4. Estrategia de Pruebas

La certificación se realizará en dos etapas:

- **1ra. Etapa:** Validar las excepciones de los módulos de autenticación y visualización (RF001, RF002).
- **2da. Etapa:** Validar las excepciones de los módulos de interacción, carga, generación, registro, asociación y exportación (RF003–RF008).

### 4.1 Catálogo de Casos de Excepción

---

#### RF001 – Iniciar Sesión

**EX001 – Error de conexión a BD**

| Campo | Detalle |
|-------|---------|
| Precondición | La base de datos no está disponible o es inaccesible. |
| Acción del usuario | El usuario ingresa credenciales válidas y presiona "Iniciar sesión". |
| Reacción esperada del sistema | El sistema intenta conectar, detecta el fallo y muestra: *"No se pudo conectar. Intente nuevamente."* El sistema mantiene la ventana de login abierta. |
| Reacción esperada de BD | La BD no responde. No se realiza ninguna validación. |
| Criticidad | Alta |

**EX002 – Campos vacíos o inválidos**

| Campo | Detalle |
|-------|---------|
| Precondición | El sistema está operativo y la BD disponible. |
| Acción del usuario | El usuario deja uno o ambos campos vacíos y presiona "Iniciar sesión". |
| Reacción esperada del sistema | El sistema valida los campos, detecta que están vacíos, resalta los campos con error y muestra: *"Complete todos los campos."* El sistema retorna al formulario para corrección. |
| Reacción esperada de BD | No se realiza ninguna consulta a la BD. |
| Criticidad | Media |

---

#### RF002 – Visualizar Conversación

**EX001 – Error al consultar o conectar con la BD**

| Campo | Detalle |
|-------|---------|
| Precondición | El usuario ha iniciado sesión (RF001). La BD está inaccesible. |
| Acción del usuario | El usuario accede a la interfaz principal y espera la carga de mensajes. |
| Reacción esperada del sistema | El sistema intenta verificar/consultar la BD, detecta timeout o error de conexión y muestra: *"No se pudieron cargar los mensajes."* |
| Reacción esperada de BD | La BD está inaccesible. No retorna ningún dato al sistema. |
| Criticidad | Alta |

**EX002 – Error de formato o renderizado de mensajes**

| Campo | Detalle |
|-------|---------|
| Precondición | El usuario espera ver los mensajes cargados. La BD retorna datos con metadatos corruptos o fechas inconsistentes. |
| Acción del usuario | El usuario espera la actualización de la vista de chat. |
| Reacción esperada del sistema | El sistema recibe los datos pero falla al formatear fechas o dibujar burbujas. Muestra: *"Error al mostrar la conversación."* |
| Reacción esperada de BD | Retorna datos con metadatos corruptos o fechas inconsistentes. |
| Criticidad | Media |

---

#### RF003 – Enviar Mensajes en el Chat

**EX001 – Error al guardar en base de datos**

| Campo | Detalle |
|-------|---------|
| Precondición | El usuario ha iniciado sesión y existe una conversación activa. |
| Acción del usuario | El usuario presiona el botón "Enviar" para enviar un mensaje de texto en la conversación. |
| Reacción esperada del sistema | Ocurre un error en la BD. El sistema muestra mensaje de error al usuario. |
| Criticidad | Alta |

**EX002 – Error en generación de respuesta**

| Campo | Detalle |
|-------|---------|
| Precondición | El usuario ha enviado un mensaje. El sistema intenta generar la respuesta simulada. |
| Acción del usuario | El sistema procesa el mensaje recibido. |
| Reacción esperada del sistema | Ocurre un error en el proceso de generación. El sistema muestra mensaje de error. |
| Criticidad | Alta |


---

#### RF004 – Carga de Archivo

**EX001 – Formato de archivo no válido**

| Campo | Detalle |
|-------|---------|
| Precondición | El usuario ha iniciado sesión y existe una conversación activa. |
| Acción del usuario | El usuario selecciona un archivo con formato no permitido por el sistema. |
| Reacción esperada del sistema | El sistema recibe el archivo, detecta que el formato no es válido, lo rechaza y muestra mensaje de error. |
| Criticidad | Media |

**EX002 – Archivo demasiado grande**

| Campo | Detalle |
|-------|---------|
| Precondición | El usuario selecciona un archivo que excede el tamaño máximo permitido. |
| Acción del usuario | El usuario intenta cargar el archivo. |
| Reacción esperada del sistema | El sistema recibe el archivo, detecta que supera el límite de tamaño, rechaza la carga y muestra mensaje indicando que el archivo es demasiado grande. |
| Criticidad | Media |

---

#### RF005 – Generación de Respuesta

**EX001 – Error al guardar en base de datos**

| Campo | Detalle |
|-------|---------|
| Precondición | El sistema intenta registrar el mensaje o la respuesta generada. |
| Acción del usuario | El sistema procesa la respuesta y la intenta persistir. |
| Reacción esperada del sistema | Ocurre un error en la BD. El sistema muestra mensaje de error. |
| Criticidad | Alta |


**EX002 – Error en la actualización de la interfaz**

| Campo | Detalle |
|-------|---------|
| Precondición | El sistema ha generado una respuesta e intenta mostrar los mensajes en la interfaz. |
| Acción del usuario | El usuario espera ver la respuesta en pantalla. |
| Reacción esperada del sistema | Ocurre un fallo en la actualización. El sistema detecta que no se pueden renderizar los mensajes correctamente, mantiene la información en BD y muestra mensaje de error al usuario intentando recargar la conversación. |
| Criticidad | Media |

---

#### RF006 – Registro de Conversaciones

**EX001 – Error de conexión con la base de datos**

| Campo | Detalle |
|-------|---------|
| Precondición | El sistema intenta guardar la conversación. |
| Acción del usuario | El usuario envía un mensaje y el sistema intenta registrar la interacción. |
| Reacción esperada del sistema | El sistema intenta guardar la conversación, ocurre una falla en la conexión, no se puede registrar la información y se muestra mensaje de error. |
| Criticidad | Alta |

**EX002 – Error en la escritura de datos**

| Campo | Detalle |
|-------|---------|
| Precondición | El sistema envía la conversación a la base de datos. |
| Acción del usuario | El sistema procesa el registro. |
| Reacción esperada del sistema | El sistema envía los datos a la BD, se detecta un fallo, la operación es rechazada y se muestra mensaje de error. |
| Criticidad | Alta |


#### RF007 – Asociar Archivo a la Conversación

**EX001 – Error al registrar la asociación**

| Campo | Detalle |
|-------|---------|
| Precondición | El sistema intenta guardar la relación archivo-conversación en la BD. |
| Acción del usuario | El usuario carga un archivo en una conversación activa. |
| Reacción esperada del sistema | El sistema intenta guardar la relación, ocurre un error en la BD, no se registra la asociación y se muestra mensaje de error. |
| Reacción esperada de BD | Ocurre un error al guardar en la BD. |
| Criticidad | Alta |

**EX002 – Archivo no válido**

| Campo | Detalle |
|-------|---------|
| Precondición | El sistema intenta asociar un archivo no válido o corrupto. |
| Acción del usuario | El usuario intenta cargar el archivo. |
| Reacción esperada del sistema | El sistema intenta asociar el archivo, detecta el fallo, cancela la asociación y muestra mensaje de error. |
| Criticidad | Media |


---

#### RF008 – Exportación de Conversación


**EX002 – Error al generar el archivo**

| Campo | Detalle |
|-------|---------|
| Precondición | El sistema intenta crear el archivo JSON o XML de exportación. |
| Acción del usuario | El sistema procesa la solicitud de exportación. |
| Reacción esperada del sistema | Ocurre un error en la generación del archivo. El sistema detiene la operación y muestra mensaje de error. |
| Criticidad | Alta |

**EX003 – Error al guardar o descargar el archivo**

| Campo | Detalle |
|-------|---------|
| Precondición | El sistema intenta guardar o permitir la descarga del archivo exportado. |
| Acción del usuario | El usuario espera la descarga del archivo. |
| Reacción esperada del sistema | Ocurre un error en el sistema de archivos. El sistema notifica al usuario y permite intentar nuevamente. |
| Criticidad | Media |

---

### 4.2 Orden de Ejecución de Pruebas

**Secuencia de configuración previa:**
1. Verificar disponibilidad del entorno de pruebas (servidor, BD, red).
2. Cargar datos de prueba: usuarios registrados, archivos de prueba (válidos, inválidos, oversized), conversaciones previas en BD.
3. Preparar escenarios de fallo: simular BD inaccesible, simular errores de escritura, preparar archivos con formatos no permitidos.

**Secuencia de ejecución:**
1. Ejecutar excepciones de RF001 (prerequisito para todos los demás módulos).
2. Ejecutar excepciones de RF002.
3. Ejecutar excepciones de RF003 y RF004 (pueden ejecutarse en paralelo).
4. Ejecutar excepciones de RF005.
5. Ejecutar excepciones de RF006 y RF007 (pueden ejecutarse en paralelo).
6. Ejecutar excepciones de RF008.

### 4.3 Equipo de Pruebas y Responsabilidades

| Nombre | Rol | Responsabilidad |
|--------|-----|-----------------|
| Miguel de Jesus Sánchez Lopez| Arquitecto de Producto | Evaluar condiciones de término del proceso de pruebas. |
| Andrea Jacqueline Soriano Romo | Analista Funcional | Resolución de incidencias de certificación en todos los módulos RF001–RF008. |
| Juan Emmanuel Sánchez Castañón| Equipo de Testing | Generación y ejecución del plan de pruebas. Registro de defectos encontrados. |
| Omar Krishnamurti Villavicencio Garcia| Equipo Mantenimiento |  Análisis técnico y corrección de defectos reportados. Soporte técnico ante fallos de infraestructura.|

---

*Documento generado el 06/05/2026 — Versión 1.0*
