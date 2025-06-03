<template>
  <div class="sudoku-solver-container vp-raw">
    <ClientOnly> <!-- Evita SSR para Pyodide -->
      <div v-if="isLoadingPyodide" class="loading-pyodide">
        Cargando Pyodide y el entorno Python...
      </div>
      <div v-else class="solver-ui">
        <div class="input-section">
          <label for="sudoku-input">Introduce el Sudoku (81 caracteres, '.' para vacíos):</label>
          <textarea
            id="sudoku-input"
            v-model="sudokuInput"
            rows="3"
            placeholder="Ej: 53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"
          ></textarea>
          <button @click="runSudokuSolver" :disabled="isExecuting" class="run-button vp-button">
            {{ isExecuting ? 'Ejecutando...' : 'Resolver Sudoku' }}
          </button>
        </div>

        <div class="output-section" v-if="outputLog">
          <h3>Salida del Script:</h3>
          <pre class="output-log">{{ outputLog }}</pre>
        </div>
        
        <div class="code-display-section">
          <button @click="showCode = !showCode" class="toggle-code-button">
            {{ showCode ? 'Ocultar Código Python' : 'Mostrar Código Python' }}
          </button>
          <div v-if="showCode" class="code-block-container">
            <pre><code class="language-python">{{ pythonCodeString }}</code></pre>
          </div>
        </div>
      </div>
    </ClientOnly>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const isLoadingPyodide = ref(true);
const isExecuting = ref(false);
const sudokuInput = ref('53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79'); // Ejemplo
const outputLog = ref('');
const showCode = ref(false);
let pyodide = null;

// El código Python completo como una cadena
// (Incluye el código Python modificado del Paso 1 aquí)
const pythonCodeString = `
import time
from collections import defaultdict
from itertools import combinations

# Funciones de validación y utilidad
def validar_fila(fila):
    numeros = [num for num in fila if num != 0]
    return len(numeros) == len(set(numeros))

def validar_tablero(tablero):
    for i in range(9):
        fila = [num for num in tablero[i] if num != 0]
        if len(fila) != len(set(fila)):
            return False
        columna = [tablero[j][i] for j in range(9) if tablero[j][i] != 0]
        if len(columna) != len(set(columna)):
            return False
    for bloque_fila in range(3):
        for bloque_col in range(3):
            bloque = []
            for r_offset in range(3):
                for c_offset in range(3):
                    num = tablero[bloque_fila*3 + r_offset][bloque_col*3 + c_offset]
                    if num != 0:
                        bloque.append(num)
            if len(bloque) != len(set(bloque)):
                return False
    return True

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
        print(fila_str.strip())
        if (i + 1) % 3 == 0 and i != 8:
            print("-" * 25)
    print("=" * 25)

def calcular_candidatos(tablero):
    candidatos = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
    for fila in range(9):
        for col in range(9):
            num = tablero[fila][col]
            if num != 0:
                candidatos[fila][col] = {num}
                for k in range(9):
                    if k != col:
                        candidatos[fila][k].discard(num)
                for k in range(9):
                    if k != fila:
                        candidatos[k][col].discard(num)
                start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
                for r_idx in range(start_row, start_row + 3):
                    for c_idx in range(start_col, start_col + 3):
                        if (r_idx, c_idx) != (fila, col):
                            candidatos[r_idx][c_idx].discard(num)
    return candidatos

def imprimir_candidatos(candidatos, paso_actual):
    print("\\n" + "=" * 40)
    print(f"Paso: {paso_actual}")
    print("=" * 40)
    max_len = 0
    for fila_idx_loop in range(9):
        for col_idx_loop in range(9):
            contenido = ''.join(str(x) for x in sorted(candidatos[fila_idx_loop][col_idx_loop]))
            if len(contenido) > max_len:
                max_len = len(contenido)
    
    cell_width = max(max_len, 1) 

    for fila_idx_print in range(9):
        fila_str = ""
        for col_idx_print in range(9):
            celd = candidatos[fila_idx_print][col_idx_print]
            contenido = ''.join(str(x) for x in sorted(celd))
            fila_str += f"{contenido:<{cell_width}} " 
            if (col_idx_print + 1) % 3 == 0 and col_idx_print != 8:
                fila_str += "| "
        print(fila_str.strip())
        if (fila_idx_print + 1) % 3 == 0 and fila_idx_print != 8:
            print("-" * ( (cell_width + 1) * 9 + 2 * 2 -1) )

def eliminar_candidato_de_unidades(candidatos, fila, col, valor):
    for k in range(9):
        if k != col:
            candidatos[fila][k].discard(valor)
    for k in range(9):
        if k != fila:
            candidatos[k][col].discard(valor)
    start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
    for r_idx in range(start_row, start_row + 3):
        for c_idx in range(start_col, start_col + 3):
            if (r_idx, c_idx) != (fila, col):
                candidatos[r_idx][c_idx].discard(valor)

def aplicar_candidato_unico(tablero, candidatos):
    cambio_realizado = False
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0 and len(candidatos[fila][col]) == 1:
                valor = candidatos[fila][col].pop() # pop() modifica el set
                tablero[fila][col] = valor
                candidatos[fila][col] = {valor} # Asegurar que la celda ahora solo tiene este candidato
                eliminar_candidato_de_unidades(candidatos, fila, col, valor)
                cambio_realizado = True
                print(f"\\nCandidato único asignado: {valor} en ({fila+1},{col+1})")
                imprimir_tablero(tablero)
                imprimir_candidatos(candidatos, f"Tras asignar {valor} en ({fila+1},{col+1})")
    return cambio_realizado

def buscar_pares_en_unidad(celdas_unidad_refs, nombre_unidad):
    cambio_hecho_en_esta_unidad = False
    pares_encontrados = {} 
    for i, celda_candidatos in enumerate(celdas_unidad_refs):
        if len(celda_candidatos) == 2:
            par = frozenset(celda_candidatos)
            if par not in pares_encontrados:
                pares_encontrados[par] = []
            pares_encontrados[par].append(i)

    for par, indices in pares_encontrados.items():
        if len(indices) == 2: 
            numeros_par = list(par)
            cambio_local = False
            for i, celda_candidatos_ref in enumerate(celdas_unidad_refs):
                if i not in indices: 
                    original_len = len(celda_candidatos_ref)
                    celda_candidatos_ref.difference_update(numeros_par)
                    if len(celda_candidatos_ref) < original_len:
                        cambio_local = True
                        cambio_hecho_en_esta_unidad = True
            if cambio_local:
                 print(f"Par desnudo {sorted(list(par))} encontrado y aplicado en {nombre_unidad}.")
    return cambio_hecho_en_esta_unidad

def aplicar_pares_desnudos(tablero, candidatos):
    cambio_realizado = False
    # Filas
    for fila_idx in range(9):
        unidad_refs = [candidatos[fila_idx][col_idx] for col_idx in range(9)]
        if buscar_pares_en_unidad(unidad_refs, f"Fila {fila_idx+1}"):
            cambio_realizado = True
    # Columnas
    for col_idx in range(9):
        unidad_refs = [candidatos[fila_idx][col_idx] for fila_idx in range(9)]
        if buscar_pares_en_unidad(unidad_refs, f"Columna {col_idx+1}"):
            cambio_realizado = True
    # Bloques
    for bloque_fila_start in range(0,9,3):
        for bloque_col_start in range(0,9,3):
            unidad_refs = []
            for r_offset in range(3):
                for c_offset in range(3):
                    unidad_refs.append(candidatos[bloque_fila_start+r_offset][bloque_col_start+c_offset])
            if buscar_pares_en_unidad(unidad_refs, f"Bloque ({bloque_fila_start//3+1},{bloque_col_start//3+1})"):
                 cambio_realizado = True
    if cambio_realizado:
        imprimir_candidatos(candidatos, "Tras aplicar Pares Desnudos")
    return cambio_realizado

def buscar_conjuntos_desnudos_en_unidad(celdas_unidad_refs, tamaño, nombre_unidad):
    cambio_hecho_en_esta_unidad = False
    posibles_celdas_indices = [i for i, c in enumerate(celdas_unidad_refs) if 2 <= len(c) <= tamaño]

    if len(posibles_celdas_indices) < tamaño:
        return False

    for combo_indices in combinations(posibles_celdas_indices, tamaño):
        union_candidatos = set()
        for idx in combo_indices:
            union_candidatos.update(celdas_unidad_refs[idx])
        
        if len(union_candidatos) == tamaño:
            cambio_local = False
            for i, celda_actual_candidatos_ref in enumerate(celdas_unidad_refs):
                if i not in combo_indices: 
                    original_len = len(celda_actual_candidatos_ref)
                    celda_actual_candidatos_ref.difference_update(union_candidatos)
                    if len(celda_actual_candidatos_ref) < original_len:
                        cambio_local = True
                        cambio_hecho_en_esta_unidad = True
            if cambio_local:
                print(f"Conjunto desnudo de tamaño {tamaño} {sorted(list(union_candidatos))} encontrado y aplicado en {nombre_unidad}.")
    return cambio_hecho_en_esta_unidad

def aplicar_conjuntos_desnudos(tablero, candidatos, tamaño):
    cambio_realizado = False
    # Filas
    for fila_idx in range(9):
        unidad_refs = [candidatos[fila_idx][col_idx] for col_idx in range(9)]
        if buscar_conjuntos_desnudos_en_unidad(unidad_refs, tamaño, f"Fila {fila_idx+1}"):
            cambio_realizado = True
    # Columnas
    for col_idx in range(9):
        unidad_refs = [candidatos[fila_idx][col_idx] for fila_idx in range(9)]
        if buscar_conjuntos_desnudos_en_unidad(unidad_refs, tamaño, f"Columna {col_idx+1}"):
            cambio_realizado = True
    # Bloques
    for bloque_fila_start in range(0,9,3):
        for bloque_col_start in range(0,9,3):
            unidad_refs = []
            for r_offset in range(3):
                for c_offset in range(3):
                    unidad_refs.append(candidatos[bloque_fila_start+r_offset][bloque_col_start+c_offset])
            if buscar_conjuntos_desnudos_en_unidad(unidad_refs, tamaño, f"Bloque ({bloque_fila_start//3+1},{bloque_col_start//3+1})"):
                cambio_realizado = True
    if cambio_realizado:
        imprimir_candidatos(candidatos, f"Tras aplicar Conjuntos Desnudos de tamaño {tamaño}")
    return cambio_realizado

def buscar_singles_ocultos_en_unidad(tablero, candidatos, celdas_coords_en_unidad, nombre_unidad):
    cambio_hecho_en_esta_unidad = False
    for num_candidato in range(1, 10):
        apariciones = []
        for r_coord, c_coord in celdas_coords_en_unidad:
            if tablero[r_coord][c_coord] == 0 and num_candidato in candidatos[r_coord][c_coord]:
                apariciones.append((r_coord, c_coord))
        
        if len(apariciones) == 1:
            r_found, c_found = apariciones[0]
            print(f"\\nSingle oculto encontrado: {num_candidato} en ({r_found+1},{c_found+1}) en {nombre_unidad}.")
            tablero[r_found][c_found] = num_candidato
            candidatos[r_found][c_found] = {num_candidato}
            eliminar_candidato_de_unidades(candidatos, r_found, c_found, num_candidato)
            cambio_hecho_en_esta_unidad = True
            imprimir_tablero(tablero)
            imprimir_candidatos(candidatos, f"Tras asignar single oculto {num_candidato} en ({r_found+1},{c_found+1})")
    return cambio_hecho_en_esta_unidad

def aplicar_singles_ocultos(tablero, candidatos):
    cambio_realizado = False
    # Filas
    for fila_idx in range(9):
        coords_unidad = [(fila_idx, col_idx) for col_idx in range(9)]
        if buscar_singles_ocultos_en_unidad(tablero, candidatos, coords_unidad, f"Fila {fila_idx+1}"):
            cambio_realizado = True
    # Columnas
    for col_idx in range(9):
        coords_unidad = [(fila_idx, col_idx) for fila_idx in range(9)]
        if buscar_singles_ocultos_en_unidad(tablero, candidatos, coords_unidad, f"Columna {col_idx+1}"):
            cambio_realizado = True
    # Bloques
    for bloque_fila_start in range(0,9,3):
        for bloque_col_start in range(0,9,3):
            coords_unidad = []
            for r_offset in range(3):
                for c_offset in range(3):
                    coords_unidad.append((bloque_fila_start+r_offset, bloque_col_start+c_offset))
            if buscar_singles_ocultos_en_unidad(tablero, candidatos, coords_unidad, f"Bloque ({bloque_fila_start//3+1},{bloque_col_start//3+1})"):
                cambio_realizado = True
    return cambio_realizado

def buscar_pares_ocultos_en_unidad(celdas_unidad_refs, nombre_unidad, tablero_estado_actual, idx_guia1, idx_guia2, full_candidatos_board):
    cambio_hecho_en_esta_unidad = False
    candidato_posiciones_en_unidad = defaultdict(list) # num_candidato -> lista de indices EN LA UNIDAD donde aparece

    for i_en_unidad, celda_cands_ref in enumerate(celdas_unidad_refs):
        # Determinar coordenada global (r,c) de la celda i_en_unidad
        r_global, c_global = -1, -1
        if "Fila" in nombre_unidad: 
            r_global, c_global = idx_guia1, i_en_unidad
        elif "Columna" in nombre_unidad: 
            r_global, c_global = i_en_unidad, idx_guia2
        elif "Bloque" in nombre_unidad: 
            r_global = idx_guia1 + (i_en_unidad // 3)
            c_global = idx_guia2 + (i_en_unidad % 3)

        if tablero_estado_actual[r_global][c_global] == 0: # Solo celdas vacías
            for candidato_num in celda_cands_ref:
                candidato_posiciones_en_unidad[candidato_num].append(i_en_unidad)

    nums_disponibles_en_unidad = list(candidato_posiciones_en_unidad.keys())
    for i_cand_list in range(len(nums_disponibles_en_unidad)):
        for j_cand_list in range(i_cand_list + 1, len(nums_disponibles_en_unidad)):
            num1 = nums_disponibles_en_unidad[i_cand_list]
            num2 = nums_disponibles_en_unidad[j_cand_list]
            
            pos_num1_en_unidad = candidato_posiciones_en_unidad[num1]
            pos_num2_en_unidad = candidato_posiciones_en_unidad[num2]

            # Si ambos candidatos aparecen exactamente en las mismas DOS posiciones en la unidad
            if len(pos_num1_en_unidad) == 2 and pos_num1_en_unidad == pos_num2_en_unidad:
                par_oculto_actual = {num1, num2}
                cambio_local_par = False
                
                # Para las dos celdas que forman el par oculto
                for idx_celda_afectada_en_unidad in pos_num1_en_unidad:
                    celda_a_modificar_ref = celdas_unidad_refs[idx_celda_afectada_en_unidad]
                    # Si la celda contiene candidatos ADEMÁS del par oculto, eliminarlos
                    if not celda_a_modificar_ref.issubset(par_oculto_actual):
                        celda_a_modificar_ref.intersection_update(par_oculto_actual)
                        cambio_local_par = True
                        cambio_hecho_en_esta_unidad = True
                
                if cambio_local_par:
                    print(f"Par oculto {sorted(list(par_oculto_actual))} restringido en celdas de {nombre_unidad}.")
    return cambio_hecho_en_esta_unidad


def aplicar_pares_ocultos(tablero, candidatos):
    cambio_realizado = False
    # Filas
    for fila_idx in range(9):
        unidad_refs = [candidatos[fila_idx][col_idx] for col_idx in range(9)]
        if buscar_pares_ocultos_en_unidad(unidad_refs, f"Fila {fila_idx+1}", tablero, fila_idx, -1, candidatos):
            cambio_realizado = True
    # Columnas
    for col_idx in range(9):
        unidad_refs = [candidatos[fila_idx][col_idx] for fila_idx in range(9)]
        if buscar_pares_ocultos_en_unidad(unidad_refs, f"Columna {col_idx+1}", tablero, -1, col_idx, candidatos):
            cambio_realizado = True
    # Bloques
    for bloque_fila_start in range(0,9,3):
        for bloque_col_start in range(0,9,3):
            unidad_refs = []
            for r_offset in range(3):
                for c_offset in range(3):
                    unidad_refs.append(candidatos[bloque_fila_start+r_offset][bloque_col_start+c_offset])
            if buscar_pares_ocultos_en_unidad(unidad_refs, f"Bloque ({bloque_fila_start//3+1},{bloque_col_start//3+1})", tablero, bloque_fila_start, bloque_col_start, candidatos):
                cambio_realizado = True
    if cambio_realizado:
        imprimir_candidatos(candidatos, "Tras aplicar Pares Ocultos")
    return cambio_realizado

# --- Backtracking ---
def encontrar_celda_vacia(tablero):
    for r_idx in range(9):
        for c_idx in range(9):
            if tablero[r_idx][c_idx] == 0:
                return (r_idx, c_idx)
    return None

def es_valido_colocar(tablero, fila, col, num):
    for c_idx in range(9):
        if c_idx != col and tablero[fila][c_idx] == num:
            return False
    for r_idx in range(9):
        if r_idx != fila and tablero[r_idx][col] == num:
            return False
    start_row, start_col = 3 * (fila // 3), 3 * (col // 3)
    for r_loop in range(start_row, start_row + 3):
        for c_loop in range(start_col, start_col + 3):
            if (r_loop != fila or c_loop != col) and tablero[r_loop][c_loop] == num:
                return False
    return True

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

def resolver_sudoku_fuerza_bruta(tablero_previo_bt):
    tablero_copia = [fila[:] for fila in tablero_previo_bt]
    stats = {'iteraciones': 0, 'profundidad_actual': 0, 'retrocesos': 0, 'max_profundidad': 0}
    start_time = time.time()
    tiene_solucion = _resolver_sudoku_backtracking_recursivo(tablero_copia, stats)
    end_time = time.time()
    tiempo_tardado = end_time - start_time
    if tiene_solucion:
        return tablero_copia, stats['iteraciones'], stats['retrocesos'], stats['max_profundidad'], tiempo_tardado
    else:
        return None, stats['iteraciones'], stats['retrocesos'], stats['max_profundidad'], tiempo_tardado

# --- Main solver logic ---
def solve_sudoku_from_string(tablero_str):
    print(f"Resolviendo tablero: {tablero_str[:27]}...")
    if not all(c.isdigit() or c == '.' for c in tablero_str):
        print("Error: La cadena de entrada solo debe contener dígitos o '.'.")
        return
    if len(tablero_str) != 81:
        print("Error: La cadena de entrada debe tener exactamente 81 caracteres.")
        return

    tablero_str_fixed = tablero_str.replace('.', '0')
    tablero_leido = [[int(tablero_str_fixed[i*9 + j]) for j in range(9)] for i in range(9)]

    print("\\nTablero Inicial:")
    imprimir_tablero(tablero_leido)

    if not validar_tablero(tablero_leido):
        print("Error: El tablero introducido es inválido (números repetidos en fila, columna o bloque).")
        return

    tablero_actual = [fila[:] for fila in tablero_leido]
    candidatos = calcular_candidatos(tablero_actual)
    imprimir_candidatos(candidatos, "Inicializar candidatos")
    
    paso_iteracion_heuristica = 1
    max_iteraciones_heuristicas = 20 # Límite
    resuelto_e_impreso_por_heuristicas = False
    tablero_antes_de_bt_definitivo = [fila[:] for fila in tablero_actual]

    while paso_iteracion_heuristica <= max_iteraciones_heuristicas:
        cambio_en_iteracion = False
        print(f"\\n--- Iteración heurística {paso_iteracion_heuristica} ---")
        
        tablero_antes_de_bt_definitivo = [fila[:] for fila in tablero_actual]

        if aplicar_candidato_unico(tablero_actual, candidatos): cambio_en_iteracion = True
        if aplicar_singles_ocultos(tablero_actual, candidatos): cambio_en_iteracion = True
        
        # Solo probar más complejas si las anteriores no hicieron cambios, para eficiencia
        if not cambio_en_iteracion: 
            if aplicar_pares_desnudos(tablero_actual, candidatos): cambio_en_iteracion = True
        if not cambio_en_iteracion:
            if aplicar_conjuntos_desnudos(tablero_actual, candidatos, 3): cambio_en_iteracion = True 
        if not cambio_en_iteracion:
            if aplicar_conjuntos_desnudos(tablero_actual, candidatos, 4): cambio_en_iteracion = True 
        if not cambio_en_iteracion:
            if aplicar_pares_ocultos(tablero_actual, candidatos): cambio_en_iteracion = True
        
        resuelto_por_heuristica_en_iteracion = all(tablero_actual[r][c] != 0 for r in range(9) for c in range(9))
        if resuelto_por_heuristica_en_iteracion:
            print("\\n¡Sudoku Resuelto con técnicas heurísticas!")
            imprimir_tablero(tablero_actual)
            resuelto_e_impreso_por_heuristicas = True
            return 

        if not cambio_en_iteracion: # Si NINGUNA heurística hizo cambio en esta iteración
            print("\\nNo se encontraron más cambios con técnicas heurísticas en esta iteración.")
            break 
        
        paso_iteracion_heuristica += 1
    
    if paso_iteracion_heuristica > max_iteraciones_heuristicas and not resuelto_e_impreso_por_heuristicas:
         print("\\nLímite de iteraciones heurísticas alcanzado.")

    resuelto_final_heuristicas = all(tablero_actual[r][c] != 0 for r in range(9) for c in range(9))

    if not resuelto_final_heuristicas:
        print("\\nEl Sudoku no pudo ser resuelto completamente con técnicas heurísticas.")
        print("Estado del tablero antes de intentar backtracking (fuerza bruta):")
        imprimir_tablero(tablero_antes_de_bt_definitivo)
        
        print("\\n--- Iniciando backtracking (fuerza bruta)... ---")
        
        tablero_solucion_bt, iter_bt, retro_bt, prof_bt, tiempo_bt = resolver_sudoku_fuerza_bruta(tablero_antes_de_bt_definitivo)

        print(f"Proceso de Backtracking finalizado en {tiempo_bt:.4f} segundos.")
        print(f"  Iteraciones (llamadas recursivas): {iter_bt}")
        print(f"  Retrocesos: {retro_bt}")
        print(f"  Profundidad máxima alcanzada: {prof_bt}")

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
            print("El tablero mostrado es el estado tras las heurísticas (antes del intento de backtracking):")
            imprimir_tablero(tablero_antes_de_bt_definitivo)

    elif resuelto_final_heuristicas and not resuelto_e_impreso_por_heuristicas:
        print("\\n¡Sudoku Resuelto con técnicas heurísticas (verificado después del bucle)!")
        imprimir_tablero(tablero_actual)
`;


async function loadPyodideAndPackages() {
  // Importar Pyodide dinámicamente
  // Asegúrate de que Pyodide esté disponible en tu proyecto (npm install pyodide)
  // o a través de un CDN en tu config.js de VitePress
  const { loadPyodide } = await import('pyodide/pyodide.mjs');
  
  pyodide = await loadPyodide({
    // Opcional: Especifica la URL de los archivos de Pyodide si no están en la ruta por defecto
    // indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/" 
  });
  // Pyodide viene con la librería estándar de Python, time, collections, itertools están incluidas.
  // Si necesitaras paquetes externos, los cargarías aquí con pyodide.loadPackage(['numpy', 'pandas']);
  isLoadingPyodide.value = false;
  console.log('Pyodide cargado.');
}

onMounted(() => {
  // Solo cargar Pyodide en el cliente
  if (typeof window !== 'undefined') {
    loadPyodideAndPackages();
  }
});

onBeforeUnmount(() => {
  // Limpieza si es necesario, aunque Pyodide no tiene un método 'destroy' explícito.
  // Podrías querer cancelar ejecuciones en curso si las hubiera.
});

async function runSudokuSolver() {
  if (!pyodide || isExecuting.value) return;

  isExecuting.value = true;
  outputLog.value = 'Ejecutando script...\n';

  try {
    // Redirigir stdout y stderr de Python a nuestra variable outputLog
    pyodide.setStdout({
      batched: (msg) => { outputLog.value += msg + '\n'; }
    });
    pyodide.setStderr({
      batched: (msg) => { outputLog.value += `ERROR: ${msg}\n`; }
    });

    // Pasar la entrada del Sudoku a Python
    pyodide.globals.set('sudoku_board_string', sudokuInput.value);

    // Ejecutar el script
    await pyodide.runPythonAsync(`
${pythonCodeString}

# Llamar a la función principal con la cadena del tablero
solve_sudoku_from_string(sudoku_board_string)
    `);
    
  } catch (error) {
    console.error('Error ejecutando Python con Pyodide:', error);
    outputLog.value += `Error en Pyodide: ${error.message}\n`;
     if (error.type === "PythonError") {
        outputLog.value += `Traceback (Python):\n${pyodide.globals.get('sys').exc_info()[2]}\n`;
     }
  } finally {
    isExecuting.value = false;
    // Limpiar stdout/stderr para futuras ejecuciones o otros componentes
    pyodide.setStdout({}); 
    pyodide.setStderr({});
  }
}
</script>

<style scoped>
.sudoku-solver-container {
  background-color: var(--vp-code-block-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--vp-c-text-1);
}

.loading-pyodide {
  text-align: center;
  padding: 2rem;
  font-style: italic;
  color: var(--vp-c-text-2);
}

.solver-ui label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.solver-ui textarea {
  width: 100%;
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid var(--vp-c-divider);
  background-color: var(--vp-input-bg-color, var(--vp-c-bg-soft)); /* Usa variable de VitePress o fallback */
  color: var(--vp-c-text-1);
  font-family: var(--vp-font-family-mono);
  font-size: 0.875em;
  margin-bottom: 1rem;
  box-sizing: border-box;
  resize: vertical;
}

.solver-ui textarea:focus {
  border-color: var(--vp-c-brand-1);
  outline: none;
  box-shadow: 0 0 0 2px var(--vp-c-brand-soft);
}

.run-button, .toggle-code-button {
  /* Estilo de botón de VitePress */
  display: inline-block;
  border: 1px solid transparent;
  text-align: center;
  font-weight: 600;
  white-space: nowrap;
  transition: color .25s,border-color .25s,background-color .25s;
  border-radius: 20px;
  padding: 0 20px;
  line-height: 38px;
  font-size: 14px;
  
  border-color: var(--vp-button-brand-border);
  color: var(--vp-button-brand-text);
  background-color: var(--vp-button-brand-bg);
  margin-bottom: 1rem;
}

.run-button:hover, .toggle-code-button:hover {
  border-color: var(--vp-button-brand-hover-border);
  color: var(--vp-button-brand-hover-text);
  background-color: var(--vp-button-brand-hover-bg);
}

.run-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: var(--vp-c-gray-soft);
  border-color: var(--vp-c-gray-soft);
  color: var(--vp-c-text-3);
}

.output-section {
  margin-top: 1.5rem;
}

.output-section h3 {
  margin-bottom: 0.75rem;
  font-size: 1.1em;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.output-log {
  background-color: var(--vp-c-bg-mute); /* Un fondo ligeramente diferente para el log */
  padding: 1rem;
  border-radius: 6px;
  max-height: 400px;
  overflow-y: auto;
  font-family: var(--vp-font-family-mono);
  font-size: 0.85em;
  white-space: pre-wrap; /* Para que los saltos de línea funcionen */
  word-wrap: break-word;
  color: var(--vp-c-text-2);
  border: 1px solid var(--vp-c-divider);
}

.code-display-section {
  margin-top: 1.5rem;
}

.toggle-code-button {
   background-color: var(--vp-button-alt-bg);
   color: var(--vp-button-alt-text);
   border-color: var(--vp-button-alt-border);
}
.toggle-code-button:hover {
   background-color: var(--vp-button-alt-hover-bg);
   color: var(--vp-button-alt-hover-text);
   border-color: var(--vp-button-alt-hover-border);
}

.code-block-container {
  margin-top: 0.5rem;
  /* Similar a los bloques de código de VitePress */
  background-color: var(--vp-code-block-bg); /* Ya está en el contenedor principal, pero puede ser específico */
  border-radius: 6px;
  overflow-x: auto; /* Para scroll horizontal si el código es muy ancho */
}
.code-block-container pre {
  padding: 1em;
  margin: 0;
  overflow-x: auto; /* Necesario para que <pre> maneje el scroll si <code> es más ancho */
}
.code-block-container code {
  font-family: var(--vp-font-family-mono);
  font-size: 0.875em;
  color: var(--vp-code-inline-color, var(--vp-c-text-1)); /* Color del texto del código */
  /* VitePress usa Shiki para el resaltado, esto será texto plano pero con el estilo base */
  white-space: pre; /* Importante para mantener el formato del código */
}
</style>
