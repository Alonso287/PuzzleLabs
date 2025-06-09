# Práctica: Programación de un algoritmo de creación de sudokus
Tras haber construido un programa capaz de resolver sudokus, el siguiente paso lógico es crear uno que los genere. Utilizaremos algunos de los conceptos que ya conocemos, como el **backtracking**, pero con un enfoque diferente para asegurar la creación de puzzles válidos y variados.

___

El código, al igual que nuestro resolvedor, se dividirá en funciones modulares, cada una encargada de una parte específica del proceso de generación.

## Funciones Auxiliares Comunes
Para empezar, nuestro generador necesitará algunas funciones de apoyo que ya nos resultan familiares del proyecto anterior. Estas funciones se encargan de tareas básicas como imprimir el tablero o validar la colocación de un número.

### Impresión del tablero
Para visualizar tanto el puzzle final como su solución, necesitamos una forma de mostrar el tablero en la consola. Reutilizaremos la función `imprimir_tablero`, que convierte nuestra matriz 2D en una cuadrícula de Sudoku fácil de leer.

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
- Su funcionamiento es idéntico al que ya conocemos: itera sobre cada celda del tablero.
- Si la celda contiene un `0`, la imprime como un punto (`.`) para indicar un hueco.
- Añade separadores verticales (`|`) y horizontales (`-`) para delinear los bloques de 3x3, mejorando la legibilidad.

### Búsqueda de celdas y validación
El corazón de nuestro generador, el algoritmo de backtracking, necesita dos herramientas clave: una para encontrar la siguiente celda a rellenar y otra para comprobar si un número puede ser colocado en ella. También usamos estas dos funciones en el algoritmo de resolución anterior.

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
        if tablero[fila][c_idx] == num:
            return False
    # Verificar columna
    for r_idx in range(9):
        if tablero[r_idx][col] == num:
            return False
    # Verificar bloque 3x3
    start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if tablero[r][c] == num:
                return False
    return True
```
- **`encontrar_celda_vacia()`**: Esta función recorre el tablero de arriba a abajo y de izquierda a derecha. Devuelve las coordenadas `(fila, col)` de la primera celda que contiene un `0`. Si no encuentra ninguna, significa que el tablero está lleno y devuelve `None`.
- **`es_valido_colocar()`**: Esta función es fundamental. Dado un tablero, unas coordenadas y un número, comprueba si colocar ese número viola las reglas del Sudoku. Revisa la fila, la columna y el bloque 3x3 correspondiente para asegurarse de que el número no está ya presente. Si el número es válido, devuelve `True`; de lo contrario, `False`.

## Generación del Sudoku
Aquí es donde reside la nueva lógica. El proceso de creación se divide en dos fases principales:
1.  **Generar una solución completa**: Crear un tablero de Sudoku 9x9 completamente resuelto y válido.
2.  **Crear el puzzle**: A partir de la solución completa, eliminar un número de casillas para crear un puzzle con un nivel de dificultad determinado por el número de pistas restantes.

### Generando una solución completa: Backtracking con aleatoriedad
Para generar un tablero resuelto, usaremos un algoritmo de backtracking, similar al que usamos para resolver. Sin embargo, hay una diferencia crucial: para crear un tablero diferente cada vez, introduciremos un elemento de **aleatoriedad**.

```python
def _generar_recursivo(tablero):
    celda_vacia = encontrar_celda_vacia(tablero)

    if not celda_vacia:
        return True

    fila, col = celda_vacia
    
    numeros_a_probar = list(range(1, 10))
    random.shuffle(numeros_a_probar)

    for num in numeros_a_probar:
        if es_valido_colocar(tablero, fila, col, num):
            tablero[fila][col] = num
            if _generar_recursivo(tablero):
                return True
            tablero[fila][col] = 0 # Backtrack
    
    return False

def generar_sudoku_lleno():
    tablero = [[0 for _ in range(9)] for _ in range(9)]
    _generar_recursivo(tablero)
    return tablero
```
- La función `generar_sudoku_lleno` simplemente crea un tablero vacío y llama a la función recursiva `_generar_recursivo` para que lo rellene.
- El núcleo de la lógica está en `_generar_recursivo`:
    - **Caso Base**: Al igual que en el resolvedor, si `encontrar_celda_vacia` devuelve `None`, el tablero está lleno y la recursión termina con éxito (`return True`).
    - **La Clave de la Generación**: En lugar de probar los números en orden (1, 2, 3...), creamos una lista `numeros_a_probar` con los números del 1 al 9 y la **desordenamos** con `random.shuffle()`.
    - **Paso Recursivo**: La función itera sobre esta lista de números desordenada. Para cada número:
        1.  Comprueba si es válido colocarlo.
        2.  Si es válido, lo coloca en el tablero y se llama a sí misma para continuar rellenando el resto.
        3.  Si la llamada recursiva tiene éxito, propaga el `True` hacia arriba.
        4.  **Backtracking**: Si la llamada recursiva falla, significa que la elección llevó a un callejón sin salida. Se deshace el movimiento (poniendo la celda a `0`) y se prueba el siguiente número de la lista aleatoria.

Este pequeño cambio (`random.shuffle()`) es lo que garantiza que cada vez que ejecutemos el programa, obtengamos un tablero de Sudoku completamente diferente.

### Creando el puzzle: Eliminando casillas
Una vez que tenemos una solución completa, necesitamos "vaciarla" para crear el puzzle que resolverá el usuario. La dificultad del puzzle dependerá del número de pistas que dejemos.

```python
def crear_puzzle(tablero_completo, pistas):
    puzzle = [fila[:] for fila in tablero_completo]
    celdas_a_eliminar = 81 - pistas
    
    coordenadas = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(coordenadas)

    for _ in range(celdas_a_eliminar):
        r, c = coordenadas.pop()
        puzzle[r][c] = 0
        
    return puzzle
```
- La función recibe el tablero resuelto y el número de `pistas` deseadas.
- Primero, crea una copia del tablero completo para no modificar el original.
- Calcula cuántas celdas necesita eliminar (`81 - pistas`).
- Para eliminar celdas de forma aleatoria, sigue estos pasos:
    1.  Crea una lista con todas las coordenadas posibles del tablero, desde `(0, 0)` hasta `(8, 8)`.
    2.  Desordena esta lista de coordenadas con `random.shuffle()`.
    3.  Itera `celdas_a_eliminar` veces, y en cada iteración, extrae la última coordenada de la lista desordenada con `.pop()` y establece el valor de esa celda en el puzzle a `0`.
- Finalmente, devuelve el tablero del puzzle con los huecos.

::: tip **Nota importante**
Este método de eliminación de casillas es sencillo y eficaz, pero no garantiza que el Sudoku resultante tenga una única solución. Los algoritmos de generación más avanzados comprueban la unicidad de la solución después de cada eliminación, pero para nuestro propósito didáctico, este enfoque es perfecto.
:::

## Flujo principal del programa
La función `main()` y el bloque `if __name__ == "__main__":` se encargan de unir todas las piezas y de interactuar con el usuario.

### La función `main()`
Esta función orquesta todo el proceso de generación y presentación.

```python
def main():
    while True:
        try:
            pistas = int(input("Introduce el número de pistas para el Sudoku (ej: 25-35 es un buen rango): ").strip())
            if 17 <= pistas <= 80:
                break
            else:
                print("Por favor, introduce un número entre 17 y 80.")
        except ValueError:
            print("Entrada inválida. Por favor, introduce un número entero.")

    print("\nGenerando un tablero de Sudoku completo...")
    solucion = generar_sudoku_lleno()
    
    print("Creando un puzzle con {} pistas a partir de la solución...".format(pistas))
    puzzle = crear_puzzle(solucion, pistas)
    
    print("\n--- Puzzle de Sudoku Generado ---")
    imprimir_tablero(puzzle)
    
    ver_solucion = input("¿Deseas ver la solución? (s/n): ").strip().lower()
    if ver_solucion == 's':
        print("\n--- Solución ---")
        imprimir_tablero(solucion)
```
- **Entrada del usuario**: Pide al usuario que introduzca el número de pistas deseadas. Incluye una validación para asegurar que el número está en un rango razonable (se sabe que un Sudoku válido necesita al menos 17 pistas).
- **Generación**: Llama a `generar_sudoku_lleno()` para crear la solución base.
- **Creación del puzzle**: Llama a `crear_puzzle()` para eliminar casillas y crear el desafío.
- **Presentación**: Imprime el puzzle generado para el usuario.
- **Mostrar solución**: Finalmente, pregunta al usuario si desea ver la solución. Si la respuesta es afirmativa, imprime el tablero completo que se generó al principio.

### Punto de entrada del programa
Este es el código que se ejecuta al iniciar el script. Al igual que en el resolvedor, presenta un menú simple.

```python
if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Generar un nuevo Sudoku")
        print("2. Salir")
        
        opcion = ""
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
- El bloque crea un bucle infinito que muestra un menú con dos opciones.
- El usuario puede elegir generar un nuevo Sudoku (que llama a la función `main`) o salir del programa.
- Proporciona una interfaz de usuario clara y reutilizable.

## ¡Pruébalo tú mismo!
Aquí tienes el código completo del generador de Sudokus, que puedes ejecutar haciendo click en el triángulo de arriba a la derecha. También puedes descargar el archivo del script entero en nuestro repositorio de GitHub.

```python:line-numbers
import random

def imprimir_tablero(tablero):
    """
    Imprime el tablero de Sudoku en formato tradicional.
    Usa '.' para representar los huecos vacíos.
    """
    print("=" * 25)
    for i, fila in enumerate(tablero):
        # Construye la representación de la fila con espacios y separadores
        fila_str = ""
        for j, num in enumerate(fila):
            if num == 0:
                fila_str += ". "
            else:
                fila_str += str(num) + " "
            if (j + 1) % 3 == 0 and j != 8:
                fila_str += "| "
        print(fila_str)
        # Imprime la línea horizontal separadora de bloques
        if (i + 1) % 3 == 0 and i != 8:
            print("-" * 25)
    print("=" * 25)

def encontrar_celda_vacia(tablero):
    """
    Encuentra la próxima celda vacía (con valor 0) en el tablero.
    Devuelve una tupla (fila, col) o None si no hay celdas vacías.
    """
    for r in range(9):
        for c in range(9):
            if tablero[r][c] == 0:
                return (r, c)
    return None

def es_valido_colocar(tablero, fila, col, num):
    """
    Verifica si es válido colocar 'num' en tablero[fila][col].
    Comprueba que 'num' no exista ya en la misma fila, columna o bloque 3x3.
    """
    # Verificar fila
    for c_idx in range(9):
        if tablero[fila][c_idx] == num:
            return False

    # Verificar columna
    for r_idx in range(9):
        if tablero[r_idx][col] == num:
            return False

    # Verificar bloque 3x3
    start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if tablero[r][c] == num:
                return False
    return True

# --- Lógica de Generación de Sudokus ---

def _generar_recursivo(tablero):
    """
    Función recursiva interna para generar un tablero de Sudoku completo.
    Utiliza backtracking con un orden de números aleatorio para crear variedad.
    Devuelve True si se genera una solución completa, False en caso contrario.
    """
    celda_vacia = encontrar_celda_vacia(tablero)

    if not celda_vacia: # Si no hay celdas vacías, el tablero está completo.
        return True

    fila, col = celda_vacia
    
    # Aquí está la clave: en lugar de probar 1-9 en orden, los probamos al azar.
    # Esto es funcionalmente idéntico a "elegir un candidato válido al azar".
    numeros_a_probar = list(range(1, 10))
    random.shuffle(numeros_a_probar)

    for num in numeros_a_probar:
        if es_valido_colocar(tablero, fila, col, num):
            tablero[fila][col] = num

            # Llama recursivamente para rellenar el resto del tablero
            if _generar_recursivo(tablero):
                return True

            # Backtrack: si la rama no llevó a una solución, deshacer el movimiento
            tablero[fila][col] = 0
    
    return False # Ningún número funcionó, es necesario retroceder

def generar_sudoku_lleno():
    """
    Crea un tablero de Sudoku completamente resuelto y válido.
    """
    # Empezamos con un tablero completamente vacío
    tablero = [[0 for _ in range(9)] for _ in range(9)]
    # Lo rellenamos usando nuestra función de generación recursiva
    _generar_recursivo(tablero)
    return tablero

def crear_puzzle(tablero_completo, pistas):
    """
    A partir de un tablero de Sudoku completo, elimina casillas para crear un puzzle.
    
    Args:
        tablero_completo (list): Un tablero 9x9 resuelto.
        pistas (int): El número de casillas que deben permanecer visibles.
    
    Returns:
        list: Un tablero de puzzle 9x9 con huecos (0).
    """
    puzzle = [fila[:] for fila in tablero_completo]
    celdas_a_eliminar = 81 - pistas
    
    # Obtenemos una lista de todas las coordenadas (0,0), (0,1), ... (8,8)
    coordenadas = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(coordenadas) # Las desordenamos

    # Eliminamos el número necesario de celdas
    for _ in range(celdas_a_eliminar):
        r, c = coordenadas.pop()
        puzzle[r][c] = 0
        
    return puzzle

def main():
    """
    Función principal que orquesta la generación y muestra del Sudoku.
    """
    while True:
        try:
            pistas = int(input("Introduce el número de pistas para el Sudoku (ej: 25-35 es un buen rango): ").strip())
            if 17 <= pistas <= 80: # Un Sudoku necesita al menos 17 pistas para tener solución única
                break
            else:
                print("Por favor, introduce un número entre 17 y 80.")
        except ValueError:
            print("Entrada inválida. Por favor, introduce un número entero.")

    print("\nGenerando un tablero de Sudoku completo...")
    solucion = generar_sudoku_lleno()
    
    print("Creando un puzzle con {} pistas a partir de la solución...".format(pistas))
    puzzle = crear_puzzle(solucion, pistas)
    
    print("\n--- Puzzle de Sudoku Generado ---")
    imprimir_tablero(puzzle)
    
    ver_solucion = input("¿Deseas ver la solución? (s/n): ").strip().lower()
    if ver_solucion == 's':
        print("\n--- Solución ---")
        imprimir_tablero(solucion)

while True:
    print("\nMenu:")
    print("1. Generar un nuevo Sudoku")
    print("2. Salir")
    
    opcion = ""
    while opcion not in ["1", "2"]:
        opcion = input("Elige una opción: ").strip()
        if opcion not in ["1", "2"]:
            print("Opción inválida. Por favor ingresa 1 o 2.")
    
    if opcion == "1":
        main()
    elif opcion == "2":
        print("Gracias por usar el programa. ¡Hasta luego!")
```
<Editor id="Generator" max-height="0px"/>