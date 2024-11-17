def translate_coord(coordenada):
    y, *x = coordenada
    if type(x) == list: x = ''.join(x)
    x = int(x) - 1
    y = ord(y) - 64 - 1
    return x, y

def translate_xy(x,y):
    x = str(x + 1)
    y = chr(y + 64 + 1)
    return x+y