# =======================================================
#                  TDA: Nodo AVL
#   (usaremos el AVL como cola de prioridad para Dijkstra)
# =======================================================

class AVLNode:
    def __init__(self, key, value):
        self.key = key        # clave para ordenar (distancia, id_vertice)
        self.value = value    # normalmente el vértice
        self.height = 1
        self.left = None
        self.right = None


class AVLTree:
    def __init__(self):
        self.root = None

    # ---------- utilidades internas ----------

    def _height(self, node):
        return node.height if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left),
                              self._height(node.right))

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        # rotar
        x.right = y
        y.left = T2

        # actualizar alturas
        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left

        # rotar
        y.left = x
        x.right = T2

        # actualizar alturas
        self._update_height(x)
        self._update_height(y)

        return y

    def _rebalance(self, node):
        self._update_height(node)
        bf = self._balance_factor(node)

        # Izquierda pesada
        if bf > 1:
            # Caso LR
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            # Caso LL
            return self._rotate_right(node)

        # Derecha pesada
        if bf < -1:
            # Caso RL
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            # Caso RR
            return self._rotate_left(node)

        return node

    # ---------- insertar (key, value) ----------

    def _insert(self, node, key, value):
        if node is None:
            return AVLNode(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        else:
            # para claves iguales, las mando a la derecha
            node.right = self._insert(node.right, key, value)

        return self._rebalance(node)

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    # ---------- extraer mínimo (como pop de una priority queue) ----------

    def _extract_min(self, node):
        if node.left is None:
            # este es el mínimo
            return node.right, node

        node.left, min_node = self._extract_min(node.left)
        node = self._rebalance(node)
        return node, min_node

    def extract_min(self):
        """Devuelve (key, value) del menor y lo elimina del AVL."""
        if self.root is None:
            return None, None

        self.root, min_node = self._extract_min(self.root)
        return min_node.key, min_node.value

    def is_empty(self):
        return self.root is None


# =======================================================
#                  TDA: Edge (Arista)
# =======================================================

class Edge:
    def __init__(self, target, weight):
        self.target = target   # vértice destino (objeto Vertex)
        self.weight = weight   # peso de la arista


# =======================================================
#                  TDA: Vertex (Vértice)
# =======================================================

class Vertex:
    def __init__(self, name):
        self.name = name       # identificador (string, número, etc.)
        self.edges = []        # lista de aristas salientes

    def add_edge(self, edge):
        self.edges.append(edge)


# =======================================================
#                  TDA: Graph (Grafo)
# =======================================================

class Graph:
    def __init__(self):
        # diccionario: nombre -> objeto Vertex
        self.vertices = {}

    def add_vertex(self, name):
        if name not in self.vertices:
            self.vertices[name] = Vertex(name)
        return self.vertices[name]

    def add_edge(self, src_name, dst_name, weight):
        """Grafo dirigido: src -> dst con peso 'weight'."""
        src = self.add_vertex(src_name)
        dst = self.add_vertex(dst_name)
        src.add_edge(Edge(dst, weight))


# =======================================================
#           Algoritmo de Dijkstra usando AVL
# =======================================================

class DijkstraSolver:
    def __init__(self, graph):
        self.graph = graph

    def shortest_paths(self, start_name):
        """
        Calcula distancias mínimas desde start_name al resto de vértices.
        Devuelve:
            dist: dict nombre -> distancia mínima
            prev: dict nombre -> nombre del predecesor en el camino
        """

        # Inicializar distancias a infinito
        dist = {name: float("inf") for name in self.graph.vertices}
        prev = {name: None for name in self.graph.vertices}

        dist[start_name] = 0

        # Cola de prioridad: AVL
        pq = AVLTree()

        # clave = (distancia, nombre_vertice) para que sea totalmente ordenable
        start_vertex = self.graph.vertices[start_name]
        pq.insert((0, start_name), start_vertex)

        visited = set()

        while not pq.is_empty():
            (d, v_name), vertex = pq.extract_min()

            # Si ya fue procesado con mejor distancia, lo saltamos
            if v_name in visited:
                continue
            visited.add(v_name)

            # Relajación de aristas
            for edge in vertex.edges:
                neighbor = edge.target
                u = v_name           # nombre del vértice actual
                v = neighbor.name    # nombre del vecino
                alt = dist[u] + edge.weight

                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    # Insertamos nueva distancia en el AVL
                    pq.insert((alt, v), neighbor)

        return dist, prev

    def build_path(self, start_name, end_name, prev):
        """
        Reconstruye el camino mínimo start -> end usando el diccionario prev.
        Devuelve una lista de nombres de vértice en orden.
        """
        path = []
        current = end_name

        while current is not None:
            path.append(current)
            current = prev[current]

        path.reverse()

        # Si el primer vértice no es el de inicio, no hay camino
        if not path or path[0] != start_name:
            return []

        return path


# =======================================================
#                     PRUEBA FINAL
#            (inicializar grafo y usar Dijkstra)
# =======================================================

if __name__ == "__main__":
    # Creamos un grafo de ejemplo (puedes imaginarlo como planetas Star Wars)
    g = Graph()

    # Añadimos vértices y aristas con pesos (distancias)
    # A-B-C-D-E es un ejemplo sencillo
    g.add_edge("Tatooine", "Naboo", 4)
    g.add_edge("Tatooine", "Coruscant", 2)
    g.add_edge("Naboo", "Coruscant", 1)
    g.add_edge("Naboo", "Kamino", 5)
    g.add_edge("Coruscant", "Kamino", 8)
    g.add_edge("Coruscant", "Kashyyyk", 10)
    g.add_edge("Kamino", "Kashyyyk", 2)
    g.add_edge("Kamino", "Endor", 6)
    g.add_edge("Kashyyyk", "Endor", 3)

    solver = DijkstraSolver(g)

    origen = "Tatooine"
    destino = "Endor"

    dist, prev = solver.shortest_paths(origen)
    path = solver.build_path(origen, destino, prev)

    print("\n=============================")
    print("     DIJKSTRA con AVL")
    print("=============================\n")

    print(f"Distancias mínimas desde {origen}:\n")
    for v, d in dist.items():
        print(f"  {origen} -> {v} = {d}")

    print("\nCamino mínimo desde", origen, "hasta", destino, ":\n")
    if path:
        print("  -> ".join(path))
        print(f"\nDistancia total: {dist[destino]}")
    else:
        print("No hay camino.")

    print("\n=============================\n")
