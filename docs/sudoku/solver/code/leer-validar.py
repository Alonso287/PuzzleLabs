def read_input():
    """
    Lee las 9 filas del sudoku desde consola.
    Cada fila debe ser una cadena de 9 dígitos (0 para celdas vacías).
    Devuelve un tablero como lista de listas de enteros.
    """
    board = []
    print("Introduce las 9 filas del Sudoku (usa 0 para huecos):")
    for i in range(9):
        while True:
            row_input = input(f"Fila {i+1}: ")
            if len(row_input) != 9 or not row_input.isdigit():
                print("Error: la fila debe contener exactamente 9 dígitos.")
                continue
            row = [int(char) for char in row_input]
            board.append(row)
            break
    return board

def validate_sudoku(board):
    """
    Valida que el tablero no tenga números repetidos en:
    - Filas
    - Columnas
    - Bloques de 3x3
    Devuelve True si es válido, False en caso contrario.
    """
    # Validar filas
    for i, row in enumerate(board):
        nums = [num for num in row if num != 0]
        if len(nums) != len(set(nums)):
            print(f"Error: Número repetido en la fila {i+1}.")
            return False

    # Validar columnas
    for col in range(9):
        nums = [board[row][col] for row in range(9) if board[row][col] != 0]
        if len(nums) != len(set(nums)):
            print(f"Error: Número repetido en la columna {col+1}.")
            return False

    # Validar bloques de 3x3
    for block_row in range(3):
        for block_col in range(3):
            nums = []
            for i in range(3):
                for j in range(3):
                    num = board[block_row*3 + i][block_col*3 + j]
                    if num != 0:
                        nums.append(num)
            if len(nums) != len(set(nums)):
                print(f"Error: Número repetido en el bloque ({block_row+1},{block_col+1}).")
                return False

    return True

def print_board(board):
    """
    Imprime el tablero de Sudoku en consola, con puntos para huecos vacíos.
    """
    print("\nTablero introducido:")
    for i, row in enumerate(board):
        row_str = ''
        for j, num in enumerate(row):
            row_str += f"{num if num != 0 else '.'} "
            if (j+1) % 3 == 0 and j < 8:
                row_str += "| "
        print(row_str)
        if (i+1) % 3 == 0 and i < 8:
            print("-" * 21)

def main():
    board = read_input()
    if not validate_sudoku(board):
        print("Sudoku inválido. Corrige los errores e inténtalo de nuevo.")
        return

    print_board(board)
    print("\nSudoku válido. ¡Listo para empezar a resolverlo!")
    # Aquí continuaríamos con el siguiente módulo (cálculo de candidatos, etc.)

if __name__ == "__main__":
    main()
