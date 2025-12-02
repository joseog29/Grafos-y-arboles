# -------------------------------------------------------
# TDA: Nodo del Árbol
# -------------------------------------------------------

class NodoArbol:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1 

    def __repr__(self):
        return f"Nodo({self.valor})"


# -------------------------------------------------------
# TDA: Árbol Binario de Búsqueda (ABB)
# -------------------------------------------------------

class ArbolABB:
    def __init__(self):
        self.raiz = None
    
    # --- 1. Inserción ---
    def insertar(self, valor):
        self.raiz = self._insertar_recursivo(self.raiz, valor)
    
    def _insertar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return NodoArbol(valor)
        
        if valor < nodo_actual.valor:
            nodo_actual.izquierdo = self._insertar_recursivo(nodo_actual.izquierdo, valor)
        elif valor > nodo_actual.valor:
            nodo_actual.derecho = self._insertar_recursivo(nodo_actual.derecho, valor)
        
        return nodo_actual
        
    # --- 2. Eliminación (Con Criterio de Reemplazo) ---
    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return nodo_actual

        if valor < nodo_actual.valor:
            nodo_actual.izquierdo = self._eliminar_recursivo(nodo_actual.izquierdo, valor)
        elif valor > nodo_actual.valor:
            nodo_actual.derecho = self._eliminar_recursivo(nodo_actual.derecho, valor)
        else:
            # Caso 1: Cero o Un hijo
            if nodo_actual.izquierdo is None:
                return nodo_actual.derecho
            elif nodo_actual.derecho is None:
                return nodo_actual.izquierdo
            
            # Caso 2: Dos hijos -> Usar el Menor de los Mayores (Mínimo Subárbol Derecho)
            sucesor = self._encontrar_minimo(nodo_actual.derecho)
            nodo_actual.valor = sucesor.valor 
            nodo_actual.derecho = self._eliminar_recursivo(nodo_actual.derecho, sucesor.valor)

        return nodo_actual

    def _encontrar_minimo(self, nodo):
        """Busca el sucesor in-orden (nodo más a la izquierda)."""
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    # --- 3. Recorrido In-orden ---
    def inorden(self):
        resultado = []
        self._recorrido_inorden(self.raiz, resultado)
        return resultado
        
    def _recorrido_inorden(self, nodo_actual, resultado):
        if nodo_actual is not None:
            self._recorrido_inorden(nodo_actual.izquierdo, resultado)
            resultado.append(nodo_actual.valor)
            self._recorrido_inorden(nodo_actual.derecho, resultado)

# =======================================================
# LÍNEAS PARA INSERTAR Y ELIMINAR (PRUEBA)
# =======================================================

# 1. Crear el árbol
abb = ArbolABB()
valores_a_insertar = [50, 30, 70, 20, 45, 65, 80, 40]

# 2. Insertar valores
print("--- INSERCIÓN DE VALORES ---")
for valor in valores_a_insertar:
    abb.insertar(valor)
    print(f"Insertado: {valor}")

print(f"\nContenido In-orden inicial: {abb.inorden()}") # Debe ser [20, 30, 40, 45, 50, 65, 70, 80]

# 3. Eliminar casos específicos:

# Prueba 3.a: Eliminar una hoja (fácil)
valor_eliminar_hoja = 40
abb.eliminar(valor_eliminar_hoja)
print(f"\n--- ELIMINACIÓN de hoja ({valor_eliminar_hoja}) ---")
print(f"Contenido In-orden tras eliminar 40: {abb.inorden()}") 
# Debe ser [20, 30, 45, 50, 65, 70, 80]

# Prueba 3.b: Eliminar un nodo con dos hijos (difícil, aplica el criterio de reemplazo)
valor_eliminar_dos_hijos = 70 
# El sucesor de 70 es 80.
abb.eliminar(valor_eliminar_dos_hijos) 
print(f"\n--- ELIMINACIÓN de nodo con dos hijos ({valor_eliminar_dos_hijos}) ---")
print(f"Contenido In-orden tras eliminar 70: {abb.inorden()}")
# Debe ser [20, 30, 45, 50, 65, 80] (El 70 fue reemplazado por 80, y el 80 original fue eliminado)