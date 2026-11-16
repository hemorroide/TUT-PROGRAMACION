def parsear_idn(respuesta):
    #creo que: el comando parsear_idn() recibe una cadena de texto que representa la respuesta de un instrumento a un comando *IDN?* y devuelve un diccionario con la información del fabricante, modelo, serie y versión del instrumento. Si la respuesta es inválida o contiene un error, devuelve None.
    if not respuesta or "ERROR" in respuesta:
        return None
    
    # Separamos la cadena por comas
    partes = respuesta.split(",")
    
    # Limpiamos los espacios en blanco alrededor de cada campo
    partes = [p.strip() for p in partes]
    
    # Validamos que tenga al menos 4 campos
    if len(partes) < 4:
        return None
    
    # Armamos y devolvemos el diccionario
    return {
        "fabricante": partes[0],
        "modelo": partes[1],
        "serie": partes[2],
        "version": partes[3]
    }

# --- Pruebas (asserts obligatorios) ---
if __name__ == "__main__":
    # Caso 1: Osciloscopio (4 campos)
    res_osc = parsear_idn("OWON, ADS3202,25470803, V1.2.0")
    assert res_osc is not None
    assert res_osc["modelo"] == "ADS3202"

    # Caso 2: Multímetro (5 campos, descarta el último)
    res_mult = parsear_idn("OWON, XDM1041,25470803,V4.4.0,3")
    assert res_mult is not None
    assert res_mult["modelo"] == "XDM1041"

    # Caso 3: Casos inválidos (deben retornar None)
    assert parsear_idn("OWON, ADS3202,254") is None
    assert parsear_idn("") is None
    assert parsear_idn("ERROR: comando desconocido") is None

    print("¡Pruebas del Ejercicio 1 OK!")