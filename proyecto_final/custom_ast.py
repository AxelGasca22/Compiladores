# ast.py

class Nodo:
    def __init__(self, tipo, valor=None, hijos=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = hijos or []

    def __repr__(self):
        return f"Nodo(tipo='{self.tipo}', valor='{self.valor}', hijos={self.hijos})"
