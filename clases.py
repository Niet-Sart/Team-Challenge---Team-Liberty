from variables import *
from funciones import *

import random
import numpy as np
import pandas as pd

class Battleship:
    def __init__(self):
        self.tablero_maquina = Tablero(player=0)
        self.tablero_jugador = Tablero(player=1)
        
    def __str__(self):
        return str(f"Tu tablero:\n{self.tablero_jugador}\n\nEl tablero rival:\n{self.tablero_maquina}")

class Tablero:
    def __init__(self, size=SIZE, player=0):
        self.player = player
        if size < 5:
            raise ValueError("El tamaño mínimo de tablero es de 5x5 celdas")
        if size > 20:
            raise ValueError("El tamaño máximo de tablero es de 20x20 celdas")
        self.grid = pd.DataFrame(np.full([SIZE, SIZE], CELDA_VACIA, dtype=str), index=range(1,SIZE+1), columns=[chr(i) for i in range(1 + 64, SIZE + 64 + 1)])
        self.size = SIZE
        self.barcos = []
        self.otro_turno = False
        for eslora in ESLORAS:
            self.posicionar_aleatorio(eslora)
        
    def __getitem__(self, key):
        k2, *k1 = key
        if type(k1) == list: k1 = ''.join(k1)
        k1 = int(k1)
        return self.grid.loc[k1, k2]
    
    def __setitem__(self, key, value):
        k2, *k1 = key
        if type(k1) == list: k1 = ''.join(k1)
        k1 = int(k1)
        self.grid.loc[k1, k2] = value
        return self.grid
    
    def __str__(self):
        return str(self.grid)
    
    def posicionar(self, origen, eslora=2, orientacion=0):
        y,x = origen
        if eslora > 5:
            raise ValueError("El tamaño máximo para un barco es de 5 celdas")
        if max(origen) > self.size:
            raise ValueError("Las dimensiones del origen no pueden ser mayores que el tamaño del tablero")
        if min(origen) < 0:
            raise ValueError("Ninguna dimensión puede ser menor que 0")
        barco = Barco(eslora, self.player)
        self.barcos.append(barco)
        if orientacion:
            x2 = x+eslora
            if x2 > self.size:
                raise ValueError("El barco se sale del tablero. Prueba a reducir el origen o el tamaño")
            if np.any(self.grid.iloc[x:x2,y] == CELDA_BARCO):
                raise ValueError("Estás intentando colocar un barco donde ya hay uno")
            self.grid.iloc[x:x2,y] = barco.df.T
            barco.pos = self.grid.iloc[x:x2,y]
        else:
            y2 = y+eslora
            if y2 > self.size:
                raise ValueError("El barco se sale del tablero. Prueba a reducir el origen o el tamaño")
            if np.any(self.grid.iloc[x,y:y2] == CELDA_BARCO):
                raise ValueError("Estás intentando colocar un barco donde ya hay uno")
            self.grid.iloc[x,y:y2] = barco.df.T
            barco.pos = self.grid.iloc[x,y:y2]
        
    def posicionar_aleatorio(self, eslora):
        orientacion = random.randint(0,1)
        if eslora > 5:
            raise ValueError("El tamaño máximo para un barco es de 5 celdas")
        x1 = random.randint(0,self.size-1)
        y1 = random.randint(0,self.size-1)
        try: self.posicionar((x1,y1),eslora=eslora,orientacion=orientacion)
        except: self.posicionar_aleatorio(eslora=eslora)
        
    def disparar(self, coordenada):
        x, y = translate_coord(coordenada)
        if min(x,y) < 0:
            raise IndexError("Ninguna dimensión puede ser menor que 0")
        if max(x,y) > self.size-1:
            raise IndexError(f"Ninguna dimensión puede ser mayor que {self.size-1}")
        casilla = self.grid.iloc[x,y]
        if type(casilla) == Barco.SubBarco:
            already_hit = casilla.hit
            if already_hit:
                print("Ya habías disparado en esa posición")
                return False
            casilla.hit = True
            barco = casilla.barco
            if barco.df.map(lambda x: x.hit).all()[0]:
                print("¡Tocado y hundido!")
                barco.hundido = True
                self.otro_turno = True
            else:
                print("¡Tocado!")
                self.otro_turno = True
        else:
            self.grid.iloc[x,y] = CELDA_AGUA
            print("¡Agua!")
            self.otro_turno = False
        return True
            
    def disparo_maquina(self):
        for intento in range(DIFICULTAD):
            x = random.choice(self.grid.columns)
            y = random.choice(self.grid.index)
            coordenada = x+str(y)
            casilla = self[coordenada]
            if type(casilla) == Barco.SubBarco:
                if not casilla.hit:
                    self.last_hit = coordenada
                    print(coordenada)
                    return self.disparar(coordenada)
        print(coordenada)
        return self.disparar(coordenada)
            
class Barco:
    def __init__(self, eslora, player):
        self.eslora = eslora
        self.hundido = False
        self.player = player
        self.df = pd.DataFrame([self.SubBarco(i, player, self) for i, sb in enumerate(range(eslora))])
        self.pos = None

    class SubBarco:
        def __init__(self, pos, player, barco):
            self.hit = False
            self.pos = pos
            self.player = player
            self.barco = barco
            
        def __str__(self):
            if self.hit:
                return CELDA_TOCADO
            else:
                if self.player:
                    return CELDA_BARCO
                else:
                    return CELDA_VACIA
            
        def hit(self):
            self.hit = True