# libestandar.py

# Definición de la biblioteca estándar con firmas de funciones

standard_library = {
    'imprimir': {
        'params': ['entero', 'cadena', 'booleano'],  # Tipos de parámetros
        'return_type': 'void'                        # Tipo de retorno
    },
    'sumar': {
        'params': ['entero', 'entero'],
        'return_type': 'entero'
    },
    'restar': {
        'params': ['entero', 'entero'],
        'return_type': 'entero'
    },
    'multiplicar': {
        'params': ['entero', 'entero'],
        'return_type': 'entero'
    },
    'dividir': {
        'params': ['entero', 'entero'],
        'return_type': 'entero'
    },
    'potencia': {
        'params': ['entero', 'entero'],
        'return_type': 'entero'
    },
    'raiz': {
        'params': ['entero', 'entero'],
        'return_type': 'entero'
    },
    'derivada': {
        'params': ['cadena', 'cadena'],  # Por ejemplo, derivada(función, variable)
        'return_type': 'cadena'
    },
    'integral': {
        'params': ['cadena', 'cadena'],  # Por ejemplo, integral(función, variable)
        'return_type': 'cadena'
    },
}
