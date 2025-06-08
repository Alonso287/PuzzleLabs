#  Creación de un sudoku
Tras haber hecho un algoritmo completo de resolución de sudokus, ahora tenemos que hallar una  manera de crear sudokus para que luego el usuario los pueda imprimir.
___

La primera idea que se nos puede ocurrir es coger una cuadrícula de sudoku y rellenar números aleatorios sin romper las reglas, pero esto no funcionaría, ya que, técnicamente, un buen sudoku debería tener una sola solución, y además, puede ocurrir que el sudoku que generemos no tenga solución, por lo tanto tenemos que descartar ese método.

___

Sin embargo, tras pensarlo un tiempo, podemos ver que podemos reutilizar el código que se encarga de analizar los números, y añadirle un factor aleatorio:

En la [página anterior](/sudoku/solver/solving-alg#_1-analisis-de-candidatos) hemos visto que la parte del programa que se encarga de buscar los números candidatos funciona de la siguiente manera:
>Este sería el proceso del algoritmo de candidatos en orden:
>1. El programa debe ir escaneando cada celda, y recolectar los números que están en su misma columna, fila y campo.
>1. Después, eliminará cada número que haya encontrado en esos lugares.
>    1. Si sólo se queda con un número, entonces asignará ese número a ese campo, y continuará al siguiente.
>    1. En cambio, si se queda con varios números, saltará al siguiente, y repetirá el proceso.
>1. Este proceso se repetirá hasta que no se puedan rellenar más celdas,y tras ello, imprimirá los resultados.

A este algoritmo le haremos las siguientes modificaciones para que se encargue de generar sudokus:

- Tomaremos el primer paso, que se encarga de buscar los números que **no** pueden estar en esa casilla, ya que están en su misma columna, fila o bloque.
- En el segundo paso, en vez de saltar al siguiente si se queda con varios números, lo que hará será elegir un número aleatorio entre ellos, y pasará al siguiente.

Esto hará que empecemos con un tablero vacío y se vayan rellenando las celdas de manera aleatoria.

___

Sin embargo, puede que tengamos mala suerte y la colocación aleatoria de números haga que lleguemos a un punto en el que no haya números posibles que se puedan rellenar, así que también tenemos que hacer un algoritmo de backtracking que compruebe posibles soluciones, con DFS, al igual que en el [algorimo anterior](/sudoku/solver/solving-alg#_4-fuerza-bruta):
- El código irá rellenando hasta que no se puedan rellenar más celdas de forma válida.
- En ese momento, deshará el "movimiento", y rellenará otra celda en su lugar.
- Repetirá todo ese proceso hasta que se complete el sudoku de manera aleatoria.
- Después, se eliminarán los números de manera aleatoria, para dejar la cantidad de pistas que haya pedido el usuario.
- Por último, se imprimirá el sudoku.
- Si el usuario lo pide, se imprimirá después la solución.

Como puedes ver, el funcionamiento de un algoritmo de creación es mucho más fácil en comparación con el de resolución.

