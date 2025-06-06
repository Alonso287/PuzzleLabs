# Práctica: Programación de un algoritmo de creación de sudokus<Badge type="warning" text="Trabajo en progreso" />
Ahora que ya hemos investigado en profundidad el funcionamiento de nuestro algoritmo de resolución, tenemos que trasladarlo a código.

___

El código se dividirá en diferentes funciones o módulos, uno para cada algoritmo o característica del programa.

# Introducción y almacenamiento de datos
Empezaremos por la primera función, que llamaremos `leer_tablero()`:
Se encargará de recibir cadenas de texto en un formato específico, que luego "traduciremos" y almacenaremos como una matriz 2D:
Utilizaremos dos métodos diferentes, según la ocasión:
- Por filas
- Como una única cadena
___
La primera parte de `leer_tablero` recibirá una cadena de 9 dígitos y las convertirá a valores en una lista. Como referencia, así es como queremos que se introduzcan los datos en la variable:
```python
tablero = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],

    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],

    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
```

## Introducción de datos por filas
Para almacenar los datos por filas, crearemos el siguiente programa:
```python
def leer_tablero():
    while True:
        tablero = []
        print("Introduce el tablero de Sudoku, fila por fila, usando 0 para los huecos.")
        print("Ejemplo: 530070000")
        for i in range(9):
            while True:
                fila_input = input(f"Fila {i+1}: ").strip()
                if len(fila_input) != 9 or not fila_input.isdigit():
                    print(f"Error: La fila {i+1} no es válida. Debe tener exactamente 9 dígitos.")
                    continue
                fila = [int(c) for c in fila_input]
                if not validar_fila(fila):
                    print(f"Error: Número repetido en la fila {i+1}.")
                        continue 
                tablero.append(fila)
                break
        print("\nTablero introducido por filas:")
        imprimir_tablero(tablero)

        if not validar_tablero(tablero):
            print("Tablero inválido. Vuelve a introducirlo.")
            continue

        correcto = input ("\n ¿El tablero introducido es correcto? (s/n): ").strip().lower()
        while correcto not in ['s', 'n']:
            print("Opción inválida. Por favor ingresa 's' o 'n'.")
            correcto = input("\n ¿El tablero introducido es correcto? (s/n): ").strip().lower()
         
        if correcto == 'n':
                continue
            elif correcto == 's':
                break
    return tablero
```
- Primero, empieza un bucle que se repite 9 veces, una para cada fila, en el que se pide al usuario que introducza una cadena de 9 caractere por cada fila (Lanzando un error si la cadena introducida no tiene 9 dígitos), utilizando `strip()`, que elimina posibles espacios al inicio y al final de la cadena.
- Después establece los elementos de la lista `fila` como cada uno de los dígitos de la cadena introducida.
- Después, se llama a la función `validar_ fila`, que se encargará de verificar si la fila introducida es correcta, y no tiene ningún número repetido.
- Tras ello, se añade esa lista `fila` a la lista `tablero`.
- Después, se llama a la función `validar_tablero`, que se encargará de verificar si el tablero es correcto.
- Por último, se imprimirá el tablero y se preguntará al usuario si es correcto. Si el tablero es incorrecto, el bucle entero vuelve a empezar.

Adicionalmente, crearemos una función `validar_fila`, a la que le pasaremos la fila introducida en el modo de introducción por filas:
```python
def validar_fila(fila):
    """
    Valida que no haya números repetidos en la fila.
    """
    numeros = [num for num in fila if num != 0]
    return len(numeros) == len(set(numeros))
```
## Introducción de datos como una única cadena
Una manera muy rápida y cómoda de compartir tableros de Sudoku es con una cadena de 81 caracteres, que representan las diferentes celdas de izquierda a derecha y de arriba a abajo, con "." para las celdas vacías.
Por lo tanto, además de poder introducir los datos por filas, también tendremos la opción de introducirlo todo como una cadena:
```python
def leer_tablero():
    while True:
        cadena_input = input('Introduce el tablero como una cadena de 81 caracteres ("." para huecos):').strip()
        if not all(c.isdigit() or c == '.' for c in cadena_input):
            print("Error: La cadena solo debe contener dígitos o '.'.")
            continue
        if len(cadena_input) != 81:
            print("Error: La cadena debe tener exactamente 81 caracteres.")
            continue

        # Reemplazar los '.' por '0'
        cadena_input = cadena_input.replace('.', '0')
            
        # Convertir la cadena en un tablero 9x9
        tablero = [ [int(cadena_input[i*9 + j]) for j in range(9)] for i in range(9)]
            
        print("\nTablero introducido desde cadena:")
        imprimir_tablero(tablero)

        if not validar_tablero(tablero):
            print("Tablero inválido. Vuelve a introducirlo.")
            continue            

        correcto = input ("\n ¿El tablero introducido es correcto? (s/n): ").strip().lower()
        while correcto not in ['s', 'n']:
            print("Opción inválida. Por favor ingresa 's' o 'n'.")
            correcto = input("\n ¿El tablero introducido es correcto? (s/n): ").strip().lower()
         
        if correcto == 'n':
            continue
        elif correcto == 's':
            break
        return tablero
```
- Primero se pide una cadena de 81 caracteres (Lanzando un error si la cadena introducida no tiene 81 dígitos o contiene algo diferente a números o `"."`), utilizando `strip()` para eliminar posibles espacios al inicio o al final de la cadena.
- Después se actualiza la cadena recibida, reemplazando los `"."` por `"0"`. Esto hace que introducir una cadena con `"0"` en vez de `"."` también funcione, ya que simplemente este paso no se ejecuta.
- Tras ello, se establece la lista `tablero` como dos bucles:
  1. Iteración sobre las filas (``i``): El primer bucle, ``for i in range(9)``, recorre las filas del tablero. Cada fila corresponde a 9 celdas, es decir, 9 caracteres consecutivos en la cadena.
  2. Acceder a las celdas dentro de cada fila (``j``): El segundo bucle, ``for j in range(9)``, recorre las celdas dentro de una fila.
  - Cálculo de la posición en la cadena: La fórmula ``i*9 + j`` se utiliza para calcular la posición en la cadena.
     - Si i = 0, la fila 0 comienza en el índice 0 de la cadena.
     - Si i = 1, la fila 1 comienza en el índice 9 de la cadena (9*1 = 9), y así sucesivamente.
     - Para obtener el número correcto de cada fila, se toma la celda correspondiente de la cadena.
-  Después, se llama a la función `validar_tablero`, que se encargará de verificar si el tablero es correcto.
- Por último, se imprimirá el tablero y se preguntará al usuario si es correcto. Si el tablero es incorrecto, el bucle entero vuelve a empezar.
## Impresión del tablero
Ya hemos decidido que el tablero va a consistir de una matriz 2D, es decir, una lista de listas, así que tenemos que escribir un código que lea esta variable e imprima el tablero correctamente.
Para ello, crearemos un bucle que vaya imprimiendo cada elemento (fila), y extraiga los elementos que contiene (celdas independientes).
El resultado sería este:
```python
def imprimir_tablero(tablero):
    """
    Imprime el tablero de Sudoku en formato tradicional.
    """
    print("=" * 25)
    for i, fila in enumerate(tablero):
        fila_str = ""
        for j, num in enumerate(fila):
            if num == 0:
                fila_str += ". "
            else:
                fila_str += str(num) + " "
            if (j + 1) % 3 == 0 and j != 8:
                fila_str += "| "
        print(fila_str)
        if (i + 1) % 3 == 0 and i != 8:
            print("-" * 25)
    print("=" * 25)
```
- Primero imprime una línea superior compuesta por signos `=`
- Después itera sobre las filas del tablero, usando `enumerate` para tener acceso al índice `i`.
- Después crea una fila vacía `fila_str` que se irá llenando con los valores de esa fila. Esta acción se hacer por cada número `num` de la fila, con su índice `j`.
    - Si el número es 0, se imprime como un punto `"."`, para representar una celda vacía.
    - Si no, se convierte el número a cadena y se añade con un espacio.
- Cada 3 columnas se añade un separador `"|"`, excepto al final de la fila (cuando `j = 0`)
- Después de procesar cada fila, se imprime la cadena construida.
- Cada 3 filas se imprime una línea horizontal separadora.
- Por último, se imprime una línea decorativa final.
## Verificación del tablero
Para verificar que el tablero introducido es válido, crearemos una función `validar_tablero`:
```python
def validar_tablero(tablero):
    for i in range(9):
        fila = [num for num in tablero[i] if num != 0]
        if len(fila) != len(set(fila)):
            print(f"Error: Número repetido en fila {i+1}.")
            return False
        columna = [tablero[j][i] for j in range(9) if tablero[j][i] != 0]
        if len(columna) != len(set(columna)):
            print(f"Error: Número repetido en columna {i+1}.")
            return False
    for bloque_fila in range(3):
        for bloque_col in range(3):
            bloque = []
            for r in range(3):
                for c in range(3):
                    num = tablero[bloque_fila*3 + r][bloque_col*3 + c]
                    if num != 0:
                        bloque.append(num)
            if len(bloque) != len(set(bloque)):
                print(f"Error: Número repetido en bloque ({bloque_fila+1},{bloque_col+1}).")
                return False
    return True
```
- La función recibirá la matriz `tablero`
  - Para comprobar las filas, ejecutará un bucle 9 veces, en el que creará una lista `fila` en la que se excluirán todos los números de la fila actual (`i`), excepto los ceros. Si la longitud de la lista `fila ` resultante es diferente a la longitud de la lista `set(fila)`, entonces significará que hay números repetidos, porque `set()` elimina los números duplicados.
  - Para comprobar las columnas, hará el mismo proceso que con las filas, con la diferencia que en la lista `fila` estarán los números que estén en la posición `j` de las diferentes filas, es decir:
    1. Iteración sobre las columnas (``i``):
        - Recorre cada columna. ``i`` va de 0 a 8 (hay 9 columnas en total).
        - Para cada columna, se revisan todos los valores de las 9 filas en esa columna.
    2. Construcción de la lista columna:
        - Aquí, para la columna ``i``, se recorre cada fila ``j`` (de 0 a 8) en esa columna. Se toma el valor de la celda ``tablero[j][i]``, pero solo si el valor no es 0 (para ignorar los huecos).
        - El resultado es una lista columna que contiene solo los números de esa columna, excluyendo los ceros (huecos).
  - Para comprobar los bloques, también se hará el mismo proceso que con las filas, pero para recolectar los números que pertenecen a cada bloque se hará un proceso diferente:
    1. Iteración sobre los bloques:
       - ``bloque_fila`` y ``bloque_col`` son las coordenadas de los subcuadros 3x3.
       - Hay 3 subcuadros en las filas (``bloque_fila``) y 3 en las columnas (``bloque_col``), lo que da un total de 9 subcuadros (3x3=9).
       - Por ejemplo, el subcuadro ``(0, 0)`` sería el primer subcuadro, que está en la esquina superior izquierda (fila 0-2, columna 0-2). El subcuadro ``(1, 2)`` está en la fila 0-2 y columna 6-8, etc.
    2. Recorrer cada celda del bloque:
       - Para cada bloque, recorremos sus 3 filas y 3 columnas. Esto nos da un total de 9 celdas por subcuadro.
       - La fórmula ``tablero[bloque_fila*3 + r][bloque_col*3 + c]`` nos da la celda exacta dentro del tablero.
         - ``bloque_fila*3 + r``: calcula la fila absoluta dentro del tablero.
         - ``bloque_col*3 + c``: calcula la columna absoluta dentro del tablero.
         - Si el valor en esa celda no es 0 (es decir, no es un hueco), se agrega a la lista bloque.

# Cálculos de candidatos
## Cálculo de candidatos

Para calcular los candidatos iniciales para cada celda, crearemos una función `calcular_candidatos`:

```python
def calcular_candidatos(tablero):
    """
    Calcula los candidatos iniciales para cada celda.
    """
    candidatos = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
    for fila in range(9):
        for col in range(9):
            num = tablero[fila][col]
            if num != 0:
                candidatos[fila][col] = {num}
                # Eliminar de fila
                for k in range(9):
                    if k != col:
                        candidatos[fila][k].discard(num)
                # Eliminar de columna
                for k in range(9):
                    if k != fila:
                        candidatos[k][col].discard(num)
                # Eliminar de bloque
                start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
                for r in range(start_row, start_row + 3):
                    for c in range(start_col, start_col + 3):
                        if (r, c) != (fila, col):
                            candidatos[r][c].discard(num)
    return candidatos
```
- Primero inicializaremos `candidatos` como una matriz 2D, donde cada elemento de esa matriz contiene los números del 1 al 9, para asegurar que todas las celdas del sudoku empiezan con todos los candidatos posibles.
- En el siguiente paso, recorremos todas las celdas del tablero, y dentro de esos bucles, obtenemos el número en la celda correspondiente.
- Después, si la celda tiene un número distinto de 0, haremos lo siguiente:
    - Primero, establecemos `num` como el número que está en esa celda.
    - Después, recorreremos todas las celdas de las filas, columnas y bloques a los que pertenece esa celda(Excepto la propia celda de la que hemos asignado `num`), y eliminaremos del elemento de la matriz `candidatos` el número `num` utilizando `.discard(num)`.
        - Para recorrer la fila, se hace un bucle `for` que se repite 9 veces, descartando `num` de cada celda.
        - Para recorrer la columna, se utiliza un método pareceido a cuando verificábamos el tablero, creando un bucle con `k` que se repite 9 veces, y eliminando `num` de cada celda con posición `[k, col]`.
        - Para recorrer el bloque, utilizaremos dos variables, `start_row` y `start_col`, que serán asignadas como `3 * (fila // 3)` y `3 * (col // 3)`, respectivamente. Estas dos variables sirven para calcular la cordenada superior izquierda del bloque 3x3 al que pertenece la celda actual. Tras ello, con un bucle, se recorrerán las filas y las columnas, pero de 3 en 3, en vez de hacerlo de 9 en 9, empezando desde las coordenadas que hemos calculado antes.
- Finalmente, devolveremos la lista `candidatos` con todos los posibles candidatos en cada celda. Las siguientes funciones utilizarán técnicas heurísticas para eliminar más números de esta matriz de candidatos.

## Impresión de candidatos

Para imprimir los candidatos, utilizaremos una función parecida a `imprimir_tablero`, ligeramente modificada para imprmir correctamente los distintos candidatos:

```python
def imprimir_candidatos(candidatos, paso_actual):
    """
    Imprime el tablero con los candidatos de cada celda.
    """
    print("\n" + "=" * 40)
    print(f"Paso: {paso_actual}")
    print("=" * 40)
    for fila in range(9):
        fila_str = ""
        for col in range(9):
            celd = candidatos[fila][col]
            contenido = ''.join(str(x) for x in sorted(celd))
            fila_str += f"{contenido:<9}"
            if (col + 1) % 3 == 0 and col != 8:
                fila_str += "| "
        print(fila_str)
        if (fila + 1) % 3 == 0 and fila != 8:
            print("-" * 40)
```
