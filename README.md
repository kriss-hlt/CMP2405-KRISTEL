# CMP2405-KRISTEL
Repositorio arquitectura de computadoras
# Mapa de Karnaugh y SOP

Programa en Python que genera el **mapa de Karnaugh** de una función booleana de **3 o 4 variables** y obtiene su **expresión mínima en suma de productos (SOP)**.

- **Nombre:** Kristel Hernadez Reyes
- **Materia:** CMP2405
- **Fecha de entrega:** 09/10/2026

---

## ¿Qué hace el programa?

1. Pide el número de variables (3 o 4), los minitérminos y, opcionalmente, los términos *don't care*.
2. Dibuja el mapa de Karnaugh en la consola, con el orden de código Gray en filas y columnas.
3. Calcula la expresión mínima en SOP.
4. Muestra los grupos elegidos y las celdas que cubre cada uno.
5. Si el usuario lo pide, genera un gráfico con matplotlib donde cada grupo se resalta con un color y un contorno. Los grupos que dan la vuelta por los bordes del mapa se dibujan con el contorno abierto del lado por el que continúan. El gráfico se guarda como `karnaugh.png`.

---

## Herramientas utilizadas

| Herramienta | Para qué se usó |
| **Python 3** | Lenguaje del proyecto (desarrollado y probado con Python 3.14) |
| **itertools** (biblioteca estándar) | Generar combinaciones al agrupar términos y al buscar la cobertura mínima |
| **matplotlib** | Dibujar el mapa de Karnaugh y resaltar los grupos |
| **Visual Studio Code** | Editor y terminal para escribir y ejecutar el código |
| **Git y GitHub** | Control de versiones y almacenamiento del proyecto |
| **Método de Quine-McCluskey** | Algoritmo de minimización (implicantes primos y cobertura mínima) |

---

## Datos de entrada

| Dato | Descripción | Ejemplo |
| Número de variables | Solo se admiten **3 o 4** | `3` |
| Minitérminos | Números de las combinaciones donde la función vale 1, separados por comas. Rango: `0 a 7` (3 variables) o `0 a 15` (4 variables) | `0,1,2,5,7` |
| Don't cares (opcional) | Combinaciones cuyo resultado no importa. Se dejan vacíos con Enter si no hay | `0,2,5` |

**Reglas de las variables:**
- Se llaman `A`, `B`, `C` y `D`. `A` es la variable más significativa.
- Un apóstrofo indica la variable negada: `A'` es "no A".
- Un mismo número no puede ser a la vez minitérmino y don't care.

---

## Requisitos e instalación

1. Instalar [Python 3](https://www.python.org/downloads/). En Windows, marcar la casilla **"Add python.exe to PATH"**.
2. Instalar matplotlib (solo hace falta para el gráfico):

```
python -m pip install matplotlib
```

---

## Cómo ejecutarlo

Desde la carpeta raíz del repositorio:

```
python Mapas_karnaugh\main.py
```

El programa pregunta los datos de entrada y, al final, si se desea mostrar el gráfico (`s` para sí, `n` para no).

---

## Ejemplos

### Ejemplo 1: 3 variables

Entrada: `3`, minitérminos `0,1,2,5,7`, sin don't cares.

```
Mapa de Karnaugh (3 variables)
  A\BC | 00  01  11  10
------------------------
     0 |  1   1   0   1
     1 |  0   1   1   0

Grupos elegidos:
  A'B'   -> celdas [0, 1]
  A'C'   -> celdas [0, 2]
  AC     -> celdas [5, 7]

F = A'B' + A'C' + AC
```

### Ejemplo 2: 4 variables con don't cares

Entrada: `4`, minitérminos `1,3,7,11,15`, don't cares `0,2,5`.

```
Grupos elegidos:
  A'D    -> celdas [1, 3, 5, 7]
  CD     -> celdas [3, 7, 11, 15]

F = A'D + CD
```

> Con estos datos también es mínima la expresión `A'B' + CD`: ambas tienen 2 términos y 4 literales. Cuando hay empate, cualquiera de las opciones es una respuesta correcta.

---

## ¿Cómo funciona?

1. **Construcción del mapa.** Las filas y columnas se ordenan con código Gray (`00, 01, 11, 10`), de modo que las celdas vecinas solo difieren en un bit. Con 3 variables, `A` va en las filas y `BC` en las columnas; con 4 variables, `AB` en las filas y `CD` en las columnas.
2. **Implicantes primos.** Se parte de los minitérminos y los don't cares, y se combinan repetidamente los términos que difieren en un solo bit, hasta que ya no se pueda simplificar más. Los términos que no se pueden combinar son los implicantes primos.
3. **Cobertura mínima.** Primero se eligen los implicantes primos esenciales (los únicos que cubren cierto minitérmino). Si quedan minitérminos sin cubrir, se busca el menor número de implicantes que los cubran y, en caso de empate, el que tenga menos literales.
4. **Don't cares.** Se usan para formar grupos más grandes, pero **no hace falta cubrirlos**: solo se cubren los minitérminos.
5. **Resultado.** Cada implicante se escribe como un producto de variables y se unen con `+` para formar la SOP.

---

## Estructura del proyecto

```
CMP2405-KRISTEL/
├── Mapas_karnaugh/
│   └── main.py        # Código del programa
├── README.md          # Este archivo
└── LICENSE
```

---

## Limitaciones

- Solo admite funciones de **3 o 4 variables, aun que de hecho la funcion de 4 variables fue extra**.
- El gráfico requiere tener matplotlib instalado; el resto del programa funciona sin él.

---

## Proceso de desarrollo

1. Se definió el problema: generar el mapa de Karnaugh y obtener la SOP mínima.
2. Se eligió el método de Quine-McCluskey para la minimización, porque es más fiable que agrupar a ojo y se puede automatizar.
3. Se programó la construcción del mapa con código Gray y el soporte para 3 y 4 variables.
4. Se agregó la minimización con implicantes primos, implicantes esenciales y búsqueda de la cobertura mínima.
5. Se agregó el soporte para don't cares.
6. Se agregó el gráfico con matplotlib, con grupos de colores y contornos abiertos en los grupos que dan la vuelta por los bordes.
7. Se probó con varios casos, incluyendo 3 variables, 4 variables y don't cares.
8. Se subió el proyecto a GitHub con Git.