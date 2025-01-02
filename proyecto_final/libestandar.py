# libestandar.py

standard_library = {
    'imprimir_entero': {
        'params': ['entero'],
        'return_type': 'void'
    },
    'imprimir_cadena': {
        'params': ['cadena'],
        'return_type': 'void'
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
        'params': ['cadena', 'cadena'],  # derivada(funcion, variable)
        'return_type': 'cadena'
    },
    'integral': {
        'params': ['cadena', 'cadena'],  # integral(funcion, variable)
        'return_type': 'cadena'
    },
}
