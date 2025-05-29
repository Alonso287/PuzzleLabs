#  Creación de un sudoku
Tras haber hecho un algoritmo completo de resolución de sudokus, ahora tenemos que hallar una  manera de crear sudokus para que luego el usuario los pueda imprimir.
___

La primera idea que se nos puede ocurrir es coger una cuadrícula de sudoku y rellenar números aleatorios sin romper las reglas, pero esto no funcionaría, ya que, técnicamente, un buen sudoku debería tener una sola solución, y además, puede ocurrir que el sudoku que generemos no tenga solución, por lo tanto tenemos que descartar ese método.