# analizador_semantico.py

from custom_ast import Nodo

class AnalizadorSemantico:
    def __init__(self, ast, tabla_simbolos):
        self.ast = ast
        self.tabla_simbolos = tabla_simbolos.copy()  # Copia para no modificar la original
        self.errores = []
        self.pila_ambitos = []

    def analizar(self):
        print("Iniciando análisis semántico")
        try:
            self.visitar(self.ast)
        except Exception as e:
            self.errores.append(f"Error inesperado durante el análisis semántico: {e}")
            print(f"Error inesperado durante el análisis semántico: {e}")
        print("Análisis semántico completado")
        print(f"Total de errores detectados: {len(self.errores)}")
        for error in self.errores:
            print(f"Error acumulado: {error}")
        return self.errores

    def visitar(self, nodo):
        metodo = f'visitar_{nodo.tipo}'
        visit = getattr(self, metodo, self.visitar_default)
        visit(nodo)

    def visitar_default(self, nodo):
        for hijo in nodo.hijos:
            self.visitar(hijo)

    # Métodos específicos para cada tipo de nodo
    def visitar_Programa(self, nodo):
        for funcion in nodo.hijos:
            self.visitar(funcion)

    def visitar_Funcion(self, nodo):
        nombre = nodo.valor
        parametros = [paramo.valor for paramo in nodo.hijos[0].hijos]

        print(f"Analizando función: {nombre} con parámetros {parametros}")

        if nombre in self.tabla_simbolos and self.tabla_simbolos[nombre]['es_funcion']:
            self.errores.append(f"Error semántico: Función '{nombre}' ya está definida.")
            print(f"Error: Función '{nombre}' ya está definida.")
        else:
            # Añadir función a la tabla de símbolos
            self.tabla_simbolos[nombre] = {'return_type': 'void', 'params': parametros, 'es_funcion': True}
            print(f"Función '{nombre}' añadida a la tabla de símbolos.")

        # Crear nuevo ámbito
        self.pila_ambitos.append({})
        print(f"Añadiendo nuevo ámbito para función '{nombre}'")
        for param in parametros:
            self.pila_ambitos[-1][param] = 'entero'  # Suponiendo que todos los parámetros son enteros
            print(f"Parámetro '{param}' de tipo 'entero' añadido al ámbito.")

        # Analizar sentencias dentro de la función
        self.visitar(nodo.hijos[1])  # Sentencias

        # Salir del ámbito
        self.pila_ambitos.pop()
        print(f"Abandono del ámbito de la función '{nombre}'")

    def visitar_Sentencias(self, nodo):
        for sentencia in nodo.hijos:
            self.visitar(sentencia)

    def visitar_Declaracion(self, nodo):
        tipo = nodo.hijos[0].valor
        nombre = nodo.valor
        print(f"Declarando variable '{nombre}' de tipo '{tipo}' en el ámbito actual.")

        ambito_actual = self.pila_ambitos[-1] if self.pila_ambitos else self.tabla_simbolos
        if nombre in ambito_actual:
            self.errores.append(f"Error semántico: Variable '{nombre}' ya está declarada en el ámbito actual.")
            print(f"Error: Variable '{nombre}' ya está declarada en el ámbito actual.")
        else:
            ambito_actual[nombre] = tipo
            print(f"Variable '{nombre}' añadida al ámbito.")

        # Manejar asignación
        if len(nodo.hijos) > 1:
            expr = nodo.hijos[1]
            # Añadir visita al nodo de expresión para verificar llamadas a funciones
            self.visitar(expr)
            tipo_expr = self.obtener_tipo_expresion(expr)
            print(f"Asignando expresión de tipo '{tipo_expr}' a variable '{nombre}' de tipo '{tipo}'")
            if tipo_expr != tipo:
                self.errores.append(f"Error semántico: Tipo inconsistente en la asignación de '{nombre}'. Esperado '{tipo}', encontrado '{tipo_expr}'.")
                print(f"Error: Tipo inconsistente en la asignación de '{nombre}'. Esperado '{tipo}', encontrado '{tipo_expr}'.")

    def visitar_Llamada(self, nodo):
        nombre_funcion = nodo.valor
        argumentos = nodo.hijos

        print(f"Analizando llamada a función: {nombre_funcion} con {len(argumentos)} argumentos.")

        if nombre_funcion not in self.tabla_simbolos or not self.tabla_simbolos[nombre_funcion]['es_funcion']:
            self.errores.append(f"Error semántico: La función '{nombre_funcion}' no está definida.")
            print(f"Error: La función '{nombre_funcion}' no está definida.")
            return  # Continúa con otras llamadas

        firma = self.tabla_simbolos[nombre_funcion]
        params_esperados = firma['params']
        print(f"Firma de la función '{nombre_funcion}': espera {len(params_esperados)} argumentos de tipos {params_esperados}.")

        if len(argumentos) != len(params_esperados):
            self.errores.append(f"Error semántico: La función '{nombre_funcion}' espera {len(params_esperados)} argumentos, pero se recibieron {len(argumentos)}.")
            print(f"Error: La función '{nombre_funcion}' espera {len(params_esperados)} argumentos, pero se recibieron {len(argumentos)}.")
            # No retornar aquí para seguir analizando los argumentos existentes

        # Analizar los argumentos hasta el mínimo entre esperados y recibidos
        for i, (arg, esperado) in enumerate(zip(argumentos, params_esperados), 1):
            tipo_arg = self.obtener_tipo_expresion(arg)
            print(f"Argumento {i}: tipo esperado '{esperado}', tipo encontrado '{tipo_arg}'.")
            if tipo_arg != esperado:
                self.errores.append(f"Error semántico: Argumento {i} de la función '{nombre_funcion}' espera tipo '{esperado}', pero se encontró tipo '{tipo_arg}'.")
                print(f"Error: Argumento {i} de la función '{nombre_funcion}' espera tipo '{esperado}', pero se encontró tipo '{tipo_arg}'.")

        # Detectar argumentos adicionales si los hay
        if len(argumentos) > len(params_esperados):
            for i in range(len(params_esperados) + 1, len(argumentos) + 1):
                arg = argumentos[i - 1]
                tipo_arg = self.obtener_tipo_expresion(arg)
                self.errores.append(f"Error semántico: Argumento {i} de la función '{nombre_funcion}' no es esperado.")
                print(f"Error: Argumento {i} de la función '{nombre_funcion}' no es esperado.")

    def visitar_Si(self, nodo):
        condicion = nodo.hijos[0]
        sentencias_si = nodo.hijos[1]
        sentencias_sino = nodo.hijos[2] if len(nodo.hijos) > 2 else None

        tipo_condicion = self.obtener_tipo_expresion(condicion)
        print(f"Condición del 'si' tiene tipo '{tipo_condicion}'")
        if tipo_condicion != 'booleano':
            self.errores.append("Error semántico: La condición del 'si' debe ser de tipo 'booleano'.")
            print("Error: La condición del 'si' debe ser de tipo 'booleano'.")

        # Crear nuevo ámbito para el 'si'
        self.pila_ambitos.append({})
        print("Añadiendo nuevo ámbito para el bloque 'si'")
        self.visitar(sentencias_si)
        self.pila_ambitos.pop()
        print("Abandono del ámbito del bloque 'si'")

        if sentencias_sino:
            # Crear nuevo ámbito para el 'sino'
            self.pila_ambitos.append({})
            print("Añadiendo nuevo ámbito para el bloque 'sino'")
            self.visitar(sentencias_sino)
            self.pila_ambitos.pop()
            print("Abandono del ámbito del bloque 'sino'")

    def obtener_tipo_expresion(self, nodo):
        if nodo.tipo == 'Identificador':
            nombre = nodo.valor
            tipo = self.buscar_variable(nombre)
            if not tipo:
                self.errores.append(f"Error semántico: Variable '{nombre}' no declarada.")
                print(f"Error: Variable '{nombre}' no declarada.")
                return 'undefined'
            print(f"Identificador '{nombre}' tiene tipo '{tipo}'")
            return tipo
        elif nodo.tipo == 'Numero':
            print(f"Constante numérica detectada: '{nodo.valor}' de tipo 'entero'")
            return 'entero'
        elif nodo.tipo == 'Cadena':
            print(f"Constante de cadena detectada: '{nodo.valor}' de tipo 'cadena'")
            return 'cadena'
        elif nodo.tipo == 'Llamada':
            nombre_funcion = nodo.valor
            if nombre_funcion in self.tabla_simbolos:
                tipo_retorno = self.tabla_simbolos[nombre_funcion]['return_type']
                print(f"Llamada a función '{nombre_funcion}' retorna tipo '{tipo_retorno}'")
                return tipo_retorno
            else:
                self.errores.append(f"Error semántico: Función '{nombre_funcion}' no está definida.")
                print(f"Error: Función '{nombre_funcion}' no está definida.")
                return 'undefined'
        else:
            print(f"Tipo de expresión desconocido: '{nodo.tipo}'")
            return 'undefined'

    def buscar_variable(self, nombre):
        for ambito in reversed(self.pila_ambitos):
            if nombre in ambito:
                print(f"Variable '{nombre}' encontrada en el ámbito actual con tipo '{ambito[nombre]}'")
                return ambito[nombre]
        if nombre in self.tabla_simbolos and not self.tabla_simbolos[nombre]['es_funcion']:
            print(f"Variable '{nombre}' encontrada en la tabla de símbolos global con tipo '{self.tabla_simbolos[nombre]['return_type']}'")
            return self.tabla_simbolos[nombre]['return_type']
        print(f"Variable '{nombre}' no encontrada en ningún ámbito")
        return None
