import random
import numpy as np
import pandas as pd

# No he comentado el código de forma exhaustiva porque creo que los mensajes de error ayudan lo suficiente a identificar las comprobaciones

SIZE = 10
CELDA_VACIA = ''
CELDA_BARCO = 'O'
CELDA_TOCADO = 'X'
CELDA_AGUA = '~'

class Barco:
    def __init__(self, eslora):
        self.eslora = eslora
        self.positions = [None] * eslora
        self.hits = [False] * eslora

class Tablero:
    def __init__(self, size=SIZE):
        if size < 5:
            raise ValueError("El tamaño mínimo de tablero es de 5x5 celdas")
        self.grid = pd.DataFrame(np.full([size, size], CELDA_VACIA, dtype=str), index=range(1,11), columns=[chr(i) for i in range(ord('A'), ord('J') + 1)])
        self.size = SIZE
        for eslora in [1]*4 + [2]*3 + [3]*2 + [4]:
            self.posicionar_aleatorio(eslora)
        
    def __getitem__(self, key):
        k2,k1 = key
        k1 = int(k1)
        return self.grid.loc[k1, k2]
    
    def __setitem__(self, key, value):
        k2,k1 = key
        k1 = int(k1)
        self.grid.loc[k1, k2] = value
        return self.grid
    
    
    def posicionar(self, origen, eslora=2, orientacion=0):
        # Aquí defino los argumentos de forma bastante distinta a cómo se implicita en el enunciado, pero es mucho más sencillo así
        y,x = origen
        if eslora > 5:
            raise ValueError("El tamaño máximo para un barco es de 5 celdas")
        if max(origen) > self.size:
            raise ValueError("Las dimensiones del origen no pueden ser mayores que el tamaño del tablero")
        if min(origen) < 0:
            raise ValueError("Ninguna dimensión puede ser menor que 0")
        if orientacion:
            x2 = x+self.size
            if x2 > self.size:
                raise ValueError("El barco se sale del tablero. Prueba a reducir el origen o el tamaño")
            if np.any(self.grid[x:x2,y] == CELDA_BARCO):
                raise ValueError("Estás intentando colocar un barco donde ya hay uno")
            self.grid[x:x2,y] = CELDA_BARCO
        else:
            y2 = y+self.size
            if y2 > self.size:
                raise ValueError("El barco se sale del tablero. Prueba a reducir el origen o el tamaño")
            if np.any(self.grid[x,y:y2] == CELDA_BARCO):
                raise ValueError("Estás intentando colocar un barco donde ya hay uno")
            self.grid[x,y:y2] = CELDA_BARCO
        print(self)
        
    def disparar(self, punto1):
        if min(punto1) < 0:
            raise IndexError("Ninguna dimensión puede ser menor que 0")
        if max(punto1) > self.size-1:
            raise IndexError(f"Ninguna dimensión puede ser mayor que {self.size-1}")
        y1, x1 = punto1
        if self.grid[x1,y1] == 2:
            print("¡Tocado!")
        else:
            print("¡Agua!")
        self.grid[x1,y1] += 1 # Esto puede ser confuso, pero básicamente el estado de cada celda viene definido por su valor numérico, así que al sumar 1 lidio tanto con las celdas vacías como las que tienen barco
        print(self)
        
    def posicionar_aleatorio(self, eslora):
        orientacion = random.randint(0,1)
        if eslora > 5:
            raise ValueError("El tamaño máximo para un barco es de 5 celdas")
        x1 = random.randint(0,self.size-1)
        y1 = random.randint(0,self.size-1)
        # Usar un try - except aquí seguramente no es la forma más limpia de lidiar con errores, pero es funcional y no entra en bucles recursivos largos
        # Lo hago así por falta de tiempo
        try: self.posicionar((x1,y1),eslora=eslora,orientacion=orientacion)
        except: self.posicionar_aleatorio(eslora=eslora)
        #self.posicionar((x1,y1),eslora=eslora,orientacion=orientacion)
        
        
tablero = Tablero()
tablero.grid
