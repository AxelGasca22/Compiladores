from ply import lex, yacc

# ---------------------------
# Analizador Léxico
# ---------------------------
tokens = (
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'EQUAL',
    'SEMICOLON', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'FUNCION', 'ENTERO'
)

reserved = {
    'funcion': 'FUNCION',
    'entero': 'ENTERO',
}

t_PLUS = r'\+'
t_MINUS = r'-'
t_EQUAL = r'='
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    num_newlines = len(t.value)
    t.lexer.lineno += num_newlines
    print(f"Newline detected. Total lines: {t.lexer.lineno}")  # Depuración

def t_error(t):
    print(f"Token no válido: {t.value[0]!r}")
    t.lexer.skip(1)

lexer = lex.lex()

# ---------------------------
# Analizador Sintáctico
# ---------------------------
precedence = (
    ('left', 'PLUS', 'MINUS'),
)

# Lista global para errores
parser_errors = []

def p_programa(p):
    '''programa : FUNCION ID LPAREN RPAREN LBRACE declaraciones RBRACE'''
    print("Programa reconocido")

def p_declaraciones(p):
    '''declaraciones : declaraciones declaracion
                     | declaracion'''
    pass

def p_declaracion_asignacion(p):
    '''declaracion : ID EQUAL expresion SEMICOLON'''
    print(f"Asignación: {p[1]} = {p[3]}")

def p_declaracion_entero_asignado(p):
    '''declaracion : ENTERO ID EQUAL expresion SEMICOLON'''
    print(f"Declaración: {p[2]} = {p[4]}")

def p_declaracion_entero_no_asignado(p):
    '''declaracion : ENTERO ID SEMICOLON'''
    print(f"Declaración: {p[2]} sin asignar")

def p_expresion_binaria(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion'''
    p[0] = f"{p[1]} {p[2]} {p[3]}"
    print(f"Expresión procesada: {p[0]}")

def p_expresion_number(p):
    '''expresion : NUMBER'''
    p[0] = p[1]

def p_expresion_id(p):
    '''expresion : ID'''
    p[0] = p[1]

def p_error(p):
    """Maneja errores de análisis sintáctico y permite la recuperación."""
    global parser_errors
    if p:
        error_message = f"Error de sintaxis en el token '{p.value}' (tipo: {p.type}) en línea {p.lineno}."
        print(error_message)  # Depuración
        parser_errors.append(error_message)
        # Recuperación: Saltar tokens hasta el próximo punto y coma o llave de cierre
        while True:
            tok = parser.token()  # Obtener el siguiente token
            if not tok:
                break  # Fin del archivo
            if tok.type in ['SEMICOLON', 'RBRACE']:
                break  # Punto y coma o llave de cierre encontrado
        parser.errok()  # Resetear el estado de error del parser
    else:
        error_message = "Error de sintaxis: Entrada incompleta o inesperada."
        print(error_message)  # Depuración
        parser_errors.append(error_message)


parser = yacc.yacc()
