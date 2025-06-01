def imprimir_candidatos(candidatos, paso_actual):
    print("\n" + "=" * 40)
    print(f"Paso: {paso_actual}")
    print("=" * 40)
    for fila in range(9):
        fila_str = ""
        for col in range(9):
            celd = candidatos[fila][col]
            # Ordenamos para que se vea bonito
            contenido = ''.join(str(x) for x in sorted(celd))
            fila_str += f"{contenido:<9}"  # Ajusta el ancho a 9 para alinear
            if (col + 1) % 3 == 0 and col != 8:
                fila_str += "| "
        print(fila_str)
        if (fila + 1) % 3 == 0 and fila != 8:
            print("-" * 40)

def calcular_candidatos(tablero):
    candidatos = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
    for fila in range(9):
        for col in range(9):
            num = tablero[fila][col]
            if num != 0:
                candidatos[fila][col] = {num}
                # Eliminar este número de los candidatos de la misma fila
                for k in range(9):
                    if k != col:
                        candidatos[fila][k].discard(num)
                # Eliminar este número de los candidatos de la misma columna
                for k in range(9):
                    if k != fila:
                        candidatos[k][col].discard(num)
                # Eliminar este número del bloque 3x3
                start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
                for r in range(start_row, start_row + 3):
                    for c in range(start_col, start_col + 3):
                        if (r, c) != (fila, col):
                            candidatos[r][c].discard(num)
    return candidatos
