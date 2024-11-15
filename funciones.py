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

# JESUS

# Gestión de los intentos de disparo en una posición ya disparada
def disparar(tablero, coordenada):
    x, y = coordenada
    if x < 0 or x >= TAMANO or y < 0 or y >= TAMANO:
        print("Coordenada fuera de rango")
        return tablero

    if coordenada in posiciones_disparadas:
        print("Ya has disparado en esta posición. Elige otra coordenada.")
        return tablero  # Devuelve el tablero sin cambios, para poder realizar más intentos

    posiciones_disparadas.append(coordenada)
    if tablero[x, y] == celda_agua:
        print("Agua!")
    elif tablero[x, y] == celda_disparo:
        print("Tocado!")
        tablero[x, y] = celda_disparo  # Actualiza el tablero con el disparo
    return tablero
 # La idea es que si el jugador ya ha disparado en esa coordenada, se le avise para que elija otra posición
