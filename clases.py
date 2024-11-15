import random

# Constantes
TAMANO = 10
CELDA_AGUA = "-"
CELDA_BARCO = "B"

class Barco:
    def _init_(self, eslora):
        self.eslora = eslora  # Tamaño del barco (número de celdas)
        self.posiciones = []  # Coordenadas que ocupa el barco en el tablero
        self.hundido = False  # Estado del barco (si está completamente hundido)

    def colocar(self, posiciones):
        """
        Asigna posiciones al barco en el tablero.
        """
        if len(posiciones) == self.eslora:
            self.posiciones = posiciones
        else:
            raise ValueError("Las posiciones asignadas no coinciden con la eslora del barco")

  class Tablero:
    def _init_(self):
        # Inicializa un tablero vacío de tamaño TAMANO x TAMANO
        self.tablero = [[CELDA_AGUA for _ in range(TAMANO)] for _ in range(TAMANO)]
        self.barcos = []  # Lista de objetos Barco en el tablero

    def mostrar_tablero(self):
        """
        Muestra el tablero en consola.
        """
        for fila in self.tablero:
            print(" ".join(fila))

    def agregar_barco(self, barco):
        """
        Coloca un barco en el tablero en posiciones aleatorias.
        """
        colocado = False
        while not colocado:
            # Elegir dirección y coordenada inicial
            orientacion = random.choice(['horizontal', 'vertical'])
            if orientacion == 'horizontal':
                fila = random.randint(0, TAMANO - 1)
                columna = random.randint(0, TAMANO - barco.eslora)
                posiciones = [(fila, columna + i) for i in range(barco.eslora)]
            else:
                fila = random.randint(0, TAMANO - barco.eslora)
                columna = random.randint(0, TAMANO - 1)
                posiciones = [(fila + i, columna) for i in range(barco.eslora)]

            # Comprobar si las posiciones están libres
            if all(self.tablero[f][c] == CELDA_AGUA for f, c in posiciones):
                # Colocar barco en el tablero
                for f, c in posiciones:
                    self.tablero[f][c] = CELDA_BARCO
                barco.colocar(posiciones)
                self.barcos.append(barco)
                colocado = True


## MARÍA

class Barco:
    def __init__(self, eslora, coordenadas):
        self.eslora = eslora
        self.coordenadas = coordenadas
        


class Tablero:
    def __init__(self, dimensiones=(10, 10)):
    
        self.dimensiones = dimensiones
        self.tablero_barcos = np.zeros(dimensiones, dtype=int) 
        self.tablero_disparos = np.zeros(dimensiones, dtype=int)
        self.barcos = []  
        self.vidas = 0 