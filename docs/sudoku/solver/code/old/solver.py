# https://chatgpt.com/share/6838c9cc-2a7c-8007-aa14-a58103694d00
# sudoku_solver.py
from time import time

def leer_sudoku_usuario():
    """Lee 9 filas de 9 números del usuario (como strings)."""
    tablero = []
    print("Introduce el sudoku fila por fila (9 dígitos entre 0 y 9, usa 0 para celdas vacías):")
    for i in range(9):
        while True:
            fila = input(f"Fila {i+1}: ").strip()
            if len(fila) == 9 and all(c in "0123456789" for c in fila):
                tablero.append([int(c) for c in fila])
                break
            else:
                print("Entrada no válida. Asegúrate de introducir exactamente 9 dígitos entre 0 y 9.")
    return tablero

def imprimir_tablero(tablero):
    """Imprime el tablero en formato simple (9x9)."""
    for i, fila in enumerate(tablero):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j, val in enumerate(fila):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(val if val != 0 else ".", end=" ")
        print()
    print()

def validar_tablero(tablero):
    """Comprueba que no haya conflictos en filas, columnas o bloques."""
    for i in range(9):
        fila = [n for n in tablero[i] if n != 0]
        if len(fila) != len(set(fila)):
            return False

        col = [tablero[j][i] for j in range(9) if tablero[j][i] != 0]
        if len(col) != len(set(col)):
            return False

    # Validar bloques 3x3
    for bi in range(3):
        for bj in range(3):
            nums = []
            for i in range(3):
                for j in range(3):
                    val = tablero[bi*3 + i][bj*3 + j]
                    if val != 0:
                        nums.append(val)
            if len(nums) != len(set(nums)):
                return False
    return True

def main():
    tablero = leer_sudoku_usuario()
    print("\nTablero introducido:")
    imprimir_tablero(tablero)

    if not validar_tablero(tablero):
        print("El tablero contiene errores (valores duplicados en filas, columnas o bloques).")
        return

    # Aquí luego conectaremos con el resolutor
    print("Tablero válido. Preparado para resolver...")

if __name__ == "__main__":
    main()
