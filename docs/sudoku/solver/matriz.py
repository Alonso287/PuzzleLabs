filas = int(input("filas: "))
columnas = int(input("columnas: "))

matrix = [] 
print("Datos por filas:")

for i in range(filas):   
    fila = []
    for j in range(columnas):
        fila.append(int(input()))    # user input for rows
    matrix.append(fila)  # adding rows to the matrix

print("\nLa matriz es:")

for i in range(filas):
    for j in range(columnas):
        print(matrix[i][j], end=" ")
    print()
    