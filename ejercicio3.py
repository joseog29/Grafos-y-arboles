# -------------------------------------------------------
# TDA: Arista (NodoArista)
# -------------------------------------------------------

class NodoArista:
    """Modela una arista saliente con su destino y peso."""
    def __init__(self, destino_id: str, peso: int):
        self.destino_id = destino_id # ID del vértice destino
        self.peso = peso
        
    def __repr__(self):
        return f"A({self.destino_id}, {self.peso})"


# -------------------------------------------------------
# TDA: Vértice (NodoVertice)
# -------------------------------------------------------

class NodoVertice:
    """Modela un nodo del grafo con su lista de adyacencia."""
    def __init__(self, id: str):
        self.id = id
        self.conexiones = [] # Lista de objetos NodoArista (Lista de adyacencia)
        
    def agregar_vecino(self, destino_id: str, peso: int):
        """Agrega una arista a la lista de conexiones."""
        self.conexiones.append(NodoArista(destino_id, peso))

    def __repr__(self):
        return f"V({self.id})"


# -------------------------------------------------------
# TDA: Grafo
# -------------------------------------------------------

class Grafo:
    def __init__(self):
        self.lista_vertices = [] # Almacena los objetos NodoVertice
        # *Mapeo auxiliar interno: Necesario para buscar por ID sin diccionarios*
        self._mapeo_id = {} 

    def agregar_vertice(self, id: str) -> NodoVertice:
        """Añade un vértice al grafo o devuelve el existente."""
        if id not in self._mapeo_id:
            nuevo_vertice = NodoVertice(id)
            self._mapeo_id[id] = len(self.lista_vertices)
            self.lista_vertices.append(nuevo_vertice)
            return nuevo_vertice
        return self.lista_vertices[self._mapeo_id[id]]
        
    def agregar_arista(self, origen_id: str, destino_id: str, peso: int):
        """Agrega la arista (dirigida) entre el origen y el destino."""
        vertice_origen = self.agregar_vertice(origen_id)
        self.agregar_vertice(destino_id)
            
        vertice_origen.agregar_vecino(destino_id, peso)

### B. TDA: Algoritmo de Dijkstra

```python
# -------------------------------------------------------
# TDA: DijkstraSolver
# -------------------------------------------------------

class DijkstraSolver:
    def __init__(self, grafo: Grafo):
        self.grafo = grafo

    def ejecutar_dijkstra(self, inicio_id: str):
        """
        Implementación de Dijkstra usando búsqueda lineal para simular la Cola de Prioridad.
        """
        num_vertices = len(self.grafo.lista_vertices)
        
        # Inicialización de distancias y estados (usando listas)
        distancias = [float('inf')] * num_vertices
        visitados = [False] * num_vertices
        
        # Obtener el índice de inicio
        inicio_idx = self.grafo._mapeo_id.get(inicio_id)
        if inicio_idx is None:
            return "Error: Vértice de inicio no encontrado."

        distancias[inicio_idx] = 0
        
        # Bucle principal de Dijkstra
        for _ in range(num_vertices):
            
            # 1. Encontrar el índice del vértice no visitado con la distancia mínima (simulación de CP)
            min_distancia = float('inf')
            vertice_actual_idx = -1
            
            for i in range(num_vertices):
                # Buscar el vértice no visitado con la distancia más corta
                if not visitados[i] and distancias[i] < min_distancia:
                    min_distancia = distancias[i]
                    vertice_actual_idx = i
            
            if vertice_actual_idx == -1:
                break
                
            # Marcar como visitado
            visitados[vertice_actual_idx] = True
            vertice_actual = self.grafo.lista_vertices[vertice_actual_idx]
            
            # 2. Relajación de aristas
            for arista in vertice_actual.conexiones:
                vecino_id = arista.destino_id
                vecino_idx = self.grafo._mapeo_id.get(vecino_id)
                peso = arista.peso
                
                # Solo relajar si el vecino no ha sido visitado
                if vecino_idx is not None and not visitados[vecino_idx]:
                    nueva_distancia = distancias[vertice_actual_idx] + peso
                    
                    if nueva_distancia < distancias[vecino_idx]:
                        distancias[vecino_idx] = nueva_distancia
                        # Aquí se actualizaría también el predecesor para reconstruir la ruta
                        
        # Formato de salida (Reconstruir ID -> Distancia para mostrar el resultado)
        resultado_distancias = {}
        for id, idx in self.grafo._mapeo_id.items():
            resultado_distancias[id] = distancias[idx]
                        
        return resultado_distancias