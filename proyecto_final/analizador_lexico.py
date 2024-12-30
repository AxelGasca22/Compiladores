import re

TOKENS = [
    ("RESERVADA", r"\b(funcion|si|sino|imprimir|entero)\b"),  # Palabras reservadas
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
                posicion = coincidencia.end()
                columna += len(coincidencia.group())
                # Manejar saltos de línea dentro de un token (poco probable aquí, pero puede ser relevante)
                if "\n" in coincidencia.group():
                    salto_lineas = coincidencia.group().count("\n")
                    linea += salto_lineas
                    columna = len(coincidencia.group().split("\n")[-1]) + 1
                break
        if not coincidencia:
            # Manejar errores léxicos
            errores.append((codigo[posicion], linea, columna))
            if codigo[posicion] == '\n':  # Manejar salto de línea
                linea += 1
                columna = 1
            else:
                columna += 1
            posicion += 1

    return tokens, errores

