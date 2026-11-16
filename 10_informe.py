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
    print("-> ¡Módulos 01 a 09 importados correctamente!")
except Exception as e:
    print(f"-> Error al importar módulos: {e}")


def armar_informe(equipos_idn, series, verificaciones):
    """Genera el texto estructurado del informe final integrado con múltiples equipos."""
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
        for nombre_serie, datos in series.items():
            n = datos.get('n', '-')
            prom = datos.get('promedio', datos.get('prom', '-'))
            minimo = datos.get('minimo', datos.get('min', '-'))
            maximo = datos.get('maximo', datos.get('max', '-'))
            if isinstance(prom, float): prom = round(prom, 4)
            if isinstance(minimo, float): minimo = round(minimo, 4)
            if isinstance(maximo, float): maximo = round(maximo, 4)
            lineas.append(f" - {nombre_serie}: n={n}, Promedio={prom}, Mín={minimo}, Máx={maximo}")
    else:
        lineas.append(" - Sin datos procesados")
        
    lineas.append("-" * 40)
    lineas.append("VERIFICACIONES:")
    if isinstance(verificaciones, list) and verificaciones:
        for verif in verificaciones:
            estado = "COINCIDE" if verif.get("coincide") else "NO COINCIDE"
            teorico = verif.get('teorico')
            medido = verif.get('medido')
            if isinstance(teorico, float): teorico = round(teorico, 4)
            if isinstance(medido, float): medido = round(medido, 4)
            lineas.append(f" - Canal {verif.get('canal')}: {estado} (Teórico: {teorico}, Medido: {medido})")
    else:
        lineas.append(" - Sin verificaciones disponibles")
        
    lineas.append("======================================")
    return "\n".join(lineas)


# --- BLOQUE DE EJECUCIÓN PRINCIPAL INTEGRADO ---
if __name__ == "__main__":
    print("=== EJECUCIÓN DEL MÓDULO 10: INFORME MULTI-INSTRUMENTO ===")
    
    # 1. Obtener la identificación de AMBOS instrumentos virtuales por red (Puertos 5555 y 5556)
    equipos_identificados = []
    
    # Consultar Osciloscopio en el puerto 5555
    try:
        inst_osc = mod_05.Instrumento("127.0.0.1", 5555)
        resp_osc = inst_osc.preguntar("*IDN?")
        inst_osc.cerrar()
        if resp_osc:
            datos_idn = mod_01.parsear_idn(resp_osc)
            if datos_idn:
                equipos_identificados.append(f"Osciloscopio (Puerto 5555): {datos_idn['fabricante']}, {datos_idn['modelo']}, Serie: {datos_idn['serie']}, {datos_idn['version']}")
            else:
                equipos_identificados.append(f"Osciloscopio (Puerto 5555): {resp_osc}")
    except Exception as e:
        print(f"-> Aviso: No se pudo conectar al Osciloscopio en el puerto 5555 ({e}).")

    # Consultar Multímetro en el puerto 5556
    try:
        inst_mult = mod_05.Instrumento("127.0.0.1", 5556)
        resp_mult = inst_mult.preguntar("*IDN?")
        inst_mult.cerrar()
        if resp_mult:
            datos_idn = mod_01.parsear_idn(resp_mult)
            if datos_idn:
                equipos_identificados.append(f"Multímetro (Puerto 5556): {datos_idn['fabricante']}, {datos_idn['modelo']}, Serie: {datos_idn['serie']}, {datos_idn['version']}")
            else:
                equipos_identificados.append(f"Multímetro (Puerto 5556): {resp_mult}")
    except Exception as e:
        print(f"-> Aviso: No se pudo conectar al Multímetro en el puerto 5556 ({e}).")

    if not equipos_identificados:
        equipos_identificados = ["Instrumento Virtual por defecto (Sin conexión activa a puertos)"]

    # 2. Localizar el archivo de log
    archivo_log = "mediciones.log"
    if not os.path.exists(archivo_log) and os.path.exists("mediciones.log.txt"):
        archivo_log = "mediciones.log.txt"

    filas_log = []
    series_reales = {}
    verificaciones_reales = []

    if os.path.exists(archivo_log):
        print(f"-> Leyendo y analizando '{archivo_log}' línea por línea...")
        with open(archivo_log, "r", encoding="utf-8") as f:
            for linea in f:
                med, err = mod_08.analizar_linea(linea)
                if med is not None:
                    filas_log.append(med)
        
        if filas_log:
            # Agrupamos los valores por canal y magnitud
            agrupados = {}
            for fila in filas_log:
                clave = f"{fila['canal']} - {fila['magnitud']}"
                if clave not in agrupados:
                    agrupados[clave] = []
                agrupados[clave].append(fila['valor'])
            
            # Calculamos estadísticas con el módulo 09
            pkpk_promedios = {}
            for nombre_serie, valores in agrupados.items():
                resumen_stat = mod_09.resumen(valores)
                if resumen_stat:
                    series_reales[nombre_serie] = resumen_stat
                    if "PKPK" in nombre_serie:
                        canal_key = nombre_serie.split(" - ")[0]
                        pkpk_promedios[canal_key] = resumen_stat['promedio']

            # Generamos verificaciones cruzando los datos teóricos y medidos
            canales_unicos = set(f['canal'] for f in filas_log)
            for canal in sorted(canales_unicos):
                verif_canal = mod_07.verificar_canal(filas_log, canal)
                if verif_canal.get("teorico") is None and canal in pkpk_promedios:
                    vpp_med = pkpk_promedios[canal]
                    teorico_calc = mod_07.vrms_teorico(vpp_med)
                    verif_canal["teorico"] = teorico_calc
                    verif_canal["medido"] = vpp_med / 2.0
                    verif_canal["coincide"] = mod_07.coincide(verif_canal["medido"], teorico_calc)

                verificaciones_reales.append(verif_canal)
        else:
            print("-> El archivo de log no arrojó líneas válidas al ser analizado.")
    else:
        print(f"-> ATENCIÓN: No se encontró el archivo de log en la ruta.")

    # 3. Generar y consolidar el informe final
    informe_final = armar_informe(equipos_identificados, series_reales, verificaciones_reales)

    # 4. Imprimir el resultado completo
    print("\n" + informe_final)
    print("\nEjercicio 10 OK")