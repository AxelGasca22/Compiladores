import re

TOKENS = [
    ("RESERVADA", r"\b(funcion|si|sino|imprimir|entero)\b"),  # Palabras reservadas
    ("CADENA", r'"[^"\n]*"'),                                 # Cadenas de texto entre comillas dobles
    ("IDENTIFICADOR", r"[a-zA-Z_][a-zA-Z_0-9]*"),             # Nombres de variables y funciones
    ("NUMERO", r"\b\d+\b"),                                   # Números enteros
    ("OPERADOR", r"[+\-*/=]"),                                # Operadores aritméticos y asignación
    ("RELACIONAL", r"(>=|<=|==|!=|>|<)"),                     # Operadores relacionales
    ("PUNTUACION", r"[;{}(),]"),                              # Caracteres de puntuación
    ("ESPACIOS", r"\s+"),                                     # Ignorar espacios en blanco
]

def analizar_lexico(codigo):
    tokens = []
    errores = []
    posicion = 0
    linea = 1
    columna = 1

    while posicion < len(codigo):
        coincidencia = None
        for tipo, patron in TOKENS:
            regex = re.compile(patron)
            coincidencia = regex.match(codigo, posicion)
            if coincidencia:
                if tipo != "ESPACIOS":  # Ignorar espacios
                    tokens.append((tipo, coincidencia.group(), linea, columna))
                # Actualizar posición y columna
                token_text = coincidencia.group()
                posicion = coincidencia.end()
                lines = token_text.split('\n')
                if len(lines) > 1:
                    linea += len(lines) - 1
                    columna = len(lines[-1]) + 1
                else:
                    columna += len(token_text)
                break
        if not coincidencia:
            # Manejar errores léxicos
            char = codigo[posicion]
            errores.append((char, linea, columna))
            if char == '\n':  # Manejar salto de línea
                linea += 1
                columna = 1
            else:
                columna += 1
            posicion += 1

    return tokens, errores
