# analizador_sintactico.py

import libestandar

class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice = 0
        self.errores = []
        self.ultimo_token_valido = None  # Último token consumido exitosamente
        self.en_recuperacion = False  # Nueva bandera de recuperación

        # Tabla de símbolos: Diccionario para almacenar variables y funciones
        # Estructura: { 'nombre': {'return_type': 'tipo', 'params': [...], 'es_funcion': bool}, ... }
        self.tabla_simbolos = {}

        # Pila de ámbitos para manejar scopes (por ejemplo, funciones)
        self.pila_ambitos = []  # Cada elemento es un diccionario de variables

        # Cargar la biblioteca estándar en la tabla de símbolos
        self.cargar_biblioteca_estandar()

    def cargar_biblioteca_estandar(self):
        for func_name, signature in libestandar.standard_library.items():
            self.tabla_simbolos[func_name] = {
                'return_type': signature['return_type'],  # Cambio clave a 'return_type'
                'params': signature['params'],
                'es_funcion': True
            }
            print(f"Función estándar cargada: {func_name} con parámetros {signature['params']} y retorno {signature['return_type']}")

        print("\nTabla de Símbolos Después de Cargar la Biblioteca Estándar:")
        for nombre, info in self.tabla_simbolos.items():
            print(f"{nombre}: {info}")

    def obtener_token(self):
        token = self.tokens[self.indice] if self.indice < len(self.tokens) else None
        print(f"Procesando token: {token}")  # Depuración
        return token  # No actualizar ultimo_token_valido aquí

    def coincidir(self, tipo, valor=None):
        token = self.obtener_token()
        if token and token[0] == tipo and (valor is None or token[1] == valor):
            self.ultimo_token_valido = token  # Actualizar solo al consumir el token
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
        if consumir and self.indice < len(self.tokens):
            self.indice += 1

    def sincronizar(self, sincronizadores):
        while self.obtener_token() and self.tokens[self.indice][0] not in sincronizadores:
            self.indice += 1
        # No consumir el token de sincronización para permitir su procesamiento
        self.en_recuperacion = False  # Desactivar modo de recuperación

    def programa(self):
        while self.obtener_token():
            if not self.funcion():
                self.registrar_error("Error en la definición de función")
                self.sincronizar(["RESERVADA", "PUNTUACION"])  # Ejemplo de sincronización

    def funcion(self):
        if not self.coincidir("RESERVADA", "funcion"):
            return False

        # Inicio de un nuevo ámbito (scope) para la función
        self.pila_ambitos.append({})

        if not self.coincidir("IDENTIFICADOR"):
            self.registrar_error("Se esperaba un nombre de función")
            self.sincronizar(["PUNTUACION", "RESERVADA"])  # Sincronizar para evitar más errores
            return False  # Evitar continuar si no hay nombre de función

        nombre_funcion = self.ultimo_token_valido[1]

        if not self.coincidir("PUNTUACION", "("):
            self.registrar_error("Se esperaba '(' después del nombre de la función")
        params = self.parametros()
        if not self.coincidir("PUNTUACION", ")"):
            self.registrar_error("Se esperaba ')' después de los parámetros")
        if not self.coincidir("PUNTUACION", "{"):
            self.registrar_error("Se esperaba '{' para abrir el cuerpo de la función")

        # Agregar la función a la tabla de símbolos
        self.tabla_simbolos[nombre_funcion] = {
            'return_type': 'void',  # Cambio clave a 'return_type'
            'params': params,
            'es_funcion': True
        }

        self.sentencias()

        if not self.coincidir("PUNTUACION", "}"):
            self.registrar_error("Se esperaba '}' para cerrar el cuerpo de la función")

        # Fin del ámbito de la función
        if self.pila_ambitos:
            self.pila_ambitos.pop()
        return True

    def parametros(self):
        params = []
        if self.coincidir("IDENTIFICADOR"):
            params.append('entero')  # Suponiendo que todos los parámetros son enteros; ajustar según sea necesario
            while self.coincidir("PUNTUACION", ","):
                if not self.coincidir("IDENTIFICADOR"):
                    self.registrar_error("Se esperaba un identificador después de ','")
                    self.sincronizar(["PUNTUACION"])
                    return params
                params.append('entero')  # Ajustar tipos según sea necesario
        return params

    def sentencias(self):
        while self.declaracion() or self.condicional():
            pass

    def declaracion(self):
        if self.coincidir("RESERVADA", "entero"):
            # Tipo de dato de la variable
            tipo_variable = "entero"

            if not self.coincidir("IDENTIFICADOR"):
                self.registrar_error("Se esperaba un identificador después del tipo de dato")
                self.sincronizar(["PUNTUACION"])
                return False  # Salir del método para evitar más errores

            token_variable = self.ultimo_token_valido
            nombre_variable = token_variable[1]

            # Verificar si la variable ya está declarada en el ámbito actual
            if self.esta_declarada_en_ambito_actual(nombre_variable):
                self.errores.append(
                    f"Error semántico: Variable '{nombre_variable}' ya está declarada en el ámbito actual (línea {token_variable[2]}, columna {token_variable[3]})"
                )
            else:
                # Agregar la variable a la tabla de símbolos en el ámbito actual
                self.agregar_variable(nombre_variable, tipo_variable)

            # Asignación opcional
            if self.coincidir("OPERADOR", "="):
                tipo_expresion = self.expresion()
                # Verificar tipos en la asignación
                if tipo_expresion and tipo_expresion != tipo_variable:
                    self.errores.append(
                        f"Error semántico: Tipo inconsistente en la asignación de '{nombre_variable}'. Esperado '{tipo_variable}', encontrado '{tipo_expresion}' (línea {token_variable[2]}, columna {token_variable[3]})"
                    )

            # Verificar el punto y coma
            if not self.coincidir("PUNTUACION", ";"):
                self.registrar_error("Se esperaba ';' al final de la declaración", consumir=False)
                self.sincronizar(["PUNTUACION"])
                return True  # Continuar analizando, pero evitar errores derivados
            return True

        elif self.coincidir("IDENTIFICADOR"):
            # Manejar asignaciones sin declaración previa
            token_variable = self.ultimo_token_valido
            nombre_variable = token_variable[1]

            # Verificar que la variable haya sido declarada
            tipo_variable = self.obtener_tipo_variable(nombre_variable)
            if not tipo_variable:
                self.errores.append(
                    f"Error semántico: Variable '{nombre_variable}' no declarada (línea {token_variable[2]}, columna {token_variable[3]})"
                )

            if self.coincidir("OPERADOR", "="):
                tipo_expresion = self.expresion()
                # Verificar tipos en la asignación
                if tipo_variable and tipo_expresion and tipo_expresion != tipo_variable:
                    self.errores.append(
                        f"Error semántico: Tipo inconsistente en la asignación de '{nombre_variable}'. Esperado '{tipo_variable}', encontrado '{tipo_expresion}' (línea {token_variable[2]}, columna {token_variable[3]})"
                    )
                # Verificar el punto y coma
                if not self.coincidir("PUNTUACION", ";"):
                    self.registrar_error("Se esperaba ';' al final de la asignación", consumir=False)
                    self.sincronizar(["PUNTUACION"])
                    return True
            else:
                self.registrar_error("Se esperaba '=' en la declaración")
                self.sincronizar(["PUNTUACION"])
                return False
            return True
        return False

    def condicional(self):
        if not self.coincidir("RESERVADA", "si"):
            return False
        if not self.coincidir("PUNTUACION", "("):
            self.registrar_error("Se esperaba '(' después de 'si'")
        tipo_condicion = self.expresion()
        # Aquí podrías verificar que la condición sea de tipo booleano si tu lenguaje lo soporta
        if not self.coincidir("PUNTUACION", ")"):
            self.registrar_error("Se esperaba ')' después de la condición")
        if not self.coincidir("PUNTUACION", "{"):
            self.registrar_error("Se esperaba '{' para abrir el bloque 'si'")

        # Inicio de un nuevo ámbito para el bloque 'si'
        self.pila_ambitos.append({})

        self.sentencias()

        if not self.coincidir("PUNTUACION", "}"):
            self.registrar_error("Se esperaba '}' para cerrar el bloque 'si'")

        # Fin del ámbito del bloque 'si'
        if self.pila_ambitos:
            self.pila_ambitos.pop()

        if self.coincidir("RESERVADA", "sino"):
            if not self.coincidir("PUNTUACION", "{"):
                self.registrar_error("Se esperaba '{' para abrir el bloque 'sino'")
                self.sincronizar(["PUNTUACION"])
                return False  # Evitar continuar si no se abre el bloque 'sino'
            # Inicio de un nuevo ámbito para el bloque 'sino'
            self.pila_ambitos.append({})

            self.sentencias()

            if not self.coincidir("PUNTUACION", "}"):
                self.registrar_error("Se espera '}' para cerrar el bloque 'sino'")

            # Fin del ámbito del bloque 'sino'
            if self.pila_ambitos:
                self.pila_ambitos.pop()
        return True

    def llamada(self):
        token_funcion = self.ultimo_token_valido
        nombre_funcion = token_funcion[1]

        # Verificar si la función está en la tabla de símbolos (incluyendo la biblioteca estándar)
        if nombre_funcion in self.tabla_simbolos and self.tabla_simbolos[nombre_funcion]['es_funcion']:
            # Obtener la firma de la función
            firma_funcion = self.tabla_simbolos[nombre_funcion]
            params_esperados = firma_funcion['params']
            num_params_esperados = len(params_esperados)

            if not self.coincidir("PUNTUACION", "("):
                self.registrar_error(f"Se esperaba '(' después de '{nombre_funcion}'")
                return False

            # Obtener la lista de argumentos
            argumentos = self.lista_argumentos()

            # Verificar el número de argumentos
            if len(argumentos) != num_params_esperados:
                self.errores.append(
                    f"Error semántico: La función '{nombre_funcion}' espera {num_params_esperados} argumentos, pero se recibieron {len(argumentos)} (línea {token_funcion[2]}, columna {token_funcion[3]})"
                )

            # Verificar los tipos de los argumentos
            for i, arg in enumerate(argumentos):
                tipo_arg = arg  # En tu implementación actual, `expresion()` retorna el tipo
                tipo_esperado = params_esperados[i]
                if tipo_arg != tipo_esperado:
                    self.errores.append(
                        f"Error semántico: Argumento {i+1} de la función '{nombre_funcion}' espera tipo '{tipo_esperado}', pero se encontró tipo '{tipo_arg}' (línea {token_funcion[2]}, columna {token_funcion[3]})"
                    )

            if not self.coincidir("PUNTUACION", ")"):
                self.registrar_error(f"Se esperaba ')' después de los argumentos de '{nombre_funcion}'")

            if not self.coincidir("PUNTUACION", ";"):
                self.registrar_error(f"Se esperaba ';' después de la llamada a '{nombre_funcion}'", consumir=False)
                self.sincronizar(["PUNTUACION"])

            return True
        else:
            # Manejar llamadas a funciones definidas por el usuario o reportar error si no existe
            self.errores.append(
                f"Error semántico: La función '{nombre_funcion}' no está definida (línea {token_funcion[2]}, columna {token_funcion[3]})"
            )
            self.sincronizar(["PUNTUACION"])
            return False

    def lista_argumentos(self):
        argumentos = []
        while True:
            tipo_expresion = self.expresion()
            if tipo_expresion is not None:
                argumentos.append(tipo_expresion)
            if not self.coincidir("PUNTUACION", ","):
                break
        return argumentos

    def expresion(self):
        # Aquí simplificamos asumiendo que todas las expresiones retornan su tipo
        tipo_resultado = None

        if self.coincidir("IDENTIFICADOR"):
            token_var = self.ultimo_token_valido
            nombre_var = token_var[1]

            # Verificar si el siguiente token es '(' para determinar si es una llamada a función
            if self.coincidir("PUNTUACION", "("):
                # Es una llamada a función
                argumentos = self.lista_argumentos()

                if not self.coincidir("PUNTUACION", ")"):
                    self.registrar_error(f"Se esperaba ')' después de los argumentos de la función '{nombre_var}'")

                # Validar la función
                if nombre_var in self.tabla_simbolos and self.tabla_simbolos[nombre_var]['es_funcion']:
                    firma_funcion = self.tabla_simbolos[nombre_var]
                    params_esperados = firma_funcion['params']
                    num_params_esperados = len(params_esperados)

                    # Verificar el número de argumentos
                    if len(argumentos) != num_params_esperados:
                        self.errores.append(
                            f"Error semántico: La función '{nombre_var}' espera {num_params_esperados} argumentos, pero se recibieron {len(argumentos)} (línea {token_var[2]}, columna {token_var[3]})"
                        )

                    # Verificar los tipos de los argumentos
                    for i, arg in enumerate(argumentos):
                        tipo_arg = arg  # `expresion()` retorna el tipo
                        tipo_esperado = params_esperados[i]
                        if tipo_arg != tipo_esperado:
                            self.errores.append(
                                f"Error semántico: Argumento {i+1} de la función '{nombre_var}' espera tipo '{tipo_esperado}', pero se encontró tipo '{tipo_arg}' (línea {token_var[2]}, columna {token_var[3]})"
                            )

                    # Asignar el tipo de retorno de la función
                    tipo_resultado = firma_funcion['return_type']
                else:
                    self.errores.append(
                        f"Error semántico: La función '{nombre_var}' no está definida (línea {token_var[2]}, columna {token_var[3]})"
                    )
                    tipo_resultado = None
            else:
                # Es una variable
                tipo_var = self.obtener_tipo_variable(nombre_var)
                if not tipo_var:
                    self.errores.append(
                        f"Error semántico: Variable '{nombre_var}' no declarada (línea {token_var[2]}, columna {token_var[3]})"
                    )
                tipo_resultado = tipo_var
        elif self.coincidir("NUMERO"):
            tipo_resultado = "entero"
        elif self.coincidir("CADENA"):
            tipo_resultado = "cadena"
        else:
            self.registrar_error("Se espera una expresión válida")
            return None

        # Manejar operadores relacionales
        if self.coincidir("RELACIONAL"):
            operador = self.ultimo_token_valido[1]
            tipo_operador = "relacional"
            # Asumimos que las expresiones relacionales retornan booleano
            tipo_resultado = "booleano"
            if not (self.coincidir("IDENTIFICADOR") or self.coincidir("NUMERO") or self.coincidir("CADENA")):
                self.registrar_error("Se espera un identificador, número o cadena después del operador relacional")

        # Manejar operadores aritméticos
        while self.coincidir("OPERADOR"):
            operador = self.ultimo_token_valido[1]
            tipo_operador = "aritmetico"
            # Verificar que los operandos sean del tipo correcto
            if not (self.coincidir("IDENTIFICADOR") or self.coincidir("NUMERO") or self.coincidir("CADENA")):
                self.registrar_error("Se espera un identificador, número o cadena después del operador")
            # Asumimos que las operaciones aritméticas resultan en 'entero'
            tipo_resultado = "entero"

        return tipo_resultado

    # Métodos de la Tabla de Símbolos

    def agregar_variable(self, nombre, tipo):
        if not self.pila_ambitos:
            # Si no hay ámbitos abiertos, crear uno global
            self.pila_ambitos.append({})
        ambito_actual = self.pila_ambitos[-1]
        ambito_actual[nombre] = tipo
        self.tabla_simbolos[nombre] = {
            'return_type': tipo,  # Cambio clave a 'return_type' para consistencia
            'params': [],
            'es_funcion': False
        }
        print(f"Variable '{nombre}' de tipo '{tipo}' agregada al ámbito actual.")
    
    def esta_declarada_en_ambito_actual(self, nombre_variable):
        if not self.pila_ambitos:
            return False
        ambito_actual = self.pila_ambitos[-1]
        return nombre_variable in ambito_actual
    
    def obtener_tipo_variable(self, nombre_variable):
        for ambito in reversed(self.pila_ambitos):
            if nombre_variable in ambito:
                return ambito[nombre_variable]
        return None


def main():
    # Puedes implementar un método main si lo deseas
    pass
