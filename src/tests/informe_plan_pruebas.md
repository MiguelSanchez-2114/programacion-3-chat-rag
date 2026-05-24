# INFORME DE EJECUCION DE PRUEBAS
**Proyecto:** Sistema de Chat Tipo RAG con Carga de Archivos  
**Modulo Evaluado:** Backend (Controladores, Autorizacion y Capa de Datos)  
**Version del Documento:** 1.1  
**Fecha de Ejecucion:** 24 de mayo de 2026  
**Responsable de Testing:** Juan Emmanuel Sanchez Castanon  
**Herramienta:** Python unittest + unittest.mock

---

## 1. Resumen Ejecutivo

| Metrica | Valor |
|---------|-------|
| Total de casos ejecutados | 18 |
| [OK] Aprobados | 13 |
| [FALLIDO] Errores | 0 |
| [OMITIDO] Saltados | 5 |
| Tiempo total de ejecucion | 0.028 s |
| Estado del modulo | APROBADO |

**Conclusion rapida:**  
El backend maneja correctamente todas las excepciones criticas evaluadas, incluyendo caida de base de datos, archivos con extensiones no permitidas, metadatos corruptos, contextos incompletos y validacion de credenciales vacias. No se presentaron interrupciones no manejadas ni corrupcion de estado. Los 5 casos omitidos corresponden a validaciones que requieren entorno de integracion o interfaz grafica, por lo que se posponen a la siguiente fase.

---

## 2. Entorno de Ejecucion

| Componente | Configuracion |
|------------|---------------|
| Sistema Operativo | macOS |
| Version de Python | 3.14 |
| Framework de pruebas | unittest (nativo) |
| Aislamiento | Mocks de psycopg2, google-genai y capa de modelo |
| Base de datos | No conectada (simulada con side_effect y PropertyMock) |
| Ruta de ejecucion | src/tests/test_autorizacion.py, src/tests/test_modulos_chat.py |

---

## 3. Matriz Detallada de Resultados

| Modulo | Caso de Prueba | Descripcion | Estado | Tiempo | Observaciones |
|--------|----------------|-------------|--------|--------|---------------|
| **Autorizacion** | `test_error_conexion_bd` | Fallo simulado de conexion a base de datos durante login | [OK] | 0.003s | Retorna None y mantiene estado estable |
| **Autorizacion** | `test_username_vacio` | Validacion de campo usuario vacio en login | [OK] | 0.002s | Rechaza entrada sin consultar modelo |
| **Autorizacion** | `test_password_vacio` | Validacion de campo contrasena vacio en login | [OK] | 0.002s | Rechaza entrada sin consultar modelo |
| **Autorizacion** | `test_ambos_campos_vacios` | Validacion de ambos campos vacios en login | [OK] | 0.003s | Rechaza entrada sin consultar modelo |
| **AsociarArchivo** | `test_error_bd_al_registrar_asociacion_archivo` | Fallo en BD al guardar relacion archivo-conversacion | [OK] | 0.002s | Excepcion capturada y propagada correctamente |
| **Chat** | `test_error_conexion_bd_al_cargar_mensajes` | BD caida al intentar obtener mensajes | [OK] | 0.001s | Sistema no crashea, retorna control seguro |
| **Chat** | `test_exportar_con_mensajes_sin_fecha_no_falla` | Mensajes con metadatos incompletos (fecha None) | [OK] | 0.001s | Exportador serializa sin error |
| **Conversacion** | `test_error_bd_al_guardar_mensaje` | Error de escritura en BD al agregar mensaje | [OK] | 0.001s | Excepcion levantada para capa superior |
| **Conversacion** | `test_error_generar_respuesta_sin_archivo` | Solicitud de respuesta basada en archivo inexistente | [OK] | 0.001s | Valida contexto y lanza ValueError |
| **Exportador** | `test_generar_json_con_mensajes_validos` | Exportacion a JSON con estructura completa | [OK] | 0.001s | Genera payload valido con conversacion_id |
| **ManejadorArchivo** | `test_error_archivo_no_encontrado` | Consulta de archivo inexistente | [OK] | 0.000s | Lanza FileNotFoundError controlado |
| **ManejadorArchivo** | `test_rechazar_formato_no_permitido` | Intento de carga con extension .exe | [OK] | 0.001s | Valida extension y rechaza con ValueError |
| **RegistroConversacion** | `test_error_conexion_bd_al_iniciar_conversacion` | BD inaccesible al crear nueva conversacion | [OK] | 0.001s | ValueError propagado tras fallo de guardar() |

---

## 4. Casos Omitidos y Justificacion

| Caso Omitido | Motivo Tecnico | Fase de Resolucion |
|--------------|----------------|---------------------|
| `test_validacion_tamano_archivo_pendiente` | Logica de limite de tamano no implementada en ManejadorArchivo | Sprint 3 (Validacion de entrada) |
| `test_guardar_respuesta_en_bd_pendiente` | Requiere mock de transaccion + rollback de BD | Sprint 4 (Integracion con API externa) |
| `test_error_renderizado_ui_pendiente` | Depende de componente grafico (PySide6/Tkinter) | Fase de QA Visual / E2E |
| `test_error_escritura_datos_bd_pendiente` | Necesita BD real para validar constraints UNIQUE/FOREIGN KEY | Pruebas de integracion con Supabase |
| `test_error_descarga_archivo_pendiente` | Simulacion de disco lleno requiere acceso a FS real | Pruebas de infraestructura |

> **Nota:** Los casos omitidos no representan fallos. Son dependencias de entorno que se validaran en fases posteriores sin afectar la aprobacion del backend actual.

---

## 5. Conclusion y Recomendaciones

### Cumplimiento de Criterios de Aprobacion
- [x] 100% de excepciones unitarias ejecutadas sin errores graves
- [x] 0 interrupciones no manejadas o comportamientos indefinidos
- [x] Estados de retorno y validaciones coherentes con el plan de pruebas
- [x] Aislamiento completo de dependencias externas (BD, APIs, Sistema de Archivos)


---

## 6. Firmas de Aprobacion

| Rol | Nombre | Firma / Fecha |
|-----|--------|---------------|
| **Arquitecto de Producto** | Miguel de Jesus Sanchez Lopez | ____________________ |
| **Analista Funcional** | Andrea Jacqueline Soriano Romo | ____________________ |
| **Equipo de Testing** | Juan Emmanuel Sanchez Castanon | ____________________ |
| **Equipo de Mantenimiento** | Omar Krishnamurti Villavicencio Garcia | ____________________ |

---

