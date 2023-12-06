#intertools para generar las combinaciones de los canales
from itertools import product
#pandas para leer el archivo excel
import pandas as pd

#Realizado por Daniel Felipe Carreño 

#Funcion para ingresar los Canales y que sean binarios
def ingresarCanales():
    # Crear un diccionario vacío para almacenar los arreglos
    listaarreglos = {}
    numeroCanales = int(input("Ingrese cuántos Canales quiere: "))
    
    # Solicita al usuario cuántos datos quiere en los Canales (una vez, y se aplica a todos los canales)
    valor = int(input("Ingrese cuántos datos quiere en los Canales: "))

    # Ciclo para pedir los datos de cada Canal y asignarle un numero
    for i in range(1, numeroCanales + 1):
        # Crea una lista vacía para guardar los datos
        nuevoarreglo = []
        # Solicita al usuario los datos y los agrega a la lista
        for _ in range(valor):
            binario = None
            # Ciclo para validar que el usuario ingrese un número binario
            while binario not in (0, 1):
                try:
                    binario = int(input(f"Ingrese el valor binario para el Canal {i}: "))
                    if binario not in (0, 1):
                        print("El valor ingresado no es binario.")
                    else:
                        nuevoarreglo.append(binario)
                except ValueError:
                    print("El valor ingresado no es un número.")
        # Agrega el arreglo a la lista de arreglos
        listaarreglos[i] = nuevoarreglo
        # Muestra el arreglo ingresado
        print(f"Canal {i}: {nuevoarreglo}")
    
    return listaarreglos


# Función para mostrar los Canales ingresados
def MostrarCanales(listaarreglos):
    print("\nLos Canales ingresados son: ")
    for numero, arreglo in listaarreglos.items():
        #le asigna un numero a cada canal
        print(f"Canal {numero}: {arreglo}")

# Función para contar los números binarios en los arreglos
def ContarBinarios(listaarreglos):
    # Solicitar al usuario los números de los arreglos
    NuevoCanal = input("Ingrese los números de los Canales separados por comas (ejemplo: 1, 2): ").split(",")

    # Convertir la entrada a una lista de enteros
    try:
        NuevoCanal = [int(numero.strip()) for numero in NuevoCanal]
    except ValueError:
        print("Ingresó un valor no numérico. Por favor, intente de nuevo.")
        return

    # Verificar la existencia de los arreglos
    CanalNoEncontrado = [numero for numero in NuevoCanal if numero not in listaarreglos]
    if CanalNoEncontrado:
        print(f"No se encontraron los siguientes Canales: {', '.join(map(str, CanalNoEncontrado))}")
        return

    # Si todos los arreglos existen, pedir el número binario a buscar
    binarioAcontar = int(input("Ingrese el valor binario que quiere contar (1 o 0): "))
    while binarioAcontar not in [0, 1]:
        print("Valor inválido. Intente de nuevo.")
        binarioAcontar = int(input("Ingrese el valor binario que quiere contar (1 o 0): "))

    # Contar y mostrar los resultados
    for numero in NuevoCanal:
        conteo = listaarreglos[numero].count(binarioAcontar)
        print(f"El Canal {numero} tiene {conteo} datos del número {binarioAcontar}.")

def CargarArchivo():
    listaarreglos = {}

    # Pedir el nombre del archivo al usuario
    NombreArchivo = input("Ingrese el nombre del archivo desde donde cargar los Canales: ")
    # Abrir el archivo en modo lectura
    try:
        with open(NombreArchivo, 'r') as archivo:
            lineas = archivo.readlines()
            # Iterar sobre las líneas del archivo
            for linea in lineas:
                datos = [int(dato.strip()) for dato in linea.split(",")]

                # Validar si todos los elementos son binarios
                if not all(d in [0, 1] for d in datos):
                    print(f"La línea '{linea.strip()}' tiene datos no binarios. Porfavor correguir.")
                    return {}  # Retornamos un diccionario vacío en caso de error

                listaarreglos[len(listaarreglos) + 1] = datos

            print(f"Se han cargado {len(lineas)} Canales desde el archivo {NombreArchivo}")
    # Manejo de excepciones error de archivo no encontrado
    except FileNotFoundError:
        print(f"No se pudo encontrar el archivo {NombreArchivo}.")
    # Manejo de excepciones error de datos no numéricos
    except ValueError:
        print("El archivo contiene datos no válidos o no numéricos.")

    return listaarreglos

def generarMatrizCanalFuturo(*canales):
    # Definir todos los posibles estados que pueden tener los canales.
    estados = [''.join(map(str, comb)) for comb in product([0, 1], repeat=len(canales))]
    
    # Inicializar el diccionario de transiciones.
    transiciones = {estado: [0] + [0]*len(canales) for estado in estados}
    
    # Recorrer los canales para llenar las transiciones.
    for i in range(len(canales[0]) - 1):
        estado_actual = ''.join([str(canal[i]) for canal in canales])
        transiciones[estado_actual][0] += 1
        for j, canal in enumerate(canales, start=1):
            transiciones[estado_actual][j] += canal[i+1]
    
    # Mostrar la matriz de transiciones.
    headers = ' '.join([f"{i:<5}" for i in range(1, len(canales) + 1)])
    print(f"{' '*5}{headers}")
    for estado in estados:
        conteo_total = transiciones[estado][0]
        if conteo_total == 0:
            probabilidades = ['{:<5}'.format('0.0') for _ in canales]
        else:
            probabilidades = [f"{transiciones[estado][j]/conteo_total:<5.2f}" for j in range(1, len(canales) + 1)]
        print(f"{estado} {' '.join(probabilidades)}")


matriz_global = []

def generarEstados(listaarreglos):
    global matriz_global

    # Convertir el diccionario a una lista de canales
    canales = list(listaarreglos.values())

    # Asegurarse de que al menos hay canales ingresados
    if not canales:
        print("No se han ingresado canales. Por favor, añada algunos canales primero.")
        return

    # Generar matriz
    estados = [''.join(map(str, comb)) for comb in product([0, 1], repeat=len(canales))]
    #matriz para guardar las probabilidades
    matriz = [[0.0 for _ in range(len(estados))] for _ in range(len(estados))]
    #For para recorrer los estados y mostrar las probabilidades
    for idx, estado in enumerate(estados):
        #count para contar los estados
        count = sum([1 for i in range(1, len(canales[0])) if 
                     # Iniciamos desde 1, porque miramos atrás
                     all([canal[i] == int(bit) for canal, bit in zip(canales, estado)])])
        #If para validar si el conteo total es 0
        if count == 0:
            continue
        #For para recorrer los estados y mostrar las probabilidades
        for j, prev_estado in enumerate(estados):
            #con esto se cuentan las ocurrencias
            occurrences = sum([1 for i in range(1, len(canales[0])) if 
                               # Iniciamos desde 1, porque miramos atrás
                               all([canal[i] == int(estado[k]) for k, canal in enumerate(canales)]) and 
                               # enumerate nos da el índice y el valor
                               all([canal[i-1] == int(prev_estado[k]) for k, canal in enumerate(canales)])])
            #matriz para guardar las probabilidades
            matriz[idx][j] = round(float(occurrences) / count, 2)

    # Mostrar la matriz original
    print("\nMatriz Original:")
    encabezado = " " * len(estados[0]) + " "
    for estado in estados:
        encabezado += "{:^7}".format(estado)
    print(encabezado)
    for i, estado_row in enumerate(estados):
        fila = estado_row + " "
        for j, estado_col in enumerate(estados):
            valor = matriz[i][j]
            fila += "{:^7.2f}".format(valor)
        print(fila)

    # Obtener lista de estados actuales (filas)
    estados_actuales = estados.copy()

    while True:
        valor1 = input("\nEscriba los números de los canales futuros separados por comas (ejemplo: 1, 2, 3): ")
        valor2 = input("\nEscriba los números de los canales actuales separados por comas (ejemplo: 1, 2, 3): ")

        # Validar que los canales sean números y estén en el rango adecuado
        valor1 = [int(canal) for canal in valor1.split(',') if canal.strip().isdigit()]
        valor2 = [int(canal) for canal in valor2.split(',') if canal.strip().isdigit()]

        if not valor1 or not valor2:
            print("Por favor, ingrese números de canal válidos.")
        elif any(canal < 1 or canal > len(canales[0]) for canal in valor1 + valor2):
            print("Por favor, ingrese números de canal que estén en la matriz.")
        else:
            break
    print("\nLos canales escogidos fueron el canal futuro", valor1, "/", valor2, "Los canales escogidos fueron el canal actual")

    while True:
        print("\nEscoja de los estados actuales que se muestran a continuación, el estado actual que desea:")

        # Filtrar y mostrar solo los estados que corresponden a la cantidad de canales seleccionados
        estados_seleccionados = [''.join(estado[i - 1] for i in valor2) for estado in estados_actuales]

        print(estados_seleccionados)

        Actual = input("\nEscriba el estado actual (ejemplo: 0000, 0001, 0010, ...): ")

        # Validar que los bits en el estado actual sean coherentes con los canales seleccionados
        for i, bit in enumerate(Actual):
            canal_actual = canales[valor2[i] - 1]
            if bit not in "01" or (canal_actual == 1 and bit == "0"):
                print("El estado actual no es coherente con los canales seleccionados o la longitud no es correcta.")
                break
        else:
            print(f"El estado actual escogido fue: {Actual}")
            break
    if set(valor2).issubset(set(valor1)) and set(valor1).issuperset(set(valor2)):
        # Obtener la fila de la matriz correspondiente al estado actual
        fila_matriz = matriz[estados.index(Actual)]

        # Imprimir solo la parte de la fila correspondiente al estado actual
        print("\nFila de la matriz para el estado actual:")
        for valor in fila_matriz:
            print(f"{valor:.2f}", end="   ")
    else:
        # Eliminar el primer canal actual
        canal_actual_eliminar = valor2[0]
        valor2.remove(canal_actual_eliminar)

        # Inicializar la fila modificada con ceros
        fila_modificada = [0] * len(canales)

        # Iterar sobre los canales restantes y sumar las columnas iguales dividido por 2
        for canal_actual in valor2:
            # Sumar los valores de la columna correspondiente al canal actual
            for i in range(len(canales)):
                # Cambiar la línea siguiente para trabajar con números
                fila_modificada[i] += matriz[estados.index(Actual)][canal_actual - 1] / 2

        # Imprimir la fila modificada
        print("\nFila modificada de la matriz después de sumar y dividir por 2 los valores de los canales actuales:")
        for valor in fila_modificada:
            #print para mostrar los valores de la fila modificada
            print(f"{valor:.2f}", end="   ")



def generarEstadosEstados(listaarreglos):
    # Convertir el diccionario a una lista de canales
    canales = list(listaarreglos.values())
    
    # Asegurarse de que al menos hay canales ingresados
    if not canales:
        print("No se han ingresado canales. Por favor, añada algunos canales primero.")
        return

    # Generar matriz
    estados = [''.join(map(str, comb)) for comb in product([0, 1], repeat=len(canales))]
    #matriz para guardar las probabilidades
    matriz = [[0.0 for _ in range(len(estados))] for _ in range(len(estados))]
    #For para recorrer los estados y mostrar las probabilidades
    for idx, estado in enumerate(estados):
        count = sum([1 for i in range(1, len(canales[0])) if  # Iniciamos desde 1, porque miramos atrás
                     all([canal[i] == int(bit) for canal, bit in zip(canales, estado)])])
        #If para validar si el conteo total es 0
        if count == 0:
            continue
        #For para recorrer los estados y mostrar las probabilidades
        for j, prev_estado in enumerate(estados):  # Ahora estamos buscando el estado anterior, así que lo llamamos prev_estado
            occurrences = sum([1 for i in range(1, len(canales[0])) if  # Iniciamos desde 1, porque miramos atrás
                               all([canal[i] == int(estado[k]) for k, canal in enumerate(canales)]) and # enumerate nos da el índice y el valor
                               all([canal[i-1] == int(prev_estado[k]) for k, canal in enumerate(canales)])])
            matriz[idx][j] = round(float(occurrences) / count, 2)#Redondeamos el valor de las probabilidades

    # Mostrar matriz
    encabezado = " " * len(estados[0]) + " "
    #For para recorrer los estados y mostrar las probabilidades
    for estado in estados:
        #For para recorrer los estados y mostrar las probabilidades
        encabezado += "{:^7}".format(estado)
    print(encabezado)
    for i, estado_row in enumerate(estados):
        fila = estado_row + " "
        for j, estado_col in enumerate(estados):
            valor = matriz[i][j]
            fila += "{:^7.2f}".format(valor)
        print(fila)


#Funcion para leer el archivo excel y cargar los canales en el diccionario
def CargarExcel(file_path, listaarreglos):
    # Leer el archivo
    df = pd.read_excel(file_path)

    # Función para procesar el nombre de una columna 
    def Eliminar(columnA):
        if '.' in str(columnA):
            parts = str(columnA).split('.')
            return parts[0]
        return columnA

    # Procesar los nombres de las columnas
    df.columns = [Eliminar(col) for col in df.columns]

    # Convertir el excel en una matriz
    Matrix = df.values.tolist()

    # Asignar cada columna de la matriz como un canal en el diccionario
    for column in Matrix:
        canalnumero = len(listaarreglos) + 1  # El número del canal es el siguiente número disponible
        listaarreglos[canalnumero] = column

    return listaarreglos  # Devolver el diccionario actualizado

def MatrizGlobal():
    global matriz_global
    print("Matriz de las probabilidades de los estados en canales:")
    for fila in matriz_global:
        print(fila)
#  I am not your enemy, I am the ENEMY 