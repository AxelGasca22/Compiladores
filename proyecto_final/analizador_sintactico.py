

class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice = 0
        self.errores = []
        self.ultimo_token_valido = None  # Último token consumido exitosamente
        self.en_recuperacion = False  # Nueva bandera de recuperación

        # Tabla de símbolos: Diccionario para almacenar variables y sus tipos
        # Estructura: { 'nombre_variable': 'tipo', ... }
        self.tabla_simbolos = {}

        # Pila de ámbitos para manejar scopes (por ejemplo, funciones)
        self.pila_ambitos = []  # Cada elemento es un diccionario de variables

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
        if self.obtener_token() and self.tokens[self.indice][0] in sincronizadores:
            self.indice += 1
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

        # Suponiendo que las funciones pueden tener parámetros, se podría manejar aquí

        if not self.coincidir("PUNTUACION", "("):
            self.registrar_error("Se esperaba '(' después del nombre de la función")
        self.parametros()
        if not self.coincidir("PUNTUACION", ")"):
            self.registrar_error("Se esperaba ')' después de los parámetros")
        if not self.coincidir("PUNTUACION", "{"):
            self.registrar_error("Se esperaba '{' para abrir el cuerpo de la función")

        self.sentencias()

        if not self.coincidir("PUNTUACION", "}"):
            self.registrar_error("Se esperaba '}' para cerrar el cuerpo de la función")

        # Fin del ámbito de la función
        if self.pila_ambitos:
            self.pila_ambitos.pop()
        return True

    def parametros(self):
        if self.coincidir("IDENTIFICADOR"):
            # Aquí podrías agregar la lógica para manejar parámetros y agregarlos a la tabla de símbolos
            while self.coincidir("PUNTUACION", ","):
                if not self.coincidir("IDENTIFICADOR"):
                    self.registrar_error("Se esperaba un identificador después de ','")
                    self.sincronizar(["PUNTUACION"])
                    return  # Salir para evitar más errores

    def sentencias(self):
        while self.declaracion() or self.condicional() or self.llamada():
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
                self.errores.append(f"Error semántico: Variable '{nombre_variable}' ya está declarada en el ámbito actual (línea {token_variable[2]}, columna {token_variable[3]})")
            else:
                # Agregar la variable a la tabla de símbolos en el ámbito actual
                self.agregar_variable(nombre_variable, tipo_variable)

            # Asignación opcional
            if self.coincidir("OPERADOR", "="):
                tipo_expresion = self.expresion()
                # Verificar tipos en la asignación
                if tipo_expresion and tipo_expresion != tipo_variable:
                    self.errores.append(f"Error semántico: Tipo inconsistente en la asignación de '{nombre_variable}'. Esperado '{tipo_variable}', encontrado '{tipo_expresion}' (línea {token_variable[2]}, columna {token_variable[3]})")

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
                self.errores.append(f"Error semántico: Variable '{nombre_variable}' no declarada (línea {token_variable[2]}, columna {token_variable[3]})")

            if self.coincidir("OPERADOR", "="):
                tipo_expresion = self.expresion()
                # Verificar tipos en la asignación
                if tipo_variable and tipo_expresion and tipo_expresion != tipo_variable:
                    self.errores.append(f"Error semántico: Tipo inconsistente en la asignación de '{nombre_variable}'. Esperado '{tipo_variable}', encontrado '{tipo_expresion}' (línea {token_variable[2]}, columna {token_variable[3]})")
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
                self.registrar_error("Se esperaba '}' para cerrar el bloque 'sino'")

            # Fin del ámbito del bloque 'sino'
            if self.pila_ambitos:
                self.pila_ambitos.pop()
        return True

    def llamada(self):
        if not self.coincidir("RESERVADA", "imprimir"):
            return False
        if not self.coincidir("PUNTUACION", "("):
            self.registrar_error("Se esperaba '(' después de 'imprimir'")
        tipo_expresion = self.expresion()
        # Podrías verificar el tipo de expresión si tu lenguaje lo requiere
        if not self.coincidir("PUNTUACION", ")"):
            self.registrar_error("Se esperaba ')' después de la expresión")
        if not self.coincidir("PUNTUACION", ";"):
            self.registrar_error("Se esperaba ';' después de la llamada a 'imprimir'", consumir=False)
            self.sincronizar(["PUNTUACION"])
            return True
        return True

    def expresion(self):
        # Aquí simplificamos asumiendo que todas las expresiones retornan su tipo
        tipo_resultado = None

        if self.coincidir("IDENTIFICADOR"):
            token_var = self.ultimo_token_valido
            nombre_var = token_var[1]
            tipo_var = self.obtener_tipo_variable(nombre_var)
            if not tipo_var:
                self.errores.append(f"Error semántico: Variable '{nombre_var}' no declarada (línea {token_var[2]}, columna {token_var[3]})")
            tipo_resultado = tipo_var
        elif self.coincidir("NUMERO"):
            tipo_resultado = "entero"
        else:
            self.registrar_error("Se esperaba una expresión válida")
            return None

        # Manejar operadores relacionales
        if self.coincidir("RELACIONAL"):
            operador = self.ultimo_token_valido[1]
            tipo_operador = "relacional"
            # Para simplificar, asumimos que las expresiones relacionales retornan booleano
            # Podrías agregar más lógica para verificar tipos si tu lenguaje lo requiere
            # Aquí simplemente retornamos un tipo ficticio 'booleano'
            tipo_resultado = "booleano"
            if not (self.coincidir("IDENTIFICADOR") or self.coincidir("NUMERO")):
                self.registrar_error("Se esperaba un identificador o número después del operador relacional")

        # Manejar operadores aritméticos
        while self.coincidir("OPERADOR"):
            operador = self.ultimo_token_valido[1]
            tipo_operador = "aritmetico"
            # Verificar que los operandos sean del tipo correcto
            if not (self.coincidir("IDENTIFICADOR") or self.coincidir("NUMERO")):
                self.registrar_error("Se esperaba un identificador o número después del operador")
            # Aquí podrías agregar más lógica para determinar el tipo_resultado basado en los operandos
            # Por simplicidad, asumimos que las operaciones aritméticas resultan en 'entero'
            tipo_resultado = "entero"

        return tipo_resultado

    # Métodos de la Tabla de Símbolos

    def agregar_variable(self, nombre, tipo):
        if not self.pila_ambitos:
            # Si no hay ámbitos abiertos, crear uno global
            self.pila_ambitos.append({})
        ambito_actual = self.pila_ambitos[-1]
        ambito_actual[nombre] = tipo
        self.tabla_simbolos[nombre] = tipo
        print(f"Variable '{nombre}' de tipo '{tipo}' agregada al ámbito actual.")

    def esta_declarada_en_ambito_actual(self, nombre):
        if not self.pila_ambitos:
            return False
        ambito_actual = self.pila_ambitos[-1]
        return nombre in ambito_actual

    def obtener_tipo_variable(self, nombre):
        # Busca la variable en los ámbitos desde el más interno al más externo
        for ambito in reversed(self.pila_ambitos):
            if nombre in ambito:
                return ambito[nombre]
        return None
