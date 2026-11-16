def armar_informe(idn, series, verificaciones):
    lineas = []
    lineas.append("=== INFORME DE BANCO DE MEDICIONES ===")
    lineas.append(f"Equipo Identificado: {idn}")
    lineas.append("-" * 40)
    
    lineas.append("RESUMEN DE SERIES:")
    for nombre_serie, datos in series.items():
        # Asumimos que podemos usar la función con_unidad del ejercicio 2 si la importamos, 
        # o formatearlo directamente:
        lineas.append(f" - {nombre_serie}: n={datos['n']}, Promedio={datos['promedio']}, Mín={datos['minimo']}, Máx={datos['maximo']}")
        
    lineas.append("-" * 40)
    lineas.append("VERIFICACIONES:")
    for verif in verificaciones:
        estado = "COINCIDE" if verif.get("coincide") else "NO COINCIDE"
        lineas.append(f" - Canal {verif['canal']}: {estado} (Teórico: {verif.get('teorico')}, Medido: {verif.get('medido')})")
        
    lineas.append("======================================")
    return "\n".join(lineas)

# --- Pruebas del Ejercicio 10 ---
if __name__ == "__main__":
    idn_ejemplo = "OWON, ADS3202, 25470803, V1.2.0"
    series_ejemplo = {
        "CH1_FREQ": {"n": 3, "minimo": 999.0, "maximo": 1001.0, "promedio": 1000.0, "desvio": 1.0}
    }
    verifs_ejemplo = [
        {"canal": "CH1", "coincide": True, "teorico": 0.7071, "medido": 0.7065}
    ]
    
    informe = armar_informe(idn_ejemplo, series_ejemplo, verifs_ejemplo)
    
    # Verificamos que el informe devuelva un texto con las secciones clave
    assert isinstance(informe, str)
    assert "INFORME DE BANCO DE MEDICIONES" in informe
    assert "ADS3202" in informe
    assert "COINCIDE" in informe

    print("¡Pruebas del Ejercicio 10 OK!")