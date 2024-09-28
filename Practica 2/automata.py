class Automata:
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

# Inicializamos la estructura de tokens como un diccionario de diccionarios de listas
tokens = {}

# Función para agregar una cadena evaluada a la estructura de tokens
def agregar_token(estado_actual, tipoCadenaAnterior, cadena_evaluada):
    # Si el estado actual no está en el diccionario, lo creamos
    if estado_actual not in tokens:
        tokens[estado_actual] = {}
    
    # Si el tipoCadenaAnterior no está en el diccionario del estado actual, lo creamos
    if tipoCadenaAnterior not in tokens[estado_actual]:
        tokens[estado_actual][tipoCadenaAnterior] = []
    
    # Añadimos la cadena evaluada a la lista correspondiente
    tokens[estado_actual][tipoCadenaAnterior].append(cadena_evaluada)

def transicion(Automata, caracter):
    estado_str = str(Automata.estado_actual)  # Convierte el estado actual a una cadena
    
    # Clasificación de entradas para manejar dígitos, letras y símbolos especiales
    if caracter.isdigit():  # Si el carácter es un dígito, tratamos la entrada como 'digit'
        entrada = 'numeros'
    elif caracter.isalpha():  # Si el carácter es una letra
        entrada = 'letras'
    elif caracter == '+' or caracter == '-' or caracter == '/' or caracter == '*' :
        entrada = 'operadores'
    else:
        entrada = caracter  # Otros caracteres posibles
    
    if(estado_str == ' '):
        return 3


    if estado_str in Automata.transiciones and entrada in Automata.transiciones[estado_str]:  # Verifica si existe una transición válida
        nuevo_estado = Automata.transiciones[estado_str][entrada]
        Automata.estado_actual = nuevo_estado
        if(entrada == 'letras'):
            entrada = 'identificadores'
        return entrada
    else:
        return 2

def inicio(Automata, cadena):
    Automata.estado_actual = Automata.estado_inicial  # Reiniciamos al estado inicial
    cadena_evaluada = ''
    tipoCadenaAnterior = ''

    #evaluar cada caracter
    for c in cadena:
        #guardar lo obtenido
        resultado = transicion(Automata,c)
        #si es una cadena se guarda el caracter actual en la cadena y el tipo de cadena
        if(isinstance(resultado, str)):
            cadena_evaluada += c
            tipoCadenaAnterior = resultado
        #si es una cadena se guarda en el tipo de cadena
        elif(resultado == 2):
            if(Automata.estado_actual in Automata.estados_aceptacion):
                agregar_token(int(Automata.estado_actual), tipoCadenaAnterior, cadena_evaluada)
            Automata.estado_actual = Automata.estado_inicial
            cadena_evaluada = ''
            tipoCadenaAnterior = ''
        #si es cadena vacia el resultado que priviene
        elif(resultado == 3):
            if(cadena_evaluada != ''):
                if(Automata.estado_actual in Automata.estados_aceptacion):
                    agregar_token(int(Automata.estado_actual), tipoCadenaAnterior, cadena_evaluada)
            Automata.estado_actual = Automata.estado_inicial
            tipoCadenaAnterior = ''
    if(Automata.estado_actual in Automata.estados_aceptacion):
                    agregar_token(int(Automata.estado_actual), tipoCadenaAnterior, cadena_evaluada)
            


# Ejemplo de uso
automata = Automata('./Practica 2/automata.txt')

cadena = input(f"Ingrese la cadena: ")
        
inicio(automata, cadena)

#imprimir todos los tokens
for estado, tipos in tokens.items():
    for tipo, cadenas in tipos.items():
        print(f"  Tipo '{tipo}':")
        for cadena in cadenas:
            print(f"    - {cadena}")
