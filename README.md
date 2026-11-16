# Banco de Mediciones Automatizado — Trabajo Final Integrador (TFI)
**Tecnicatura Universitaria en Telecomunicaciones — UTN FRBA**  
**Ciclo lectivo 2026**

## Integrantes del Grupo
* AGUSTIN MAURICIO MEZA

---

## Descripción del Proyecto
Este repositorio contiene el desarrollo del Trabajo Final Integrador de la materia Programación. El sistema implementa un **banco de mediciones automatizado** en Python que se comunica mediante protocolos SCPI a través de sockets TCP con un instrumento virtual de laboratorio, parsea respuestas, valida sintaxis, procesa registros históricos (`mediciones.log`), aplica análisis estadístico y genera un informe integrado completo.

---

## Estructura del Repositorio
El proyecto está dividido en módulos independientes, siguiendo la convención de nombres solicitada por la cátedra:

* `instrumento_virtual.py` — Servidor virtual provisto por la cátedra.
* `mediciones.log` — Archivo de registro histórico de mediciones provisto por la cátedra.
* `01_identificacion.py` — Parseo de cadenas de identificación.
* `02_magnitudes.py` — Conversión numérica y formateo dinámico con prefijos de unidades.
* `03_comandos.py` — Validación de sintaxis de órdenes y consultas SCPI.
* `04_configurar.py` — Generación de comandos de configuración para canales.
* `05_cliente.py` — Cliente de red TCP con sockets.
* `06_barrido.py` — Barrido secuencial de magnitudes por canal.
* `07_verificacion.py` — Verificación teórica del valor RMS con tolerancia relativa.
* `08_log.py` — Análisis, filtrado y lectura del registro de sesión.
* `09_estadistica.py` — Resumen estadístico y control de rangos.
* `10_informe.py` — Armado modular del informe final integrado.
* `bitacora-ia.md` — Registro de interacciones con herramientas de IA según normativa de cátedra.

---

## Instrucciones de Ejecución


1. **Levantar el instrumento virtual:**
   Abrir una terminal en la carpeta del proyecto y ejecutar el servidor virtual. El programa quedará ejecutando en `127.0.0.1`:
   ```bash
   python3 instrumento_virtual.py
   ```

2. **Ejecutar el programa:**
   ```bash
   python3 10_informe.py
   ```
