# Ejercicio 8 - Leer las mediciones que quedaron guardadas

from datetime import datetime
from importlib import import_module

a_numero = import_module("02_magnitudes").a_numero


def analizar_linea(linea):
    linea_str = linea.strip()
    
    # Si está vacía o empieza con '#', se ignora (devuelve None, None)
    if not linea_str or linea_str.startswith("#"):
        return None, None
        
    # split() sin argumentos separa por cualquier espacio en blanco (incluyendo tabs \t)
    campos = linea_str.split()
    
    # Debe tener exactamente 6 campos: [fecha, hora, equipo, canal, magnitud, valor]
    if len(campos) != 6:
        return None, "Cantidad de campos incorrecta"
        
    fecha, hora, equipo, canal, magnitud, val_str = campos
    
    # Validamos hora básica (ej: ver que tenga dos ':' y formato numérico)
    partes_hora = hora.split(":")
    if len(partes_hora) != 3:
        return None, "Formato de hora inválido"
    try:
        hh, mm, ss = int(partes_hora[0]), int(partes_hora[1]), int(partes_hora[2])
        if not (0 <= hh < 24 and 0 <= mm < 60 and 0 <= ss < 60):
            return None, "Hora imposible"
    except ValueError:
        return None, "Hora no numérica"
        
    # Validar canal y magnitud (incluyendo variantes de CYCRMS)
    if canal not in ["CH1", "CH2"]:
        return None, "Canal inválido"
    if magnitud not in ["FREQ", "PKPK", "CYCRMS", "CYCRms"]:
        return None, "Magnitud inválida"
        
    # Validar valor numérico usando a_numero
    valor = a_numero(val_str)
    if valor is None:
        return None, "Valor no numérico"
        
    medicion = {
        "fecha": fecha,
        "hora": hora,
        "equipo": equipo,
        "canal": canal,
        "magnitud": magnitud.upper(),
        "valor": valor
    }
    
    return medicion, None


def leer_log(ruta):
    """Lee un archivo de log línea por línea, agrupa las series y lista las rechazadas."""
    series = {}
    rechazadas = []

    with open(ruta, "r", encoding="utf-8") as archivo:
        for numero, linea in enumerate(archivo, 1):
            medicion, motivo = analizar_linea(linea)

            if medicion is not None:
                clave = (medicion["equipo"], medicion["canal"], medicion["magnitud"])
                if clave not in series:
                    series[clave] = []
                series[clave].append(medicion["valor"])

            elif motivo is not None:
                rechazadas.append({
                    "linea": numero,
                    "motivo": motivo,
                    "texto": linea.rstrip("\n")
                })

    return series, rechazadas


# --- Pruebas del Ejercicio 8 ---
if __name__ == "__main__":
    # Caso línea válida con espacios normales
    med, err = analizar_linea("2026-09-08 09:14:02 ADS3202 CH1 FREQ 1.000431E+03")
    assert med is not None
    assert med["valor"] == 1000.431
    assert err is None
    
    # Caso línea con hora imposible (debe rechazarla)
    _, err_hora = analizar_linea("2026-09-08 25:61:00 ADS3202 CH1 FREQ 1.000431E+03")
    assert err_hora == "Hora imposible"
    
    print("¡Pruebas del Ejercicio 8 OK!")