from variables import *
from funciones import *

import random
import numpy as np
import pandas as pd

class Battleship:
    """Clase para iniciar el juego
    
    Se instancia sin atributos explícitos e instancia a su vez 2 tableros, uno para jugador y otro para máquina
    
    Tiene un método __str__ para imprimir ambos tableros por pantalla
    """
    def __init__(self):
        self.tablero_maquina = Tablero(player=0)
        self.tablero_jugador = Tablero(player=1)
        
    def __str__(self):
        return str(f"Tu tablero:\n{self.tablero_jugador}\n\nEl tablero rival:\n{self.tablero_maquina}")

class Tablero:
    def __init__(self, size=SIZE, player=0):
        """Clase tablero que alojará un DataFrame en su atributo grid
        
        También alberga una lista de objetos Barco en su atributo barcos
        
        Y también alberga un booleano en el atributo otro_turno para saber si el usuario vuelve a disparar
        
        Asímismo posiciona todos los barcos definidos en la constante ESLORA (variables.py) llamando a su método posicionar_aleatorio
        
        Y finalmente alberga una lista de las posiciones disparadas en el atributo posiciones_disparadas

        Args:
            size (int between 5 and 20, optional): Dimensión del lado del tablero. Defaults to constant SIZE defined in variables.py.
            player (int: 0 or 1, optional): Identificador: 1 para el jugador, 0 para la máquina. Nos sirve para ocultar los barcos enemigos.
        """
        self.player = player
        if size < 5:
            raise ValueError("El tamaño mínimo de tablero es de 5x5 celdas")
        if size > 20:
            raise ValueError("El tamaño máximo de tablero es de 20x20 celdas")
        # Usamos un DataFrame con índices numéricos y nombres de columnas con las letras del abecedario
        self.grid = pd.DataFrame(np.full([SIZE, SIZE], CELDA_VACIA, dtype=str), index=range(1,SIZE+1), columns=[chr(i) for i in range(1 + 64, SIZE + 64 + 1)])
        self.size = SIZE
        self.barcos = [] # Se llena durante la ejecución del método posicionar_aleatorio
        self.otro_turno = False # Inicializado en False por defecto, se cambia durante la ejecución del método disparar
        self.posiciones_disparadas = []
        for eslora in ESLORAS:
            self.posicionar_aleatorio(eslora)
        
    def __getitem__(self, key):
        """Getter usando el formato de coordenada LETRA+NÚMERO (str)

        Args:
            key (str): Por ejemplo "A1"

        Returns:
            Devuelve el elemento del DataFrame correspondiente a la coordenada
        """
        k2, *k1 = key
        if type(k1) == list: k1 = ''.join(k1)
        k1 = int(k1)
        return self.grid.loc[k1, k2]
    
    def __setitem__(self, key, value):
        """Setter usando el formato de coordenada LETRA+NÚMERO (str)

        Args:
            key (str): Por ejemplo "A1"
            value: Valor a añadir en la coordenada especificada

        Returns:
            Devuelve el valor del atributo grid (Pandas.DataFrame)
        """
        k2, *k1 = key
        if type(k1) == list: k1 = ''.join(k1)
        k1 = int(k1)
        self.grid.loc[k1, k2] = value
        return self.grid
    
    def __str__(self):
        """Representación string del tablero

        Returns:
            str: Devuelve directamente la representación string del DataFrame contenido en el atributo grid
        """
        return str(self.grid)
    
    def posicionar(self, origen, eslora=2, orientacion=0):
        """Método para posicionar un barco

        Args:
            origen (tupla o lista): conteniendo dos int que se tratarán como variables x, y en la ejecución
            eslora (int, optional): longitud del barco. Defaults to 2.
            orientacion (int, optional): 0 para horizontal, 1 para vertical. Defaults to 0.

        Raises:
            ValueError: "El tamaño máximo para un barco es de 5 celdas" si argumento eslora > 5
            ValueError: "Las dimensiones del origen no pueden ser mayores que el tamaño del tablero" si argumento origen contiene un int > atributo size
            ValueError: "Ninguna dimensión puede ser menor que 0" si argumento origen contiene un int < 0
            ValueError: "El barco se sale del tablero. Prueba a reducir el origen o el tamaño" si la posición final (origen + eslora) sale de los límites
            ValueError: "Estás intentando colocar un barco donde ya hay uno" si alguna de las posiciones del barco ya está ocupada por otro barco
        """
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
        """Método para posicionar un barco de forma aleatoria.
        Hace una llamada al método posicionar pasando el argumento eslora y un origen y orientación aleatorias

        Args:
            eslora (int): longitud del barco

        Raises:
            ValueError: "El tamaño máximo para un barco es de 5 celdas" si argumento eslora > 5
        """
        orientacion = random.randint(0,1)
        if eslora > 5:
            raise ValueError("El tamaño máximo para un barco es de 5 celdas")
        x1 = random.randint(0,self.size-1)
        y1 = random.randint(0,self.size-1)
        # Usamos un try... except de manera que si un intento falla (excepciones definidas en el método posicionar)
        # entonces la función se llama a sí misma y lo vuelve a intentar con otros valores aleatorios
        try: self.posicionar((x1,y1),eslora=eslora,orientacion=orientacion)
        except: self.posicionar_aleatorio(eslora=eslora)
        
    def disparar(self, coordenada):
        """Método para los disparos del jugador

        Args:
            coordenada (str): Coordenada con formato LETRA+NÚMERO (por ejemplo "A1")

        Raises:
            IndexError: "Ninguna dimensión puede ser menor que 0" si la coordenada apunta fuera del tablero
            IndexError: "Ninguna dimensión puede ser mayor que {self.size-1}" si la coordenada apunta fuera del tablero

        Returns:
            Bool: False si se intenta disparar una casilla-barco ya disparada, True en el resto de casos
        """
        x, y = translate_coord(coordenada)
        if min(x,y) < 0:
            raise IndexError("Ninguna dimensión puede ser menor que 0")
        if max(x,y) > self.size-1:
            raise IndexError(f"Ninguna dimensión puede ser mayor que {self.size-1}")
        self.posiciones_disparadas.append(coordenada) # Añadimos la coordenada a la lista para que la máquina no vuelva a disparar ahí
        casilla = self.grid.iloc[x,y]
        if type(casilla) == Barco.SubBarco: # Si la coordenada apunta a un barco
            already_hit = casilla.hit
            if already_hit:
                print("Ya habías disparado en esa posición")
                return False
            casilla.hit = True
            barco = casilla.barco
            if barco.df.map(lambda x: x.hit).all().all(): # Si todas las casillas del barco tocado ya han sido tocadas
                print("¡Tocado y hundido!")
                barco.hundido = True
                self.otro_turno = True
            else: # Si el disparo ha sido un acierto pero el barco sigue teniendo posiciones sin tocar
                print("¡Tocado!")
                self.otro_turno = True
        else: # Si la coordenada apunta al agua
            self.grid.iloc[x,y] = CELDA_AGUA
            print("¡Agua!")
            self.otro_turno = False
        return True
            
    def disparo_maquina(self):
        """Método para los disparos de la máquina.
        Hace una llamada al método disparar con una coordenada aleatoria
        
        Usa la constante DIFICULTAD (variables.py) para dar múltiples intentos a la máquina

        Returns:
            Bool: False si se intenta disparar una casilla-barco ya disparada, True en el resto de casos
        """
        intentos = 0
        if DIFICULTAD < 1: DIFICULTAD = 1 # La dificultad tiene que ser mínimo 1 para que no se rompa el código
        while intentos < DIFICULTAD:
            x = random.choice(self.grid.columns)
            y = random.choice(self.grid.index)
            coordenada = x+str(y)
            if coordenada in self.posiciones_disparadas: # Si ya se ha disparado en esa posición, el intento no cuenta
                continue
            casilla = self[coordenada]
            if type(casilla) == Barco.SubBarco: # Si la casilla seleccionada contiene un barco
                if not casilla.hit: # Si no había disparado ahí antes
                    print(coordenada)
                    return self.disparar(coordenada) # Realiza el disparo
            else: # El intento ha fallado y se consume
                intentos += 1
                continue
        # Si ha agotado los intentos sin acertar, hace el disparo en la última coordenada generada
        print(coordenada)
        return self.disparar(coordenada)
            
class Barco:
    def __init__(self, eslora, player):
        """Clase Barco. En su inicialización también instancia tantos SubBarco como número de eslora tiene y los guarda en un DataFrame (atributo df)

        Args:
            eslora (int): Longitud del barco
            player (int): 1 para el jugador, 0 para la máquina
        """
        self.eslora = eslora
        self.hundido = False # Si todas las casillas que ocupa el barco han sido disparadas y, por tanto, es un "¡Tocado y hundido!"
        self.player = player
        self.df = pd.DataFrame([self.SubBarco(i, player, self) for i, sb in enumerate(range(eslora))])
        self.pos = None

    class SubBarco: # Clase anidada
        def __init__(self, pos, player, barco):
            """Clase SubBarco (anidada dentro de la clase Barco)

            Args:
                pos (int): Índice dentro de barco.df (actualmente no usado)
                player (int): 1 para el jugador, 0 para la máquina
                barco (Barco): referencia al objeto de la clase Barco al cual pertenece cada instancia de SubBarco
            """
            self.hit = False # Si la casilla que ocupa ha sido disparada y, por tanto, es un "¡Tocado!"
            self.pos = pos # No necesario en el código actual, pero puede ser útil en posteriores versiones
            self.player = player
            self.barco = barco
            
        def __str__(self):
            f"""Representación string de cada casilla-barco. Usa los carácteres definidos en las constantes de funciones.py
            Usamos el valor identificativo del atributo player (heredado de Barco, a su vez heredado de Tablero) para ocultar los barcos enemigos

            Returns:
                str: {CELDA_BARCO} si es una celda-barco del jugador sin tocar, {CELDA_TOCADO} si es una celda-barco tocada, {CELDA_VACIA} si es una celda-barco enemiga sin tocar
            """
            if self.hit:
                return CELDA_TOCADO
            else:
                if self.player:
                    return CELDA_BARCO
                else:
                    return CELDA_VACIA
                
        def hit(self):
            """Método para cambiar el atributo hit a True
            """
            self.hit = True