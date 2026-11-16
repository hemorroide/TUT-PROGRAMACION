def es_consulta(comando):
    if not comando:
        return False
    return comando.strip().endswith("?")

def validar(comando):
    if not comando or not isinstance(comando, str):
        return "El comando no puede estar vacío"
    
    cmd = comando.strip()
    
    # Regla: Empieza con : o con *
    if not (cmd.startswith(":") or cmd.startswith("*")):
        return "Debe empezar con ':' o '*'"
    
    # Regla: No hay dos espacios seguidos
    if "  " in cmd:
        return "No puede tener dos espacios seguidos"
    
    # Regla: A lo sumo un '?' y va al final
    cantidad_signos = cmd.count("?")
    if cantidad_signos > 1:
        return "Tiene más de un signo de pregunta"
    if cantidad_signos == 1 and not cmd.endswith("?"):
        return "El signo de pregunta debe ir al final"
        
    return None

# --- Pruebas del Ejercicio 3 ---
if __name__ == "__main__":
    assert es_consulta(":CH1:FREQuency?") is True
    assert es_consulta(":CH1:DISPlay ON") is False
    
    # Casos válidos devuelven None
    assert validar(":CH1:DISPlay ON") is None
    assert validar(":CH1:FREQuency?") is None
    
    # Casos inválidos devuelven un mensaje de error
    assert validar("") is not None
    assert validar("CH1:DISPlay ON") is not None  # Le falta el ':' adelante
    assert validar(":CH1:DISPlay  ON") is not None # Doble espacio
    
    print("¡Pruebas del Ejercicio 3 OK!")