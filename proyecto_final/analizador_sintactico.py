class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice = 0
        self.errores = []
        self.ultimo_token_valido = None  # Nuevo atributo

    def obtener_token(self):
        token = self.tokens[self.indice] if self.indice < len(self.tokens) else None
        print(f"Procesando token: {token}")  # Depuración
        return token


    def coincidir(self, tipo, valor=None):
        token = self.obtener_token()
        if token and token[0] == tipo and (valor is None or token[1] == valor):
            self.ultimo_token_valido = token  # Actualizar solo al consumir el token
            self.indice += 1
            return True
        return False


    def registrar_error(self, mensaje, consumir=True):
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
        if consumir and self.indice < len(self.tokens):
            self.indice += 1


    def sincronizar(self, sincronizadores):
        while self.obtener_token() and self.tokens[self.indice][0] not in sincronizadores:
            self.indice += 1

    def programa(self):
        while self.obtener_token():
            if not self.funcion():
                self.registrar_error("Error en la definición de función")
                self.sincronizar(["RESERVADA", "PUNTUACION"])  # Ejemplo de sincronización

    def funcion(self):
        if not self.coincidir("RESERVADA", "funcion"):
            return False
        if not self.coincidir("IDENTIFICADOR"):
            self.registrar_error("Se esperaba un nombre de función")
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
        return True

    def parametros(self):
        if self.coincidir("IDENTIFICADOR"):
            while self.coincidir("PUNTUACION", ","):
                if not self.coincidir("IDENTIFICADOR"):
                    self.registrar_error("Se esperaba un identificador después de ','")

    def sentencias(self):
        while self.declaracion() or self.condicional() or self.llamada():
            pass

    def declaracion(self):
        if self.coincidir("RESERVADA", "entero"):
            if not self.coincidir("IDENTIFICADOR"):
                self.registrar_error("Se esperaba un identificador después del tipo de dato")
            if self.coincidir("OPERADOR", "="):
                self.expresion()
            if not self.coincidir("PUNTUACION", ";"):
                self.registrar_error("Se esperaba ';' al final de la declaración", consumir=False)
                self.sincronizar(["PUNTUACION"])
            return True
        elif self.coincidir("IDENTIFICADOR"):
            if self.coincidir("OPERADOR", "="):
                self.expresion()
                if not self.coincidir("PUNTUACION", ";"):
                    self.registrar_error("Se esperaba ';' al final de la asignación", consumir=False)
                    self.sincronizar(["PUNTUACION"])
                    return False
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
        self.expresion()
        if not self.coincidir("PUNTUACION", ")"):
            self.registrar_error("Se esperaba ')' después de la condición")
        if not self.coincidir("PUNTUACION", "{"):
            self.registrar_error("Se esperaba '{' para abrir el bloque 'si'")
        self.sentencias()
        if not self.coincidir("PUNTUACION", "}"):
            self.registrar_error("Se esperaba '}' para cerrar el bloque 'si'")
        if self.coincidir("RESERVADA", "sino"):
            if not self.coincidir("PUNTUACION", "{"):
                self.registrar_error("Se esperaba '{' para abrir el bloque 'sino'")
            self.sentencias()
            if not self.coincidir("PUNTUACION", "}"):
                self.registrar_error("Se esperaba '}' para cerrar el bloque 'sino'")
        return True

    def llamada(self):
        if not self.coincidir("RESERVADA", "imprimir"):
            return False
        if not self.coincidir("PUNTUACION", "("):
            self.registrar_error("Se esperaba '(' después de 'imprimir'")
        self.expresion()
        if not self.coincidir("PUNTUACION", ")"):
            self.registrar_error("Se esperaba ')' después de la expresión")
        if not self.coincidir("PUNTUACION", ";"):
            self.registrar_error("Se esperaba ';' después de la llamada a 'imprimir'", consumir=False)
            self.sincronizar(["PUNTUACION"])
        return True

    def expresion(self):
        if self.coincidir("IDENTIFICADOR") or self.coincidir("NUMERO"):
            if self.coincidir("RELACIONAL"):
                if not (self.coincidir("IDENTIFICADOR") or self.coincidir("NUMERO")):
                    self.registrar_error("Se esperaba un identificador o número después del operador relacional")
            while self.coincidir("OPERADOR"):
                if not (self.coincidir("IDENTIFICADOR") or self.coincidir("NUMERO")):
                    self.registrar_error("Se esperaba un identificador o número después del operador")
            return True
        return False
