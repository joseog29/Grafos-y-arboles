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

# ======================================================
# 3. ALGORITMO DIJKSTRA (SIN DICCIONARIOS EN LA LÓGICA)
# ======================================================

def buscar_vertice(grafo, info):
    """Función de búsqueda mantenida."""
    aux = grafo.inicio
    while aux is not None:
        if aux.info == info:
            return aux
        aux = aux.sig
    return None

def dijkstra_sin_dict(grafo, origen_id, destino_id):
    
    # --- A. PREPARACIÓN E INICIALIZACIÓN ---
    # Reiniciar todos los nodos (necesario si dijkstra se llama varias veces)
    aux = grafo.inicio
    while aux is not None:
        aux.distancia = float('inf')
        aux.anterior = None
        aux.visitado = False
        aux = aux.sig
    
    # Nodo de origen
    nodo_origen = buscar_vertice(grafo, origen_id)
    if nodo_origen is None:
        return [], float('inf')
        
    nodo_origen.distancia = 0

    # --- B. BUCLE PRINCIPAL (Vuelve al inicio del grafo en cada iteración) ---
    for _ in range(grafo.tamano):
        
        # 1. SELECCIÓN: Buscar el nodo NO visitado con la distancia más pequeña
        actual_id = None
        menor_distancia = float('inf')
        
        # Recorremos la lista completa de vértices del grafo
        aux = grafo.inicio
        while aux is not None:
            if not aux.visitado and aux.distancia < menor_distancia:
                menor_distancia = aux.distancia
                actual_id = aux.info
            aux = aux.sig
            
        # Si no encontramos nada, paramos (grafo desconectado o terminado)
        if actual_id is None:
            break
            
        # 2. OBTENER Y MARCAR
        nodo_actual = buscar_vertice(grafo, actual_id)
        if nodo_actual is None: continue 
        
        nodo_actual.visitado = True # Marcar como visitado

        # 3. RELAJACIÓN (Actualizar vecinos)
        arista = nodo_actual.adyacentes
        while arista is not None:
            
            vecino_id = arista.destino
            costo_viaje = arista.peso
            
            # Buscamos el objeto nodo del vecino
            nodo_vecino = buscar_vertice(grafo, vecino_id)
            if nodo_vecino is None: 
                arista = arista.sig
                continue

            # Relajación
            nueva_distancia = nodo_actual.distancia + costo_viaje
            
            if not nodo_vecino.visitado and nueva_distancia < nodo_vecino.distancia:
                
                # SÍ: Actualizamos la distancia y el predecesor
                nodo_vecino.distancia = nueva_distancia
                nodo_vecino.anterior = nodo_actual # Guardamos el puntero al nodo

            arista = arista.sig

    # ==========================================
    # 4. RECONSTRUCCIÓN DEL CAMINO
    # ==========================================
    
    camino = []
    nodo_destino = buscar_vertice(grafo, destino_id)

    if nodo_destino is None or nodo_destino.distancia == float('inf'):
        return [], float('inf')

    # Saltamos hacia atrás usando los punteros 'anterior'
    curr = nodo_destino
    while curr is not None:
        camino.insert(0, curr.info)
        curr = curr.anterior # Usamos el puntero anterior

    return camino, nodo_destino.distancia

# ==========================================
# MAIN PARA PROBARLO
# ==========================================
if __name__ == "__main__":
    # 1. Crear el grafo
    mi_grafo = Grafo()
    
    # 2. Insertar vértices y aristas (Usamos las funciones definidas arriba para crear la estructura)
    # Nota: Tendrías que definir las funciones insertar_vertice e insertar_arista con la misma lógica
    # que en tu código original, pero usando las nuevas clases.
    
    # Ejemplo de inserción usando las funciones originales (asumiendo que están disponibles)
    def insertar_vertice(grafo, info):
        nuevo = NodoVertice(info)
        if grafo.inicio is None:
            grafo.inicio = nuevo
        else:
            aux = grafo.inicio
            while aux.sig is not None:
                aux = aux.sig
            aux.sig = nuevo
        grafo.tamano += 1

    def insertar_arista(grafo, origen, destino, peso):
        nodo_origen = buscar_vertice(grafo, origen)
        if nodo_origen:
            nueva = NodoArista(destino, peso)
            nueva.sig = nodo_origen.adyacentes
            nodo_origen.adyacentes = nueva

    insertar_vertice(mi_grafo, "Madrid")
    insertar_vertice(mi_grafo, "Paris")
    insertar_vertice(mi_grafo, "Berlin")
    insertar_arista(mi_grafo, "Madrid", "Paris", 10)
    insertar_arista(mi_grafo, "Paris", "Berlin", 5)
    insertar_arista(mi_grafo, "Madrid", "Berlin", 20)
    
    print("Calculando ruta...")
    ruta, coste = dijkstra_sin_dict(mi_grafo, "Madrid", "Berlin")

    print(f"La ruta más rápida es: {ruta}")
    print(f"El coste total es: {coste}")