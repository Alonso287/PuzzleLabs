# Práctica: Programación de un algoritmo de creación de sudokus
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

- Primero imprime una línea superior compuesta por signos ``=`` 
- Después imprime el paso actual, ya que este tablero de candidatos se imprimirá cada vez que se complete un paso con éxito.
- Tras eso se ejecuta un bucle `for` que se repite 9 veces, una por cada fila, y un segundo bucle va recorriendo las columnas de cada fila.
- Después, se asigna a `celd` la lista de candidatos que corresponda a esa celda, y se concatenan todos ellos para que se pueda imprimir correctamente, con `.join()`. Después, esa acadena se añade a `fila_str`, asegurándose de que cada celda ocupe un espacio de 9 caracteres con la alineación a la izquierda (`<9`).
- Después, se añade una barra vertical cada 3 celdas, excepto al final (`col != 8`), para visualizar la separación entre bloques.
- Después de eso se hace lo mismo para las divisiones horizontales.

# Técnicas heurísticas de resolución
Una vez que tenemos los candidatos iniciales, el programa intentará resolver el Sudoku utilizando una serie de técnicas lógicas o "heurísticas", que son las mismas que usaría una persona. Estas técnicas eliminan candidatos de las celdas vacías hasta que, idealmente, cada celda tiene un solo candidato, resolviendo así el puzzle.

El programa aplicará estas técnicas en un bucle, ya que la aplicación de una técnica puede abrir la puerta a que otra sea aplicable. Además, como queremos utilizar siempre el método más "sencillo", el bucle se reiniciará si vemos que se han realizado cambios en los candidatos.

Puedes ver una explicación más detallada sobre las técnicas heurísticas en la página anterior

## Aplicación de candidatos únicos
Esta es la técnica más básica y se conoce como "Naked Single". Si una celda vacía solo tiene un candidato posible, ese número debe ser la solución para esa celda.
```python
def aplicar_candidato_unico(tablero, candidatos):
    cambio_realizado = False
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0 and len(candidatos[fila][col]) == 1:
                valor = candidatos[fila][col].pop()
                tablero[fila][col] = valor
                candidatos[fila][col] = {valor}
                # Eliminar de fila
                for k in range(9):
                    if k != col:
                        candidatos[fila][k].discard(valor)
                # Eliminar de columna
                for k in range(9):
                    if k != fila:
                        candidatos[k][col].discard(valor)
                # Eliminar de bloque
                start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
                for r in range(start_row, start_row + 3):
                    for c in range(start_col, start_col + 3):
                        if (r, c) != (fila, col):
                            candidatos[r][c].discard(valor)
                cambio_realizado = True
                imprimir_tablero(tablero)
                imprimir_candidatos(candidatos, f"Candidato único asignado en fila {fila+1}, columna {col+1}")
    return cambio_realizado
```
- La función recorre cada celda del tablero.
- Comprueba dos condiciones para cada celda: que esté vacía (`tablero[fila][col] == 0`) y que solo tenga un candidato (`len(candidatos[fila][col]) == 1`).
- Si ambas condiciones son ciertas:
    - Se extrae el único candidato con `.pop()` y se asigna a la celda en el `tablero`.
    - Se actualiza la lista de candidatos de esa celda para que solo contenga el valor asignado.
    - Se elimina ese valor de los candidatos de todas las demás celdas en la misma fila, columna y bloque 3x3. Esta es la parte más importante, ya que resolver una celda nos da más información para resolver las demás.
    - Se establece `cambio_realizado` en `True` para indicar que el tablero ha progresado.
    - Se imprime el estado actual del tablero y los candidatos para que el usuario vea el progreso.
- Finalmente, devuelve `True` si se ha realizado algún cambio, o `False` si no. Esta variable la utilizaremos más tarde para saber si debemos aplicar la siguiente técnica o volver a aplicar todas las técnicas desde el principio

## Eliminar candidatos

Para algunas de las técnicas siguientes, usaremos una función auxiliar `eliminar_candidato` para no repetir código:

```python
def eliminar_candidato(tablero, candidatos, fila, col, valor):
    # Eliminar de fila
    for k in range(9):
        if k != col:
            candidatos[fila][k].discard(valor)
    # Eliminar de columna
    for k in range(9):
        if k != fila:
            candidatos[k][col].discard(valor)
    # Eliminar de bloque
    start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r, c) != (fila, col):
                candidatos[r][c].discard(valor)
```
- Esta función simplemente toma un valor y sus coordenadas, y lo elimina como candidato de las celdas afectadas en la misma fila, columna y bloque.

## Aplicación de singles ocultos
Esta técnica, conocida como "Hidden Single", es ligeramente más avanzada. Busca un candidato que, dentro de una unidad (fila, columna o bloque), solo aparece en una celda. Aunque esa celda pueda tener otros candidatos, si es el único lugar posible para ese número en toda la unidad, debe ser el valor de la celda:

```python
def aplicar_singles_ocultos(tablero, candidatos):
    cambio_realizado = False
    # Filas
    for fila in range(9):
        cambio_realizado |= buscar_singles_ocultos_en_unidad(
            tablero,
            candidatos,
            [ (fila, col) for col in range(9) ],
            f"Fila {fila+1}"
        )
    # Columnas
    for col in range(9):
        cambio_realizado |= buscar_singles_ocultos_en_unidad(
            tablero,
            candidatos,
            [ (fila, col) for fila in range(9) ],
            f"Columna {col+1}"
        )
    # Bloques
    for bloque_fila in range(3):
        for bloque_col in range(3):
            celdas = []
            for r in range(3):
                for c in range(3):
                    fila = bloque_fila * 3 + r
                    col = bloque_col * 3 + c
                    celdas.append((fila, col))
            cambio_realizado |= buscar_singles_ocultos_en_unidad(
                tablero,
                candidatos,
                celdas,
                f"Bloque ({bloque_fila+1},{bloque_col+1})"
            )
    return cambio_realizado

def buscar_singles_ocultos_en_unidad(tablero, candidatos, celdas, nombre_unidad):
    from collections import defaultdict
    cambio = False

    candidato_a_indices = defaultdict(list)
    for idx, (fila, col) in enumerate(celdas):
        if tablero[fila][col] == 0:
            for candidato in candidatos[fila][col]:
                candidato_a_indices[candidato].append((fila, col))

    for candidato, posiciones in candidato_a_indices.items():
        if len(posiciones) == 1:
            fila, col = posiciones[0]
            tablero[fila][col] = candidato
            candidatos[fila][col] = {candidato}
            eliminar_candidato(tablero, candidatos, fila, col, candidato)
            # ... (impresiones para el usuario) ...
            cambio = True
    return cambio
```
- La función `aplicar_singles_ocultos` actúa como un despachador: invoca a `buscar_singles_ocultos_en_unidad` para cada una de las 9 filas, 9 columnas y 9 bloques.
- La función `buscar_singles_ocultos_en_unidad` es el donde verdaderamente se aplica la lógica:
    - Recibe una lista con las coordenadas de las celdas de una unidad (ej. `[(0,0), (0,1), ..., (0,8)]` para la primera fila).
    - Crea un diccionario `candidato_a_indices` que mapea cada número candidato a una lista de las celdas donde aparece.
    - Una vez construido el mapa, lo recorre. Si un candidato solo aparece en una posición (`len(posiciones) == 1`), ¡hemos encontrado un single oculto!
    - Se asigna ese `candidato` a la celda correspondiente del `tablero`.
    - Se actualiza la lista de candidatos de esa celda y se llama a `eliminar_candidato` para propagar la nueva información.

## Aplicación de pares desnudos
La técnica de pares desnudos o _"Naked Pairs"_ busca dos celdas en la misma unidad (fila, columna o bloque) que contienen exactamente el mismo par de candidatos (y solo esos dos). Si se encuentra este par, sabemos que esos dos números deben ir en esas dos celdas, por lo que podemos eliminarlos como candidatos del resto de celdas de esa unidad.

```python
def buscar_pares_en_unidad(celdas, nombre_unidad):
    cambio = False
    pares = {}
    for i, celda in enumerate(celdas):
        if len(celda) == 2:
            clave = frozenset(celda)
            pares.setdefault(clave, []).append(i)
    for par, indices in pares.items():
        if len(indices) == 2:
            # Encontrado un par desnudo
            for i, celda in enumerate(celdas):
                if i not in indices:
                    antes = set(celda)
                    celda.difference_update(par)
                    if antes != celda:
                        cambio = True
    if cambio:
        print(f"Par desnudo encontrado en {nombre_unidad}: {sorted(par)}")
    return cambio

def buscar_pares_en_unidad(celdas, nombre_unidad):
    cambio = False
    pares = {}
    for i, celda in enumerate(celdas):
        if len(celda) == 2:
            clave = frozenset(celda)
            pares.setdefault(clave, []).append(i)

    for par, indices in pares.items():
        if len(indices) == 2:
            # Encontrado un par desnudo
            for i, celda in enumerate(celdas):
                if i not in indices:
                    antes = set(celda)
                    celda.difference_update(par)
                    if antes != celda:
                        cambio = True
            if cambio:
                print(f"Par desnudo encontrado en {nombre_unidad}: {sorted(par)}")
    return cambio
```
- De nuevo, `aplicar_pares_desnudos` es un despachador que recorre filas, columnas y bloques.
- `buscar_pares_en_unidad` implementa la lógica:
    - Primero, busca todas las celdas que tengan exactamente 2 candidatos.
    - Utiliza un diccionario para agrupar las celdas por su par de candidatos. Usamos `frozenset` porque los sets no pueden ser claves de diccionario, pero los `frozenset` sí.
    - Después, recorre el diccionario. Si un par de candidatos aparece exactamente en dos celdas (`len(indices) == 2`), hemos encontrado un par desnudo.
    - Por último, recorre todas las celdas de la unidad. A las celdas que *no* forman parte del par, les elimina los dos números del par de sus candidatos usando `difference_update`.

## Aplicación de conjuntos desnudos (Tríos y Cuartetos)
Esta es una generalización de los Pares Desnudos. La lógica es: si encontramos un grupo de **N** celdas en la misma unidad que, entre todas, contienen un conjunto de exactamente **N** candidatos, podemos eliminar esos **N** candidatos de todas las demás celdas de esa unidad. El programa lo implementa para tríos (N=3) y cuartetos (N=4):

```python
def aplicar_conjuntos_desnudos(tablero, candidatos, tamaño):
    cambio_realizado = False
    # Filas
    for fila in range(9):
        cambio_realizado |= buscar_conjuntos_desnudos_en_unidad(
            [candidatos[fila][col] for col in range(9)],
            tamaño,
            f"Fila {fila+1}"
        )
    # Columnas
    for col in range(9):
        cambio_realizado |= buscar_conjuntos_desnudos_en_unidad(
            [candidatos[fila][col] for fila in range(9)],
            tamaño,
            f"Columna {col+1}"
        )
    # Bloques
    for bloque_fila in range(3):
        for bloque_col in range(3):
            celdas = []
            for r in range(3):
                for c in range(3):
                    fila = bloque_fila * 3 + r
                    col = bloque_col * 3 + c
                    celdas.append(candidatos[fila][col])
            cambio_realizado |= buscar_conjuntos_desnudos_en_unidad(
                celdas,
                tamaño,
                f"Bloque ({bloque_fila+1},{bloque_col+1})"
            )
    return cambio_realizado

def buscar_conjuntos_desnudos_en_unidad(celdas, tamaño, nombre_unidad):
    from itertools import combinations
    cambio = False
    indices = [i for i, celda in enumerate(celdas) if 2 <= len(celda) <= tamaño]
    for combo in combinations(indices, tamaño):
        conjunto = set()
        for idx in combo:
            conjunto |= celdas[idx]
        if len(conjunto) == tamaño:
            # Se ha encontrado un conjunto desnudo
            for i, celda in enumerate(celdas):
                if i not in combo:
                    antes = set(celda)
                    celda.difference_update(conjunto)
                    if antes != celda:
                        cambio = True
            if cambio:
                print(f"{tamaño}-desnudo encontrado en {nombre_unidad}: {sorted(conjunto)}")
    return cambio
```
- La lógica es similar a la de los pares, pero más potente.
- `buscar_conjuntos_desnudos_en_unidad` utiliza `itertools.combinations` para generar todas las posibles combinaciones de `tamaño` celdas (ej., todas las combinaciones de 3 celdas para buscar tríos).
- Para cada combinación, une todos sus candidatos en un único `conjunto`.
- La condición clave es `if len(conjunto) == tamaño`. Si se cumple, significa que la longitud de la lista `conjunto` es la misma que la que hemos pedido (3 o 4), por lo tanto, cumple la definición de conjunto desnudo.
- Al igual que con los pares, se eliminan los candidatos del `conjunto` del resto de celdas de la unidad.

## Aplicación de pares ocultos
La técnica de "Hidden Pairs" es la parte opuesta de los Pares Desnudos. Si dos candidatos aparecen únicamente en las mismas dos celdas dentro de una unidad (aunque esas celdas puedan tener otros candidatos), entonces sabemos que esas dos celdas deben contener esos dos números. Por lo tanto, podemos eliminar todos los *otros* candidatos de esas dos celdas.

```python
def aplicar_pares_ocultos(tablero, candidatos):
    cambio_realizado = False
    # Filas
    for fila in range(9):
        cambio_realizado |= buscar_pares_ocultos_en_unidad(
            [candidatos[fila][col] for col in range(9)],
            f"Fila {fila+1}"
        )
    # Columnas
    for col in range(9):
        cambio_realizado |= buscar_pares_ocultos_en_unidad(
            [candidatos[fila][col] for fila in range(9)],
            f"Columna {col+1}"
        )
    # Bloques
    for bloque_fila in range(3):
        for bloque_col in range(3):
            celdas = []
            for r in range(3):
                for c in range(3):
                    fila = bloque_fila * 3 + r
                    col = bloque_col * 3 + c
                    celdas.append(candidatos[fila][col])
            cambio_realizado |= buscar_pares_ocultos_en_unidad(
                celdas,
                f"Bloque ({bloque_fila+1},{bloque_col+1})"
            )
    return cambio_realizado

def buscar_pares_ocultos_en_unidad(celdas, nombre_unidad):
    from collections import defaultdict
    cambio = False
    candidato_a_indices = defaultdict(set)
    for idx, celda in enumerate(celdas):
        for candidato in celda:
            candidato_a_indices[candidato].add(idx)
    
    candidatos_lista = list(candidato_a_indices.keys())
    for i in range(len(candidatos_lista)):
        for j in range(i+1, len(candidatos_lista)):
            indices_i = candidato_a_indices[candidatos_lista[i]]
            indices_j = candidato_a_indices[candidatos_lista[j]]
            if indices_i == indices_j and len(indices_i) == 2:
                # Pares ocultos encontrados
                for idx in indices_i:
                    celda = celdas[idx]
                    antes = set(celda)
                    celda.intersection_update({candidatos_lista[i], candidatos_lista[j]})
                    if celda != antes:
                        cambio = True
                if cambio:
                    print(f"Par oculto encontrado en {nombre_unidad}: {sorted([candidatos_lista[i], candidatos_lista[j]])}")
    return cambio
```
- `buscar_pares_ocultos_en_unidad` es la función clave.
    - Primero, crea un mapa `candidato_a_indices` para saber en qué celdas aparece cada candidato.
    - Luego, itera sobre todas las combinaciones posibles de dos candidatos.
    - Comprueba si ambos candidatos aparecen exactamente en el mismo conjunto de dos celdas (`indices_i == indices_j and len(indices_i) == 2`).
    - Si se encuentra un par oculto, itera sobre las dos celdas identificadas. Para cada una, elimina todos los candidatos que no sean los dos que forman el par. Esto se hace eficientemente con `intersection_update`.

# Resolución por Fuerza Bruta: Backtracking
Si las técnicas heurísticas no logran resolver el Sudoku por completo, el programa recurre a un algoritmo de fuerza bruta con retroceso (backtracking). Este método prueba sistemáticamente todos los números posibles en las celdas vacías hasta encontrar una solución o demostrar que no existe.

## El núcleo recursivo del Backtracking
El corazón del algoritmo es una función recursiva que intenta rellenar el tablero:

```python
def _resolver_sudoku_backtracking_recursivo(tablero, stats):
    stats['iteraciones'] += 1
    stats['profundidad_actual'] += 1
    stats['max_profundidad'] = max(stats['max_profundidad'], stats['profundidad_actual'])

    celda_vacia = encontrar_celda_vacia(tablero)

    if not celda_vacia:
        stats['profundidad_actual'] -= 1
        return True

    fila, col = celda_vacia

    for num_intento in range(1, 10):
        if es_valido_colocar(tablero, fila, col, num_intento):
            tablero[fila][col] = num_intento

            if _resolver_sudoku_backtracking_recursivo(tablero, stats):
                stats['profundidad_actual'] -= 1
                return True
            stats['retrocesos'] += 1
            tablero[fila][col] = 0
    
    stats['profundidad_actual'] -= 1
    return False
```
- **Caso Base:** La función primero busca una celda vacía. Si no encuentra ninguna (`if not celda_vacia`), significa que el tablero está completo y, por lo tanto, resuelto. Devuelve `True`.
- **Paso Recursivo:**
    1.  Toma la primera celda vacía que encuentra.
    2.  Inicia un bucle para probar cada número del 1 al 9.
    3.  Para cada número, comprueba si es válido colocarlo en esa celda (usando la función `es_valido_colocar`).
    4.  Si es válido, coloca el número en el tablero y **se llama a sí misma (recursión)** para continuar resolviendo el resto del tablero.
    5.  Si la llamada recursiva devuelve `True`, significa que se encontró una solución, por lo que propaga el `True` hacia arriba.
    6.  **Backtracking:** Si la llamada recursiva devuelve `False`, significa que la elección de ese número llevó a un callejón sin salida. En este punto, se "deshace" la elección poniendo la celda a `0` de nuevo y el bucle continúa para probar el siguiente número.
- **Fallo:** Si el bucle termina sin que ningún número del 1 al 9 haya llevado a una solución, la función devuelve `False`, indicando a la llamada anterior que debe retroceder.

## Funciones auxiliares para Backtracking
El algoritmo de backtracking se apoya en dos funciones sencillas:

```python
def encontrar_celda_vacia(tablero):
    for r in range(9):
        for c in range(9):
            if tablero[r][c] == 0:
                return (r, c)
    return None

def es_valido_colocar(tablero, fila, col, num):
    # Verificar fila
    for c_idx in range(9):
        if c_idx != col and tablero[fila][c_idx] == num:
            return False
    # Verificar columna
    for r_idx in range(9):
        if r_idx != fila and tablero[r_idx][col] == num:
            return False
    # Verificar bloque 3x3
    start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r != fila or c != col) and tablero[r][c] == num:
                return False
    return True
```
- `encontrar_celda_vacia()`: Simplemente recorre el tablero de arriba abajo y de izquierda a derecha, y devuelve las coordenadas de la primera celda con un `0` que encuentra. Si no hay ninguna, devuelve `None`.
- `es_valido_colocar()`: Comprueba si colocar un `num` en una `(fila, col)` determinada viola las reglas del Sudoku (es decir, si ese número ya existe en la misma fila, columna o bloque 3x3).

## Wrapper para llamar la función
Para dar algún información al usuario en este proceso que no se realiza de una manera lógica o sistemática, crearemos una función que servirá como wrapper para llamar a la función principal de resolución y hacer un seguimiento de algunas estadísticas.
```python
def resolver_sudoku_fuerza_bruta(tablero_previo_bt):
    tablero_copia = [fila[:] for fila in tablero_previo_bt]

    stats = {
        'iteraciones': 0,         # Total de llamadas recursivas
        'profundidad_actual': 0,  # Nivel de recursión actual
        'retrocesos': 0,          # Total de retrocesos
        'max_profundidad': 0      # Máxima profundidad alcanzada
    }

    start_time = time.time()
    
    tiene_solucion = _resolver_sudoku_backtracking_recursivo(tablero_copia, stats)
    
    end_time = time.time()
    tiempo_tardado = end_time - start_time

    if tiene_solucion:
        return tablero_copia, stats['iteraciones'], stats['max_profundidad'], tiempo_tardado, stats['retrocesos']
    else:
        # Si no hay solución, tablero_previo_bt no fue modificado.
        # Devolvemos None para el tablero, y las estadísticas del intento fallido.
        return None, stats['iteraciones'], stats['max_profundidad'], tiempo_tardado, stats['retrocesos']
```
- Como no sabemos si el Sudoku tiene solución, crearemos una copia exacta del tablero al que hemos llegado antes con las técnicas heurísticas, y trabajaremos sobre esta copia para que, si el tablero no tiene solución, se muestre al usuario el tablero resultante tras la resolución por técnicas heurísticas.
- También inicializaremos diferentes variables que sirvan como estadísticas que el usuario sepa cómo ha ido la resolución.
- Se establece una variable en la que se guarda el tablero de inicio.
- Se llama a la función de resolución.
- Cuando termina, se resta el tiempo de inicio con el del final para averiguar el tiempo que se ha tardado.
- Si el sudoku tiene solución, la devuelve, y si no, devuelve `None`, en ambos casos junto con las estadísticas.
# Flujo principal del programa
Finalmente, la función `main()` y el bloque de inicio del script (`if __name__ == "__main__":`) orquestan todo el proceso.

## La función `main()`
Esta función controla el flujo de resolución completo.

```python
def main():
    resuelto_e_impreso_por_heuristicas = False

    tablero_leido = leer_tablero()

    tablero_actual = [fila[:] for fila in tablero_leido]

    tablero_original_para_bt_stats = [fila[:] for fila in tablero_leido] # Copia para comparar celdas llenadas

    candidatos = calcular_candidatos(tablero_actual) # Calcular sobre la copia
    imprimir_candidatos(candidatos, "Inicializar candidatos")
    
    paso_iteracion_heuristica = 1
    max_iteraciones_heuristicas = 20 # Límite para heurísticas
    resuelto_e_impreso_por_heuristicas = False

    while paso_iteracion_heuristica <= max_iteraciones_heuristicas:
        cambio_en_iteracion = False
        print(f"\nIteración heurística {paso_iteracion_heuristica}")
        
        # Guardar estado del tablero antes de las heurísticas de esta iteración para estadísticas de BT
        if paso_iteracion_heuristica == 1: # Guardar el estado inicial antes de cualquier heurística para el cálculo de celdas llenadas por BT
            tablero_antes_de_bt_definitivo = [fila[:] for fila in tablero_actual]

        # Aplicar técnicas más directas primero
        if aplicar_candidato_unico(tablero_actual, candidatos): cambio_en_iteracion = True
        if aplicar_singles_ocultos(tablero_actual, candidatos): cambio_en_iteracion = True
        
        # Si las directas no hicieron cambio, probar las más complejas de eliminación
        if not cambio_en_iteracion: 
            if aplicar_pares_desnudos(tablero_actual, candidatos): cambio_en_iteracion = True
            if aplicar_conjuntos_desnudos(tablero_actual, candidatos, 3): cambio_en_iteracion = True 
            if aplicar_conjuntos_desnudos(tablero_actual, candidatos, 4): cambio_en_iteracion = True 
            if aplicar_pares_ocultos(tablero_actual, candidatos): cambio_en_iteracion = True
        
        # Comprobar si el tablero está resuelto después de esta iteración de heurísticas
        resuelto_por_heuristica_en_iteracion = all(tablero_actual[r][c] != 0 for r in range(9) for c in range(9))
        if resuelto_por_heuristica_en_iteracion:
            print("\n¡Sudoku Resuelto con técnicas heurísticas!")
            imprimir_tablero(tablero_actual)
            resuelto_e_impreso_por_heuristicas = True
            return # Fin del programa si se resuelve

        if not cambio_en_iteracion:
            print("\nNo se encontraron más cambios con técnicas heurísticas en esta iteración.")
            break # Salir del bucle de heurísticas si no hay más progreso
        
        paso_iteracion_heuristica += 1
        if paso_iteracion_heuristica > max_iteraciones_heuristicas:
            print("\nLímite de iteraciones heurísticas alcanzado.")
            break

    # Si no se actualizó tablero_antes_de_bt_definitivo porque el bucle terminó por max_iteraciones o resolución
    if 'tablero_antes_de_bt_definitivo' not in locals():
         tablero_antes_de_bt_definitivo = [fila[:] for fila in tablero_actual]
    
    # Después del bucle de heurísticas, verificar si está resuelto
    resuelto_final_heuristicas = all(tablero_actual[r][c] != 0 for r in range(9) for c in range(9))

    if not resuelto_final_heuristicas:
        print("\nEl Sudoku no pudo ser resuelto completamente con técnicas heurísticas.")
        print("Estado del tablero antes de intentar backtracking (fuerza bruta):")
        imprimir_tablero(tablero_antes_de_bt_definitivo) # Mostrar el tablero que ENTRARÁ al BT
        # Opcionalmente, mostrar candidatos si son relevantes para el usuario en este punto
        
        print("\nIniciando backtracking (fuerza bruta)...")
        
        # Llamar a la función de backtracking. Esta recibe el estado actual del tablero
        # (modificado por heurísticas) y trabaja sobre una copia.
        tablero_solucion_bt, iter_bt, prof_bt, tiempo_bt, retrocesos_bt = resolver_sudoku_fuerza_bruta(tablero_actual)

        print(f"Proceso de Backtracking finalizado en {tiempo_bt:.4f} segundos.")
        print(f"  Iteraciones (llamadas recursivas): {iter_bt}")
        print(f"  Profundidad máxima alcanzada: {prof_bt}")
        print(f"  Total de retrocesos: {retrocesos_bt}")

        if tablero_solucion_bt:
            print("¡Sudoku Resuelto con backtracking!")

            celdas_llenadas_por_bt = 0
            for r in range(9):
                for c in range(9):
                    if tablero_antes_de_bt_definitivo[r][c] == 0 and tablero_solucion_bt[r][c] != 0:
                        celdas_llenadas_por_bt +=1
            print(f"  Celdas llenadas por backtracking: {celdas_llenadas_por_bt}")

            imprimir_tablero(tablero_solucion_bt)
        else:
            print("El Sudoku no tiene solución (verificado por backtracking).")
            print("El tablero mostrado a continuación es el estado en el que quedó después de las técnicas heurísticas (antes del intento de backtracking):")
            imprimir_tablero(tablero_antes_de_bt_definitivo) # tablero_actual no fue modificado por el BT fallido

    elif resuelto_final_heuristicas and not resuelto_e_impreso_por_heuristicas:
        print("\n¡Sudoku Resuelto con técnicas heurísticas (verificado después del bucle)!")
        imprimir_tablero(tablero_actual)
```
- **Inicialización:** Pide al usuario el tablero, crea una copia de trabajo y calcula los candidatos iniciales.
- **Bucle de Heurísticas:**
    - Entra en un bucle con un número máximo de iteraciones para evitar bucles infinitos.
    - En cada iteración, aplica secuencialmente las técnicas heurísticas.
    - Utiliza una bandera `cambio_en_iteracion` para detectar si alguna técnica tuvo éxito. Si en una pasada completa ninguna técnica puede hacer un cambio, el bucle se rompe, ya que no se puede progresar más por esta vía.
- **Fase de Backtracking:**
    - Después del bucle, comprueba si el tablero está resuelto.
    - Si no lo está, informa al usuario y llama a `resolver_sudoku_fuerza_bruta` para que termine el trabajo.
    - Finalmente, imprime la solución (si se encontró) junto con estadísticas interesantes como el tiempo tardado, el número de iteraciones y las celdas que rellenó el backtracking.
- **Éxito por Heurísticas:** Si el tablero se resolvió solo con heurísticas, se informa al usuario y se muestra el tablero resuelto.

## Punto de entrada del programa
Este es el código que se ejecuta cuando se inicia el script. Presenta un menú simple al usuario.

```python
if __name__ == "__main__":
    while True:
        opcion = ""
        print("\nMenu:")
        print("1. Resolver un sudoku")
        print("2. Salir")
        while opcion not in ["1", "2"]:
            opcion = input("Elige una opción: ").strip()
            if opcion not in ["1", "2"]:
                print("Opción inválida. Por favor ingresa 1 o 2.")
        
        if opcion == "1":
            main() 
        elif opcion == "2":
            print("Gracias por usar el programa. ¡Hasta luego!")
            exit()
```
- Este bloque crea un bucle infinito que muestra un menú.
- El usuario puede elegir resolver un Sudoku (lo que llama a la función `main`) o salir del programa.
- Esto proporciona una interfaz de usuario sencilla y reutilizable para el programa.

# ¡Pruébalo tú mismo!

Aquí tienes el código completo del resolutor de Sudokus, que puedes ejecutar haciendo click en el triángulo de arriba a la derecha. También puedes descargar el archivo del script entero en nuestro repositorio de GitHub.

```python:line-numbers
def leer_tablero():
    """
    Lee un tablero de Sudoku de 9 filas desde consola y lo devuelve como una lista de listas.
    Usa 0 para representar los huecos vacíos.
    """
    opcion = input("¿Cómo deseas introducir el tablero de Sudoku?\n1. Por filas\n2. Como una cadena única\nOpción: ").strip()

    while opcion not in ['1', '2']:
        print("Opción inválida. Por favor ingresa 1 o 2.")
        opcion = input("¿Cómo deseas introducir el tablero de Sudoku?\n1. Por filas\n2. Como una cadena única\nOpción: ").strip()

    if opcion == '1':
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
    
    elif opcion == '2':
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

def validar_fila(fila):
    """
    Valida que no haya números repetidos en la fila.
    """
    numeros = [num for num in fila if num != 0]
    return len(numeros) == len(set(numeros))

def validar_tablero(tablero):
    """
    Valida que no haya números repetidos en filas, columnas y bloques.
    """
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

def aplicar_candidato_unico(tablero, candidatos):
    """
    Aplica la técnica de candidato único:
    - Si una celda tiene un solo candidato, asigna ese valor.
    - Luego elimina ese valor de la fila, la columna y el bloque.
    """
    cambio_realizado = False
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0 and len(candidatos[fila][col]) == 1:
                valor = candidatos[fila][col].pop()
                tablero[fila][col] = valor
                candidatos[fila][col] = {valor}
                # Eliminar de fila
                for k in range(9):
                    if k != col:
                        candidatos[fila][k].discard(valor)
                # Eliminar de columna
                for k in range(9):
                    if k != fila:
                        candidatos[k][col].discard(valor)
                # Eliminar de bloque
                start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
                for r in range(start_row, start_row + 3):
                    for c in range(start_col, start_col + 3):
                        if (r, c) != (fila, col):
                            candidatos[r][c].discard(valor)
                cambio_realizado = True
                imprimir_tablero(tablero)
                imprimir_candidatos(candidatos, f"Candidato único asignado en fila {fila+1}, columna {col+1}")
    return cambio_realizado

def aplicar_pares_desnudos(tablero, candidatos):
    """
    Aplica la técnica de pares desnudos:
    - Busca pares desnudos en filas, columnas y bloques.
    - Elimina esos candidatos del resto de las celdas de la misma unidad.
    """
    cambio_realizado = False
    # Aplicar en filas
    for fila in range(9):
        cambio_realizado |= buscar_pares_en_unidad([candidatos[fila][col] for col in range(9)], f"Fila {fila+1}")

    # Aplicar en columnas
    for col in range(9):
        cambio_realizado |= buscar_pares_en_unidad([candidatos[fila][col] for fila in range(9)], f"Columna {col+1}")

    # Aplicar en bloques
    for bloque_fila in range(3):
        for bloque_col in range(3):
            celdas = []
            for r in range(3):
                for c in range(3):
                    fila = bloque_fila * 3 + r
                    col = bloque_col * 3 + c
                    celdas.append(candidatos[fila][col])
            cambio_realizado |= buscar_pares_en_unidad(celdas, f"Bloque ({bloque_fila+1},{bloque_col+1})")

    return cambio_realizado

def buscar_pares_en_unidad(celdas, nombre_unidad):
    """
    Busca pares desnudos en una unidad (fila, columna o bloque).
    """
    cambio = False
    pares = {}
    for i, celda in enumerate(celdas):
        if len(celda) == 2:
            clave = frozenset(celda)
            pares.setdefault(clave, []).append(i)
    for par, indices in pares.items():
        if len(indices) == 2:
            # Encontrado un par desnudo
            for i, celda in enumerate(celdas):
                if i not in indices:
                    antes = set(celda)
                    celda.difference_update(par)
                    if antes != celda:
                        cambio = True
    if cambio:
        print(f"Par desnudo encontrado en {nombre_unidad}: {sorted(par)}")
    return cambio

def eliminar_candidato(tablero, candidatos, fila, col, valor):
    # Eliminar de fila
    for k in range(9):
        if k != col:
            candidatos[fila][k].discard(valor)
    # Eliminar de columna
    for k in range(9):
        if k != fila:
            candidatos[k][col].discard(valor)
    # Eliminar de bloque
    start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r, c) != (fila, col):
                candidatos[r][c].discard(valor)

def aplicar_conjuntos_desnudos(tablero, candidatos, tamaño):
    """
    Aplica la técnica de conjuntos desnudos (tríos o cuartetos) en filas, columnas y bloques.
    - tamaño: 3 (tríos) o 4 (cuartetos).
    """
    cambio_realizado = False

    # Filas
    for fila in range(9):
        cambio_realizado |= buscar_conjuntos_desnudos_en_unidad(
            [candidatos[fila][col] for col in range(9)],
            tamaño,
            f"Fila {fila+1}"
        )

    # Columnas
    for col in range(9):
        cambio_realizado |= buscar_conjuntos_desnudos_en_unidad(
            [candidatos[fila][col] for fila in range(9)],
            tamaño,
            f"Columna {col+1}"
        )

    # Bloques
    for bloque_fila in range(3):
        for bloque_col in range(3):
            celdas = []
            for r in range(3):
                for c in range(3):
                    fila = bloque_fila * 3 + r
                    col = bloque_col * 3 + c
                    celdas.append(candidatos[fila][col])
            cambio_realizado |= buscar_conjuntos_desnudos_en_unidad(
                celdas,
                tamaño,
                f"Bloque ({bloque_fila+1},{bloque_col+1})"
            )

    return cambio_realizado

def buscar_conjuntos_desnudos_en_unidad(celdas, tamaño, nombre_unidad):
    """
    Busca conjuntos desnudos de tamaño `tamaño` en una unidad (fila, columna o bloque).
    - tamaño: 3 (tríos) o 4 (cuartetos).
    """
    cambio = False
    from itertools import combinations

    # Recorremos todas las combinaciones de celdas
    indices = [i for i, celda in enumerate(celdas) if 2 <= len(celda) <= tamaño]
    for combo in combinations(indices, tamaño):
        conjunto = set()
        for idx in combo:
            conjunto |= celdas[idx]
        if len(conjunto) == tamaño:
            # Se ha encontrado un conjunto desnudo
            for i, celda in enumerate(celdas):
                if i not in combo:
                    antes = set(celda)
                    celda.difference_update(conjunto)
                    if antes != celda:
                        cambio = True
            if cambio:
                print(f"{tamaño}-desnudo encontrado en {nombre_unidad}: {sorted(conjunto)}")
    return cambio

def aplicar_singles_ocultos(tablero, candidatos):
    """
    Aplica la técnica de singles ocultos:
    - Si un candidato aparece solo una vez en una fila, columna o bloque, se asigna ese valor.
    - Luego elimina ese valor de las demás celdas de la misma unidad.
    """
    cambio_realizado = False

    # Filas
    for fila in range(9):
        cambio_realizado |= buscar_singles_ocultos_en_unidad(
            tablero,
            candidatos,
            [ (fila, col) for col in range(9) ],
            f"Fila {fila+1}"
        )

    # Columnas
    for col in range(9):
        cambio_realizado |= buscar_singles_ocultos_en_unidad(
            tablero,
            candidatos,
            [ (fila, col) for fila in range(9) ],
            f"Columna {col+1}"
        )

    # Bloques
    for bloque_fila in range(3):
        for bloque_col in range(3):
            celdas = []
            for r in range(3):
                for c in range(3):
                    fila = bloque_fila * 3 + r
                    col = bloque_col * 3 + c
                    celdas.append((fila, col))
            cambio_realizado |= buscar_singles_ocultos_en_unidad(
                tablero,
                candidatos,
                celdas,
                f"Bloque ({bloque_fila+1},{bloque_col+1})"
            )

    return cambio_realizado

def buscar_singles_ocultos_en_unidad(tablero, candidatos, celdas, nombre_unidad):
    """
    Busca singles ocultos en una unidad (fila, columna o bloque):
    - Si un candidato aparece solo una vez en la unidad, se asigna a esa celda.
    """
    from collections import defaultdict
    cambio = False

    # Mapeamos cada candidato a las celdas donde aparece
    candidato_a_indices = defaultdict(list)
    for idx, (fila, col) in enumerate(celdas):
        if tablero[fila][col] == 0:
            for candidato in candidatos[fila][col]:
                candidato_a_indices[candidato].append((fila, col))

    # Buscamos candidatos que aparecen solo una vez
    for candidato, posiciones in candidato_a_indices.items():
        if len(posiciones) == 1:
            fila, col = posiciones[0]
            tablero[fila][col] = candidato
            candidatos[fila][col] = {candidato}
            eliminar_candidato(tablero, candidatos, fila, col, candidato)
            print(f"Single oculto encontrado en {nombre_unidad}: {candidato} en fila {fila+1}, columna {col+1}")
            imprimir_tablero(tablero)
            imprimir_candidatos(candidatos, f"Single oculto asignado en fila {fila+1}, columna {col+1}")
            cambio = True

    return cambio

def buscar_pares_ocultos_en_unidad(celdas, nombre_unidad):
    """
    Busca pares ocultos en una unidad (fila, columna o bloque).
    """
    cambio = False
    from collections import defaultdict
    # Mapeamos candidato -> conjunto de índices donde aparece
    candidato_a_indices = defaultdict(set)
    for idx, celda in enumerate(celdas):
        for candidato in celda:
            candidato_a_indices[candidato].add(idx)
    # Buscamos pares de candidatos que aparezcan exactamente en las mismas dos celdas
    candidatos = list(candidato_a_indices.keys())
    for i in range(len(candidatos)):
        for j in range(i+1, len(candidatos)):
            indices_i = candidato_a_indices[candidatos[i]]
            indices_j = candidato_a_indices[candidatos[j]]
            # Verificar si ambos aparecen en las mismas dos celdas
            if indices_i == indices_j and len(indices_i) == 2:
                # Pares ocultos encontrados
                for idx in indices_i:
                    celda = celdas[idx]
                    antes = set(celda)
                    celda.intersection_update({candidatos[i], candidatos[j]})
                    if celda != antes:
                        cambio = True
                if cambio:
                    print(f"Par oculto encontrado en {nombre_unidad}: {sorted([candidatos[i], candidatos[j]])}")
    return cambio

def aplicar_pares_ocultos(tablero, candidatos):
    """
    Aplica la técnica de pares ocultos en filas, columnas y bloques.
    """
    cambio_realizado = False
    # Filas
    for fila in range(9):
        cambio_realizado |= buscar_pares_ocultos_en_unidad(
            [candidatos[fila][col] for col in range(9)],
            f"Fila {fila+1}"
        )
    # Columnas
    for col in range(9):
        cambio_realizado |= buscar_pares_ocultos_en_unidad(
            [candidatos[fila][col] for fila in range(9)],
            f"Columna {col+1}"
        )
    # Bloques
    for bloque_fila in range(3):
        for bloque_col in range(3):
            celdas = []
            for r in range(3):
                for c in range(3):
                    fila = bloque_fila * 3 + r
                    col = bloque_col * 3 + c
                    celdas.append(candidatos[fila][col])
            cambio_realizado |= buscar_pares_ocultos_en_unidad(
                celdas,
                f"Bloque ({bloque_fila+1},{bloque_col+1})"
            )
    return cambio_realizado

#############################################################################################################################################################

import time # Para medir el tiempo del backtracking

def encontrar_celda_vacia(tablero):
    """
    Encuentra la próxima celda vacía (con valor 0) en el tablero.
    Devuelve una tupla (fila, col) o None si no hay celdas vacías.
    Busca de arriba a abajo, de izquierda a derecha.
    """
    for r in range(9):
        for c in range(9):
            if tablero[r][c] == 0:
                return (r, c)
    return None

def es_valido_colocar(tablero, fila, col, num):
    """
    Verifica si es válido colocar 'num' en tablero[fila][col].
    Esta función asume que estamos intentando colocar 'num' en una celda (potencialmente
    sobrescribiendo un valor anterior o llenando una vacía) y verifica
    si 'num' causa un conflicto con OTROS números en la misma fila, columna o bloque.
    """
    # Verificar fila (sin contar la propia celda si ya tuviera ese número)
    for c_idx in range(9):
        if c_idx != col and tablero[fila][c_idx] == num:
            return False

    # Verificar columna (sin contar la propia celda)
    for r_idx in range(9):
        if r_idx != fila and tablero[r_idx][col] == num:
            return False

    # Verificar bloque 3x3 (sin contar la propia celda)
    start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r != fila or c != col) and tablero[r][c] == num:
                return False
    return True

def _resolver_sudoku_backtracking_recursivo(tablero, stats):
    """
    Función recursiva interna para backtracking con recolección de estadísticas.
    Modifica el 'tablero' (que es una copia) en el lugar.
    Devuelve True si se encuentra una solución, False en caso contrario.
    """
    stats['iteraciones'] += 1
    stats['profundidad_actual'] += 1
    stats['max_profundidad'] = max(stats['max_profundidad'], stats['profundidad_actual'])

    celda_vacia = encontrar_celda_vacia(tablero)

    if not celda_vacia: # No hay celdas vacías, Sudoku resuelto
        stats['profundidad_actual'] -= 1
        return True

    fila, col = celda_vacia

    for num_intento in range(1, 10):
        # La función es_valido_colocar ya está pensada para cuando la celda (fila,col)
        # aún no tiene num_intento. Si (fila,col) ya tuviera un valor, es_valido_colocar
        # lo ignoraría para la comprobación, lo cual es correcto si se está
        # validando la colocación de un nuevo número.
        # En nuestro caso, tablero[fila][col] es 0.
        # Una versión más simple de es_valido_colocar (que no necesite el 'and c_idx != col')
        # también funcionaría si se garantiza que tablero[fila][col] es 0.
        if es_valido_colocar(tablero, fila, col, num_intento):
            tablero[fila][col] = num_intento

            if _resolver_sudoku_backtracking_recursivo(tablero, stats):
                stats['profundidad_actual'] -= 1
                return True

            # Backtrack: si la rama no llevó a solución, deshacer
            stats['retrocesos'] += 1
            tablero[fila][col] = 0
    
    stats['profundidad_actual'] -= 1
    return False # Ningún número funcionó para esta celda, retroceder

def resolver_sudoku_fuerza_bruta(tablero_previo_bt):
    """
    Wrapper para el solver de backtracking (fuerza bruta).
    Trabaja sobre una copia del tablero_previo_bt.
    Devuelve: (tablero_solucionado o None, num_iteraciones, max_profundidad, tiempo_tardado)
    """
    # Crear una copia profunda para que el backtracking no modifique el tablero original (previo_bt)
    tablero_copia = [fila[:] for fila in tablero_previo_bt]

    stats = {
        'iteraciones': 0,         # Total de llamadas recursivas
        'profundidad_actual': 0,  # Nivel de recursión actual
        'retrocesos': 0,          # Total de retrocesos
        'max_profundidad': 0      # Máxima profundidad alcanzada
    }

    start_time = time.time()
    
    tiene_solucion = _resolver_sudoku_backtracking_recursivo(tablero_copia, stats)
    
    end_time = time.time()
    tiempo_tardado = end_time - start_time

    if tiene_solucion:
        return tablero_copia, stats['iteraciones'], stats['max_profundidad'], tiempo_tardado, stats['retrocesos']
    else:
        # Si no hay solución, tablero_previo_bt no fue modificado.
        # Devolvemos None para el tablero, y las estadísticas del intento fallido.
        return None, stats['iteraciones'], stats['max_profundidad'], tiempo_tardado, stats['retrocesos']

#############################################################################################################################################################

def main():
    resuelto_e_impreso_por_heuristicas = False

    tablero_leido = leer_tablero()
    # leer_tablero ya valida la entrada inicial y pide reintentar si es inválida.
    # Si se quisiera manejar un fallo de leer_tablero (ej. devuelve None), se haría aquí.

    # tablero_actual será el tablero en el que se trabaja.
    # Se inicializa con el tablero leído y se modifica por las heurísticas y, si tiene éxito, por el backtracking.
    tablero_actual = [fila[:] for fila in tablero_leido]

    tablero_original_para_bt_stats = [fila[:] for fila in tablero_leido] # Copia para comparar celdas llenadas

    candidatos = calcular_candidatos(tablero_actual) # Calcular sobre la copia
    imprimir_candidatos(candidatos, "Inicializar candidatos")
    
    paso_iteracion_heuristica = 1
    max_iteraciones_heuristicas = 20 # Límite para heurísticas
    resuelto_e_impreso_por_heuristicas = False

    while paso_iteracion_heuristica <= max_iteraciones_heuristicas:
        cambio_en_iteracion = False
        print(f"\nIteración heurística {paso_iteracion_heuristica}")
        
        # Guardar estado del tablero antes de las heurísticas de esta iteración para estadísticas de BT
        if paso_iteracion_heuristica == 1: # Guardar el estado inicial antes de cualquier heurística para el cálculo de celdas llenadas por BT
            tablero_antes_de_bt_definitivo = [fila[:] for fila in tablero_actual]

        # Aplicar técnicas más directas primero
        if aplicar_candidato_unico(tablero_actual, candidatos): cambio_en_iteracion = True
        if aplicar_singles_ocultos(tablero_actual, candidatos): cambio_en_iteracion = True
        
        # Si las directas no hicieron cambio, probar las más complejas de eliminación
        if not cambio_en_iteracion: 
            if aplicar_pares_desnudos(tablero_actual, candidatos): cambio_en_iteracion = True
            # Podrías re-evaluar `cambio_en_iteracion` después de cada llamada si quieres ser granular
            if aplicar_conjuntos_desnudos(tablero_actual, candidatos, 3): cambio_en_iteracion = True 
            if aplicar_conjuntos_desnudos(tablero_actual, candidatos, 4): cambio_en_iteracion = True 
            if aplicar_pares_ocultos(tablero_actual, candidatos): cambio_en_iteracion = True
        
        # Comprobar si el tablero está resuelto después de esta iteración de heurísticas
        resuelto_por_heuristica_en_iteracion = all(tablero_actual[r][c] != 0 for r in range(9) for c in range(9))
        if resuelto_por_heuristica_en_iteracion:
            print("\n¡Sudoku Resuelto con técnicas heurísticas!")
            imprimir_tablero(tablero_actual)
            resuelto_e_impreso_por_heuristicas = True
            return # Fin del programa si se resuelve

        if not cambio_en_iteracion:
            print("\nNo se encontraron más cambios con técnicas heurísticas en esta iteración.")
            break # Salir del bucle de heurísticas si no hay más progreso
        
        paso_iteracion_heuristica += 1
        if paso_iteracion_heuristica > max_iteraciones_heuristicas:
            print("\nLímite de iteraciones heurísticas alcanzado.")
            break

    # Si no se actualizó tablero_antes_de_bt_definitivo porque el bucle terminó por max_iteraciones o resolución
    if 'tablero_antes_de_bt_definitivo' not in locals():
         tablero_antes_de_bt_definitivo = [fila[:] for fila in tablero_actual]
    
    # Después del bucle de heurísticas, verificar si está resuelto
    resuelto_final_heuristicas = all(tablero_actual[r][c] != 0 for r in range(9) for c in range(9))

    if not resuelto_final_heuristicas:
        print("\nEl Sudoku no pudo ser resuelto completamente con técnicas heurísticas.")
        print("Estado del tablero antes de intentar backtracking (fuerza bruta):")
        imprimir_tablero(tablero_antes_de_bt_definitivo) # Mostrar el tablero que ENTRARÁ al BT
        # Opcionalmente, mostrar candidatos si son relevantes para el usuario en este punto
        # imprimir_candidatos(candidatos, "Candidatos pre-backtracking")
        
        print("\nIniciando backtracking (fuerza bruta)...")
        
        # Llamar a la función de backtracking. Esta recibe el estado actual del tablero
        # (modificado por heurísticas) y trabaja sobre una copia.
        tablero_solucion_bt, iter_bt, prof_bt, tiempo_bt, retrocesos_bt = resolver_sudoku_fuerza_bruta(tablero_actual)

        print(f"Proceso de Backtracking finalizado en {tiempo_bt:.4f} segundos.")
        print(f"  Iteraciones (llamadas recursivas): {iter_bt}")
        print(f"  Profundidad máxima alcanzada: {prof_bt}")
        print(f"  Total de retrocesos: {retrocesos_bt}")

        if tablero_solucion_bt:
            print("¡Sudoku Resuelto con backtracking!")

            celdas_llenadas_por_bt = 0
            for r in range(9):
                for c in range(9):
                    if tablero_antes_de_bt_definitivo[r][c] == 0 and tablero_solucion_bt[r][c] != 0:
                        celdas_llenadas_por_bt +=1
            print(f"  Celdas llenadas por backtracking: {celdas_llenadas_por_bt}") # << NUEVA ESTADÍSTICA

            imprimir_tablero(tablero_solucion_bt)
        else:
            print("El Sudoku no tiene solución (verificado por backtracking).")
            print("El tablero mostrado a continuación es el estado en el que quedó después de las técnicas heurísticas (antes del intento de backtracking):")
            imprimir_tablero(tablero_antes_de_bt_definitivo) # tablero_actual no fue modificado por el BT fallido

    elif resuelto_final_heuristicas and not resuelto_e_impreso_por_heuristicas:
        print("\n¡Sudoku Resuelto con técnicas heurísticas (verificado después del bucle)!")
        imprimir_tablero(tablero_actual)

    # La variable tablero_actual contiene el estado final del tablero
    # (ya sea resuelto por heurísticas, resuelto por backtracking, o el estado
    # pre-backtracking si no tuvo solución). Las impresiones ya se hicieron.
while True:
    opcion = ""
    print("\nMenu:")
    print("1. Resolver un sudoku")
    print("2. Salir")
    # Bucle para asegurar una opción válida
    while opcion not in ["1", "2"]:
        opcion = input("Elige una opción: ").strip()
        if opcion not in ["1", "2"]:
            print("Opción inválida. Por favor ingresa 1 o 2.")
    
    if opcion == "1":
        main() 
        # main() ahora maneja todas las impresiones del resultado del Sudoku.
    elif opcion == "2":
        print("Gracias por usar el programa. ¡Hasta luego!")
```
<Editor id="Solver" max-height="0px"/>