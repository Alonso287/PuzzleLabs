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
        return tablero_copia, stats['iteraciones'], stats['max_profundidad'], tiempo_tardado
    else:
        # Si no hay solución, tablero_previo_bt no fue modificado.
        # Devolvemos None para el tablero, y las estadísticas del intento fallido.
        return None, stats['iteraciones'], stats['max_profundidad'], tiempo_tardado

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
        tablero_solucion_bt, iter_bt, prof_bt, tiempo_bt = resolver_sudoku_fuerza_bruta(tablero_actual)

        print(f"Proceso de Backtracking finalizado en {tiempo_bt:.4f} segundos.")
        print(f"  Iteraciones (llamadas recursivas): {iter_bt}")
        print(f"  Profundidad máxima alcanzada: {prof_bt}")

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

if __name__ == "__main__":
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
            exit()