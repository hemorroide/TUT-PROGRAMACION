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

* `instrumento_virtual.py` — Servidor virtual provisto por la cátedra (sin modificar).
* `mediciones.log` — Archivo de registro histórico de mediciones provisto por la cátedra.
* `01_identificacion.py` — Parseo de cadenas de identificación (`*IDN?`).
* `02_magnitudes.py` — Conversión numérica y formateo dinámico con prefijos de unidades.
* `03_comandos.py` — Validación de sintaxis de órdenes y consultas SCPI.
* `04_configurar.py` — Generación de comandos de configuración para canales.
* `05_cliente.py` — Cliente de red TCP con sockets (`Instrumento`).
* `06_barrido.py` — Barrido secuencial de magnitudes por canal.
* `07_verificacion.py` — Verificación teórica del valor RMS con tolerancia relativa.
* `08_log.py` — Análisis, filtrado y lectura del registro de sesión.
* `09_estadistica.py` — Resumen estadístico (promedio, desvío muestral $n-1$) y control de rangos.
* `10_informe.py` — Armado modular del informe final integrado.
* `bitacora-ia.md` — Registro de interacciones con herramientas de IA según normativa de cátedra.

---

## Instrucciones de Ejecución

El sistema requiere trabajar con **dos terminales en paralelo** para los ejercicios con conexión de red (ejercicios 5, 6 y 10):

1. **Levantar el instrumento virtual (Terminal 1):**
   Abrir una terminal en la carpeta del proyecto y ejecutar el servidor virtual. El programa quedará ejecutando en `127.0.0.1`:
   ```bash
   python3 instrumento_virtual.py
   ```
   *(Dejar esta terminal abierta en segundo plano; para detenerla luego usar `Ctrl + C`).*

2. **Ejecutar el programa o las pruebas individuales (Terminal 2):**
   Abrir una segunda terminal independiente y ejecutar cualquiera de los scripts. Cada archivo incluye sus propias pruebas automatizadas (`assert`) al final:
   ```bash
   python3 01_identificacion.py
   ```
   Para ejecutar el banco de mediciones completo y generar el informe final:
   ```bash
   python3 10_informe.py
   ```