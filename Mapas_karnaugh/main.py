"""
Mapa de Karnaugh (3 o 4 variables) y expresión mínima en suma de productos (SOP).

Minimización: Quine-McCluskey (implicantes primos + cobertura mínima).
Variables: A es el bit más significativo (A B C [D]).
"""

from itertools import combinations

NOMBRES = "ABCD"
# (bits que van en las filas, bits que van en las columnas)
DISTRIBUCION = {3: (1, 2), 4: (2, 2)}


# ---------------------------------------------------------------- utilidades
def gray(bits):
    """Secuencia de código Gray de 'bits' bits (00, 01, 11, 10 ...)."""
    return [i ^ (i >> 1) for i in range(1 << bits)]


def literales(imp, n):
    _, mascara = imp
    return n - bin(mascara).count("1")


def cubre(imp, m):
    valor, mascara = imp
    return (m & ~mascara) == valor


def termino_a_texto(imp, n):
    valor, mascara = imp
    partes = []
    for i in range(n):
        pos = n - 1 - i
        if mascara >> pos & 1:
            continue  # variable eliminada
        partes.append(NOMBRES[i] + ("" if valor >> pos & 1 else "'"))
    return "".join(partes) if partes else "1"


# ------------------------------------------------------- Quine-McCluskey
def implicantes_primos(terminos):
    """Devuelve el conjunto de implicantes primos como tuplas (valor, mascara)."""
    actual = {(t, 0) for t in terminos}
    primos = set()
    while actual:
        siguiente, usados = set(), set()
        for (v1, m1), (v2, m2) in combinations(sorted(actual), 2):
            if m1 != m2:
                continue
            d = v1 ^ v2
            if d and d & (d - 1) == 0:  # difieren en exactamente un bit
                siguiente.add((v1 & v2, m1 | d))
                usados.add((v1, m1))
                usados.add((v2, m2))
        primos |= actual - usados
        actual = siguiente
    return primos


def cobertura_minima(primos, minterminos, n):
    """Elige el menor conjunto de primos que cubre todos los minterminos."""
    primos = list(primos)
    cubiertos = {p: {m for m in minterminos if cubre(p, m)} for p in primos}

    # 1) implicantes primos esenciales
    elegidos = set()
    for m in minterminos:
        candidatos = [p for p in primos if m in cubiertos[p]]
        if len(candidatos) == 1:
            elegidos.add(candidatos[0])

    pendientes = set(minterminos)
    for p in elegidos:
        pendientes -= cubiertos[p]

    # 2) lo que falte: búsqueda exhaustiva (el problema es pequeño)
    if pendientes:
        restantes = [p for p in primos
                     if p not in elegidos and cubiertos[p] & pendientes]
        mejor, mejor_costo = None, None
        for k in range(1, len(restantes) + 1):
            for comb in combinations(restantes, k):
                if set().union(*(cubiertos[p] for p in comb)) >= pendientes:
                    costo = sum(literales(p, n) for p in comb)
                    if mejor is None or costo < mejor_costo:
                        mejor, mejor_costo = comb, costo
            if mejor is not None:  # ya encontramos con k términos: el mínimo
                break
        elegidos |= set(mejor)

    return sorted(elegidos)


def minimizar_sop(n, minterminos, dontcares=()):
    minterminos, dontcares = set(minterminos), set(dontcares)
    if not minterminos:
        return "0", []
    primos = implicantes_primos(minterminos | dontcares)
    elegidos = cobertura_minima(primos, minterminos, n)
    expresion = " + ".join(termino_a_texto(p, n) for p in elegidos)
    return expresion, elegidos


# ------------------------------------------------------------ mapa de K
def imprimir_mapa(n, minterminos, dontcares=()):
    bits_f, bits_c = DISTRIBUCION[n]
    filas, columnas = gray(bits_f), gray(bits_c)
    et_f, et_c = NOMBRES[:bits_f], NOMBRES[bits_f:n]

    print(f"\nMapa de Karnaugh ({n} variables)")
    print(f"{et_f}\\{et_c}".rjust(6) + " | " +
          "  ".join(format(c, f"0{bits_c}b") for c in columnas))
    print("-" * (9 + 4 * len(columnas)))
    for f in filas:
        celdas = []
        for c in columnas:
            m = (f << bits_c) | c
            celdas.append(" 1" if m in minterminos
                          else " X" if m in dontcares else " 0")
        print(format(f, f"0{bits_f}b").rjust(6) + " | " + "  ".join(celdas))


# ------------------------------------------------- gráfico (matplotlib)
def dibujar_mapa(n, minterminos, dontcares, grupos, expresion, archivo=None):
    """Dibuja el mapa y resalta cada grupo con un color y un contorno propio.

    Los grupos que dan la vuelta por los bordes se dibujan con el contorno
    abierto del lado por el que continúan.
    """
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Rectangle

    bits_f, bits_c = DISTRIBUCION[n]
    filas, columnas = gray(bits_f), gray(bits_c)
    nf, nc = len(filas), len(columnas)
    et_f, et_c = NOMBRES[:bits_f], NOMBRES[bits_f:n]
    colores = ["#e63946", "#2a9d8f", "#f4a261", "#457b9d",
               "#9b5de5", "#6a994e", "#d62828", "#fb8500"]

    fig, ax = plt.subplots(figsize=(1.2 * nc + 2, 1.2 * nf + 3))
    ax.set_xlim(-0.9, nc)
    ax.set_ylim(nf, -0.8)  # eje y invertido: la fila 0 queda arriba
    ax.set_aspect("equal")
    ax.axis("off")

    # cuadrícula, valores y etiquetas
    celda_de = {}
    for r, f in enumerate(filas):
        for c, col in enumerate(columnas):
            m = (f << bits_c) | col
            celda_de[m] = (r, c)
            ax.add_patch(Rectangle((c, r), 1, 1, fill=False,
                                   edgecolor="#999999", lw=1))
            valor = "1" if m in minterminos else "X" if m in dontcares else "0"
            ax.text(c + 0.5, r + 0.5, valor, ha="center", va="center",
                    fontsize=16, fontweight="normal" if valor == "0" else "bold",
                    color="#999999" if valor == "0" else "black")
            ax.text(c + 0.93, r + 0.07, str(m), ha="right", va="top",
                    fontsize=7, color="#999999")
    for c, col in enumerate(columnas):
        ax.text(c + 0.5, -0.3, format(col, f"0{bits_c}b"),
                ha="center", va="center", fontsize=12)
    for r, f in enumerate(filas):
        ax.text(-0.4, r + 0.5, format(f, f"0{bits_f}b"),
                ha="center", va="center", fontsize=12)
    ax.text(-0.4, -0.3, f"{et_f}\\{et_c}", ha="center", va="center",
            fontsize=11, fontweight="bold")

    # grupos
    leyenda = []
    for gi, g in enumerate(grupos):
        color = colores[gi % len(colores)]
        d = min(0.07 + 0.04 * gi, 0.3)  # sangría para distinguir traslapes
        celdas = {celda_de[m] for m in range(1 << n) if cubre(g, m)}
        kw = dict(color=color, lw=2.5, solid_capstyle="round")

        for (r, c) in celdas:
            ax.add_patch(Rectangle((c, r), 1, 1, facecolor=color,
                                   alpha=0.15, edgecolor="none"))
        if len(celdas) == nf * nc:  # el grupo es todo el mapa
            ax.add_patch(Rectangle((d, d), nc - 2 * d, nf - 2 * d,
                                   fill=False, edgecolor=color, lw=2.5))
        else:
            for (r, c) in celdas:
                izq = (r, (c - 1) % nc) in celdas
                der = (r, (c + 1) % nc) in celdas
                arr = ((r - 1) % nf, c) in celdas
                aba = ((r + 1) % nf, c) in celdas
                x0, x1 = c + (0 if izq else d), c + 1 - (0 if der else d)
                y0, y1 = r + (0 if arr else d), r + 1 - (0 if aba else d)
                if not arr:
                    ax.plot([x0, x1], [r + d] * 2, **kw)
                if not aba:
                    ax.plot([x0, x1], [r + 1 - d] * 2, **kw)
                if not izq:
                    ax.plot([c + d] * 2, [y0, y1], **kw)
                if not der:
                    ax.plot([c + 1 - d] * 2, [y0, y1], **kw)
        leyenda.append(Line2D([0], [0], color=color, lw=3,
                              label=termino_a_texto(g, n)))

    ax.set_title(f"F = {expresion}", fontsize=14, pad=12)
    if leyenda:
        ax.legend(handles=leyenda, loc="upper center",
                  bbox_to_anchor=(0.5, 0.0), ncol=min(len(leyenda), 4),
                  frameon=False)

    if archivo:
        fig.savefig(archivo, dpi=150, bbox_inches="tight")
        print(f"Gráfico guardado en {archivo}")
    plt.show()


# ------------------------------------------------------------------ main
def leer_lista(texto, maximo):
    if not texto.strip():
        return set()
    valores = {int(x) for x in texto.replace(",", " ").split()}
    fuera = [v for v in valores if not 0 <= v < maximo]
    if fuera:
        raise ValueError(f"Valores fuera de rango (0 a {maximo - 1}): {fuera}")
    return valores


def main():
    n = int(input("Número de variables (3 o 4): "))
    if n not in DISTRIBUCION:
        raise SystemExit("Solo se admiten 3 o 4 variables.")
    total = 1 << n
    minterminos = leer_lista(input(f"Minitérminos (0 a {total - 1}), separados por comas: "), total)
    dontcares = leer_lista(input("Don't cares (opcional): "), total)
    if minterminos & dontcares:
        raise SystemExit("Un término no puede ser minitérmino y don't care a la vez.")

    imprimir_mapa(n, minterminos, dontcares)
    expresion, grupos = minimizar_sop(n, minterminos, dontcares)

    print("\nGrupos elegidos:")
    for g in grupos:
        celdas = sorted(m for m in range(total) if cubre(g, m))
        print(f"  {termino_a_texto(g, n):<6} -> celdas {celdas}")
    print(f"\nF = {expresion}")

    if input("\n¿Mostrar el gráfico con matplotlib? (s/n): ").strip().lower().startswith("s"):
        try:
            dibujar_mapa(n, minterminos, dontcares, grupos, expresion, "karnaugh.png")
        except ImportError:
            print("Falta matplotlib. Instálalo con: pip install matplotlib")


if __name__ == "__main__":
    main()
