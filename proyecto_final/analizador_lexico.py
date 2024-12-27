import re

TOKENS = [
    ("RESERVADA", r"\b(funcion|si|sino|imprimir)\b"),  # Palabras reservadas
    ("IDENTIFICADOR", r"[a-zA-Z_][a-zA-Z_0-9]*"),      # Nombres de variables y funciones
    ("NUMERO", r"\b\d+\b"),                           # Números enteros
    ("OPERADOR", r"[+\-*/=]"),                        # Operadores aritméticos y asignación
    ("RELACIONAL", r"(>=|<=|==|!=|>|<)"),             # Operadores relacionales
    ("PUNTUACION", r"[;{}(),]"),                      # Caracteres de puntuación
    ("ESPACIOS", r"\s+"),                             # Ignorar espacios en blanco
]

def analizar_lexico(codigo):
    tokens = []
    errores = []
    posicion = 0

    while posicion < len(codigo):
        coincidencia = None
        for tipo, patron in TOKENS:
            regex = re.compile(patron)
            coincidencia = regex.match(codigo, posicion)
            if coincidencia:
                if tipo != "ESPACIOS":  # Ignorar espacios
                    tokens.append((tipo, coincidencia.group(), posicion))
                posicion = coincidencia.end()
                break
        if not coincidencia:
            errores.append((codigo[posicion], posicion))
            posicion += 1

    return tokens, errores
