<script setup lang="ts">
import { ref, onMounted } from 'vue'

// Referencia para la instancia de Pyodide
const pyodide = ref<any>(null)
const isLoadingPyodide = ref(true)
const isExecuting = ref(false)
const output = ref<string[]>([])
const errorOutput = ref<string>('')

const sudokuInputType = ref<'filas' | 'cadena'>('cadena')
const sudokuFilas = ref(Array(9).fill(''))
const sudokuCadena = ref('003020600900305001001806400008102900700000008006708200002609500800203009005010300') // Ejemplo difícil

// El código Python completo que proporcionaste
const pythonCodeInitial = ref(`
def leer_tablero():
    """
    Lee un tablero de Sudoku de 9 filas desde consola y lo devuelve como una lista de listas.
    Usa 0 para representar los huecos vacíos.
    """
    opcion = input("¿Cómo deseas introducir el tablero de Sudoku?\\n1. Por filas\\n2. Como una cadena única\\nOpción: ").strip()

    while opcion not in ['1', '2']:
        print("Opción inválida. Por favor ingresa 1 o 2.")
        opcion = input("¿Cómo deseas introducir el tablero de Sudoku?\\n1. Por filas\\n2. Como una cadena única\\nOpción: ").strip()

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
            print("\\nTablero introducido por filas:")
            imprimir_tablero(tablero)

            if not validar_tablero(tablero):
                print("Tablero inválido. Vuelve a introducirlo.")
                continue

            # Esta parte de confirmación será automatizada en Pyodide
            # correcto = input ("\\n ¿El tablero introducido es correcto? (s/n): ").strip().lower()
            # while correcto not in ['s', 'n']:
            #     print("Opción inválida. Por favor ingresa 's' o 'n'.")
            #     correcto = input("\\n ¿El tablero introducido es correcto? (s/n): ").strip().lower()
            # if correcto == 'n':
            #         continue
            # elif correcto == 's':
            #         break
            print("Confirmación automática del tablero (Pyodide).") # Simulación
            break # Asumir correcto para Pyodide
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

            cadena_input = cadena_input.replace('.', '0')
            tablero = [ [int(cadena_input[i*9 + j]) for j in range(9)] for i in range(9)]
            
            print("\\nTablero introducido desde cadena:")
            imprimir_tablero(tablero)

            if not validar_tablero(tablero):
                print("Tablero inválido. Vuelve a introducirlo.")
                continue            

            # Esta parte de confirmación será automatizada en Pyodide
            # correcto = input ("\\n ¿El tablero introducido es correcto? (s/n): ").strip().lower()
            # while correcto not in ['s', 'n']:
            #     print("Opción inválida. Por favor ingresa 's' o 'n'.")
            #     correcto = input("\\n ¿El tablero introducido es correcto? (s/n): ").strip().lower()
            # if correcto == 'n':
            #         continue
            # elif correcto == 's':
            #         break
            print("Confirmación automática del tablero (Pyodide).") # Simulación
            break # Asumir correcto para Pyodide
        return tablero

def validar_fila(fila):
    numeros = [num for num in fila if num != 0]
    return len(numeros) == len(set(numeros))

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

def imprimir_tablero(tablero):
    print("=" * 25)
    for i, fila_val in enumerate(tablero): # Renombrado 'fila' a 'fila_val' para evitar conflicto
        fila_str = ""
        for j, num in enumerate(fila_val):
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
    candidatos = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
    for r_idx in range(9): # Renombrado 'fila' y 'col' para evitar conflictos
        for c_idx in range(9):
            num = tablero[r_idx][c_idx]
            if num != 0:
                candidatos[r_idx][c_idx] = {num}
                for k in range(9):
                    if k != c_idx:
                        candidatos[r_idx][k].discard(num)
                for k in range(9):
                    if k != r_idx:
                        candidatos[k][c_idx].discard(num)
                start_row, start_col = 3 * (r_idx // 3), 3 * (c_idx // 3)
                for r_loop in range(start_row, start_row + 3):
                    for c_loop in range(start_col, start_col + 3):
                        if (r_loop, c_loop) != (r_idx, c_idx):
                            candidatos[r_loop][c_loop].discard(num)
    return candidatos

def imprimir_candidatos(candidatos, paso_actual):
    print("\\n" + "=" * 40)
    print(f"Paso: {paso_actual}")
    print("=" * 40)
    for r_idx in range(9): # Renombrado 'fila' y 'col'
        fila_str = ""
        for c_idx in range(9):
            celd = candidatos[r_idx][c_idx]
            contenido = ''.join(str(x) for x in sorted(celd))
            fila_str += f"{contenido:<9}"
            if (c_idx + 1) % 3 == 0 and c_idx != 8:
                fila_str += "| "
        print(fila_str)
        if (r_idx + 1) % 3 == 0 and r_idx != 8:
            print("-" * 40)

def aplicar_candidato_unico(tablero, candidatos):
    cambio_realizado = False
    for r_idx in range(9): # Renombrado
        for c_idx in range(9):
            if tablero[r_idx][c_idx] == 0 and len(candidatos[r_idx][c_idx]) == 1:
                valor = candidatos[r_idx][c_idx].pop()
                tablero[r_idx][c_idx] = valor
                candidatos[r_idx][c_idx] = {valor}
                for k in range(9):
                    if k != c_idx:
                        candidatos[r_idx][k].discard(valor)
                for k in range(9):
                    if k != r_idx:
                        candidatos[k][c_idx].discard(valor)
                start_row, start_col = 3 * (r_idx // 3), 3 * (c_idx // 3)
                for r_loop in range(start_row, start_row + 3):
                    for c_loop in range(start_col, start_col + 3):
                        if (r_loop, c_loop) != (r_idx, c_idx):
                            candidatos[r_loop][c_loop].discard(valor)
                cambio_realizado = True
                imprimir_tablero(tablero)
                imprimir_candidatos(candidatos, f"Candidato único asignado en fila {r_idx+1}, columna {c_idx+1}")
    return cambio_realizado

def aplicar_pares_desnudos(tablero, candidatos):
    cambio_realizado = False
    for r_idx in range(9): # Renombrado
        cambio_realizado |= buscar_pares_en_unidad([candidatos[r_idx][c_val] for c_val in range(9)], f"Fila {r_idx+1}")
    for c_idx in range(9): # Renombrado
        cambio_realizado |= buscar_pares_en_unidad([candidatos[r_val][c_idx] for r_val in range(9)], f"Columna {c_idx+1}")
    for bloque_fila_idx in range(3): # Renombrado
        for bloque_col_idx in range(3):
            celdas = []
            for r_loop in range(3):
                for c_loop in range(3):
                    r_val = bloque_fila_idx * 3 + r_loop
                    c_val = bloque_col_idx * 3 + c_loop
                    celdas.append(candidatos[r_val][c_val])
            cambio_realizado |= buscar_pares_en_unidad(celdas, f"Bloque ({bloque_fila_idx+1},{bloque_col_idx+1})")
    return cambio_realizado

def buscar_pares_en_unidad(celdas, nombre_unidad):
    cambio = False
    pares = {}
    for i, celda in enumerate(celdas):
        if len(celda) == 2:
            clave = frozenset(celda)
            pares.setdefault(clave, []).append(i)
    for par, indices in pares.items():
        if len(indices) == 2:
            for i, celda in enumerate(celdas):
                if i not in indices:
                    antes = set(celda)
                    celda.difference_update(par)
                    if antes != celda:
                        cambio = True
    if cambio:
        print(f"Par desnudo encontrado en {nombre_unidad}: {sorted(list(par))}") # list(par)
    return cambio

def eliminar_candidato(tablero, candidatos, r_idx, c_idx, valor): # Renombrado
    for k in range(9):
        if k != c_idx:
            candidatos[r_idx][k].discard(valor)
    for k in range(9):
        if k != r_idx:
            candidatos[k][c_idx].discard(valor)
    start_row, start_col = 3 * (r_idx // 3), 3 * (c_idx // 3)
    for r_loop in range(start_row, start_row + 3):
        for c_loop in range(start_col, start_col + 3):
            if (r_loop, c_loop) != (r_idx, c_idx):
                candidatos[r_loop][c_loop].discard(valor)

def aplicar_conjuntos_desnudos(tablero, candidatos, tamaño):
    cambio_realizado = False
    from itertools import combinations # Mover import aquí si no está global
    for r_idx in range(9): # Renombrado
        cambio_realizado |= buscar_conjuntos_desnudos_en_unidad(
            [candidatos[r_idx][c_val] for c_val in range(9)], tamaño, f"Fila {r_idx+1}", combinations)
    for c_idx in range(9): # Renombrado
        cambio_realizado |= buscar_conjuntos_desnudos_en_unidad(
            [candidatos[r_val][c_idx] for r_val in range(9)], tamaño, f"Columna {c_idx+1}", combinations)
    for bloque_fila_idx in range(3): # Renombrado
        for bloque_col_idx in range(3):
            celdas_unidad = [] # Renombrado para evitar conflicto con celdas en buscar_singles_ocultos_en_unidad
            for r_loop in range(3):
                for c_loop in range(3):
                    r_val = bloque_fila_idx * 3 + r_loop
                    c_val = bloque_col_idx * 3 + c_loop
                    celdas_unidad.append(candidatos[r_val][c_val])
            cambio_realizado |= buscar_conjuntos_desnudos_en_unidad(
                celdas_unidad, tamaño, f"Bloque ({bloque_fila_idx+1},{bloque_col_idx+1})", combinations)
    return cambio_realizado

def buscar_conjuntos_desnudos_en_unidad(celdas_param, tamaño, nombre_unidad, combinations_func): # Renombrado y pasado combinations
    cambio = False
    indices = [i for i, celda in enumerate(celdas_param) if 2 <= len(celda) <= tamaño]
    for combo in combinations_func(indices, tamaño):
        conjunto = set()
        for idx in combo:
            conjunto |= celdas_param[idx]
        if len(conjunto) == tamaño:
            for i, celda in enumerate(celdas_param):
                if i not in combo:
                    antes = set(celda)
                    celda.difference_update(conjunto)
                    if antes != celda:
                        cambio = True
            if cambio: # Mover esta impresión fuera del bucle interno para que se imprima una vez por conjunto encontrado
                print(f"{tamaño}-desnudo encontrado en {nombre_unidad}: {sorted(list(conjunto))}") # list(conjunto)
    return cambio


def aplicar_singles_ocultos(tablero, candidatos):
    cambio_realizado = False
    from collections import defaultdict # Mover import
    for r_idx in range(9): # Renombrado
        cambio_realizado |= buscar_singles_ocultos_en_unidad(
            tablero, candidatos, [ (r_idx, c_val) for c_val in range(9) ], f"Fila {r_idx+1}", defaultdict)
    for c_idx in range(9): # Renombrado
        cambio_realizado |= buscar_singles_ocultos_en_unidad(
            tablero, candidatos, [ (r_val, c_idx) for r_val in range(9) ], f"Columna {c_idx+1}", defaultdict)
    for bloque_fila_idx in range(3): # Renombrado
        for bloque_col_idx in range(3):
            celdas_coords = [] # Renombrado
            for r_loop in range(3):
                for c_loop in range(3):
                    r_val = bloque_fila_idx * 3 + r_loop
                    c_val = bloque_col_idx * 3 + c_loop
                    celdas_coords.append((r_val, c_val))
            cambio_realizado |= buscar_singles_ocultos_en_unidad(
                tablero, candidatos, celdas_coords, f"Bloque ({bloque_fila_idx+1},{bloque_col_idx+1})", defaultdict)
    return cambio_realizado

def buscar_singles_ocultos_en_unidad(tablero, candidatos, celdas_coords_param, nombre_unidad, defaultdict_func): # Renombrado y pasado defaultdict
    cambio = False
    candidato_a_indices = defaultdict_func(list)
    for r_idx, c_idx in celdas_coords_param: # Renombrado
        if tablero[r_idx][c_idx] == 0:
            for candidato_val in candidatos[r_idx][c_idx]: # Renombrado
                candidato_a_indices[candidato_val].append((r_idx, c_idx))
    for candidato_val, posiciones in candidato_a_indices.items(): # Renombrado
        if len(posiciones) == 1:
            r_res, c_res = posiciones[0] # Renombrado
            tablero[r_res][c_res] = candidato_val
            candidatos[r_res][c_res] = {candidato_val}
            eliminar_candidato(tablero, candidatos, r_res, c_res, candidato_val)
            print(f"Single oculto encontrado en {nombre_unidad}: {candidato_val} en fila {r_res+1}, columna {c_res+1}")
            imprimir_tablero(tablero)
            imprimir_candidatos(candidatos, f"Single oculto asignado en fila {r_res+1}, columna {c_res+1}")
            cambio = True
    return cambio

def buscar_pares_ocultos_en_unidad(celdas_param, nombre_unidad, defaultdict_func): # Renombrado y pasado defaultdict
    cambio = False
    candidato_a_indices = defaultdict_func(set)
    for idx, celda in enumerate(celdas_param):
        for candidato_val in celda: # Renombrado
            candidato_a_indices[candidato_val].add(idx)
    
    lista_candidatos = list(candidato_a_indices.keys()) # Renombrado
    for i in range(len(lista_candidatos)):
        for j in range(i+1, len(lista_candidatos)):
            candidato_i = lista_candidatos[i] # Renombrado
            candidato_j = lista_candidatos[j] # Renombrado
            indices_i = candidato_a_indices[candidato_i]
            indices_j = candidato_a_indices[candidato_j]
            if indices_i == indices_j and len(indices_i) == 2:
                # Pares ocultos encontrados
                # Solo se actualiza el estado de 'cambio' una vez por par, y se imprime una vez.
                par_encontrado_y_aplicado_en_iteracion = False
                for idx_celda in indices_i: # Renombrado
                    celda_actual = celdas_param[idx_celda] # Renombrado
                    antes = set(celda_actual)
                    celda_actual.intersection_update({candidato_i, candidato_j})
                    if celda_actual != antes:
                        par_encontrado_y_aplicado_en_iteracion = True
                if par_encontrado_y_aplicado_en_iteracion: # Si hubo algún cambio en las celdas
                    print(f"Par oculto encontrado en {nombre_unidad}: {sorted([candidato_i, candidato_j])}")
                    cambio = True # Marcar cambio general para la unidad
    return cambio


def aplicar_pares_ocultos(tablero, candidatos):
    cambio_realizado = False
    from collections import defaultdict # Mover import
    for r_idx in range(9): # Renombrado
        cambio_realizado |= buscar_pares_ocultos_en_unidad(
            [candidatos[r_idx][c_val] for c_val in range(9)], f"Fila {r_idx+1}", defaultdict)
    for c_idx in range(9): # Renombrado
        cambio_realizado |= buscar_pares_ocultos_en_unidad(
            [candidatos[r_val][c_idx] for r_val in range(9)], f"Columna {c_idx+1}", defaultdict)
    for bloque_fila_idx in range(3): # Renombrado
        for bloque_col_idx in range(3):
            celdas_unidad = [] # Renombrado
            for r_loop in range(3):
                for c_loop in range(3):
                    r_val = bloque_fila_idx * 3 + r_loop
                    c_val = bloque_col_idx * 3 + c_loop
                    celdas_unidad.append(candidatos[r_val][c_val])
            cambio_realizado |= buscar_pares_ocultos_en_unidad(
                celdas_unidad, f"Bloque ({bloque_fila_idx+1},{bloque_col_idx+1})", defaultdict)
    return cambio_realizado

import time 

def encontrar_celda_vacia(tablero):
    for r_idx in range(9): # Renombrado
        for c_idx in range(9):
            if tablero[r_idx][c_idx] == 0:
                return (r_idx, c_idx)
    return None

def es_valido_colocar(tablero, r_idx, c_idx, num_val): # Renombrado
    for c_loop in range(9):
        if c_loop != c_idx and tablero[r_idx][c_loop] == num_val:
            return False
    for r_loop in range(9):
        if r_loop != r_idx and tablero[r_loop][c_idx] == num_val:
            return False
    start_row, start_col = 3 * (r_idx // 3), 3 * (c_idx // 3)
    for r_block in range(start_row, start_row + 3): # Renombrado
        for c_block in range(start_col, start_col + 3):
            if (r_block != r_idx or c_block != c_idx) and tablero[r_block][c_block] == num_val:
                return False
    return True

def _resolver_sudoku_backtracking_recursivo(tablero, stats):
    stats['iteraciones'] += 1
    stats['profundidad_actual'] += 1
    stats['max_profundidad'] = max(stats['max_profundidad'], stats['profundidad_actual'])
    celda_vacia_coords = encontrar_celda_vacia(tablero) # Renombrado
    if not celda_vacia_coords: 
        stats['profundidad_actual'] -= 1
        return True
    r_idx, c_idx = celda_vacia_coords # Renombrado
    for num_intento in range(1, 10):
        if es_valido_colocar(tablero, r_idx, c_idx, num_intento):
            tablero[r_idx][c_idx] = num_intento
            if _resolver_sudoku_backtracking_recursivo(tablero, stats):
                stats['profundidad_actual'] -= 1
                return True
            stats['retrocesos'] += 1
            tablero[r_idx][c_idx] = 0
    stats['profundidad_actual'] -= 1
    return False

def resolver_sudoku_fuerza_bruta(tablero_previo_bt):
    tablero_copia = [fila_val[:] for fila_val in tablero_previo_bt] # Renombrado
    stats = {
        'iteraciones': 0,
        'profundidad_actual': 0,
        'retrocesos': 0,
        'max_profundidad': 0,
        'tiempo_tardado': 0.0 # Añadido para consistencia
    }
    start_time_bt = time.time() # Renombrado
    tiene_solucion = _resolver_sudoku_backtracking_recursivo(tablero_copia, stats)
    end_time_bt = time.time() # Renombrado
    stats['tiempo_tardado'] = end_time_bt - start_time_bt # Asignar tiempo a stats

    # Modificado para devolver stats como un diccionario
    if tiene_solucion:
        return tablero_copia, stats
    else:
        return None, stats

def main():
    # No necesitamos pedir_confirmacion aquí porque leer_tablero_modificado lo manejará
    tablero_leido = leer_tablero() # Esta será la versión modificada por Pyodide
    if tablero_leido is None: # Si leer_tablero_modificado indica un error
        print("Error al leer o validar el tablero inicial. No se puede continuar.")
        return

    tablero_actual = [fila_val[:] for fila_val in tablero_leido] # Renombrado
    tablero_antes_de_bt_definitivo = [fila_val[:] for fila_val in tablero_leido] # Para estadísticas

    candidatos = calcular_candidatos(tablero_actual)
    imprimir_candidatos(candidatos, "Inicializar candidatos")
    
    paso_iteracion_heuristica = 1
    max_iteraciones_heuristicas = 20
    resuelto_e_impreso_por_heuristicas = False

    while paso_iteracion_heuristica <= max_iteraciones_heuristicas:
        cambio_en_iteracion = False
        print(f"\\nIteración heurística {paso_iteracion_heuristica}")
        
        if aplicar_candidato_unico(tablero_actual, candidatos): cambio_en_iteracion = True
        if aplicar_singles_ocultos(tablero_actual, candidatos): cambio_en_iteracion = True
        
        if not cambio_en_iteracion: 
            if aplicar_pares_desnudos(tablero_actual, candidatos): cambio_en_iteracion = True
            if aplicar_conjuntos_desnudos(tablero_actual, candidatos, 3): cambio_en_iteracion = True 
            if aplicar_conjuntos_desnudos(tablero_actual, candidatos, 4): cambio_en_iteracion = True 
            if aplicar_pares_ocultos(tablero_actual, candidatos): cambio_en_iteracion = True
        
        resuelto_por_heuristica_en_iteracion = all(tablero_actual[r_idx][c_idx] != 0 for r_idx in range(9) for c_idx in range(9))
        if resuelto_por_heuristica_en_iteracion:
            print("\\n¡Sudoku Resuelto con técnicas heurísticas!")
            imprimir_tablero(tablero_actual)
            resuelto_e_impreso_por_heuristicas = True
            return 

        if not cambio_en_iteracion:
            print("\\nNo se encontraron más cambios con técnicas heurísticas en esta iteración.")
            tablero_antes_de_bt_definitivo = [fila_val[:] for fila_val in tablero_actual] # Actualizar
            break 
        
        paso_iteracion_heuristica += 1
        if paso_iteracion_heuristica > max_iteraciones_heuristicas:
            print("\\nLímite de iteraciones heurísticas alcanzado.")
            tablero_antes_de_bt_definitivo = [fila_val[:] for fila_val in tablero_actual] # Actualizar
            break
    
    # Asegurar que tablero_antes_de_bt_definitivo esté actualizado si el bucle no se rompió explícitamente
    if paso_iteracion_heuristica > max_iteraciones_heuristicas or resuelto_e_impreso_por_heuristicas:
         # Si el bucle terminó por max_iteraciones o ya está resuelto, tablero_actual es el estado final de heurísticas
         if not resuelto_e_impreso_por_heuristicas: # Solo actualizar si no se rompió por resolución
            tablero_antes_de_bt_definitivo = [fila_val[:] for fila_val in tablero_actual]


    resuelto_final_heuristicas = all(tablero_actual[r_idx][c_idx] != 0 for r_idx in range(9) for c_idx in range(9))

    if not resuelto_final_heuristicas:
        print("\\nEl Sudoku no pudo ser resuelto completamente con técnicas heurísticas.")
        print("Estado del tablero antes de intentar backtracking (fuerza bruta):")
        imprimir_tablero(tablero_antes_de_bt_definitivo)
        
        print("\\nIniciando backtracking (fuerza bruta)...")
        
        # Usar el estado del tablero tal como quedó después de las heurísticas
        tablero_solucion_bt, stats_bt = resolver_sudoku_fuerza_bruta(tablero_antes_de_bt_definitivo)

        print(f"Proceso de Backtracking finalizado en {stats_bt['tiempo_tardado']:.4f} segundos.")
        print(f"  Iteraciones (llamadas recursivas): {stats_bt['iteraciones']}")
        print(f"  Profundidad máxima alcanzada: {stats_bt['max_profundidad']}")
        print(f"  Número de retrocesos (backtracks): {stats_bt['retrocesos']}")

        if tablero_solucion_bt:
            print("¡Sudoku Resuelto con backtracking!")
            celdas_llenadas_por_bt = 0
            for r_idx in range(9):
                for c_idx in range(9):
                    if tablero_antes_de_bt_definitivo[r_idx][c_idx] == 0 and tablero_solucion_bt[r_idx][c_idx] != 0:
                        celdas_llenadas_por_bt +=1
            print(f"  Celdas llenadas por backtracking: {celdas_llenadas_por_bt}")
            imprimir_tablero(tablero_solucion_bt)
        else:
            print("El Sudoku no tiene solución (verificado por backtracking).")
            print("El tablero mostrado a continuación es el estado en el que quedó después de las técnicas heurísticas (antes del intento de backtracking):")
            imprimir_tablero(tablero_antes_de_bt_definitivo)
    
    elif resuelto_final_heuristicas and not resuelto_e_impreso_por_heuristicas:
        print("\\n¡Sudoku Resuelto con técnicas heurísticas (verificado después del bucle)!")
        imprimir_tablero(tablero_actual)

# No incluir if __name__ == "__main__" aquí, será llamado desde JS.
`);

// --- EL RESTO DEL COMPONENTE VUE ---
// (Función para cargar Pyodide, ejecutar Python, template y estilos)
// (Será idéntico al proporcionado en mi respuesta anterior, pero con `pythonCodeInitial` en lugar de `pythonCode`)
// (Y la lógica en `executePython` usará `pythonCodeInitial.value` para construir `modifiedPythonCode`)

</script>

<script lang="ts">
// Necesario para que onMounted etc. funcionen si este script no es parte del <script setup>
// Si todo está en <script setup>, esto no es necesario.
// Sin embargo, para mantener la lógica junta, podemos dejarlo así o mover todo a setup.
// Por simplicidad, lo mantendré como en la respuesta anterior.


</script>

<template>
  <div class="sudoku-solver-component">
    <div v-if="isLoadingPyodide" class="loading-pyodide">
      Cargando Pyodide y motor Python...
    </div>

    <div v-else class="solver-ui">
      <div class="input-section">
        <h3>Introduce el Sudoku</h3>
        <div class="input-type-selector">
          <label>
            <input type="radio" v-model="sudokuInputType" value="cadena"> Cadena única (81 caracteres, '.' o '0' para vacíos)
          </label>
          <label>
            <input type="radio" v-model="sudokuInputType" value="filas"> Por filas (9 filas, 9 dígitos por fila)
          </label>
        </div>

        <div v-if="sudokuInputType === 'cadena'" class="sudoku-input-cadena">
          <textarea v-model="sudokuCadena" rows="3" placeholder="Ej: 0030206009003050010018064..."></textarea>
        </div>
        <div v-if="sudokuInputType === 'filas'" class="sudoku-input-filas">
          <div v-for="i in 9" :key="i">
            <input type="text" v-model="sudokuFilas[i-1]" :placeholder="`Fila ${i}`" maxlength="9">
          </div>
        </div>
         <button @click="executePython" :disabled="isExecuting || isLoadingPyodide" class="execute-button">
          {{ isExecuting ? 'Resolviendo...' : 'Resolver Sudoku' }}
        </button>
      </div>

      <div v-if="output.length > 0 || errorOutput" class="output-section">
        <h3>Salida</h3>
        <button @click="clearOutput" class="clear-button">Limpiar Salida</button>
        <pre v-if="errorOutput" class="error-output">{{ errorOutput }}</pre>
        <!-- Usar v-html con precaución. Aquí es para preservar espacios de la salida del tablero -->
        <div v-for="(line, index) in output" :key="index" class="output-line">
          <pre v-html="line.replace(/ /g, '&nbsp;')"></pre>
        </div>
      </div>
    </div>

    <details class="code-details">
      <summary>Ver/Ocultar Código Python Original</summary>
      <div class="language-python extra-class">
        <pre class="language-python"><code v-text="pythonCodeInitial"></code></pre>
      </div>
    </details>
  </div>
</template>

<style scoped>
.sudoku-solver-component {
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1.5em;
  margin-block: 1em;
  background-color: var(--vp-c-bg-soft);
}

.loading-pyodide, .solver-ui {
  color: var(--vp-c-text-1);
}

.input-section, .output-section {
  margin-bottom: 1.5em;
}

.input-section h3, .output-section h3 {
  margin-top: 0;
  margin-bottom: 0.8em;
  font-size: 1.2em;
  color: var(--vp-c-text-1);
  border-bottom: 1px solid var(--vp-c-divider);
  padding-bottom: 0.3em;
}

.input-type-selector {
  margin-bottom: 1em;
  display: flex;
  flex-direction: column;
  gap: 0.5em;
}
.input-type-selector label {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5em;
}


.sudoku-input-cadena textarea,
.sudoku-input-filas input[type="text"] {
  width: 100%;
  padding: 0.6em 0.8em;
  border-radius: 6px;
  border: 1px solid var(--vp-c-divider);
  background-color: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-family: var(--vp-font-family-mono);
  font-size: 0.9em;
  box-sizing: border-box; 
}
.sudoku-input-cadena textarea {
  min-height: 60px;
  resize: vertical;
}
.sudoku-input-filas div {
  margin-bottom: 0.3em;
}


.execute-button, .clear-button {
  background-color: var(--vp-c-brand-1);
  color: var(--vp-c-white);
  border: none;
  padding: 0.6em 1.2em;
  border-radius: 20px; 
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s ease;
  margin-top: 1em;
}
.execute-button:hover, .clear-button:hover {
  background-color: var(--vp-c-brand-2);
}
.execute-button:disabled {
  background-color: var(--vp-c-gray-soft);
  cursor: not-allowed;
}
.output-section .clear-button { /* Especificidad para el botón de limpiar */
  background-color: var(--vp-c-default-soft);
  color: var(--vp-c-text-1);
  float: right; /* Alinearlo a la derecha */
  margin-top: -0.5em; /* Ajuste vertical */
  margin-bottom: 0.5em;
  padding: 0.4em 0.8em; /* Más pequeño */
}
.output-section .clear-button:hover {
  background-color: var(--vp-c-default-hover);
}


.output-section .output-line pre { /* Aplicar estilos de bloque de código a cada línea de salida */
  background-color: var(--vp-code-block-bg);
  padding: 0.5em 1em; /* Menos padding vertical por línea */
  border-radius: 4px; /* Bordes más sutiles por línea */
  overflow-x: auto;
  white-space: pre-wrap; 
  word-wrap: break-word; 
  color: var(--vp-code-block-color);
  font-family: var(--vp-font-family-mono);
  font-size: 0.875em; 
  line-height: 1.7; 
  margin-bottom: 0.2em; /* Espacio entre líneas de salida */
}
.output-section .output-line:last-child pre {
  margin-bottom: 0;
}

.output-section .error-output {
  color: var(--vp-c-red-1);
  border: 1px solid var(--vp-c-red-dimm-1);
  background-color: var(--vp-c-red-soft);
  padding: 1em;
  border-radius: 6px;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: var(--vp-font-family-mono);
  font-size: 0.875em;
  line-height: 1.7;
}

.code-details {
  margin-top: 1.5em;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
}
.code-details summary {
  cursor: pointer;
  padding: 0.8em 1em;
  font-weight: 600;
  color: var(--vp-c-text-2);
  background-color: var(--vp-c-bg-mute);
  border-radius: 8px 8px 0 0; 
}
.code-details[open] summary {
    border-bottom: 1px solid var(--vp-c-divider);
}
.code-details div.language-python {
  background-color: var(--vp-code-block-bg); 
  border-radius: 0 0 8px 8px;
  max-height: 500px; /* Para que no sea demasiado largo */
  overflow-y: auto;
}
.code-details pre {
  margin: 0 !important; 
  border-radius: 0 0 6px 6px !important; 
  padding: 1em; /* Añadir padding interno al pre */
}
.code-details code {
    color: var(--vp-code-block-color);
    font-family: var(--vp-font-family-mono);
    font-size: 0.875em;
}
</style>