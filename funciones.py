def disparar(tablero, coordenada):
    if min(coordenada) < 0:
        raise IndexError("Ninguna dimensión puede ser menor que 0")
    if max(coordenada) > TAMANO - 1:
        raise IndexError(f"Ninguna dimensión puede ser mayor que {TAMANO-1}")
    if tablero[coordenada] == celda_barco:
        tablero[coordenada] = celda_disparo
        print("¡Tocado!")
    elif tablero[coordenada] == celda_agua:
        print("¡Agua!")
    elif tablero[coordenada] == celda_disparo:
        pass # Hay que decidir cómo gestionamos los disparos en posiciones ya disparadas     
    return tablero

posiciones_disparadas = []

def maquina_dispara(tablero):
    x = random.randint(1, TAMANO)
    y = random.randint(1, TAMANO)
    coordenada = x,y
    posiciones_disparadas.append(coordenada)
    return disparar(tablero, coordenada)