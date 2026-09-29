# Escape room difuso (versión consola, sin interfaz gráfica)

# ---------- Operadores difusos ----------
def y_min(a, b): return min(a, b)          # AND clásico
def y_prod(a, b): return a * b             # AND alternativo
def o_max(a, b): return max(a, b)          # OR clásico
def o_suma(a, b): return a + b - a * b     # OR alternativo
def no(a): return 1 - a                    # NOT

# ---------- Puertas: (nombre, regla, función, cuenta, umbral, energía) ----------
PUERTAS = [
    ("Recepción",         "A AND B (mínimo)",             y_min,                        "mín({a}, {b})",         0.5,  1.2),
    ("Pasillo",           "A OR B (máximo)",              o_max,                        "máx({a}, {b})",         0.7,  0.8),
    ("Archivo",           "A AND B (mínimo)",             y_min,                        "mín({a}, {b})",         0.6,  1.4),
    ("Laboratorio",       "A OR B (máximo)",              o_max,                        "máx({a}, {b})",         0.9,  1.0),
    ("Cuarto de cámaras", "A AND NOT B",                  lambda a, b: y_min(a, no(b)), "mín({a}, 1 − {b})",     0.6,  1.0),
    ("Servidores",        "NOT A AND B",                  lambda a, b: y_min(no(a), b), "mín(1 − {a}, {b})",     0.6,  1.0),
    ("Bóveda interna",    "A AND NOT B",                  lambda a, b: y_min(a, no(b)), "mín({a}, 1 − {b})",     0.7,  1.0),
    ("Reactor",           "A AND B (producto)",           y_prod,                       "{a} × {b}",             0.36, 1.2),
    ("Sala de control",   "A OR B (suma probabilística)", o_suma,                       "{a} + {b} − {a}×{b}",   0.8,  0.9),
    ("Salida final",      "A AND B (producto)",           y_prod,                       "{a} × {b}",             0.49, 1.4),
]


# ---------- Fuzzificación: pasar un número a etiquetas (bajo, medio, alto) ----------
def fuzzificar(x):
    bajo = max(0, 1 - x / 0.5)
    medio = max(0, 1 - abs(x - 0.5) / 0.5)
    alto = max(0, (x - 0.5) / 0.5)
    partes = [f"{nombre} {grado:.1f}" for nombre, grado in (("bajo", bajo), ("medio", medio), ("alto", alto)) if round(grado, 1) > 0]
    return ", ".join(partes)


def pedir_valor(nombre):
    while True:
        texto = input(f"  Palanca {nombre} (0 a 1): ").replace(",", ".")
        try:
            valor = round(float(texto), 2)
        except ValueError:
            print("  Escribe un número, por ejemplo 0.6")
            continue
        if 0 <= valor <= 1:
            return valor
        print("  El valor debe estar entre 0 y 1")


def jugar():
    vidas, puntos = 3, 0
    print("\n=== ESCAPE ROOM DIFUSO ===")
    print("Cada puerta abre si el resultado de su regla llega al umbral.")
    print("No puedes gastar más energía de la disponible (A + B). Tienes 3 vidas.")
    
    print("\n=== EXPLICACIÓN ===")
    print("Si es AND, vamos a considerar el mínimo entre los dos números. Es decir, si el umbral para abrir la puerta es 0.5. \n La combinación ganadora es A(0.5) y B(0.5).")

    for numero, (nombre, regla, funcion, cuenta, umbral, energia) in enumerate(PUERTAS, 1):
        fallos = 0
        print(f"\n--- Puerta {numero} de 10: {nombre} ---")
        print(f"Regla: {regla} | Umbral: {umbral:g} | Energía: {energia:g} | Vidas: {vidas}")

        while True:
            a, b = pedir_valor("A"), pedir_valor("B")
            if a + b > energia + 1e-9:
                print(f"  Usaste {a + b:g} de energía y solo hay {energia:g}. Baja alguna palanca (no pierdes vida).")
                continue

            resultado = round(funcion(a, b), 2)
            print(f"  A = {a:g} → {fuzzificar(a)}")
            print(f"  B = {b:g} → {fuzzificar(b)}")
            print(f"  {cuenta.format(a=f'{a:g}', b=f'{b:g}')} = {resultado:g} → {fuzzificar(resultado)}")

            if resultado + 1e-9 >= umbral:
                puntos += 100 if fallos == 0 else 50
                print(f"  ¡La puerta se abrió! Puntos: {puntos}")
                break

            vidas -= 1
            fallos += 1
            print(f"  No abrió: {resultado:g} no llega a {umbral:g}.")
            if vidas == 0:
                print(f"\nGAME OVER. Llegaste a la puerta {numero}. Puntaje: {puntos} de 1000.")
                return
            print(f"  Te quedan {vidas} vidas. Inténtalo otra vez.")

    print(f"\n¡ESCAPASTE! Puntaje final: {puntos} de 1000.")


if __name__ == "__main__":
    while True:
        jugar()
        if input("\n¿Jugar otra vez? (s/n): ").strip().lower() != "s":
            break