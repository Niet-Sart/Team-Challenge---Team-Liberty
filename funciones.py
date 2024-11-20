def translate_coord(coordenada: str) -> tuple:
    """Convierte una coordenada de formato LETRA+NÚMERO a una tupla con dos índices

    Args:
        coordenada (str): Por ejemplo: "A1"

    Returns:
        tuple: "A1" devuelve 0, 0; "A2" devuelve 1, 0; "B1" devuelve 0, 1; etc.
    """
    y, *x = coordenada.upper() # Pasamos la letra a la variable y, y las cifras a la variable x
    if type(x) == list: x = ''.join(x) # Si x es una lista (caso de coordenadas con números > 9), la pasamos a str
    x = int(x) - 1 # Los índices empiezan por 0, así que hay que restar 1
    y = ord(y) - 64 - 1 # ord("A") == 65 así que ord("A") - 64 == 1. Restamos 1 porque los índices empiezan por 0
    return x, y

def translate_xy(x: int,y: int) -> str:
    """Convierte dos índices numéricos en una coordenada de formato LETRA+NÚMERO

    Args:
        x (int): Un índice numérico en forma de entero positivo
        y (int): Un índice numérico en forma de entero positivo

    Returns:
        str: 0, 0 devuelve "A1"; 0, 1 devuelve "B1"; 1, 0 devuelve "A2"; etc.
    """
    x,y = y,x # Invertimos el orden de los ejes
    x = str(x + 1) # Los índices empiezan por 0, así que hay que sumar 1
    y = chr(y + 64 + 1) # Para hacer corresponder 0 con "A" y sucesivamente
    return x+y