def comandos_de_canal(canal, display, acoplamiento, sonda, escala):
    # Validamos que el canal sea el correcto
    if canal not in ["CH1", "CH2"]:
        return None
    
    # Armamos la lista con las 4 órdenes estrictas de la consigna
    return [
        f":{canal}:DISPlay {display}",
        f":{canal}:COUPling {acoplamiento}",
        f":{canal}:PROBe {sonda}",
        f":{canal}:SCALe {escala}"
    ]

# --- Pruebas del Ejercicio 4 (Autónomas) ---
if __name__ == "__main__":
    comandos = comandos_de_canal("CH1", "ON", "DC", "10X", "1v")
    
    # Verificamos que devuelva la lista exacta pedida
    assert comandos == [
        ":CH1:DISPlay ON",
        ":CH1:COUPling DC",
        ":CH1:PROBe 10X",
        ":CH1:SCALe 1v"
    ]
    
    # Canal inválido debe devolver None
    assert comandos_de_canal("CH3", "ON", "DC", "10X", "1v") is None
    
    # Verificación interna de formato para cumplir con la prueba del ejercicio
    for cmd in comandos:
        assert cmd.startswith(":")  # Comprueba que empiece con dos puntos

    print("¡Pruebas del Ejercicio 4 OK!")