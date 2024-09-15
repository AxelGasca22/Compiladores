class AutomataNumeros:
    def __init__(self, archivo_automata):
        self.transiciones = {}   # Diccionario para almacenar las transiciones
        self.estados = set()     # Conjunto Q de estados
        self.alfabeto = set()    # Alfabeto Σ
        self.estado_inicial = None  # Estado inicial q0
        self.estados_aceptacion = set()  # Conjunto F de estados de aceptación
        self.estado_actual = None  # Estado actual del autómata
        self.cargar_automata(archivo_automata)

    def cargar_automata(self, archivo_automata):
        with open(archivo_automata, 'r') as archivo:
            lineas = archivo.readlines()
            
            # Cargar conjunto de estados Q
            self.estados = set(lineas[0].strip().split(','))
            print(f"Estados cargados: {self.estados}")  # Depuración: imprimir estados

            # Cargar alfabeto Σ
            self.alfabeto = set(lineas[1].strip().split(','))
            print(f"Alfabeto cargado: {self.alfabeto}")  # Depuración: imprimir alfabeto

            # Cargar estado inicial q0
            self.estado_inicial = lineas[2].strip()
            print(f"Estado inicial: {self.estado_inicial}")  # Depuración: imprimir estado inicial

            # Cargar conjunto de estados de aceptación F
            self.estados_aceptacion = set(lineas[3].strip().split(','))
            print(f"Estados de aceptación: {self.estados_aceptacion}")  # Depuración: imprimir estados de aceptación

            # Cargar las transiciones δ
            for linea in lineas[4:]:
                estado_actual, entrada, estado_siguiente = linea.strip().split(',')
                if estado_actual not in self.transiciones:
                    self.transiciones[estado_actual] = {}
                self.transiciones[estado_actual][entrada] = estado_siguiente
                print(f"Transición cargada: {estado_actual} --{entrada}--> {estado_siguiente}")  # Depuración: imprimir transición cargada

    def transicion(self, caracter):
        estado_str = str(self.estado_actual)  # Convierte el estado actual a una cadena
        
        # Clasificación de entradas para manejar dígitos y símbolos especiales
        if caracter.isdigit():  # Si el carácter es un dígito, tratamos la entrada como 'digit'
            entrada = 'digit'
        elif caracter == '.':  # El punto decimal
            entrada = '.'
        elif caracter == '-':  # El signo negativo
            entrada = '-'
        else:
            entrada = caracter  # Otros caracteres posibles

        # Depuración: mostrar estado actual y entrada
        print(f"Estado actual: {estado_str}, Entrada: {entrada}")

        if estado_str in self.transiciones and entrada in self.transiciones[estado_str]:  # Verifica si existe una transición válida
            nuevo_estado = self.transiciones[estado_str][entrada]
            print(f"Transición válida: {estado_str} --{entrada}--> {nuevo_estado}")  # Depuración: transición válida
            self.estado_actual = nuevo_estado
            return True
        else:
            print(f"Transición inválida para el estado {estado_str} con entrada '{entrada}'")  # Depuración: transición inválida
            return False

    def es_numero(self, cadena):
        self.estado_actual = self.estado_inicial  # Reiniciamos al estado inicial
        print(f"\nProcesando cadena: {cadena}")  # Depuración: nueva cadena a procesar
        print(f"Estado inicial: {self.estado_actual}")  # Depuración: mostrar estado inicial

        for c in cadena:
            if not self.transicion(c):
                print(f"Cadena '{cadena}' no es válida.")  # Depuración: cadena no válida
                return False

        # Debe acabar en un estado de aceptación
        if self.estado_actual in self.estados_aceptacion:
            print(f"Cadena '{cadena}' es válida. Estado final: {self.estado_actual}")  # Depuración: cadena aceptada
            return True
        else:
            print(f"Cadena '{cadena}' no es válida. Estado final: {self.estado_actual}")  # Depuración: cadena no aceptada
            return False

# Ejemplo de uso
automata = AutomataNumeros('automata3.txt')

# Cadenas de ejemplo para probar
#cadenas = ["123", "-123", "+123", "12.34", "-0.45", "+45.67", "abc", "12.a34"]
cadenas = ["bbaaba","aaabb"]
#cadenas = ["100"]
for cadena in cadenas:
    if automata.es_numero(cadena):
        print(f"La cadena '{cadena}' es una cadena válida.")
    else:
        print(f"La cadena '{cadena}' NO es una cadena válida.")
