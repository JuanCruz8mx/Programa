import networkx as Nx; import matplotlib.pyplot as plt; import tkinter as Tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk


class main():
    def __init__(self):
        self.G=Nx.Graph()
        self.v=Tk.Tk()
        self.v.geometry('500x700+150+150')
        self.v.title('RouteLigic')
        self.ventana()
        self.csv()
        self.Grafo()
        self.v.mainloop()
    def ventana(self):
        titulo=Tk.Label(self.v, text='Mejor Ruta', font=('Arial', 12)); titulo.pack(pady=5)
        n_name=Tk.Label(self.v, text='Origen: ', font=('Arial', 12)); n_name.pack(pady=5)
        i_name=Tk.Entry(self.v, width=10); i_name.pack(pady=5)
        n2_name=Tk.Label(self.v, text='Destino: ', font=('Arial', 12)); n2_name.pack(pady=5)
        i2_name=Tk.Entry(self.v, width=10); i2_name.pack(pady=5)
        boton=Tk.Button(self.v, text='Encontrar la mejor ruta: ', command=lambda: self.Grafo_ruta(i_name.get(), i2_name.get())); boton.pack(pady=5)
        self.respuesta=ScrolledText(self.v, width=40, height=20, wrap='word'); self.respuesta.pack(padx=5)
    def csv(self):
        with open('centros.csv', 'r') as archivo:
            f=archivo.readlines()
            nodos=set()         # Cojunto para evitar nodos duplicados
            for i in f[1:]:     # split(','): Divide cada dato separados por comas y los guarda en una lista
                N1, N2, Distancia, Capacidad, Tiempo=[x for x in i.split(',')] # Da el valor a cada uno de las variables
                #print(N1)
                if N1 not in nodos:
                    self.G.add_node(N1, distancia=Distancia, capacidad=Capacidad)    # Crea el N1
                    nodos.add(N1)
                if N2 not in nodos:
                    self.G.add_node(N2, distancia=Distancia, tiempo=Tiempo)      # Crea el N2
                    nodos.add(N2)
                self.G.add_edge(N1, N2, distancia=float(Distancia), tiempo=float(Tiempo))     # Hace el grafo dirigido
                self.pos=Nx.spring_layout(self.G, seed=20)    # Calcula las cordenadas y mantenerlas evitando que cambien
                self.etiquetas={(origen, destino): f'{atributo['distancia']} km\n{atributo['tiempo']} h' for origen, destino, atributo in self.G.edges(data=True)}  # Obtiene etiquetas
    def Grafo(self):
        self.g=Tk.Toplevel()
        self.g.geometry('800x800+300+300')
        self.g.title('Grafo')
        respuesta=ScrolledText(self.g, width=500, height=100, wrap='word'); respuesta.pack(padx=5)
        Nx.draw(self.G, self.pos, with_labels=True, node_color='lightblue', edge_color='black', arrows=True)   # Diseño del grafo
        Nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=self.etiquetas) # Ver las etiquetas en el grafo
        plt.savefig('grafo.png', bbox_inches='tight', dpi=300)
        imagen = Image.open('grafo.png')
        respuesta.configure(state='normal')
        respuesta.delete("1.0", Tk.END)
        respuesta.image_create(Tk.END, image=imagen)
        respuesta.configure(state='disabled')
    def Ruta(self, ruta):
        r=list(zip(ruta[:-1], ruta[1:]))
        Nx.draw(self.G, self.pos, with_labels=True, node_color='lightgray', edge_color='lightgray', arrows=True)  # Diseño de los nodes y aristas completo
        Nx.draw_networkx_edges(self.G, self.pos, edgelist=r, edge_color='red', width=2.5, arrows=True)    # Diseño de los nodos de la ruta
        Nx.draw_networkx_nodes(self.G, self.pos, nodelist=ruta, node_color='red')     # Diseño de las aristas de la ruta
        Nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=self.etiquetas)
        plt.title('Mejor ruta'); self.t
        plt.show()
    def Grafo_ruta(self, origen, destino):
        if origen in self.G.nodes and destino in self.G.nodes:
            if Nx.has_path(self.G, origen, destino):     # Revisa si existe una ruta
                ruta = Nx.dijkstra_path(self.G, origen, destino, weight='distancia')     # Busca la ruta mas corta con base a la distancia
                distancia_total=Nx.dijkstra_path_length(self.G, origen, destino, weight='distancia')     # Calcula la distancia total
                tiempo_total=Nx.dijkstra_path_length(self.G, origen, destino, weight='tiempo')       # Calcula el tiempo total
                self.respuesta.insert('insert', f'Ruta más corta de {origen} a {destino}:\n {" → ".join(ruta)}\n')
                self.respuesta.insert('insert', f'Distancia total: {distancia_total} km\n')
                self.respuesta.insert('insert', f'Tiempo total: {tiempo_total} h')
                self.Ruta(ruta)
            else:
                self.respuesta.insert('insert',"No hay ruta.")
        else:
            self.respuesta.insert('insert','Uno o ambos nodos no existen.')

if __name__=='__main__':
    main()
