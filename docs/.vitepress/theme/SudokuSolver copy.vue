<script setup lang="ts">
import { ref, onMounted } from 'vue'

// Referencia para la instancia de Pyodide
const pyodide = ref<any>(null)
const isLoadingPyodide = ref(true)
const isExecuting = ref(false)
const output = ref<string[]>([])
const errorOutput = ref<string>('')

const sudokuInputType = ref<'filas' | 'cadena'>('cadena') // 'filas' o 'cadena'
const sudokuFilas = ref(Array(9).fill('')) // Para entrada por filas
const sudokuCadena = ref('003020600900305001001806400008102900700000008006708200002609500800203009005010300') // Ejemplo

// El código Python completo
const pythonCode = ref(`
import time
from collections import defaultdict
from itertools import combinations

# --- COMIENZO DEL CÓDIGO PYTHON DEL USUARIO ---
# (Aquí pegarás TODO tu script Python, desde def leer_tablero() hasta if __name__ == "__main__":)
# PERO CON MODIFICACIONES para input() y print(), y para llamar a main() directamente.

# ... (Python code will be pasted here later, modified) ...

# --- FIN DEL CÓDIGO PYTHON DEL USUARIO ---
`)

// Función para cargar Pyodide
async function loadPyodideInstance() {
  try {
    // @ts-ignore (para evitar error de tipo con window.loadPyodide)
    const pyodideInstance = await window.loadPyodide({
      // Opcional: especificar paquetes a cargar inicialmente
      // indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/"
    });
    // Hacer que las funciones print de Python llamen a addToOutput
    pyodideInstance.globals.set('print_to_js', addToOutput);
    pyodideInstance.runPython(`
      import sys
      import io
      sys.stdout = io.StringIO() # Redirigir stdout
      sys.stderr = io.StringIO() # Redirigir stderr
      
      # Sobrescribir print para que llame a la función JS
      def custom_print(*args, **kwargs):
        output_str = io.StringIO()
        _print_builtin(*args, **kwargs, file=output_str)
        print_to_js(output_str.getvalue())
        output_str.close()

      _print_builtin = print # Guardar el print original
      __builtins__.print = custom_print
    `);
    pyodide.value = pyodideInstance;
    isLoadingPyodide.value = false;
    addToOutput("Pyodide cargado y listo.");
  } catch (error) {
    console.error("Error cargando Pyodide:", error);
    errorOutput.value = `Error cargando Pyodide: ${error}`;
    isLoadingPyodide.value = false;
  }
}

// Llamar a loadPyodideInstance cuando el componente se monte
onMounted(() => {
  // Asegurarse de que loadPyodide está disponible (puede tardar un poco después de que el script del head cargue)
  const checkInterval = setInterval(() => {
    // @ts-ignore
    if (window.loadPyodide) {
      clearInterval(checkInterval);
      loadPyodideInstance();
    }
  }, 100);
});

// Función para añadir mensajes al output
function addToOutput(message: string) {
  // Python print() a menudo incluye un \n al final, StringIO puede capturarlo.
  // Si el mensaje ya tiene un \n, no añadimos otro.
  // Si no, y no es una línea vacía, puede que queramos añadirlo para separar prints.
  // Esto es un poco heurístico.
  output.value.push(message.endsWith('\n') ? message.slice(0, -1) : message);
}

function clearOutput() {
  output.value = [];
  errorOutput.value = '';
}

// Función para ejecutar el código Python
async function executePython() {
  if (!pyodide.value || isExecuting.value) return;

  isExecuting.value = true;
  clearOutput();
  addToOutput("Ejecutando Sudoku solver...");

  let boardStringForPython = "";
  if (sudokuInputType.value === 'cadena') {
    if (sudokuCadena.value.length !== 81) {
      errorOutput.value = "La cadena del Sudoku debe tener 81 caracteres.";
      isExecuting.value = false;
      return;
    }
    boardStringForPython = sudokuCadena.value.replace(/\./g, '0'); // Reemplazar puntos por ceros si los hay
  } else { // 'filas'
    const tempFilas = sudokuFilas.value.map(f => f.trim());
    if (tempFilas.some(f => f.length !== 9 || !/^[0-9.]+$/.test(f))) {
      errorOutput.value = "Cada fila debe tener 9 dígitos (0-9 o '.').";
      isExecuting.value = false;
      return;
    }
    boardStringForPython = tempFilas.join('').replace(/\./g, '0');
  }

  // Modificar el código Python para inyectar el tablero y automatizar "confirmaciones"
  // Esto es CRUCIAL. No podemos usar input() de Python directamente.
  const modifiedPythonCode = `
# --- CÓDIGO MODIFICADO PARA PYODIDE ---
${pythonCode.value}

# --- EJECUCIÓN CONTROLADA ---
# Simular la entrada del tablero y las confirmaciones
simulated_sudoku_string = "${boardStringForPython}"

# Modificar leer_tablero para usar la cadena simulada
def leer_tablero_modificado():
    print("Usando tablero predefinido para Pyodide:")
    # Convertir la cadena en un tablero 9x9
    tablero = [ [int(simulated_sudoku_string[i*9 + j]) for j in range(9)] for i in range(9)]
    imprimir_tablero(tablero) # Mostrar el tablero inicial
    
    # Validar el tablero introducido
    if not validar_tablero(tablero):
        print("ERROR: El tablero introducido es inválido según las reglas del Sudoku.")
        # Podríamos devolver None o lanzar una excepción para detener la ejecución
        raise ValueError("Tablero inválido") # O return None y manejarlo en main_modificado
    return tablero

# Modificar pedir_confirmacion para que siempre devuelva True
def pedir_confirmacion_modificado(mensaje):
    print(f"Confirmación automática (Pyodide): {mensaje} -> Sí")
    return True

# Reemplazar las funciones originales en el ámbito global del script
# Esto es un poco hacky, pero funciona para este contexto.
# Una mejor forma sería pasar estas funciones como dependencias.
__main_globals = globals()
__main_globals['leer_tablero'] = leer_tablero_modificado
__main_globals['pedir_confirmacion'] = pedir_confirmacion_modificado


# Modificar main para no tener el bucle de menú y llamar directamente a la lógica de resolución
def main_modificado():
    tablero_leido = leer_tablero_modificado()
    if tablero_leido is None: # Si leer_tablero_modificado puede devolver None en error
        print("No se pudo leer o validar el tablero.")
        return

    tablero_actual = [fila[:] for fila in tablero_leido] 
    
    # Guardar una copia del tablero tal como fue introducido (o tras heurísticas iniciales si se quiere)
    # Esto es para la estadística de 'celdas llenadas por BT'
    # y para mostrar el tablero pre-BT si BT falla.
    tablero_antes_de_bt_definitivo = [fila[:] for fila in tablero_actual]


    candidatos = calcular_candidatos(tablero_actual)
    imprimir_candidatos(candidatos, "Inicializar candidatos")
    
    paso_iteracion_heuristica = 1
    max_iteraciones_heuristicas = 20 # Límite para heurísticas
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
        
        resuelto_por_heuristica_en_iteracion = all(tablero_actual[r][c] != 0 for r in range(9) for c in range(9))
        if resuelto_por_heuristica_en_iteracion:
            print("\\n¡Sudoku Resuelto con técnicas heurísticas!")
            imprimir_tablero(tablero_actual)
            resuelto_e_impreso_por_heuristicas = True 
            return 

        if not cambio_en_iteracion:
            print("\\nNo se encontraron más cambios con técnicas heurísticas en esta iteración.")
            tablero_antes_de_bt_definitivo = [fila[:] for fila in tablero_actual]
            break 
        
        paso_iteracion_heuristica += 1
        if paso_iteracion_heuristica > max_iteraciones_heuristicas:
            print("\\nLímite de iteraciones heurísticas alcanzado.")
            tablero_antes_de_bt_definitivo = [fila[:] for fila in tablero_actual]
            break
    
    if 'tablero_antes_de_bt_definitivo' not in locals() or paso_iteracion_heuristica == 1: # Si salió muy rápido o no entró al bucle
         tablero_antes_de_bt_definitivo = [fila[:] for fila in tablero_actual]


    resuelto_final_heuristicas = all(tablero_actual[r][c] != 0 for r in range(9) for c in range(9))

    if not resuelto_final_heuristicas:
        print("\\nEl Sudoku no pudo ser resuelto completamente con técnicas heurísticas.")
        print("Estado del tablero antes de intentar backtracking (fuerza bruta):")
        imprimir_tablero(tablero_antes_de_bt_definitivo)
        
        print("\\nIniciando backtracking (fuerza bruta)...")
        
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

# Llamar a la función principal modificada
try:
    main_modificado()
except ValueError as e: # Capturar el ValueError de tablero inválido
    print(f"ERROR DURANTE LA EJECUCIÓN: {e}")
except Exception as e:
    print(f"OTRO ERROR INESPERADO: {e}")

# Capturar cualquier cosa que haya quedado en stdout/stderr de Python
# (aunque nuestro custom_print ya debería haberlo hecho)
py_stdout = sys.stdout.getvalue()
py_stderr = sys.stderr.getvalue()
if py_stdout:
  print_to_js("--- Python stdout residual ---\\n" + py_stdout)
if py_stderr:
  print_to_js("--- Python stderr residual ---\\n" + py_stderr)

  `; // Fin de modifiedPythonCode

  try {
    // Reiniciar stdout/stderr de Pyodide para cada ejecución
    pyodide.value.runPython(`
      import sys
      import io
      sys.stdout = io.StringIO()
      sys.stderr = io.StringIO()
      __builtins__.print = custom_print # Asegurarse que nuestro print sigue activo
    `);

    await pyodide.value.runPythonAsync(modifiedPythonCode);
    
    // Capturar stdout/stderr después de la ejecución (si nuestro print_to_js falló o algo se imprimió de otra forma)
    const finalPyStdout = pyodide.value.runPython("sys.stdout.getvalue()");
    const finalPyStderr = pyodide.value.runPython("sys.stderr.getvalue()");
    if (finalPyStdout) {
        addToOutput("--- Python stdout (final) ---\n" + finalPyStdout);
    }
    if (finalPyStderr) {
        errorOutput.value += "--- Python stderr (final) ---\n" + finalPyStderr;
    }

  } catch (e: any) {
    console.error("Error ejecutando Python:", e);
    errorOutput.value += `Error durante la ejecución de Python: ${e.message}\n`;
    // Intentar obtener el traceback de Python si está disponible
    if (pyodide.value) {
      try {
        const traceback = pyodide.value.runPython(`
          import traceback
          traceback.format_exc()
        `);
        errorOutput.value += `\nPython Traceback:\n${traceback}`;
      } catch (tbError) {
        console.error("Error obteniendo traceback:", tbError);
      }
    }
  } finally {
    isExecuting.value = false;
  }
}
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
        <pre class_output_text v-for="(line, index) in output" :key="index" v-html="line.replace(/ /g, '&nbsp;')"></pre>
      </div>
    </div>

    <details class="code-details">
      <summary>Ver/Ocultar Código Python</summary>
      <div class="language-python extra-class"> <!-- Para que VitePress aplique su resaltado si lo tiene -->
        <pre class="language-python"><code v-text="pythonCode"></code></pre>
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
  box-sizing: border-box; /* Para que padding no aumente el width */
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
  border-radius: 20px; /* Vitepress button style */
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
.clear-button {
  background-color: var(--vp-c-gray-1); /* Un color más sutil */
  color: var(--vp-c-text-1);
  margin-left: auto; /* Empujar a la derecha si está en un flex container */
  display: block; /* o inline-block */
  margin-bottom: 0.5em;
}
.clear-button:hover {
  background-color: var(--vp-c-gray-2);
}

.output-section pre {
  background-color: var(--vp-code-block-bg);
  padding: 1em;
  border-radius: 6px;
  overflow-x: auto;
  white-space: pre-wrap; /* Para que las líneas largas del output se ajusten */
  word-wrap: break-word; /* Para romper palabras largas si es necesario */
  color: var(--vp-code-block-color);
  font-family: var(--vp-font-family-mono);
  font-size: 0.875em; /* default pre font-size */
  line-height: 1.7; /* default pre line-height */
}
.output-section .error-output {
  color: var(--vp-c-red-1);
  border: 1px solid var(--vp-c-red-dimm-1);
  background-color: var(--vp-c-red-soft);
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
  border-radius: 8px 8px 0 0; /* Redondear esquinas superiores */
}
.code-details[open] summary {
    border-bottom: 1px solid var(--vp-c-divider);
}
.code-details div.language-python {
  /* VitePress normalmente aplica estilos a .language-python dentro de .vp-doc pre
     Podemos intentar replicar o usar las variables de VitePress para el fondo del código */
  background-color: var(--vp-code-block-bg); /* Usa la variable de VitePress */
  border-radius: 0 0 8px 8px; /* Redondear esquinas inferiores */
}
.code-details pre {
  margin: 0 !important; /* Anular márgenes de <pre> si los hay por defecto */
  border-radius: 0 0 6px 6px !important; /* Para que no se salga del details */
}
/* Para que el texto dentro del code block también use el color de VitePress */
.code-details code {
    color: var(--vp-code-block-color);
}
</style>