import json
import networkx as nx 

cedis = {
    "metropolitano en azcapotzalco": "ciudad de mexico",
    "tijuana": "baja california",
    "mexicali": "baja california",
    "hermosillo": "sonora",
    "cd juarez/cd obregon": "sonora",
    "monterrey": "nuevo leon",
    "saltillo": "coahuila",
    "torreon": "coahuila",
    "reyona": "tamaulipas",
    "matamoros": "tamaulipas",
    "cd victoria": "tamaulipas",
    "altamira": "tamaulipas",
    "ciudad mante": "tamaulipas",
    "guadalajara": "jalisco",
    "leon": "guanajuato",
    "aguas calientes": "aguas calientes",
    "colima": "colima",
    "morelia": "michoacan",
    "puebla": "puebla",
    "queretaro": "queretaro",
    "pachuca": "hidalgo",
    "toluca": "estado de mexico",
    "cuernavaca": "morelos",
    "ciudad de mexico": "CDMX",
    "acapulco": "guerrero",
    "chipalcingo": "guerrero",
    "oaxaca": "oaxaca",
    "tapachula": "chiapas",
    "veracruz": "veracruz",
    "villa hermosa": "tabasco",
    "coatzacoalcos": "veracruz",
    "merida": "yucatan",
    "cancun": "quintana roo",
    "chetumal": "quintana roo"
}

# --- PARTE 1: Guardar CEDIS en JSON (código original) ---
nombre_de_archivo_json = "centros_de_distribucion_BIMBO_en_Mexico.json"
try:
    with open(nombre_de_archivo_json, 'w', encoding='utf-8') as archivo_json:
        json.dump(cedis, archivo_json, indent=4, ensure_ascii=False)
        print(f"'{nombre_de_archivo_json}' creado exitosamente.")
except IOError as e:
    print(f'Error al escribir en el archivo JSON: {e}')

# --- PARTE 2: Construir el Grafo sin Coordenadas ---

# 1. Inicializa un Grafo No Dirigido
G = nx.Graph()

# 2. Añade los Nodos al Grafo
print("\n--- Añadiendo nodos al grafo ---")
for cedi_nombre, estado in cedis.items():
    # Añadimos cada centro de distribución como un nodo.
    # El estado se guarda como un atributo del nodo.
    G.add_node(cedi_nombre, estado=estado)
    # print(f"  Nodo añadido: {cedi_nombre} (Estado: {estado})")

# 3. Conecta los Nodos (Grafo Completo - Todos con Todos)
print("\n--- Conectando todos los nodos (grafo completo) ---")
nodos_en_grafo = list(G.nodes()) # Obtiene una lista de todos los nombres de los CEDIS

# Iteramos sobre todos los pares de nodos para crear aristas
for i in range(len(nodos_en_grafo)):
    for j in range(i + 1, len(nodos_en_grafo)): # Para evitar duplicados (A-B es igual a B-A)
        cedi1 = nodos_en_grafo[i]
        cedi2 = nodos_en_grafo[j]
        
        # Añadir la arista sin un peso numérico basado en distancia
        # Podrías añadir un peso arbitrario como 1 si lo necesitas para algunos algoritmos,
        # o simplemente no especificar 'weight' si no es relevante.
        G.add_edge(cedi1, cedi2) 
        # print(f"  Arista añadida entre '{cedi1}' y '{cedi2}'")

print(f"\nGrafo creado con {G.number_of_nodes()} nodos y {G.number_of_edges()} aristas.")

# --- Opcional: Guardar el grafo ---
# Aún puedes guardar este grafo para visualizarlo con Gephi, por ejemplo.
try:
    nombre_de_archivo_grafo = "grafo_distribucion_BIMBO_sin_coords.gexf"
    nx.write_gexf(G, nombre_de_archivo_grafo)
    print(f"Grafo guardado como '{nombre_de_archivo_grafo}' (formato GEXF).")
except Exception as e:
    print(f"Error al guardar el grafo: {e}")

# --- Opcional: Mostrar algunas propiedades del grafo ---
print("\n--- Propiedades del Grafo ---")
print(f"Número de nodos: {G.number_of_nodes()}")
print(f"Número de aristas: {G.number_of_edges()}")