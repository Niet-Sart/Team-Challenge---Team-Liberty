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
    """
    Realiza un disparo en la coordenada dada y actualiza el tablero.
    Maneja los casos de disparos repetidos.
    """
    x, y = coordenada
    
    # Verificar que la coordenada está dentro de los límites del tablero
    if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
        print("Coordenada fuera de rango. Elige otra coordenada.")
        return tablero

    # Verificar si ya se disparó en esta posición
    if coordenada in posiciones_disparadas:
        print("Ya has disparado en esta posición. Elige otra coordenada.")
        return tablero  # Devuelve el tablero sin cambios para realizar otro intento

    # Registrar el disparo
    posiciones_disparadas.append(coordenada)
    
    # Evaluar el resultado del disparo
    if tablero[x][y] == CELDA_BARCO:
        print("¡Tocado!")
        tablero[x][y] = CELDA_TOCADO  # Actualiza el tablero con el impacto
    elif tablero[x][y] == CELDA_VACIA:
        print("¡Agua!")
        tablero[x][y] = CELDA_AGUA  # Marca la celda como agua
    else:
        # Si la celda ya está marcada como agua o tocado, no debería entrar aquí
        print("A

# La idea es que si el jugador ya ha disparado en esa coordenada, se le avise para que elija otra posición

# JESUS 

# Implementar una dificultad adicional donde la máquina tenga más probabilidades de acertar    
import random

# Dimensiones del tablero y constantes
SIZE = 10
CELDA_VACIA = ''
CELDA_BARCO = 'O'
CELDA_TOCADO = 'X'
CELDA_AGUA = '~'

# Lista de posiciones ya disparadas y de objetivos prioritarios
posiciones_disparadas = []
objetivos_prioritarios = []

def disparar(tablero, coordenada):
    """
    Realiza un disparo en la coordenada dada y actualiza el tablero.
    """
    x, y = coordenada
    if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
        print("Coordenada fuera de rango")
        return tablero

    if coordenada in posiciones_disparadas:
        print("Ya has disparado en esta posición. Elige otra coordenada.")
        return tablero

    posiciones_disparadas.append(coordenada)
    if tablero[x][y] == CELDA_BARCO:
        print("¡Tocado!")
        tablero[x][y] = CELDA_TOCADO  # Marca como tocado
        agregar_objetivos_prioritarios(tablero, x, y)  # Añadir objetivos prioritarios
    elif tablero[x][y] == CELDA_VACIA:
        print("¡Agua!")
        tablero[x][y] = CELDA_AGUA  # Marca como agua
    else:
        print("Esta posición ya ha sido disparada.")
    return tablero

def agregar_objetivos_prioritarios(tablero, x, y):
    """
    Añade las coordenadas adyacentes como objetivos prioritarios si son válidas y no han sido disparadas.
    """
    adyacentes = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    for coord in adyacentes:
        # Verificar que la posición está dentro del tablero y no ha sido disparada
        if 0 <= coord[0] < SIZE and 0 <= coord[1] < SIZE:
            if coord not in posiciones_disparadas and coord not in objetivos_prioritarios:
                # Solo añadir si la celda no es agua ni ya disparada
                if tablero[coord[0]][coord[1]] in [CELDA_VACIA, CELDA_BARCO]:
                    objetivos_prioritarios.append(coord)

def maquina_dispara(tablero):
    """
    Realiza un disparo de la máquina, priorizando los objetivos adyacentes antes de disparar aleatoriamente.
    """
    # Primero intenta disparar en una coordenada de objetivos prioritarios
    if objetivos_prioritarios:
        coordenada = objetivos_prioritarios.pop(0)
    else:
        # Si no hay objetivos prioritarios, dispara aleatoriamente
        while True:
            x = random.randint(0, SIZE - 1)
            y = random.randint(0, SIZE - 1)
            coordenada = (x, y)
            if coordenada not in posiciones_disparadas:
                break
    
    # Dispara y actualiza el tablero
    return disparar(tablero, coordenada)
