# Métodos de resolución
Ahora que ya estamos familiarizados con el juego, tenemos que analizarlo para buscar diferentes maneras de resolverlo.
## Cómo podemos resolverlo?
Para resolver un sudoku, existen diferentes métodos, pero los que nos importan son los **métodos analítico-sistemáticos**, conjuntos de métodos que conducen a un resultado claro, para evitar soluciones falsas.
### Cribado
<div style="display: flex; justify-content: center;flex-wrap: wrap;">
    <img src="/sudoku/sudoku3.png" alt="Método de cribado" style="max-width: 40%; margin: 10px;">
</div>
Tomemos el mismo ejemplo, y busquemos una cifra frecuente, como el 5. En las líneas rojas trazadas en el dibujo no puede haber un 5, y en el bloque superior derecho, la única posición que queda libre es la resaltada en verde, por lo tanto el número 5 debe ir ahí.4

### _Counting through_
 <div style="display: flex; justify-content: center;flex-wrap: wrap;">
    <img src="/sudoku/sudoku3.png" alt="Método de cribado" style="max-width: 40%; margin: 10px;">
</div>
En el ejemplo de antes, busquemos líneas que tengan muchos números, como las dos resaltadas con los números en azul, y eliminando dichos números, podemos concluir que en el campo resaltado en azul sólo puede ir el número 5.

### Método de los desnudo
En este método, primero seleccionamos un campo, y eliminamos los números que pertenezcan a su misma columna, fila o bloque. Si sólo nos queda un número, entonces esa es la solución.

