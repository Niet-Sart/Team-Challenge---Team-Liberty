from variables import *
from clases import *
from funciones import *

import time

if __name__ == '__main__':
    game = Battleship()
    print(f"Tu tablero:\n{game.tablero_jugador}")
    print()
    while True:
        
        # Turno jugador
        print(f"Tablero rival:\n{game.tablero_maquina}")
        print()
        
        while True:
            coordenada = input("Es tu turno. Introduce una coordenada con el formato LETRA+NÚMERO (por ejemplo: A1): ")
            try: # Usamos un try... except porque el método al que vamos a llamar tiene varios errores definidos, pero no queremos parar la ejecución
                if game.tablero_maquina.disparar(coordenada): # Este método retorna False si se intenta disparar un barco ya disparado, y True en el resto de casos
                    print(game.tablero_maquina)
                    print()
                    # Tenemos otro turno si acertamos, en caso contrario se para el while anidado. También se para si ya no quedan barcos por disparar
                    if not game.tablero_maquina.otro_turno or game.tablero_maquina.grid.map(lambda x: x.hit if type(x)==Barco.SubBarco else True).all().all():
                        break
            except: # En vez de parar la ejecución con un RaiseError, imprimimos una advertencia por pantalla y seguimos en el while anidado
                print("Parece que la coordenada que has introducido no tiene el formato correcto o se sale de las dimensiones del tablero. Inténtalo de nuevo")
            
        # Comprobación victoria
        if game.tablero_maquina.grid.map(lambda x: x.hit if type(x)==Barco.SubBarco else True).all().all(): # Comprobamos el estado de todas las posiciones donde hay barco
            print("¡HAS GANADO! ¡ENHORABUENA!")
            break
        
        # Turno máquina
        print("Es el turno de la máquina...")
        print()
        while True:
            # El try... except no es necesario en el turno de la máquina, ya que el método disparo_maquina lidia con las excepciones del método disparar
            time.sleep(2) # Añadimos una pausa entre posibles disparos para poder seguir el progreso en pantalla
            if game.tablero_jugador.disparo_maquina():
                print(game.tablero_jugador)
                print()
                # Tiene otro turno si acierta, en caso contrario se para el while anidado. También se para si ya no quedan barcos por disparar
                if not game.tablero_jugador.otro_turno or game.tablero_jugador.grid.map(lambda x: x.hit if type(x)==Barco.SubBarco else True).all().all():
                    break
        
        # Comprobación derrota
        if game.tablero_jugador.grid.map(lambda x: x.hit if type(x)==Barco.SubBarco else True).all().all(): # Comprobamos el estado de todas las posiciones donde hay barco
            print("Has perdido. Más suerte la próxima vez")
            break
        