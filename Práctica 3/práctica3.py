import re

class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens  # Tokens de la expresión
        self.current_token = None  # Token actual
        self.next_token()  # Avanza al primer token

    def next_token(self):
        # Avanza al siguiente token o a None si no hay más tokens
        self.current_token = self.tokens.pop(0) if self.tokens else None

    def parse_E(self):
        # E -> T + E | T - E | T
        if self.parse_T():  # Intenta parsear T
            if self.current_token == '+':
                self.next_token()  # Avanza al siguiente token
                return self.parse_E()  # Recursión para el siguiente E
            elif self.current_token == '-':
                self.next_token()  # Avanza al siguiente token
                return self.parse_E()  # Recursión para el siguiente E
            # Si no hay + o -, la producción es E -> T
            return True
        return False  # La regla E -> T falló

    def parse_T(self):
        # T -> F * T | F / T | F
        if self.parse_F():  # Intenta parsear F
            if self.current_token == '*':
                self.next_token()  # Avanza al siguiente token
                return self.parse_T()  # Recursión para el siguiente T
            elif self.current_token == '/':
                self.next_token()  # Avanza al siguiente token
                return self.parse_T()  # Recursión para el siguiente T
            # Si no hay * o /, la producción es T -> F
            return True
        return False  # La regla T -> F falló

    def parse_F(self):
        # F -> (E) | id | #
        if self.current_token == '(':
            self.next_token()  # Avanza al siguiente token
            if self.parse_E():  # Llama a parsear E dentro del paréntesis
                if self.current_token == ')':  # Verifica que cierre el paréntesis
                    self.next_token()  # Avanza al siguiente token
                    return True
                return False  # Falta el paréntesis de cierre
        elif self.current_token and (self.current_token.isalnum()):  # id o número
            self.next_token()  # Avanza al siguiente token
            return True
        return False  # No cumple con F

def tokenize(expression):
    # Divide la expresión en tokens usando una expresión regular
    token_pattern = re.compile(r'\d+|[a-zA-Z_]\w*|[()+*/-]')
    tokens = token_pattern.findall(expression)
    return tokens

def main():
    # Solicita la expresión al usuario
    expression = input("Introduce la expresión a evaluar: ")
    tokens = tokenize(expression)  # Tokeniza la expresión
    parser = AnalizadorSintactico(tokens)  # Crea el analizador con los tokens
    if parser.parse_E() and not parser.current_token:  # Comienza el análisis desde E y verifica que no haya tokens sobrantes
        print("Expresión reconocida.")
    else:
        print("Expresión no reconocida.")

# Ejecutar el programa
if __name__ == "__main__":
    main()
