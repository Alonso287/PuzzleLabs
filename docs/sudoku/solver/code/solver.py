
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
            print("\nTablero introducido desde cadena:")
            imprimir_tablero(tablero)

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


def main():
    tablero = leer_tablero()
    candidatos = calcular_candidatos(tablero)
    imprimir_candidatos(candidatos, "Inicializar candidatos")
    paso_actual = 1
    # Aplicar los métodos
    while True:
        cambio = False
        print(f"\nIteración {paso_actual}")
        cambio |= aplicar_candidato_unico(tablero, candidatos)
        cambio |= aplicar_pares_desnudos(tablero, candidatos)
        cambio |= aplicar_conjuntos_desnudos(tablero, candidatos, 3)  # Tríos desnudos
        cambio |= aplicar_conjuntos_desnudos(tablero, candidatos, 4)  # Cuartetos desnudos
        cambio |= aplicar_singles_ocultos(tablero, candidatos) # Singles ocultos
        if not cambio:
            break 
        paso_actual += 1

if __name__ == "__main__":
    main()
