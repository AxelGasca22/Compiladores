# libestandar.py

standard_library = {
    'imprimir_entero': {
        'params': ['entero'],
        'return_type': 'void',
        'es_funcion': True
    },
    'imprimir_cadena': {
        'params': ['cadena'],
        'return_type': 'void',
        'es_funcion': True
    },
    'sumar': {
        'params': ['entero', 'entero'],
        'return_type': 'entero',
        'es_funcion': True
    },
    'restar': {
        'params': ['entero', 'entero'],
        'return_type': 'entero',
        'es_funcion': True
    },
    'multiplicar': {
        'params': ['entero', 'entero'],
        'return_type': 'entero',
        'es_funcion': True
    },
    'dividir': {
        'params': ['entero', 'entero'],
        'return_type': 'entero',
        'es_funcion': True
    },
    'potencia': {
        'params': ['entero', 'entero'],
        'return_type': 'entero',
        'es_funcion': True
    },
    'raiz': {
        'params': ['entero', 'entero'],
        'return_type': 'entero',
        'es_funcion': True
    },
    'derivada': {
        'params': ['cadena', 'cadena'],  # derivada(funcion, variable)
        'return_type': 'cadena',
        'es_funcion': True
    },
    'integral': {
        'params': ['cadena', 'cadena'],  # integral(funcion, variable)
        'return_type': 'cadena',
        'es_funcion': True
    },
}
