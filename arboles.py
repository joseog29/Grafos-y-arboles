"""
Módulo para implementar un Árbol Binario de Búsqueda AVL
Tipos de Datos Abstractos (TDA) con Programación Orientada a Objetos (POO)
"""


class Nodo:
    """
    Clase que representa un nodo del árbol AVL.
    
    Atributos:
        valor: Valor almacenado en el nodo
        izquierdo: Referencia al nodo hijo izquierdo
        derecho: Referencia al nodo hijo derecho
        altura: Altura del nodo en el árbol (usado para balance AVL)
    """
    
    def __init__(self, valor):
        """
        Inicializa un nodo con un valor.
        
        Args:
            valor: Valor a almacenar en el nodo
        """
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1


class ArbolAVL:
    """
    Clase que implementa un Árbol Binario de Búsqueda AVL (Auto-equilibrado).
    
    Un árbol AVL es un árbol binario de búsqueda que se mantiene equilibrado
    automáticamente. La diferencia de altura entre los subárboles izquierdo
    y derecho de cualquier nodo no excede 1.
    
    Atributos:
        raiz: Referencia al nodo raíz del árbol
    """
    
    def __init__(self):
        """Inicializa un árbol AVL vacío."""
        self.raiz = None
    
    # ==================== MÉTODOS BÁSICOS ====================
    
    def obtener_altura(self, nodo):
        """
        Obtiene la altura de un nodo.
        
        Args:
            nodo: Nodo del cual se desea obtener la altura
            
        Returns:
            int: Altura del nodo (0 si es None)
        """
        if nodo is None:
            return 0
        return nodo.altura
    
    def obtener_balance(self, nodo):
        """
        Calcula el factor de balance de un nodo.
        Factor de balance = altura_izquierda - altura_derecha
        
        Args:
            nodo: Nodo del cual se desea calcular el balance
            
        Returns:
            int: Factor de balance del nodo
        """
        if nodo is None:
            return 0
        return self.obtener_altura(nodo.izquierdo) - self.obtener_altura(nodo.derecho)
    
    def actualizar_altura(self, nodo):
        """
        Actualiza la altura de un nodo basándose en sus hijos.
        
        Args:
            nodo: Nodo cuya altura se desea actualizar
        """
        if nodo is not None:
            nodo.altura = 1 + max(self.obtener_altura(nodo.izquierdo),
                                   self.obtener_altura(nodo.derecho))
    
    # ==================== ROTACIONES ====================
    
    def rotacion_derecha(self, nodo):
        """
        Realiza una rotación a la derecha en el árbol.
        
        Caso: Árbol cargado hacia la izquierda
        
        Args:
            nodo: Nodo raíz de la rama a rotar
            
        Returns:
            Nodo: Nueva raíz después de la rotación
        """
        nuevo_padre = nodo.izquierdo
        nodo.izquierdo = nuevo_padre.derecho
        nuevo_padre.derecho = nodo
        
        self.actualizar_altura(nodo)
        self.actualizar_altura(nuevo_padre)
        
        return nuevo_padre
    
    def rotacion_izquierda(self, nodo):
        """
        Realiza una rotación a la izquierda en el árbol.
        
        Caso: Árbol cargado hacia la derecha
        
        Args:
            nodo: Nodo raíz de la rama a rotar
            
        Returns:
            Nodo: Nueva raíz después de la rotación
        """
        nuevo_padre = nodo.derecho
        nodo.derecho = nuevo_padre.izquierdo
        nuevo_padre.izquierdo = nodo
        
        self.actualizar_altura(nodo)
        self.actualizar_altura(nuevo_padre)
        
        return nuevo_padre
    
    # ==================== INSERCIÓN ====================
    
    def insertar(self, valor):
        """
        Inserta un valor en el árbol AVL manteniendo el balance.
        
        Args:
            valor: Valor a insertar
        """
        self.raiz = self._insertar_recursivo(self.raiz, valor)
    
    def _insertar_recursivo(self, nodo, valor):
        """
        Función auxiliar recursiva para insertar un valor.
        
        Args:
            nodo: Nodo actual en el proceso de inserción
            valor: Valor a insertar
            
        Returns:
            Nodo: Nodo actualizado después de la inserción y rebalanceo
        """
        # Caso base: crear nuevo nodo
        if nodo is None:
            return Nodo(valor)
        
        # Insertar en el subárbol izquierdo si valor < nodo.valor
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, valor)
        # Insertar en el subárbol derecho si valor > nodo.valor
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, valor)
        else:
            # Valor duplicado: no se inserta
            return nodo
        
        # Actualizar altura del nodo actual
        self.actualizar_altura(nodo)
        
        # Obtener el factor de balance
        balance = self.obtener_balance(nodo)
        
        # CASO 1: Desbalance izquierda-izquierda
        if balance > 1 and valor < nodo.izquierdo.valor:
            return self.rotacion_derecha(nodo)
        
        # CASO 2: Desbalance derecha-derecha
        if balance < -1 and valor > nodo.derecho.valor:
            return self.rotacion_izquierda(nodo)
        
        # CASO 3: Desbalance izquierda-derecha
        if balance > 1 and valor > nodo.izquierdo.valor:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)
        
        # CASO 4: Desbalance derecha-izquierda
        if balance < -1 and valor < nodo.derecho.valor:
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)
        
        return nodo
    
    # ==================== BÚSQUEDA ====================
    
    def buscar(self, valor):
        """
        Busca un valor en el árbol.
        
        Args:
            valor: Valor a buscar
            
        Returns:
            bool: True si el valor existe, False en caso contrario
        """
        return self._buscar_recursivo(self.raiz, valor)
    
    def _buscar_recursivo(self, nodo, valor):
        """
        Función auxiliar recursiva para buscar un valor.
        
        Args:
            nodo: Nodo actual en la búsqueda
            valor: Valor a buscar
            
        Returns:
            bool: True si el valor se encuentra, False en caso contrario
        """
        if nodo is None:
            return False
        
        if valor == nodo.valor:
            return True
        elif valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierdo, valor)
        else:
            return self._buscar_recursivo(nodo.derecho, valor)
    
    # ==================== ELIMINACIÓN ====================
    
    def eliminar(self, valor):
        """
        Elimina un valor del árbol manteniendo el balance AVL.
        
        Args:
            valor: Valor a eliminar
        """
        self.raiz = self._eliminar_recursivo(self.raiz, valor)
    
    def _eliminar_recursivo(self, nodo, valor):
        """
        Función auxiliar recursiva para eliminar un valor.
        
        Args:
            nodo: Nodo actual en el proceso de eliminación
            valor: Valor a eliminar
            
        Returns:
            Nodo: Nodo actualizado después de la eliminación y rebalanceo
        """
        if nodo is None:
            return nodo
        
        # Buscar el nodo a eliminar
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, valor)
        else:
            # Nodo encontrado, proceder con eliminación
            
            # CASO 1: Nodo sin hijos (hoja)
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            
            # CASO 2: Nodo con un solo hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            
            # CASO 3: Nodo con dos hijos
            # Encontrar el nodo mínimo en el subárbol derecho (sucesor)
            minimo = self._encontrar_minimo(nodo.derecho)
            nodo.valor = minimo.valor
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, minimo.valor)
        
        if nodo is None:
            return nodo
        
        # Actualizar altura
        self.actualizar_altura(nodo)
        
        # Rebalancear el árbol
        balance = self.obtener_balance(nodo)
        
        # CASO 1: Desbalance izquierda-izquierda
        if balance > 1 and self.obtener_balance(nodo.izquierdo) >= 0:
            return self.rotacion_derecha(nodo)
        
        # CASO 2: Desbalance izquierda-derecha
        if balance > 1 and self.obtener_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)
        
        # CASO 3: Desbalance derecha-derecha
        if balance < -1 and self.obtener_balance(nodo.derecho) <= 0:
            return self.rotacion_izquierda(nodo)
        
        # CASO 4: Desbalance derecha-izquierda
        if balance < -1 and self.obtener_balance(nodo.derecho) > 0:
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)
        
        return nodo
    
    def _encontrar_minimo(self, nodo):
        """
        Encuentra el nodo con el valor mínimo en un subárbol.
        
        Args:
            nodo: Raíz del subárbol
            
        Returns:
            Nodo: Nodo con el valor mínimo
        """
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual
    
    # ==================== RECORRIDOS ====================
    
    def recorrido_inorden(self):
        """
        Realiza un recorrido inorden (izquierda-raíz-derecha).
        
        Returns:
            list: Lista con los valores en orden inorden
        """
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _inorden_recursivo(self, nodo, resultado):
        """Función auxiliar para recorrido inorden."""
        if nodo is not None:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_recursivo(nodo.derecho, resultado)
    
    def recorrido_preorden(self):
        """
        Realiza un recorrido preorden (raíz-izquierda-derecha).
        
        Returns:
            list: Lista con los valores en orden preorden
        """
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _preorden_recursivo(self, nodo, resultado):
        """Función auxiliar para recorrido preorden."""
        if nodo is not None:
            resultado.append(nodo.valor)
            self._preorden_recursivo(nodo.izquierdo, resultado)
            self._preorden_recursivo(nodo.derecho, resultado)
    
    def recorrido_postorden(self):
        """
        Realiza un recorrido postorden (izquierda-derecha-raíz).
        
        Returns:
            list: Lista con los valores en orden postorden
        """
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _postorden_recursivo(self, nodo, resultado):
        """Función auxiliar para recorrido postorden."""
        if nodo is not None:
            self._postorden_recursivo(nodo.izquierdo, resultado)
            self._postorden_recursivo(nodo.derecho, resultado)
            resultado.append(nodo.valor)
    
    # ==================== CONSULTAS ====================
    
    def es_vacio(self):
        """
        Verifica si el árbol está vacío.
        
        Returns:
            bool: True si el árbol está vacío, False en caso contrario
        """
        return self.raiz is None
    
    def obtener_altura_arbol(self):
        """
        Obtiene la altura del árbol completo.
        
        Returns:
            int: Altura del árbol (0 si está vacío)
        """
        return self.obtener_altura(self.raiz)
    
    def contar_nodos(self):
        """
        Cuenta el número total de nodos en el árbol.
        
        Returns:
            int: Número de nodos
        """
        return self._contar_recursivo(self.raiz)
    
    def _contar_recursivo(self, nodo):
        """Función auxiliar para contar nodos."""
        if nodo is None:
            return 0
        return 1 + self._contar_recursivo(nodo.izquierdo) + self._contar_recursivo(nodo.derecho)
    
    def contar_hojas(self):
        """
        Cuenta el número de nodos hoja en el árbol.
        Una hoja es un nodo sin hijos.
        
        Returns:
            int: Número de hojas
        """
        return self._contar_hojas_recursivo(self.raiz)
    
    def _contar_hojas_recursivo(self, nodo):
        """Función auxiliar para contar hojas."""
        if nodo is None:
            return 0
        
        # Si el nodo no tiene hijos, es una hoja
        if nodo.izquierdo is None and nodo.derecho is None:
            return 1
        
        return (self._contar_hojas_recursivo(nodo.izquierdo) +
                self._contar_hojas_recursivo(nodo.derecho))
    
    def obtener_minimo(self):
        """
        Obtiene el valor mínimo del árbol.
        
        Returns:
            Valor mínimo o None si el árbol está vacío
        """
        if self.raiz is None:
            return None
        return self._encontrar_minimo(self.raiz).valor
    
    def obtener_maximo(self):
        """
        Obtiene el valor máximo del árbol.
        
        Returns:
            Valor máximo o None si el árbol está vacío
        """
        if self.raiz is None:
            return None
        nodo = self.raiz
        while nodo.derecho is not None:
            nodo = nodo.derecho
        return nodo.valor
    
    # ==================== VISUALIZACIÓN ====================
    
    def mostrar_arbol(self, nodo=None, prefijo="", es_izquierdo=None):
        """
        Muestra el árbol en la consola de forma visual.
        
        Args:
            nodo: Nodo actual (usa raíz por defecto)
            prefijo: Prefijo para alineación
            es_izquierdo: Indica si el nodo es hijo izquierdo
        """
        if nodo is None:
            nodo = self.raiz
        
        if nodo is None:
            print("Árbol vacío")
            return
        
        if es_izquierdo is None:
            print(f"[RAÍZ] {nodo.valor} (h={nodo.altura}, balance={self.obtener_balance(nodo)})")
        else:
            print(f"{prefijo}{'├─ ' if es_izquierdo else '└─ '}{nodo.valor} (h={nodo.altura}, balance={self.obtener_balance(nodo)})")
            prefijo += "│  " if es_izquierdo else "   "
        
        if nodo.izquierdo is not None or nodo.derecho is not None:
            if nodo.izquierdo is not None:
                self.mostrar_arbol(nodo.izquierdo, prefijo, True)
            if nodo.derecho is not None:
                self.mostrar_arbol(nodo.derecho, prefijo, False)


# ==================== EJEMPLO DE USO ====================

if __name__ == "__main__":
    # Crear un árbol AVL
    arbol = ArbolAVL()
    
    # Insertar valores
    valores = [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 55, 65, 90]
    
    print("=== INSERCIÓN DE VALORES ===")
    for valor in valores:
        arbol.insertar(valor)
        print(f"Insertado: {valor}")
    
    print("\n=== ÁRBOL RESULTANTE ===")
    arbol.mostrar_arbol()
    
    print("\n=== INFORMACIÓN DEL ÁRBOL ===")
    print(f"Árbol vacío: {arbol.es_vacio()}")
    print(f"Altura del árbol: {arbol.obtener_altura_arbol()}")
    print(f"Número total de nodos: {arbol.contar_nodos()}")
    print(f"Número de hojas: {arbol.contar_hojas()}")
    print(f"Valor mínimo: {arbol.obtener_minimo()}")
    print(f"Valor máximo: {arbol.obtener_maximo()}")
    
    print("\n=== RECORRIDOS ===")
    print(f"Inorden (izq-raíz-der): {arbol.recorrido_inorden()}")
    print(f"Preorden (raíz-izq-der): {arbol.recorrido_preorden()}")
    print(f"Postorden (izq-der-raíz): {arbol.recorrido_postorden()}")
    
    print("\n=== BÚSQUEDAS ===")
    print(f"¿Existe 30? {arbol.buscar(30)}")
    print(f"¿Existe 100? {arbol.buscar(100)}")
    
    print("\n=== ELIMINACIÓN DE VALORES ===")
    valores_eliminar = [5, 25, 50]
    for valor in valores_eliminar:
        arbol.eliminar(valor)
        print(f"Eliminado: {valor}")
    
    print("\n=== ÁRBOL DESPUÉS DE ELIMINACIONES ===")
    arbol.mostrar_arbol()
    
    print("\n=== INFORMACIÓN ACTUALIZADA ===")
    print(f"Número total de nodos: {arbol.contar_nodos()}")
    print(f"Número de hojas: {arbol.contar_hojas()}")
    print(f"Recorrido inorden: {arbol.recorrido_inorden()}")
