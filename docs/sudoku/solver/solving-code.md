# Práctica: Programación de un algoritmo de creación de sudokus<Badge type="warning" text="Trabajo en progreso" />
Ahora que ya hemos investigado en profundidad el funcionamiento de nuestro algoritmo de resolución, tenemos que trasladarlo a código.

___

El código se dividirá en diferentes funciones o módulos, uno para cada algoritmo o característica del programa.

# 1. Introducción y almacenamiento de datos
Empezaremos por la primera función, que llamaremos `leer_tablero()`:
Se encargará de recibir cadenas de texto en un formato específico, que luego "traduciremos" y almacenaremos como una matriz 2D:
Utilizaremos dos métodos diferentes, según la ocasión:


## Por filas
El programa recibirá el sudoku en forma de 9 cadenas con 9 dígitos cada una, con "0" para las celdas vacías.
```python
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
```
La parte fundamental está dentro del bucle `for i in range(9):`:recibe una cadena de 9