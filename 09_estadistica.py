import math

def resumen(valores):
    if not valores:
        return None
    
    n = len(valores)
    minimo = min(valores)
    maximo = max(valores)
    promedio = sum(valores) / n
    
    # Cálculo del desvío estándar muestral (dividiendo por n - 1)
    if n == 1:
        desvio = 0.0
    else:
        suma_cuadrados = sum((v - promedio) ** 2 for v in valores)
        desvio = math.sqrt(suma_cuadrados / (n - 1))
        
    return {
        "n": n,
        "minimo": minimo,
        "maximo": maximo,
        "promedio": promedio,
        "desvio": desvio
    }

def fuera_de_rango(valores, minimo, maximo):
    # Devuelve las posiciones (índices) de los valores que están fuera del rango [minimo, maximo]
    posiciones_fuera = []
    for i, v in enumerate(valores):
        if v < minimo or v > maximo:
            posiciones_fuera.append(i)
    return posiciones_fuera

# --- Pruebas del Ejercicio 9 ---
if __name__ == "__main__":
    serie = [1000.0, 1001.0, 999.0, 1000.5]
    res = resumen(serie)
    assert res["n"] == 4
    assert res["minimo"] == 999.0
    assert res["maximo"] == 1001.0
    
    # Prueba de fuera_de_rango (los extremos cuentan como adentro)
    datos = [10, 5, 20, 15]
    # Si el rango es [10, 15], el 5 (índice 1) y el 20 (índice 2) están afuera
    assert fuera_de_rango(datos, 10, 15) == [1, 2]

    print("¡Pruebas del Ejercicio 9 OK!")