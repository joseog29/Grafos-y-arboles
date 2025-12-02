# -------------------------------------------------------
# TDA: Elemento de la Cola (Clase Auxiliar)
# -------------------------------------------------------

class ElementoCola:
    """Clase auxiliar para almacenar valor y prioridad juntos."""
    def __init__(self, valor, prioridad):
        self.valor = valor
        self.p = prioridad # Prioridad del elemento (clave del montículo)

    def __repr__(self):
        return f"({self.valor}, P:{self.p})"


# -------------------------------------------------------
# TDA: Cola de Prioridad (Implementada con Montículo/Heap)
# -------------------------------------------------------

class ColaPrioridad:
    def __init__(self, datos_iniciales=None):
        """
        Constructor que inicializa y, si hay datos, llama a _construir_monticulo (Heapify).
        """
        self.datos = [] 
        if datos_iniciales:
            self.datos = [ElementoCola(v, p) for v, p in datos_iniciales]
            self._construir_monticulo() 

    def __repr__(self):
        """Muestra el estado interno del montículo (lista)."""
        return f"Montículo Actual: {self.datos}"

    
    # --- B. Constructor y Ajuste Inicial ---

    def _construir_monticulo(self):
        """
        Método 'Heapify': Construye el montículo llamando a _hundir 
        desde el último nodo padre hacia la raíz.
        """
        tamano = len(self.datos)
        indice_inicio = tamano // 2 - 1 
        
        for i in range(indice_inicio, -1, -1):
            self._hundir(i)


    # --- C. Métodos de Ajuste (Hundir y Flotar) ---

    def _flotar(self, indice: int):
        """
        Ajusta el elemento hacia arriba (Heapify Up) tras una inserción.
        """
        padre_indice = (indice - 1) // 2
        
        # Usamos el atributo .p (prioridad)
        while indice > 0 and self.datos[indice].p > self.datos[padre_indice].p:
            # Intercambiar (swap)
            self.datos[indice], self.datos[padre_indice] = self.datos[padre_indice], self.datos[indice]
            indice = padre_indice
            padre_indice = (indice - 1) // 2

    def _hundir(self, indice: int):
        """
        Ajusta el elemento hacia abajo (Heapify Down) tras una extracción.
        """
        tamano = len(self.datos)
        
        while True:
            max_hijo = indice
            hijo_izq = 2 * indice + 1
            hijo_der = 2 * indice + 2
            
            # 1. Comparar con hijo izquierdo
            if hijo_izq < tamano and self.datos[hijo_izq].p > self.datos[max_hijo].p:
                max_hijo = hijo_izq
                
            # 2. Comparar con hijo derecho
            if hijo_der < tamano and self.datos[hijo_der].p > self.datos[max_hijo].p:
                max_hijo = hijo_der
                
            if max_hijo == indice:
                break
                
            # Intercambia y continúa
            self.datos[indice], self.datos[max_hijo] = self.datos[max_hijo], self.datos[indice]
            indice = max_hijo


    # --- D. Operaciones del TDA ---

    def insertar(self, valor, prioridad):
        """Inserta un nuevo elemento en la cola de prioridad."""
        self.datos.append(ElementoCola(valor, prioridad))
        self._flotar(len(self.datos) - 1)
        
    def extraer_max(self):
        """Extrae la raíz (elemento de máxima prioridad)."""
        if not self.datos:
            # Manejo de cola vacía
            return None
        
        if len(self.datos) == 1:
            return self.datos.pop().valor
        
        # Intercambiar la raíz con el último elemento
        max_elemento = self.datos[0]
        self.datos[0] = self.datos.pop()
        
        self._hundir(0)
        
        return max_elemento.valor