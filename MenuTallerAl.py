#Comnado para importar las funciones del archivo TallerAlgo1.py
from TallerAlgo1 import *
#Parte Numero 3 del taller de Algoritmos 

#Realizado por Daniel Felipe Carreño 

#Menu para el usuario
def menu():
    # Crear un diccionario vacío para almacenar los arreglos
    listaarreglos = {}
    # Ciclo infinito para mostrar el menú
    while True:
        print("\n--- Menú ---")
        print("1. Ingresar Canales")
        print("2. Mostrar Canales")
        print("3. Buscar numeros binarios en cada canal")
        print("4. Cargar Canales desde archivo de texto")
        print("5. Cargar Canales desde archivo excel")
        print("6. Estado CanalFuturo")
        print("7. Matriz EstadoFuturo")
        print("8. Matriz EstadoCanalIP")
        print("9. Matriz EstadoEstadoP")
        print("10. Probabilidad de transición de estados")
        print("11. Salir ")
        # Solicitar al usuario la opción
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            listaarreglos = ingresarCanales()
        elif opcion == "2":
            if not listaarreglos:
                print("Primero debe ingresar los Canales.")
            else:
                MostrarCanales(listaarreglos)
        elif  opcion == "3":
          ContarBinarios(listaarreglos)
        elif opcion == "4":
            listaarreglos = CargarArchivo()
        elif opcion == "5":
            file_path = input("Ingrese nombre del archivo Excel: ")
            try:
                listaarreglos = CargarExcel(file_path, listaarreglos)
                print("Canales cargados con éxito desde el archivo Excel.")
            except Exception as e:
                print(f"Error al cargar el archivo: {e}")
        elif opcion == "6":
             if listaarreglos:
                generarMatrizCanalFuturo(*listaarreglos.values())
             else:
               print("No tienes canales ingresados.")
        elif opcion == "7":
           if listaarreglos:
              generarEstados(listaarreglos)
           else:
                print("No tienes canales ingresados.")
        elif opcion == "8":
            if listaarreglos:
                generarMatrizCanalFuturo(*listaarreglos.values())
            else:
                print("No tienes canales ingresados.")
        elif opcion == "9":
            if listaarreglos:
                generarEstadosEstados(listaarreglos)
            else:
                print("No tienes canales ingresados.")
        elif opcion == "10":
            MatrizGlobal()
        elif opcion == "11":
            print("Gracias por utilizar el programa diseñado por Daniel Felipe Carreño Chavarro.")
            break
       
menu()
 # I am not your enemy, I am the ENEMY 