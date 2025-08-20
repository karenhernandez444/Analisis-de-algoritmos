import tkinter as tk
from tkinter import ttk, messagebox
import random, time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def busqueda_lineal(lista, x):
    for i, val in enumerate(lista):
        if val == x:
            return i
    return -1

def busqueda_binaria(lista, x):
    izquierda, derecha = 0, len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista[medio] == x:
            return medio
        elif lista[medio] < x:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1

# GUI principal

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparación: Búsqueda Lineal vs Binaria")
        self.lista = []

        # Controles
        frame_controls = tk.Frame(root, padx=10, pady=10)
        frame_controls.pack(side="top", fill="x")

        tk.Label(frame_controls, text="Tamaño de lista:").grid(row=0, column=0)
        self.tam_var = tk.StringVar(value="1000")
        self.combo_tam = ttk.Combobox(frame_controls, textvariable=self.tam_var,
                                      values=["100","1000","10000","100000"], width=10)
        self.combo_tam.grid(row=0, column=1, padx=5)

        self.btn_gen = tk.Button(frame_controls, text="Generar datos", command=self.generar_datos)
        self.btn_gen.grid(row=0, column=2, padx=5)

        tk.Label(frame_controls, text="Valor a buscar:").grid(row=1, column=0, pady=5)
        self.entry_valor = tk.Entry(frame_controls, width=12)
        self.entry_valor.grid(row=1, column=1, padx=5)

        self.btn_lin = tk.Button(frame_controls, text="Búsqueda lineal", command=self.buscar_lineal)
        self.btn_lin.grid(row=2, column=0, pady=5)

        self.btn_bin = tk.Button(frame_controls, text="Búsqueda binaria", command=self.buscar_binaria)
        self.btn_bin.grid(row=2, column=1, pady=5)

        # Resultados
        frame_res = tk.LabelFrame(root, text="Resultados", padx=10, pady=10)
        frame_res.pack(side="top", fill="x", padx=10, pady=5)

        self.lbl_tam = tk.Label(frame_res, text="Tamaño de lista: —")
        self.lbl_tam.pack(anchor="w")
        self.lbl_res = tk.Label(frame_res, text="Resultado: —")
        self.lbl_res.pack(anchor="w")
        self.lbl_tiempo = tk.Label(frame_res, text="Tiempo: — ms")
        self.lbl_tiempo.pack(anchor="w")

        # la grafica
        frame_graf = tk.LabelFrame(root, text="Comparación de tiempos promedio", padx=10, pady=10)
        frame_graf.pack(fill="both", expand=True, padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(5,3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_graf)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.btn_graf = tk.Button(root, text="Actualizar gráfica", command=self.actualizar_grafica)
        self.btn_graf.pack(pady=5)

    # Funciones auxiliares

    def generar_datos(self):
        try:
            n = int(self.tam_var.get())
        except ValueError:
            messagebox.showerror("Error", "Selecciona un tamaño válido.")
            return

        # para hacer lista ordenada de enteros aleatorios
        self.lista = sorted(random.sample(range(n*10), n))
        self.lbl_tam.config(text=f"Tamaño de lista: {n}")
        self.lbl_res.config(text="Resultado: —")
        self.lbl_tiempo.config(text="Tiempo: — ms")
        messagebox.showinfo("Éxito", f"Lista de {n} elementos generada.")

    def buscar_lineal(self):
        self._buscar(busqueda_lineal)

    def buscar_binaria(self):
        self._buscar(busqueda_binaria)

    def _buscar(self, algoritmo):
        if not self.lista:
            messagebox.showwarning("Atención", "Primero genera los datos.")
            return
        try:
            valor = int(self.entry_valor.get())
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido.")
            return

        inicio = time.perf_counter()
        idx = algoritmo(self.lista, valor)
        fin = time.perf_counter()

        ms = (fin - inicio) * 1000
        self.lbl_res.config(text=f"Resultado: {idx if idx!=-1 else 'No encontrado'}")
        self.lbl_tiempo.config(text=f"Tiempo: {ms:.3f} ms")

    def actualizar_grafica(self):
        tamanos = [100, 1000, 10000, 100000]
        promedios_lineal = []
        promedios_binaria = []

        for n in tamanos:
            lista = sorted(random.sample(range(n*10), n))
            valor = random.choice(lista)

            # medir lineal
            tiempos = []
            for _ in range(5):
                t1 = time.perf_counter()
                busqueda_lineal(lista, valor)
                t2 = time.perf_counter()
                tiempos.append((t2-t1)*1000)
            promedios_lineal.append(sum(tiempos)/len(tiempos))

            # medir binaria
            tiempos = []
            for _ in range(5):
                t1 = time.perf_counter()
                busqueda_binaria(lista, valor)
                t2 = time.perf_counter()
                tiempos.append((t2-t1)*1000)
            promedios_binaria.append(sum(tiempos)/len(tiempos))

        # Graficar
        self.ax.clear()
        self.ax.plot(tamanos, promedios_lineal, marker="o", label="Lineal")
        self.ax.plot(tamanos, promedios_binaria, marker="o", label="Binaria")
        self.ax.set_xlabel("Tamaño de lista")
        self.ax.set_ylabel("Tiempo promedio (ms)")
        self.ax.set_xscale("log")   # Escala log para mejor visualización
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

# Ejecutar

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
