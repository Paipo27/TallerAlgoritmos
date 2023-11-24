#collections para crear diccionarios
from collections import defaultdict
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

    # Ciclo para pedir los datos de cada Canal
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

def generarMatriz(*canales):
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
    matriz = [[0.0 for _ in range(len(estados))] for _ in range(len(estados))]

    for idx, estado in enumerate(estados):
        count = sum([1 for i in range(1, len(canales[0])) if 
                     all([canal[i] == int(bit) for canal, bit in zip(canales, estado)])])
        if count == 0:
            continue
        for j, prev_estado in enumerate(estados):
            occurrences = sum([1 for i in range(1, len(canales[0])) if 
                               all([canal[i] == int(estado[k]) for k, canal in enumerate(canales)]) and 
                               all([canal[i-1] == int(prev_estado[k]) for k, canal in enumerate(canales)])])
            matriz[idx][j] = round(float(occurrences) / count, 2)
            

    # Mostrar matriz
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

    # Obtener lista de estados futuros (columnas)
    estados_futuros = estados.copy()

    # Mostrar las listas
    print("\nLista de Estados Actuales:")
    print(estados_actuales)

    print("\nLista de Estados Futuros:")
    print(estados_futuros)

    # Solicitar al usuario el estado actual y el estado futuro un while true para validar que el estado ingresado sea valido
    while True:
        estado_actual = input("Ingrese el estado actual que desea seleccionar dependiendo de la cantidad de canales existentes (por ejemplo, 01, 101): ")
        if all(bit in '01' for bit in estado_actual) and estado_actual in estados:
            break
        else:
            print("Estado inválido. Asegúrese de ingresar un estado válido que contenga solo 0s y 1s y que exista en la lista de estados.")

    while True:
        estado_futuro = input("Ingrese el estado futuro que desea seleccionar dependiendo de la cantidad de canales existentes (por ejemplo, 01, 101): ")
        if all(bit in '01' for bit in estado_futuro) and estado_futuro in estados:
            break
        else:
            print("Estado inválido. Asegúrese de ingresar un estado válido que contenga solo 0s y 1s y que exista en la lista de estados.")

    print(f"\nHa seleccionado el estado actual: {estado_actual}")
    print(f"El estado futuro es: {estado_futuro}")

     # Obtener la matriz de probabilidades para el estado actual y futuro seleccionados
    if estado_actual == estado_futuro:
        # Imprimir los números de las columnas para el estado seleccionado
        indices_columnas = [i for i, estado in enumerate(estados_actuales) if estado == estado_actual]
        #asignar los datos a una matriz global para ser impresas en otra funcion
        matriz_global=[matriz[i]for i in indices_columnas]
    else:  
        estado_futuro_modificado = estado_futuro[1:]

        # Actualizar la lista de estados futuros después de la modificación
        estados_futuros_modificados = [estado[1:] for estado in estados_futuros]

        # Verificar si el estado futuro modificado está en la lista actualizada
        if estado_futuro_modificado not in estados_futuros_modificados:
            print(f"\nError: El estado futuro modificado '{estado_futuro_modificado}' no está en la lista de estados futuros.")
            return

        # Obtener el índice correspondiente al estado futuro modificado
        indice_columna_futuro = estados_futuros_modificados.index(estado_futuro_modificado)

        # Sumar las filas con estados futuros iguales y obtener la columna resultante del estado futuro
        matriz_resultante_futuro = [sum(fila[idx] for fila in matriz if fila[1:] == fila_futuro) for idx, fila_futuro in enumerate(matriz)]

        # Almacenar la columna resultante del estado futuro
        matriz_global_columna_actual = matriz_resultante_futuro

        # Mostrar la columna resultante del estado actual después de las sumas
        print("\nColumna Resultante del Estado Actual Después de las Sumas:")
        for valor in matriz_global_columna_actual:
            print(f"{valor:.2f}", end=" ")  # Mostrar en horizontal           

def generrEstadoCanalIP(*canales):
    # Definir todos los posibles estados que pueden tener los canales.
    estados = [''.join(map(str, comb)) for comb in product([0, 1], repeat=len(canales))]
    
    # Inicializar el diccionario de transiciones.
    transiciones = {estado: [0] + [0]*len(canales) for estado in estados}
    
    # Recorrer los canales para llenar las transiciones.
    for i in range(1, len(canales[0])):
        estado_actual = ''.join(map(str, [canal[i] for canal in canales]))
        
        # Líneas de diagnóstico
        if estado_actual not in transiciones:
            print(f"Error: '{estado_actual}' no está en las claves de 'transiciones'.")
            print(f"Canales: {canales}")
            return
        # Fin de líneas de diagnóstico
        transiciones[estado_actual][0] += 1
        for j, canal in enumerate(canales, start=1):
            transiciones[estado_actual][j] += canal[i-1]
    
    # Mostrar la matriz de transiciones.
    headers = ' '.join([f"{i:<5}" for i in range(1, len(canales) + 1)])
    print(f"{' '*5}{headers}")
    #For para recorrer los estados y mostrar las probabilidades
    for estado in estados:
        conteo_total = transiciones[estado][0]
        #If para validar si el conteo total es 0
        if conteo_total == 0:
            probabilidades = ['{:<5}'.format('0.0') for _ in canales]
        else:
            probabilidades = [f"{transiciones[estado][j]/conteo_total:<5.2f}" for j in range(1, len(canales) + 1)]
        print(f"{estado} {' '.join(probabilidades)}")

#matriz global para guardar la matriz de estados
matriz_global = []

def generarEstadosEstados(listaarreglos):
    # Convertir el diccionario a una lista de canales
    canales = list(listaarreglos.values())
    
    # Asegurarse de que al menos hay canales ingresados
    if not canales:
        print("No se han ingresado canales. Por favor, añada algunos canales primero.")
        return

    # Generar matriz
    estados = [''.join(map(str, comb)) for comb in product([0, 1], repeat=len(canales))]
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
                               all([canal[i] == int(estado[k]) for k, canal in enumerate(canales)]) and 
                               all([canal[i-1] == int(prev_estado[k]) for k, canal in enumerate(canales)])])
            matriz[idx][j] = round(float(occurrences) / count, 2)

    # Mostrar matriz
    encabezado = " " * len(estados[0]) + " "
    #For para recorrer los estados y mostrar las probabilidades
    for estado in estados:
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
    def process_column_name(column_name):
        if '.' in str(column_name):
            parts = str(column_name).split('.')
            return parts[0]
        return column_name

    # Procesar los nombres de las columnas
    df.columns = [process_column_name(col) for col in df.columns]

    # Convertir el excel en una matriz
    matrix_representation = df.values.tolist()

    # Asignar cada columna de la matriz como un canal en el diccionario
    for column in matrix_representation:
        canal_numero = len(listaarreglos) + 1  # El número del canal es el siguiente número disponible
        listaarreglos[canal_numero] = column

    return listaarreglos  # Devolver el diccionario actualizado

def MatrizGlobal():
    global matriz_global
    print("Matriz de las probabilidades de los estados en canales:")
    for fila in matriz_global:
        print(fila)
#  I am not your enemy, I am the ENEMY 