import math

def vrms_teorico(vpp):
    if vpp is None or vpp < 0:
        return None
    vp = vpp / 2.0
    return vp / math.sqrt(2.0)

def coincide(medido, teorico, tolerancia=0.02):
    if medido is None or teorico is None or teorico == 0:
        return False
    # Fórmula del error relativo pedida por la cátedra:
    error = abs(medido - teorico) / abs(teorico)
    return error <= tolerancia

def verificar_canal(filas, canal):
    pkpk = None
    vrms_medido = None
    
    for fila in filas:
        if fila["canal"] == canal:
            if fila["magnitud"] == "PKPK":
                pkpk = fila["valor"]
            elif fila["magnitud"] == "CYCRms":
                vrms_medido = fila["valor"]
                
    if pkpk is None or vrms_medido is None:
        return {"canal": canal, "coincide": False, "motivo": "Faltan datos"}
        
    teorico = vrms_teorico(pkpk)
    resultado_ok = coincide(vrms_medido, teorico)
    
    return {
        "canal": canal,
        "teorico": teorico,
        "medido": vrms_medido,
        "coincide": resultado_ok
    }

# --- Pruebas del Ejercicio 7 ---
if __name__ == "__main__":
    # 1. Prueba de la fórmula teórica: Vpp = 2.0V -> Vrms teórico = ~0.7071V
    assert round(vrms_teorico(2.0), 4) == 0.7071
    assert vrms_teorico(-1) is None
    
    # 2. Prueba de tolerancia (dentro del 2% de margen da True, fuera da False)
    assert coincide(0.705, 0.7071, 0.02) is True
    assert coincide(0.900, 0.7071, 0.02) is False 
    
    # 3. La prueba de la señal cuadrada (la trampa de la cátedra):
    # Una señal cuadrada de Vpp = 2V tiene un Vrms de 1.0V (no de 0.707V). 
    # Al pasarla por verificar_canal, tiene que decir obligatoriamente que NO coincide.
    barrido_cuadrada = [
        {"canal": "CH1", "magnitud": "PKPK", "valor": 2.0},
        {"canal": "CH1", "magnitud": "CYCRms", "valor": 1.0}
    ]
    res_verificacion = verificar_canal(barrido_cuadrada, "CH1")
    assert res_verificacion["coincide"] is False

    print("¡Pruebas del Ejercicio 7 OK!")