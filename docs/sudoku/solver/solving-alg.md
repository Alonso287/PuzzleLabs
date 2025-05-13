::: warning **ATENCIÓN**    
**Todavía no he aprendido a programar, así que el contenido de esta parte de la guía es puramente teórico, y puede tener cambios en la práctica.**
**La guía será actualizada con código real en Python tan pronto como aprenda a programar**
:::
# Creación de un algoritmo de resolución de sudokus
Ahora que conocemos el juego y sus formas de resolverlo en profundidad, tenemos que intentar crear un algoritmo que pueda resolver sudokus de manera eficiente.
He elegido Python como lenguaje de programación debido a su facilidad de uso.
## Inserción de los datos
Lógicamente, para que el programa funcione, tenemos que averiguar un método eficiente para insertar nuestros datos.

Como el programa se va a encargar de resolver sudokus, creo que la manera más fácil de insertar el problema en el programa es que vaya preguntando por el número que está en cada celda.
<div style="display: flex; justify-content: center;flex-wrap: wrap;">
    <img src="/sudoku/sudoku1.png" alt="Sudoku vacío con coordenadas" style="max-width: 40%; margin: 10px;">
</div>

Por ejemplo, si queremos insertar el siguiente sudoku, escribiremos lo siguiente:
```ansi
Datos por filas:
> 5
> 3
> 0
> 0
> 7
> 0
...
```
Escribiremos 0 si la celda está vacía, y los datos serán almacenados en una matriz de Python, básicamente una lista con listas.
Un ejemplo de código sería este:
```python
filas = int(input("filas: "))
columnas = int(input("columnas: "))

matrix = [] 
print("Datos por filas:")

for i in range(filas):   
    fila = []
    for j in range(columnas):
        fila.append(int(input()))    # el usuario introduc las filas
    matrix.append(fila)  # para añadir filas

print("\nLa matriz es:")

for i in range(filas):
    for j in range(columnas):
        print(matrix[i][j], end=" ")
    print()
```
## Algoritmo de resolución
Para que el programa resuelva el sudoku, debemos establecer un orden de ejecución de los diferentes métodos de resolución.
Todos ellos se basan en encontrar los números candidatos, es decir, eliminar los números que estén en la misma fila, columna o bloque, o campo que estemos analizando.
Por lo tanto, el primer paso será el análisis de candidatos.
### 1. Análisis de candidatos.
Para analizar los candidatos de una celda, debemos asumir que son candidatos todos los posibles números, es decir, del 1 al 9.
Después, escanearemos la fila, columna y campo en la que está el número, y eliminaremos los números que encontremos. 
Por ejemplo, para el primmer campo vacío, en a3, eliminaríamos los números 5,3,7,6,9, y 8, y así sucesivamente con todos los números.
Tras hacer eso, nos quedaría algo así:
<div style="display: flex; justify-content: center;flex-wrap: wrap;">
    <img src="/sudoku/candidatos1.png" alt="candidatos" style="max-width: 40%; margin: 10px;">
</div>
Como puedes ver, hay ocasiones en las que nos queda sólo un número candidato, por lo que podemos rellenarlo, lo que va a causar que se eliminen más candidatos en otras celdas, de hecho este ejemplo se puede resolver entero utilizando este método.
___
Pero, qué ocurre si nos quedamos sin candidatos?

### 2. Análisis de parejas y tríos desnudos
Veamos este ejemplo:
<div style="display: flex; justify-content: center;flex-wrap: wrap;">
    <img src="/sudoku/pares.png" alt="Pares" style="max-width: 40%; margin: 10px;">
</div>

Aquí ya hemos aplicado el primer paso del algoritmo, y todavía nos quedan muchos huecos. ¿Qué hacemos?

La pareja de números que hay resaltada en azul se llama "par desnudo", es decir, es una pareja de números candidatos que comparten la misma unidad, es decir: la misma fila, columna o blloque. 
Cuando esto ocurre, sabemos que un número va a estar en una casilla y el otro en la otra, y, aunque no sabemos cuál de los dos está en qué casilla, podemos eliminar los dos de la unidad correspondiente, en este caso, del mismo campo. En este caso, eliminamos el 9 del campo resaltado en verde, lo que nos deja con una sola posibilidad.

<!-- https://www.sudokuwiki.org/Naked_Candidates#NP -->










































<!-- 

### Parte 1
1. El programa debe ir escaneando cada celda, y recolectar los números que están en su misma columna, fila y campo.
1. Después, eliminará cada número que haya encontrado en esos lugares.
    1. Si sólo se queda con un número, entonces asignará ese número a ese campo, y continuará al siguiente.
    1. En cambio, si se queda con varios números, saltará al siguiente, y repetirá el proceso.
1. Este proceso se repetirá hasta que haya completado el sudoku entero,y tras ello, imprimirá los resultados.
### Parte 2
Es posible que el sudoku se quede con algunos huecos que no se pueden resolver por este método, así que tras esto utilizaremos el método de fuerza bruta, o _"brute-force"_.
La variante de este método que vamos a utilizar es el llamado "búsqueda en profundidad", o _"depth-first search"_, que analiza cada posible "rama" de soluciones hasta el final, antes de pasar a la siguiente, de la siguiente manera:
<div style="display: flex; justify-content: center;flex-wrap: wrap;">
    <img src="/sudoku/search.gif" alt="Búsqueda en profundidad" style="max-width: 40%; margin: 10px;">
</div>
Aunque esto pueda parecer muy ineficiente, en realidad no lo es tanto, ya que las opciones que quedarán tras resolver el sudoku de forma analítica serían bastantes menos.
Por ejemplo, el sudoku de los ejemplos anteriores se puede resolver únicamente con el algoritmo analítico.

### Parte 3
Otra manera de hacer el algoritmo más rápido es eliminar "parejas desnudas".
Veamos este otro ejemplo:
<div style="display: flex; justify-content: center;flex-wrap: wrap;">
    <img src="/sudoku/sudoku4.png" alt="Eliminación de parejas" style="max-width: 40%; margin: 10px;">
</div>
En este sudoku, los números en negro son los que ya venían, los números en azul son los que han sido rellenados por el primer algoritmo y las casillas marcadas en verde y rojo son parejas desnudas, es decir, son dos celdas que están en el mismo campo, fila o columna,y comparten los mismos números candidatos
Esto significa que si un número va en una casilla, el restante va en la otra, y, aunque no sabemos cuál es la combinación correcta, podemos eliminar los dos números del resto de filas.
Por lo tanto, podemos eliminar los números 8 y 1 de la casilla naranja y el 7 de la casilla azul. 

-->

