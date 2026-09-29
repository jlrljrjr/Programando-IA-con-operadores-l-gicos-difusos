import tkinter as tk

# ---------- Operadores difusos ----------
def y_min(a, b): return min(a, b)          # AND clásico
def y_prod(a, b): return a * b             # AND alternativo
def o_max(a, b): return max(a, b)          # OR clásico
def o_suma(a, b): return a + b - a * b     # OR alternativo
def no(a): return 1 - a                    # NOT

# ---------- Puertas: (nombre, fórmula, función, cálculo, umbral, energía) ----------
PUERTAS = [
    ("Recepción",        "A AND B (mínimo)",          y_min,                    "mín({a}, {b})",           0.5,  1.2),
    ("Pasillo",          "A OR B (máximo)",           o_max,                    "máx({a}, {b})",           0.7,  0.8),
    ("Archivo",          "A AND B (mínimo)",          y_min,                    "mín({a}, {b})",           0.6,  1.4),
    ("Laboratorio",      "A OR B (máximo)",           o_max,                    "máx({a}, {b})",           0.9,  1.0),
    ("Cuarto de cámaras","A AND NOT B",               lambda a, b: y_min(a, no(b)), "mín({a}, 1 − {b})",   0.6,  1.0),
    ("Servidores",       "NOT A AND B",               lambda a, b: y_min(no(a), b), "mín(1 − {a}, {b})",   0.6,  1.0),
    ("Bóveda interna",   "A AND NOT B",               lambda a, b: y_min(a, no(b)), "mín({a}, 1 − {b})",   0.7,  1.0),
    ("Reactor",          "A AND B (producto)",        y_prod,                   "{a} × {b}",               0.36, 1.2),
    ("Sala de control",  "A OR B (suma probabilística)", o_suma,                "{a} + {b} − {a}×{b}",     0.8,  0.9),
    ("Salida final",     "A AND B (producto)",        y_prod,                   "{a} × {b}",               0.49, 1.4),
]

# ---------- Colores ----------
FONDO, PANEL, LATON = "#0f1a24", "#182633", "#e0b458"
ABIERTA, ALARMA, TEXTO, APAGADO = "#4fd1a5", "#e5645a", "#e8e4d8", "#8a9aa8"


class Juego:
    def __init__(self, root):
        self.root = root
        root.title("Escape room difuso")
        root.configure(bg=FONDO)
        root.resizable(False, False)
        self.va, self.vb = tk.DoubleVar(value=0), tk.DoubleVar(value=0)
        self.construir()
        self.fase = "inicio"
        self.reiniciar()

    def etiqueta(self, **kw):
        return tk.Label(self.root, **{"bg": FONDO, "fg": TEXTO, **kw})

    def construir(self):
        barra = tk.Frame(self.root, bg=FONDO)
        barra.pack(fill="x", padx=24, pady=(16, 0))
        self.lbl_nivel = tk.Label(barra, bg=FONDO, fg=TEXTO, font=("Helvetica", 12))
        self.lbl_nivel.pack(side="left")
        self.lbl_puntos = tk.Label(barra, bg=FONDO, fg=LATON, font=("Helvetica", 12, "bold"))
        self.lbl_puntos.pack(side="right")
        self.lbl_vidas = tk.Label(barra, bg=FONDO, fg=ALARMA, font=("Helvetica", 14))
        self.lbl_vidas.pack(side="right", padx=20)

        self.etiqueta(text="Escape room difuso", fg=LATON, font=("Georgia", 24, "bold")).pack(pady=(6, 0))
        self.canvas = tk.Canvas(self.root, width=760, height=200, bg=PANEL, highlightthickness=0)
        self.canvas.pack(padx=24, pady=10)

        self.lbl_regla = self.etiqueta(font=("Helvetica", 14, "bold"))
        self.lbl_regla.pack()
        self.lbl_meta = self.etiqueta(font=("Helvetica", 12), fg=APAGADO)
        self.lbl_meta.pack()

        for texto, var in (("Palanca A", self.va), ("Palanca B", self.vb)):
            fila = tk.Frame(self.root, bg=FONDO)
            fila.pack(pady=4)
            tk.Label(fila, text=texto, width=10, bg=FONDO, fg=TEXTO, font=("Helvetica", 12)).pack(side="left")
            tk.Scale(fila, variable=var, from_=0, to=1, resolution=0.1, orient="horizontal",
                     length=420, bg=FONDO, fg=LATON, troughcolor=PANEL, highlightthickness=0,
                     activebackground=LATON, command=self.al_mover).pack(side="left")

        self.lbl_energia = self.etiqueta(font=("Helvetica", 12, "bold"))
        self.lbl_energia.pack(pady=(4, 0))
        self.lbl_msg = self.etiqueta(font=("Helvetica", 12), wraplength=700, height=4, justify="center")
        self.lbl_msg.pack(pady=6)
        self.btn = tk.Button(self.root, font=("Helvetica", 13, "bold"), bg=LATON, fg=FONDO,
                             activebackground=TEXTO, relief="flat", padx=24, pady=6, command=self.boton)
        self.btn.pack(pady=(0, 18))

    # ---------- Estado del juego ----------
    def reiniciar(self):
        self.nivel, self.vidas, self.puntos, self.fallos = 0, 3, 0, 0
        self.fase = "inicio"
        self.estado = "cerrada"
        self.btn.config(text="Comenzar")
        self.lbl_msg.config(fg=TEXTO, text="Cada puerta abre si el resultado de su regla difusa llega al umbral.\n"
                            "Mueve las palancas, pero no gastes más energía de la que tienes (A + B).\n"
                            "Tienes 3 vidas: cada intento fallido te quita una.")
        self.refrescar()

    def cargar_puerta(self):
        self.fase, self.estado, self.fallos = "jugando", "cerrada", 0
        self.va.set(0)
        self.vb.set(0)
        self.lbl_msg.config(fg=TEXTO, text="Elige los valores de A y B, y prueba la puerta.")
        self.btn.config(text="Probar puerta")
        self.refrescar()

    def refrescar(self):
        nombre, regla, _, _, umbral, energia = PUERTAS[min(self.nivel, 9)]
        self.lbl_nivel.config(text=f"Puerta {self.nivel + 1} de 10 · {nombre}")
        self.lbl_puntos.config(text=f"{self.puntos} puntos")
        self.lbl_vidas.config(text="♥ " * self.vidas + "♡ " * (3 - self.vidas))
        self.lbl_regla.config(text=f"Regla: {regla}")
        self.lbl_meta.config(text=f"Umbral para abrir: {umbral:g}   ·   Energía disponible: {energia:g}")
        self.al_mover()

    def al_mover(self, _=None):
        energia = PUERTAS[min(self.nivel, 9)][5]
        usada = round(self.va.get() + self.vb.get(), 1)
        self.lbl_energia.config(text=f"Energía usada: {usada:g} de {energia:g}",
                                fg=ALARMA if usada > energia + 1e-9 else ABIERTA)
        if self.estado == "fallo":
            self.estado = "cerrada"
        self.dibujar()

    # ---------- Dibujo de la puerta ----------
    def dibujar(self):
        c = self.canvas
        c.delete("all")
        color = {"cerrada": LATON, "abierta": ABIERTA, "fallo": ALARMA}[self.estado]
        hueco = 48 if self.estado == "abierta" else 0
        c.create_rectangle(300, 18, 460, 190, fill="#0a2e26" if hueco else "#0b131b", outline=color, width=4)
        c.create_rectangle(304, 22, 380 - hueco, 186, fill=PANEL, outline=color, width=2)
        c.create_rectangle(380 + hueco, 22, 456, 186, fill=PANEL, outline=color, width=2)
        for x, letra, var in ((130, "A", self.va), (630, "B", self.vb)):
            c.create_oval(x - 50, 50, x + 50, 150, outline=color, width=3, fill=FONDO)
            c.create_text(x, 78, text=f"Palanca {letra}", fill=APAGADO, font=("Helvetica", 10))
            c.create_text(x, 108, text=f"{var.get():.1f}", fill=TEXTO, font=("Georgia", 26, "bold"))
        c.create_line(180, 100, 300, 100, fill=color, width=3)
        c.create_line(460, 100, 580, 100, fill=color, width=3)

    # ---------- Botón principal ----------
    def boton(self):
        if self.fase == "inicio":
            self.cargar_puerta()
        elif self.fase == "jugando":
            self.probar()
        elif self.fase == "abierta":
            self.nivel += 1
            self.cargar_puerta()
        else:
            self.reiniciar()

    def probar(self):
        _, _, funcion, calculo, umbral, energia = PUERTAS[self.nivel]
        a, b = round(self.va.get(), 1), round(self.vb.get(), 1)
        if a + b > energia + 1e-9:
            self.lbl_msg.config(fg=ALARMA, text="Gastaste más energía de la disponible. Baja alguna palanca (no pierdes vida).")
            return
        resultado = round(funcion(a, b), 2)
        cuenta = calculo.format(a=f"{a:g}", b=f"{b:g}")
        if resultado + 1e-9 >= umbral:
            self.puntos += 100 if self.fallos == 0 else 50
            self.estado, self.fase = "abierta", "abierta"
            self.lbl_msg.config(fg=ABIERTA, text=f"¡Se abrió! {cuenta} = {resultado:g}, que alcanza el umbral de {umbral:g}.")
            ultimo = self.nivel == len(PUERTAS) - 1
            if ultimo:
                self.fase = "fin"
                self.lbl_msg.config(text=f"¡Escapaste! {cuenta} = {resultado:g}. Puntaje final: {self.puntos} de 1000.")
            self.btn.config(text="Jugar de nuevo" if ultimo else "Siguiente puerta")
        else:
            self.vidas -= 1
            self.fallos += 1
            self.estado = "fallo"
            texto = f"No abrió. {cuenta} = {resultado:g}, y el umbral es {umbral:g}."
            if self.vidas == 0:
                self.fase = "fin"
                texto += f"\nTe quedaste sin vidas. Puntaje final: {self.puntos}."
                self.btn.config(text="Jugar de nuevo")
            else:
                texto += "\nAjusta las palancas e inténtalo otra vez."
            self.lbl_msg.config(fg=ALARMA, text=texto)
        self.refrescar_sin_reset()

    def refrescar_sin_reset(self):
        self.lbl_puntos.config(text=f"{self.puntos} puntos")
        self.lbl_vidas.config(text="♥ " * self.vidas + "♡ " * (3 - self.vidas))
        self.dibujar()


if __name__ == "__main__":
    ventana = tk.Tk()
    Juego(ventana)
    ventana.mainloop()
