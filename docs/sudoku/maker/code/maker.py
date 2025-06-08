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