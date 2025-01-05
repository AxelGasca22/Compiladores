# analizador_sintactico.py (actualizado con depuración)

import libestandar
from custom_ast import Nodo

class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice = 0
        self.errores = []
        self.ultimo_token_valido = None
        self.en_recuperacion = False

        # Tabla de símbolos: Diccionario para almacenar variables y funciones
        # Estructura: { 'nombre': {'return_type': 'tipo', 'params': [...], 'es_funcion': bool}, ... }
        self.tabla_simbolos = {}

        # Cargar la biblioteca estándar en la tabla de símbolos
        self.cargar_biblioteca_estandar()

    def cargar_biblioteca_estandar(self):
        for func_name, signature in libestandar.standard_library.items():
            self.tabla_simbolos[func_name] = {
                'return_type': signature['return_type'],
                'params': signature['params'],
                'es_funcion': signature['es_funcion']
            }
            print(f"Función estándar cargada: {func_name} con parámetros {signature['params']} y retorno {signature['return_type']}")

        print("\nTabla de Símbolos Después de Cargar la Biblioteca Estándar:")
        for nombre, info in self.tabla_simbolos.items():
            print(f"{nombre}: {info}")

    def obtener_token(self):
        return self.tokens[self.indice] if self.indice < len(self.tokens) else None

    def coincidir(self, tipo, valor=None):
        token = self.obtener_token()
        if token and token[0] == tipo and (valor is None or token[1] == valor):
            self.ultimo_token_valido = token
            print(f"Coincidir: {token} en índice {self.indice}")
            self.indice += 1
            return True
        return False

    def registrar_error(self, mensaje, consumir=True):
        if not self.en_recuperacion:
            if self.ultimo_token_valido:
                tipo, valor, linea, columna = self.ultimo_token_valido
                self.errores.append(f"{mensaje} después de '{valor}' en la línea {linea}, columna {columna}")
            else:
                token = self.obtener_token()
                if token:
                    tipo, valor, linea, columna = token
                    self.errores.append(f"{mensaje} en la línea {linea}, columna {columna} (token '{valor}')")
                else:
                    self.errores.append(f"{mensaje} al final del archivo")
            self.en_recuperacion = True  # Activar modo de recuperación
            print(f"Error: {self.errores[-1]}")
        if consumir and self.indice < len(self.tokens):
            print(f"Consumir token: {self.tokens[self.indice]} en índice {self.indice}")
            self.indice += 1

    def sincronizar(self, sincronizadores):
        print(f"Sincronizar buscando {sincronizadores} desde índice {self.indice}")
        while self.obtener_token() and self.tokens[self.indice][0] not in sincronizadores:
            print(f"Sincronizando: descartando {self.tokens[self.indice]}")
            self.indice += 1
        self.en_recuperacion = False  # Desactivar modo de recuperación

    def programa(self):
        ast = Nodo('Programa', hijos=[])
        print("Iniciando análisis de programa")
        while self.obtener_token():
            nodo_funcion = self.funcion()
            if nodo_funcion:
                ast.hijos.append(nodo_funcion)
                print(f"Función '{nodo_funcion.valor}' agregada al AST")
            else:
                self.registrar_error("Error en la definición de función")
                self.sincronizar(["RESERVADA", "PUNTUACION"])
        print("Análisis de programa completado")
        return ast

    def funcion(self):
        print(f"Intentando parsear función en índice {self.indice}")
        if not self.coincidir("RESERVADA", "funcion"):
            print("No se encontró la palabra reservada 'funcion'")
            return None

        if not self.coincidir("IDENTIFICADOR"):
            self.registrar_error("Se esperaba un nombre de función")
            self.sincronizar(["PUNTUACION", "RESERVADA"])
            return None

        nombre_funcion = self.ultimo_token_valido[1]
        print(f"Nombre de función detectado: {nombre_funcion}")

        if not self.coincidir("PUNTUACION", "("):
            self.registrar_error("Se esperaba '(' después del nombre de la función")
        params = self.parametros()
        if not self.coincidir("PUNTUACION", ")"):
            self.registrar_error("Se esperaba ')' después de los parámetros")
        if not self.coincidir("PUNTUACION", "{"):
            self.registrar_error("Se esperaba '{' para abrir el cuerpo de la función")

        nodo_funcion = Nodo('Funcion', valor=nombre_funcion, hijos=[
            Nodo('Parametros', hijos=[Nodo('Parametro', valor=p) for p in params]),
            self.sentencias()
        ])

        if not self.coincidir("PUNTUACION", "}"):
            self.registrar_error("Se esperaba '}' para cerrar el cuerpo de la función")

        return nodo_funcion

    def parametros(self):
        params = []
        print(f"Parseando parámetros en índice {self.indice}")
        if self.coincidir("IDENTIFICADOR"):
            params.append(self.ultimo_token_valido[1])
            while self.coincidir("PUNTUACION", ","):
                if not self.coincidir("IDENTIFICADOR"):
                    self.registrar_error("Se esperaba un identificador después de ','")
                    self.sincronizar(["PUNTUACION"])
                    return params
                params.append(self.ultimo_token_valido[1])
        print(f"Parámetros detectados: {params}")
        return params

    def sentencias(self):
        sentencias = []
        print(f"Inicio de parseo de sentencias en índice {self.indice}")
        while True:
            nodo = self.declaracion()
            if nodo:
                sentencias.append(nodo)
                print(f"Declaración '{nodo.valor}' agregada al AST")
                continue
            nodo = self.condicional()
            if nodo:
                sentencias.append(nodo)
                print(f"Condicional agregada al AST")
                continue
            nodo = self.llamada()
            if nodo:
                sentencias.append(nodo)
                print(f"Llamada a función '{nodo.valor}' agregada al AST")
                continue
            break  # Si ninguna de las sentencias coincide, salir del bucle
        print(f"Fin de parseo de sentencias en índice {self.indice}")
        return Nodo('Sentencias', hijos=sentencias)

    def declaracion(self):
        if self.coincidir("RESERVADA", "entero"):
            tipo = "entero"
            if not self.coincidir("IDENTIFICADOR"):
                self.registrar_error("Se esperaba un identificador después del tipo de dato")
                self.sincronizar(["PUNTUACION"])
                return None
            nombre_var = self.ultimo_token_valido[1]
            print(f"Declaración de variable detectada: {nombre_var} de tipo {tipo}")
            nodo_declaracion = Nodo('Declaracion', valor=nombre_var, hijos=[Nodo('Tipo', valor=tipo)])
            if self.coincidir("OPERADOR", "="):
                expr = self.expresion()
                if expr:
                    nodo_declaracion.hijos.append(expr)
            if not self.coincidir("PUNTUACION", ";"):
                self.registrar_error("Se esperaba ';' al final de la declaración", consumir=False)
                self.sincronizar(["PUNTUACION"])
            return nodo_declaracion
        return None

    def condicional(self):
        if not self.coincidir("RESERVADA", "si"):
            return None
        if not self.coincidir("PUNTUACION", "("):
            self.registrar_error("Se esperaba '(' después de 'si'")
        condicion = self.expresion()
        if not self.coincidir("PUNTUACION", ")"):
            self.registrar_error("Se esperaba ')' después de la condición")
        if not self.coincidir("PUNTUACION", "{"):
            self.registrar_error("Se esperaba '{' para abrir el bloque 'si'")
        sentencias_si = self.sentencias()
        if not self.coincidir("PUNTUACION", "}"):
            self.registrar_error("Se esperaba '}' para cerrar el bloque 'si'")
        nodo_condicional = Nodo('Si', hijos=[condicion, sentencias_si])

        if self.coincidir("RESERVADA", "sino"):
            if not self.coincidir("PUNTUACION", "{"):
                self.registrar_error("Se esperaba '{' para abrir el bloque 'sino'")
                self.sincronizar(["PUNTUACION"])
                return nodo_condicional
            sentencias_sino = self.sentencias()
            if not self.coincidir("PUNTUACION", "}"):
                self.registrar_error("Se esperaba '}' para cerrar el bloque 'sino'")
            nodo_condicional.hijos.append(sentencias_sino)
        return nodo_condicional

    def llamada(self):
        if not self.coincidir("IDENTIFICADOR"):
            return None
        nombre_funcion = self.ultimo_token_valido[1]
        print(f"Llamada a función detectada: {nombre_funcion}")
        if not self.coincidir("PUNTUACION", "("):
            self.registrar_error(f"Se esperaba '(' después de '{nombre_funcion}'")
            return None
        args = self.lista_argumentos()
        if not self.coincidir("PUNTUACION", ")"):
            self.registrar_error(f"Se esperaba ')' después de los argumentos de '{nombre_funcion}'")
        if not self.coincidir("PUNTUACION", ";"):
            self.registrar_error(f"Se esperaba ';' después de la llamada a '{nombre_funcion}'", consumir=False)
            self.sincronizar(["PUNTUACION"])
        nodo_llamada = Nodo('Llamada', valor=nombre_funcion, hijos=args)
        print(f"Llamada a función '{nombre_funcion}' agregada al AST")
        return nodo_llamada

    def lista_argumentos(self):
        args = []
        print(f"Parseando lista de argumentos en índice {self.indice}")
        if self.obtener_token() and self.tokens[self.indice][0] != "PUNTUACION" and self.tokens[self.indice][1] != ")":
            arg = self.expresion()
            if arg:
                args.append(arg)
            while self.coincidir("PUNTUACION", ","):
                arg = self.expresion()
                if arg:
                    args.append(arg)
        print(f"Argumentos detectados: {args}")
        return args

    def expresion(self):
        # Simplificación: retorna un nodo de Identificador, Llamada, Numero o Cadena
        if self.coincidir("IDENTIFICADOR"):
            nombre = self.ultimo_token_valido[1]
            print(f"Expresión con Identificador detectado: {nombre}")
            # Verificar si el siguiente token es '(' para determinar si es una llamada a función
            if self.coincidir("PUNTUACION", "("):
                print(f"Expresión detectada como llamada a función: {nombre}")
                args = self.lista_argumentos()
                if not self.coincidir("PUNTUACION", ")"):
                    self.registrar_error(f"Se espera ')' después de los argumentos de la función '{nombre}'")
                nodo_llamada = Nodo('Llamada', valor=nombre, hijos=args)
                return nodo_llamada
            else:
                nodo_identificador = Nodo('Identificador', valor=nombre)
                return nodo_identificador
        elif self.coincidir("NUMERO"):
            valor = self.ultimo_token_valido[1]
            print(f"Expresión con Número detectado: {valor}")
            nodo_numero = Nodo('Numero', valor=valor)
            return nodo_numero
        elif self.coincidir("CADENA"):
            valor = self.ultimo_token_valido[1]
            print(f"Expresión con Cadena detectada: {valor}")
            nodo_cadena = Nodo('Cadena', valor=valor)
            return nodo_cadena
        else:
            self.registrar_error("Se espera una expresión válida")
            return None
