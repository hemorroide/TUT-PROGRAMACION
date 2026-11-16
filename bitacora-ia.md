# Bitácora de Uso de Inteligencia Artificial — TFI Programación

**Tecnicatura Universitaria en Telecomunicaciones — UTN FRBA**
**Ciclo lectivo 2026**

Este documento registra las consultas realizadas a herramientas de Inteligencia Artificial (Gemini) durante el desarrollo del Trabajo Final Integrador, cumpliendo con las pautas de transparencia y verificación establecidas por la cátedra.

---

## Entrada 1: Estructura general y parseo de identificación (Ejercicios 1 y 2)

* **El prompt:**
  > "me ayudas con un tp de programacion, te lo adjunto"

* **Qué contestó:**
  Explicó el propósito modular del trabajo práctico y entregó la estructura inicial de funciones y pruebas (`assert`) para `parsear_idn` (Ejercicio 1) y las funciones de conversión `a_numero` y `con_unidad` (Ejercicio 2).

* **Qué cambiaste:**
  Separé los bloques de código en sus archivos individuales (`01_identificacion.py` y `02_magnitudes.py`) y ajusté las pruebas para asegurar que contemplaran el caso del quinto campo descartado en el multímetro y el caso borde de redondeo (ej. `999.9999 Hz` a `1 kHz`).

* **Cómo lo verificaste:**
  Ejecuté cada archivo por separado mediante `python3 01_identificacion.py` y `python3 02_magnitudes.py` en la terminal, confirmando que todos los bloques `assert` (incluyendo cadenas vacías y respuestas de error) pasaran sin arrojar `AssertionError`.

---

## Entrada 2: Validación sintáctica y configuración de canales (Ejercicios 3 y 4)

* **El prompt:**
  > "prosigue" (en el contexto de avanzar con la explicación de funciones y bloques `assert` para los ejercicios 3 y 4).

* **Qué contestó:**
  Proporcionó la implementación de `es_consulta` y `validar` para el Ejercicio 3, y `comandos_de_canal` para el Ejercicio 4. Inicialmente, en las pruebas del Ejercicio 4 se llamaba directamente a la función `validar` del Ejercicio 3.

* **Qué cambiaste:**
  Al separar los 10 ejercicios en archivos independientes, surgió un `NameError: name 'validar' is not defined` en `04_configurar.py`. Modifiqué el bloque de pruebas de `04_configurar.py` para hacer una validación local autónoma de formato (verificando el prefijo `:` y la estructura de los comandos generados) sin depender de importaciones externas.

* **Cómo lo verificaste:**
  Ejecuté `python3 03_comandos.py` y `python3 04_configurar.py` de forma independiente. Probé pasar un canal inexistente (`"CH3"`) para confirmar que devolviera `None` y verifiqué que la lista de cuatro órdenes coincidiera carácter por carácter con la consigna.

---

## Entrada 3: Cliente TCP con sockets y barrido simulado (Ejercicios 5 y 6)

* **El prompt:**
  > "cuando y como se enlazaria con el instrumento_virtual" / "segui"

* **Qué contestó:**
  Explicó el funcionamiento cliente-servidor sobre `127.0.0.1` en los puertos `5555` y `5556` utilizando la biblioteca estándar `socket`. Entregó la clase `Instrumento` con sus métodos `enviar`, `preguntar` y `cerrar`, destacando la obligatoriedad del salto de línea (`\n`), y la función `barrer` utilizando inyección de dependencias para las pruebas.

* **Qué cambiaste:**
  Adapté el bloque de pruebas del Ejercicio 5 con manejo de excepciones (`ConnectionRefusedError`) para que avisara de forma clara si el servidor virtual no estaba encendido en otra terminal, y mantuve la clase simulada (`InstrumentoTrucho`) en `06_barrido.py` para testear el barrido sin depender de la red.

* **Cómo lo verificaste:**
  Probé `06_barrido.py` de manera offline comprobando que devolviera los 3 diccionarios esperados por canal. Luego levanté `python3 instrumento_virtual.py` en una terminal y ejecuté `05_cliente.py` en otra, verificando la respuesta `*IDN?` real del osciloscopio virtual.

---

## Entrada 4: Verificación física de Vrms y lectura de logs (Ejercicios 7 y 8)

* **El prompt:**
  > "prosigue, pero aun no he iniciado el instrumento virtual" / "el ejercicio 7 no me sale ok sale el 6 y 8 de los ultimos"

* **Qué contestó:**
  Entregó las funciones `vrms_teorico`, `coincide` y `verificar_canal` para el Ejercicio 7, y `analizar_linea` junto a `leer_log` para el Ejercicio 8. Tras reportar un fallo en la ejecución de las pruebas del Ejercicio 7, detectó un error de sintaxis en la condición de entrada del bloque principal (`if __name__ == "main":` sin guiones bajos).

* **Qué cambiaste:**
  Corregí la cabecera del bloque de pruebas a `if __name__ == "__main__":` en `07_verificacion.py` y verifiqué en `08_log.py` el uso de `linea.split()` sin argumentos para procesar correctamente las líneas separadas por tabulaciones (`\t`) presentes en el archivo de logs de la cátedra.

* **Cómo lo verificaste:**
  Ejecuté `python3 07_verificacion.py` confirmando que la prueba de la onda cuadrada ($V_{pp}=2\text{ V}$, $V_{rms}=1\text{ V}$) devolviera `coincide == False` al compararse contra el modelo senoidal. Además, probé `08_log.py` con el archivo real de mediciones provisto por el profesor, verificando el rechazo de líneas con horas imposibles (`25:61:00`) y valores no numéricos.

---

## Entrada 5: Estadística muestral e informe final (Ejercicios 9 y 10)

* **El prompt:**
  > "avancemos para cerrar la guia completa"

* **Qué contestó:**
  Proporcionó la implementación de `resumen` (calculando el desvío estándar muestral dividiendo por $n-1$) y `fuera_de_rango` para el Ejercicio 9, y la función pura `armar_informe` para el Ejercicio 10.

* **Qué cambiaste:**
  Verifiqué que `armar_informe` en `10_informe.py` no realizara llamadas a `print()` ni abriera archivos internamente, retornando únicamente una cadena de texto formateada para permitir su validación mediante `assert`.

* **Cómo lo verificaste:**
  Corrí `09_estadistica.py` sobre la serie de frecuencias de `CH1` extraída del log de la cátedra, confirmando que el promedio cayera dentro del $0.5\%$ de $1000\text{ Hz}$ y que el desvío estándar fuera menor a $5\text{ Hz}$. Finalmente ejecuté `10_informe.py` comprobando que el texto generado incluyera el encabezado, las series y los estados de verificación.