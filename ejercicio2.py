# ======================================================
# CLASE MONTÍCULO HÍBRIDA (SIRVE PARA TODO)
# ======================================================
class Monticulo:
    def _init_(self, es_min=True): # Por defecto es Min (para Dijkstra)
        self.vector = []
        self.tamano = 0
        self.es_min = es_min         # True = El menor sube. False = El mayor sube.

    # --- FUNCIÓN AUXILIAR: ¿Es 'a' más prioritario que 'b'? ---
    def es_mejor(self, a, b):
        if self.es_min: return a < b  # Modo Min-Heap
        else:           return a > b  # Modo Max-Heap

    # ---------------------------------------------------------
    # FLOTAR (INSERTAR)
    # ---------------------------------------------------------
    def flotar(self, i):
        while i > 0:
            padre = (i - 1) // 2

            # Usamos nuestra función auxiliar para decidir
            if self.es_mejor(self.vector[i], self.vector[padre]):
                self.vector[i], self.vector[padre] = self.vector[padre], self.vector[i]
                i = padre
            else:
                break

    # ---------------------------------------------------------
    # HUNDIR (ELIMINAR)
    # ---------------------------------------------------------
    def hundir(self, i):
        while True:
            izq = 2 * i + 1
            der = 2 * i + 2
            mejor = i

            # Comparamos hijo izq con el actual
            if izq < self.tamano and self.es_mejor(self.vector[izq], self.vector[mejor]):
                mejor = izq

            # Comparamos hijo der con el mejor que llevamos
            if der < self.tamano and self.es_mejor(self.vector[der], self.vector[mejor]):
                mejor = der

            if mejor == i: break

            self.vector[i], self.vector[mejor] = self.vector[mejor], self.vector[i]
            i = mejor

    # ---------------------------------------------------------
    # FUNCIONES PÚBLICAS
    # ---------------------------------------------------------
    def agregar(self, dato):
        self.vector.append(dato)
        self.tamano += 1
        self.flotar(self.tamano - 1)

    def quitar(self):
        if self.tamano == 0: return None
        dato = self.vector[0]
        ultimo = self.vector.pop()
        self.tamano -= 1
        if self.tamano > 0:
            self.vector[0] = ultimo
            self.hundir(0)
        return dato

# ======================================================
# MAIN DE PRUEBA (DEMOSTRACIÓN)
# ======================================================
if _name_ == "_main_":
    datos = [50, 10, 80, 5, 30]

    # --- CASO A: MONTÍCULO MÍNIMO (Para Dijkstra) ---
    print("--- PRUEBA MIN-HEAP (El menor arriba) ---")
    min_heap = Monticulo(es_min=True) # <--- MODO MIN

    for x in datos: min_heap.agregar(x)
    print(f"Vector Min: {min_heap.vector} (El 5 debe estar en pos 0)")
    print(f"Sacamos el prioritario: {min_heap.quitar()}") # Sale 5

    print("\n" + "="*30 + "\n")

    # --- CASO B: MONTÍCULO MÁXIMO (Para Urgencias) ---
    print("--- PRUEBA MAX-HEAP (El mayor arriba) ---")
    max_heap = Monticulo(es_min=False) # <--- MODO MAX

    for x in datos: max_heap.agregar(x)
    print(f"Vector Max: {max_heap.vector} (El 80 debe estar en pos 0)")
    print(f"Sacamos el prioritario: {max_heap.quitar()}") # Sale 80