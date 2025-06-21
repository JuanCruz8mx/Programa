import networkx as Nx; import matplotlib.pyplot as plt; import tkinter as Tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

class main():
    def __init__(self):
        self.G=Nx.Graph()
        self.v=Tk.Tk()
        self.v.geometry('1500x800+200+100')
        self.v.title('RouteLigic')
        self.v.config(bg="skyblue")
        self.nodos=set()         # Cojunto para evitar nodos duplicados
        self.csv()
        self.Grafo()
        self.ventana()
        self.v.mainloop()
    def ventana(self):
        frame=Tk.Frame(self.v); frame.grid(row=0, column=0,sticky='N',padx=1,pady=1)
        frame2=Tk.Frame(self.v); frame2.grid(row=1, column=0, columnspan=2, sticky='S',padx=1,pady=1)
        self.frame3=Tk.Frame(self.v); self.frame3.grid(row=0, column=2, rowspan=3, columnspan=4, sticky='NE',padx=5,pady=5)

        self.canvas = Tk.Canvas(self.frame3, width=1200, height=700, bg='white')
        self.scroll_x = Tk.Scrollbar(self.frame3, orient='horizontal', command=self.canvas.xview)
        self.scroll_y = Tk.Scrollbar(self.frame3, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        self.scroll_x.pack(side='bottom', fill='x')
        self.scroll_y.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)

        opciones = sorted(self.nodos)   # Ordena los nodos en una lista ordenada

        origen=Tk.Label(frame, text='Origen: ', font=('arial', 12)); origen.grid(row=0, column=1, padx=2, pady=2, sticky='E')
        origen_var = Tk.StringVar()     # Lo guarda para poder usar iterar despues
        origen_var.set(opciones[0])
        i_name = Tk.OptionMenu(frame, origen_var, *opciones)
        i_name.config(font=('arial',12), width=15); i_name.grid(row=0, column=2, padx=2, pady=2, sticky='NSEW')
        
        destino=Tk.Label(frame, text='Destino: ', font=('arial', 12)); destino.grid(row=1, column=1, padx=2, pady=2,sticky='E')
        destino_var = Tk.StringVar()
        destino_var.set(opciones[0])
        i2_name = Tk.OptionMenu(frame, destino_var, *opciones)
        i2_name.config(font=('arial',12), width=15); i2_name.grid(row=1, column=2, padx=2, pady=2, sticky='NSEW')

        boton = Tk.Button(frame, text='Mejor ruta', font=('arial',12), bg='#0000FF', command=lambda: self.Grafo_ruta(origen_var.get(), destino_var.get())); boton.grid(row=3, column=2, padx=2, pady=2)

        self.respuesta=ScrolledText(frame2, width=50, height=29, wrap='word',font=('arial',12)); self.respuesta.grid(row=3,column=1, columnspan=3,padx=2,pady=2,sticky='NSEW')
        self.mostrar_imagen('grafoCompleto.png')

    def mostrar_imagen(self, ruta):
        imagen_original = Image.open(ruta)
        imagen_redimensionada = imagen_original.resize((1000, 700))
        self.image = ImageTk.PhotoImage(imagen_redimensionada)
        self.canvas.delete("all")  # Limpia el canvas anterior
        self.canvas.create_image(0, 0, anchor='nw', image=self.image)
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
    def csv(self):
        self.G.clear()
        with open('centros.csv', 'r') as archivo:
            f=archivo.readlines()
            for i in f[1:]:     # split(','): Divide cada dato separados por comas y los guarda en una lista
                N1, N2, Distancia, Capacidad, Tiempo=[x.strip() for x in i.split(',')] # Da el valor a cada uno de las variables
                #print(N1)
                if N1 not in self.nodos:
                    self.G.add_node(N1, distancia=Distancia, capacidad=Capacidad)    # Crea el N1
                    self.nodos.add(N1)
                if N2 not in self.nodos:
                    self.G.add_node(N2, distancia=Distancia, tiempo=Tiempo)      # Crea el N2
                    self.nodos.add(N2)
                self.G.add_edge(N1, N2, distancia=float(Distancia), tiempo=float(Tiempo))     # Hace el grafo dirigido
                self.pos=Nx.spring_layout(self.G, seed=20)    # Calcula las cordenadas y mantenerlas evitando que cambien
                self.etiquetas={(origen, destino): f"{atributo['distancia']} km\n{atributo['tiempo']} h" for origen, destino, atributo in self.G.edges(data=True)}  # Obtiene etiquetas
    def Grafo(self):
        Nx.draw(self.G, self.pos, with_labels=True, node_color='lightblue', edge_color='black', arrows=True)   # Diseño del grafo
        Nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=self.etiquetas) # Ver las etiquetas en el grafo
        plt.savefig('grafoCompleto.png')  # Guardar la imagen
        plt.close()
    def Ruta(self, ruta):
        r=list(zip(ruta[:-1], ruta[1:]))
        Nx.draw(self.G, self.pos, with_labels=True, node_color='lightgray', edge_color='lightgray', arrows=True)  # Diseño de los nodes y aristas completo
        Nx.draw_networkx_edges(self.G, self.pos, edgelist=r, edge_color='red', width=2.5, arrows=True)    # Diseño de los nodos de la ruta
        Nx.draw_networkx_nodes(self.G, self.pos, nodelist=ruta, node_color='red')     # Diseño de las aristas de la ruta
        Nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=self.etiquetas)
        plt.savefig('grafoRuta.png')  # Guardar la imagen
        plt.close()
        self.mostrar_imagen('grafoRuta.png')
    def Grafo_ruta(self, origen, destino):
        if origen in self.G.nodes and destino in self.G.nodes:
            if Nx.has_path(self.G, origen, destino):     # Revisa si existe una ruta
                ruta = Nx.dijkstra_path(self.G, origen, destino, weight='distancia')     # Busca la ruta mas corta con base a la distancia
                distancia_total=sum(self.G[a][b]['distancia'] for a, b in zip(ruta[:-1], ruta[1:]))
                tiempo_total=sum(self.G[a][b]['tiempo'] for a, b in zip(ruta[:-1], ruta[1:]))
                self.respuesta.insert('insert', f'Ruta más corta de {origen} a {destino}:\n {" → ".join(ruta)}\n')
                self.respuesta.insert('insert', f'Distancia total: {distancia_total} km\n')
                self.respuesta.insert('insert', f'Tiempo total: {tiempo_total} h\n\n')
                self.Ruta(ruta)
            else:
                self.respuesta.insert('insert',"No hay ruta.\n")
        else:
            self.respuesta.insert('insert','Uno o ambos nodos no existen.\n')

if __name__=='__main__':
    main()
    