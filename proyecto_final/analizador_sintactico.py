class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice = 0
        self.errores = []  # Lista para almacenar errores

    def obtener_token(self):
        return self.tokens[self.indice] if self.indice < len(self.tokens) else None

    def coincidir(self, tipo, valor=None):
        token = self.obtener_token()
        if token and token[0] == tipo and (valor is None or token[1] == valor):
            self.indice += 1
            return True
        return False

    def registrar_error(self, mensaje):
        token = self.obtener_token()
        if token:
            self.errores.append(f"{mensaje} en el token '{token[1]}' en la posición {self.indice}")
        else:
            self.errores.append(f"{mensaje} al final del archivo")

    def programa(self):
        while self.obtener_token():
            if not self.funcion():
                self.registrar_error("Error en la definición de función")
                self.indice += 1  # Avanzar para evitar bucle infinito

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
        if not self.coincidir("IDENTIFICADOR"):
            return False
        if not self.coincidir("OPERADOR", "="):
            self.registrar_error("Se esperaba '=' en la declaración")
        self.expresion()
        if not self.coincidir("PUNTUACION", ";"):
            self.registrar_error("Se esperaba ';' al final de la declaración")
        return True

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
            self.registrar_error("Se esperaba ';' después de la llamada a 'imprimir'")
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
