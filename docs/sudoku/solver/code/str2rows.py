def convertir_a_tablero(sudoku_str):
    # Verificar que la cadena tenga exactamente 81 caracteres
    while True:
        if len(sudoku_str) != 81:
            print("La cadena debe tener exactamente 81 caracteres.")
            sudoku_str = input(
                "Introduce nuevamente la cadena de 81 caracteres del tablero de Sudoku: "
            )
            continue
        break

    # Convertir la cadena en una lista de 9 listas (filas del tablero)
    tablero = []
    for i in range(9):
        fila = []
        for j in range(9):
            caracter = sudoku_str[i * 9 + j]
            if caracter == ".":
                fila.append(0)  # Reemplazar el punto por 0
            else:
                fila.append(int(caracter))  # Convertir el número a entero
        tablero.append(fila)

    return tablero


# Solicitar al usuario la cadena de 81 caracteres
cadena = input("Introduce la cadena de 81 caracteres del tablero de Sudoku: ")

# Verificar si la longitud es válida
if len(cadena) != 81:
    print("Error: La cadena debe tener exactamente 81 caracteres.")
else:
    # Convertir la cadena en el tablero
    tablero = convertir_a_tablero(cadena)

    # Mostrar el tablero como 9 líneas de números (sin comas ni corchetes)
    print("\nTablero de Sudoku:")
    for fila in tablero:
        print("".join(map(str, fila)))  # Unir los números de la fila en un string
