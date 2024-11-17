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

import numpy as np
import random

class Barco:
    def __init__(self, eslora, coordenadas):
        #eslora: Longitud del barco.
        # coordenadas: Lista de coordenadas donde está ubicado el barco. 
        self.eslora = eslora
        self.coordenadas = coordenadas
       

    def recibir_disparo(self, coord): #Marca una coordenada como tocada.
        #coord: Coordenada del disparo.
        if coord in self.coordenadas:
            self.tocados.add(coord)
            return True #return: True si el disparo impacta en este barco.
        return False

    def esta_hundido(self): #Verifica si el barco está hundido.
        #return: True si todas las coordenadas del barco han sido tocadas.
        return set(self.coordenadas) == self.tocados



class Tablero:
    def __init__(self, size):
        
        self.size = size
        self.tablero_barcos = np.zeros(size, dtype=int)  # Tablero oculto con los barcos
        self.tablero_disparos = np.zeros(size, dtype=int)  # Tablero visible de disparos
        self.barcos = []  # Lista de objetos Barco

    def inicializar_tablero(self): # pone los barcos de forma aleatoria
        configuracion_barcos = {1: 4, 2: 3, 3: 2, 4: 1}  # Eslora: Cantidad
        
        
        # sé que hay que hacer un bucle for que recorra los barcos pero no sé muy bien como

   
   

    def colocar_barco(self, fila, col, eslora, orientacion):
        coordenadas = []
        if orientacion == "H":
            for i in range(eslora): # para estos bucles he buscado un poco de ayuda :')
                self.tablero_barcos[fila, col + i] = eslora
                coordenadas.append((fila, col + i))
        else:
            for i in range(eslora):
                self.tablero_barcos[fila + i, col] = eslora
                coordenadas.append((fila + i, col))
        # Crear un nuevo barco y añadirlo a la lista
        barco = Barco(eslora, coordenadas)
        self.barcos.append(barco)
    

    def disparo (self, fila, col):
        
        if self.tablero_disparos[fila, col] != 0:
            return "Has repetido tu disparo"

        if self.tablero_barcos[fila, col] > 0:  
            self.tablero_disparos[fila, col] = 2  
            for barco in self.barcos:
                if barco.recibir_disparo((fila, col)):
                    if barco.esta_hundido():
                        return f"Impacto y hundiste un barco de eslora {barco.eslora}."
                    return "Impacto"
        else:  # Agua
            self.tablero_disparos[fila, col] = 1  # Marcamos agua con un 1
            return "Agua"

    def mostrar_tablero(self, mostrar_barcos=False):
        if mostrar_barcos:
            print("Tablero con barcos:")
            print(self.tablero_barcos)
        print("Tablero de disparos:")
        print(self.tablero_disparos)

    
