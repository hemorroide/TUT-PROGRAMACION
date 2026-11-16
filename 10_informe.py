import importlib
import os

# --- IMPORTACIÓN DINÁMICA DE LOS MÓDULOS 01 AL 09 ---
try:
    mod_01 = importlib.import_module("01_identificacion")
    mod_02 = importlib.import_module("02_magnitudes")
    mod_03 = importlib.import_module("03_comandos")
    mod_04 = importlib.import_module("04_configurar")
    mod_05 = importlib.import_module("05_cliente")
    mod_06 = importlib.import_module("06_barrido")
    mod_07 = importlib.import_module("07_verificacion")
    mod_08 = importlib.import_module("08_log")
    mod_09 = importlib.import_module("09_estadistica")
    
    # Recargamos para evitar problemas de caché si modificaste algún archivo recién
    importlib.reload(mod_01)
    importlib.reload(mod_02)
    importlib.reload(mod_03)
    importlib.reload(mod_04)
    importlib.reload(mod_05)
    importlib.reload(mod_06)
    importlib.reload(mod_07)
    importlib.reload(mod_08)
    importlib.reload(mod_09)
    
    print("-> ¡Módulos 01 a 09 importados y listos correctamente!")
except Exception as e:
    print(f"-> Error al importar módulos: {e}")


def armar_informe(equipos_idn, series, verificaciones):
    """Genera el texto estructurado del informe final integrado."""
    lineas = []
    lineas.append("=== INFORME DE BANCO DE MEDICIONES ===")
    lineas.append("Equipos Identificados:")
    if isinstance(equipos_idn, list):
        for eq in equipos_idn:
            lineas.append(f" - {eq}")
    else:
        lineas.append(f" - {equipos_idn}")
    lineas.append("-" * 40)
    
    lineas.append("RESUMEN DE SERIES:")
    if isinstance(series, dict) and series:
        for clave, valores in sorted(series.items()):
            equipo, canal, magnitud = clave
            datos = mod_09.resumen(valores)
            if datos is None:
                continue

            unidad = "Hz" if magnitud == "FREQ" else "V"
            promedio = mod_02.con_unidad(datos["promedio"], unidad)
            minimo = mod_02.con_unidad(datos["minimo"], unidad)
            maximo = mod_02.con_unidad(datos["maximo"], unidad)

            lineas.append(f" - {equipo} {canal} {magnitud}: n={datos['n']}, Promedio={promedio}, Mín={minimo}, Máx={maximo}")
    else:
        lineas.append(" - Sin datos procesados")
        
    lineas.append("-" * 40)
    lineas.append("VERIFICACIONES:")
    if isinstance(verificaciones, list) and verificaciones:
        for verif in verificaciones:
            estado = "COINCIDE" if verif.get("coincide") else "NO COINCIDE"
            lineas.append(f" - Canal {verif.get('canal')}: {estado}")
    else:
        lineas.append(" - Sin verificaciones disponibles")
        
    lineas.append("======================================")
    return "\n".join(lineas)


# --- BLOQUE DE EJECUCIÓN PRINCIPAL INTEGRADO ---
if __name__ == "__main__":
    print("=== EJECUCIÓN DEL MÓDULO 10: INFORME MULTI-INSTRUMENTO REAL ===")
    
    # 1. Obtener la identificación de AMBOS instrumentos virtuales por red (Puertos 5555 y 5556)
    equipos_identificados = []
    
    inst_osc = None
    try:
        inst_osc = mod_05.Instrumento("127.0.0.1", 5555)
        resp_osc = inst_osc.preguntar("*IDN?")
        if resp_osc:
            datos_idn = mod_01.parsear_idn(resp_osc)
            if datos_idn:
                equipos_identificados.append(f"Osciloscopio (Puerto 5555): {datos_idn['fabricante']} {datos_idn['modelo']}, Serie: {datos_idn['serie']}, Versión: {datos_idn['version']}")
            else:
                equipos_identificados.append(f"Osciloscopio (Puerto 5555): {resp_osc}")
    except Exception as e:
        print(f"-> Aviso: No se pudo conectar al Osciloscopio en el puerto 5555 ({e}).")

    try:
        inst_mult = mod_05.Instrumento("127.0.0.1", 5556)
        resp_mult = inst_mult.preguntar("*IDN?")
        inst_mult.cerrar()
        if resp_mult:
            datos_idn = mod_01.parsear_idn(resp_mult)
            if datos_idn:
                equipos_identificados.append(f"Multímetro (Puerto 5556): {datos_idn['fabricante']} {datos_idn['modelo']}, Serie: {datos_idn['serie']}, Versión: {datos_idn['version']}")
            else:
                equipos_identificados.append(f"Multímetro (Puerto 5556): {resp_mult}")
    except Exception as e:
        print(f"-> Aviso: No se pudo conectar al Multímetro en el puerto 5556 ({e}).")

    if not equipos_identificados:
        equipos_identificados = ["Instrumento Virtual por defecto (Sin conexión activa)"]

    # 2. Realizar el barrido en vivo para las verificaciones
    verificaciones_reales = []
    if inst_osc:
        try:
            mediciones_en_vivo = mod_06.barrer(inst_osc, ["CH1", "CH2"])
            for canal in ("CH1", "CH2"):
                verif = mod_07.verificar_canal(mediciones_en_vivo, canal)
                verificaciones_reales.append(verif)
        except Exception as e:
            print(f"-> Error durante el barrido en vivo: {e}")
        finally:
            inst_osc.cerrar()

    # 3. Localizar y procesar el archivo de log para las estadísticas históricas
    archivo_log = "mediciones.log"
    if not os.path.exists(archivo_log) and os.path.exists("mediciones.log.txt"):
        archivo_log = "mediciones.log.txt"

    series_reales = {}
    rechazadas = []
    if os.path.exists(archivo_log):
        print(f"-> Leyendo y analizando '{archivo_log}'...")
        series_reales, rechazadas = mod_08.leer_log(archivo_log)
    else:
        print(f"-> ATENCIÓN: No se encontró el archivo de log en la ruta.")

    # 4. Generar y consolidar el informe final
    informe_final = armar_informe(equipos_identificados, series_reales, verificaciones_reales)

    # 5. Imprimir el resultado completo
    print("\n" + informe_final)
    print(f"\nLíneas rechazadas del log: {len(rechazadas)}")
    print("\nEjercicio 10 OK")