import re

# Función de análisis LL1
def analizadorLL1(tokens):
    tablaLL1 = {
        'E': {'numero': ['T', 'Ep'], 'identificador': ['T', 'Ep'], '(': ['T', 'Ep']},
        'Ep': {'+': ['+', 'T', 'Ep'], '-': ['-', 'T', 'Ep'], ')': [''], '$': ['']},
        'T': {'numero': ['F', 'Tp'], 'identificador': ['F', 'Tp'], '(': ['F', 'Tp']},
        'Tp': {'+': [''], '-': [''], '*': ['*', 'F', 'Tp'], '/': ['/', 'F', 'Tp'], ')': [''], '$': ['']},
        'F': {'numero': ['numero'], 'identificador': ['identificador'], '(': ['(', 'E', ')']}
    }
    pila = ['$', 'E']
    num = 0
    
    while pila.__len__() > 0:
        x = pila[-1]
        a = tokens[num][0]
        if a == 'operador':
            a = tokens[num][1]
        
        if x == '$' or x == 'numero' or x == 'identificador' or x == '(' or x == ')' or x == '+' or x == '-' or x == '*' or x == '/':
            if x == a:
                pila.pop()
                num += 1
                if pila.__len__() > 0:
                    x = pila[-1]
            else:
                if a == 'identificador' or a == 'numero':
                    print(f'Error: se esperaba un número o identificador después de {tokens[num-1][1]}')
                else:
                    print(f'Error: se esperaba un operador después de {tokens[num-1][1]}')
                return False
        else:
            try:
                pila.pop()
                for i in range(len(tablaLL1[x][a])):
                    if tablaLL1[x][a][len(tablaLL1[x][a])-1-i] != '':
                        pila.append(tablaLL1[x][a][len(tablaLL1[x][a])-1-i])
            except KeyError:
                if a == 'identificador' or a == 'numero':
                    print(f'Error: se esperaba un operador después de {tokens[num-1][1]}')
                else:
                    print(f'Error: se esperaba un número o identificador después de {tokens[num-1][1]}')
                return False
    return True

# Función para tokenizar
def tokenize(expression):
    token_pattern = re.compile(r'\d+|[a-zA-Z_]\w*|[()+*/-]')
    tokens = token_pattern.findall(expression)
    
    categorized_tokens = []
    for token in tokens:
        if token.isdigit():
            categorized_tokens.append(['numero', token])
        elif re.match(r'^[a-zA-Z_]\w*$', token):
            categorized_tokens.append(['identificador', token])
        else:
            categorized_tokens.append(['operador', token])
    
    categorized_tokens.append(['$', '$'])
    return categorized_tokens
