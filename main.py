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
            try:
                if game.tablero_maquina.disparar(coordenada):
                    print(game.tablero_maquina)
                    print()
                    if not game.tablero_maquina.otro_turno:
                        break
            except:
                print("Parece que la coordenada que has introducido no tiene el formato correcto o se sale de las dimensiones del tablero. Inténtalo de nuevo")
            
        # Comprobación victoria
        if game.tablero_maquina.grid.map(lambda x: x.hit if type(x)==Barco.SubBarco else True).all().all():
            print("¡HAS GANADO! ¡ENHORABUENA!")
            break
        
        # Turno máquina
        print("Es el turno de la máquina...")
        print()
        while True:
            time.sleep(2)
            if game.tablero_jugador.disparo_maquina():
                print(game.tablero_jugador)
                print()
                if not game.tablero_jugador.otro_turno:
                    break
        
        # Comprobación derrota
        if game.tablero_jugador.grid.map(lambda x: x.hit if type(x)==Barco.SubBarco else True).all().all():
            print("Has perdido. Más suerte la próxima vez")
            break
        