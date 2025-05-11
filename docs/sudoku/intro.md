---
prev: false
---
# Introducción
## ¿Qué es el Sudoku?
[Sudoku](https://es.wikipedia.org/wiki/Sudoku) es un juego matemático inventado a finales de la década de 1970 en japón.
## ¿Cómo se juega ?
El objetivo del sudoku es rellenar una cuadrícula de 9x9 celdas, cada una dividida en subcuadrículas de 3x3, con las cifras del 1 al 9. Algunos números ya están rellenados y no se debe repetir el mismo número en la misma fila, columna o subcuadrícula.s

Si el sudoku está bien planteado, sólo puede tener una solución, y debería tener 17 pistas iniciales, es decir, 17 números ya rellenados como mínimo.

Aquí hay un ejemplo de un sudoku sin resolver y uno resuelto:
<div style="display: flex; justify-content: center;flex-wrap: wrap;">
    <img src="/sudoku/sudoku1.png" alt="Sudoku sin resolver" style="max-width: 40%; margin: 10px;">
    <img src="/sudoku/sudoku2.png" alt="Sudoku sin resolver" style="max-width: 40%; margin: 10px;">
</div>

## Equivalente matemático
Matemáticamente, la solución de un sudoku es siempre un cuadrado latino, es decir, una matriz de $n * n$ elementos, en la que cada casilla está ocupada por uno de los n símbolos de tal manera que cada uno de ellos aparece exactamente una vez en cada columna y en cada fila.

$$\begin{bmatrix}
a & b & d & c\\
b & c & a & d\\
c & d & b & a\\
d & a & c & b
\end{bmatrix}$$

Un cuadrado latino está reducido si la primera fila y la primera columna están en orden natural.

La cantidad de números de cuadrados latinos de $n \times n$ No tiene una fórmula sencilla, pero crece increíblemente rápido.
Como curiosidad, aquí tenéis una tabla con la cantidad de cuadrados latinos y cuadrados latinos reducidos desde $n = 1$ hasta $n = 11$:
<div style="justify-content: center; display: flex;">

|$n$ | Número de cuadrados latinos de tamaño $n \times n$  |
| -- | --------------------------------------------------: |
|  1 |                                                   1 |
|  2 |                                                   2 |
|  3 |                                                  12 |
|  4 |                                                 576 |
|  5 |                                              161280 |
|  6 |                                           812851200 |
|  7 |                                      61479419904000 |
|  8 |                               108776032459082956800 |
|  9 |                        5524751496156892842531225600 |
| 10 |               9982437658213039871725064756920320000 |
| 11 |    776966836171770144107444346734230682311065600000 |
</div>

Sin embargo, el sudoku impone una restricción adicional a los subgrupos de 3 x 3 , como si fuera un caso especial de cuadrado latino, lo que nos deja con $6,670,903,752,021,072,936,960\approx6.67\times10^{21}$ soluciones posibles, pero esa cifra baja a $5,472,730,538$ si tenemos en cuenta las simetrías que puedan surgir.

$$\begin{bmatrix}\begin{bmatrix}
 e & c & d \\
 f & g & b \\
 a & i & h
\end{bmatrix}\begin{bmatrix}
 f & g & h \\
 a & i & e \\
 c & d & b
\end{bmatrix}\begin{bmatrix}
 i & a & b \\
 c & d & h \\
 e & f & g
\end{bmatrix}
\\
\begin{bmatrix}
 h & e & i \\
 d & b & f \\
 g & a & c
\end{bmatrix}\begin{bmatrix}
 g & f & a \\
 h & e & c \\
 i & b & d
\end{bmatrix}\begin{bmatrix}
 d & b & c \\
 g & i & a \\
 h & e & f
\end{bmatrix}
\\
\begin{bmatrix}
 i & f & a \\
 b & h & g \\
 c & d & e
\end{bmatrix}\begin{bmatrix}
 e & c & g \\
 d & a & i \\
 b & h & f
\end{bmatrix}\begin{bmatrix}
 b & h & d \\
 f & c & e \\
 a & g & i
\end{bmatrix}\end{bmatrix}$$
La representación matemática del primer sudoku sería algo parecido a esto, 9 cuadrados latinos diferentes, cuyas filas y columnas juntas no pueden tener los mismos elementos, es decir, 9 cuadrados latinos dentro de un cuadrado latino.