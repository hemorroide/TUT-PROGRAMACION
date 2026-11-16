def barrer(instrumento, canales=["CH1", "CH2"]):
    magnitudes = ["FREQuency", "PKPK", "CYCRms"]
    resultados = []
    
    for canal in canales:
        for mag in magnitudes:
            # Armamos el comando SCPI exacto con el signo de pregunta obligatorio
            comando = f":MEASUrement:{canal}:{mag}?"
            
            # Consultamos al instrumento
            texto_crudo = instrumento.preguntar(comando)
            
            # Intentamos convertir la respuesta a número (usando la lógica del ej 2)
            try:
                valor_num = float(texto_crudo)
            except (ValueError, TypeError):
                valor_num = None
                
            # Guardamos el diccionario con todos los datos de la medición
            resultados.append({
                "canal": canal,
                "magnitud": mag,
                "unidad": "Hz" if mag == "FREQuency" else "V",
                "crudo": texto_crudo,
                "valor": valor_num
            })
            
    return resultados

# --- Pruebas del Ejercicio 6 (Usando un instrumento "trucho") ---
class InstrumentoTrucho:
    def preguntar(self, comando):
        # Simulamos una respuesta fija del equipo de mentira
        return "1.000000E+03"

if __name__ == "__main__":
    inst_falso = InstrumentoTrucho()
    mediciones = barrer(inst_falso, ["CH1"])
    
    # Verificamos que devuelva las 3 magnitudes del CH1
    assert len(mediciones) == 3
    assert mediciones[0]["canal"] == "CH1"
    assert mediciones[0]["magnitud"] == "FREQuency"
    assert mediciones[0]["valor"] == 1000.0

    print("¡Pruebas del Ejercicio 6 OK!")