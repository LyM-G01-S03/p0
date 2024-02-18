"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
import sys
import controllerparser

def menu():
    #nombre_archivo = str(input("Introduzca el nombre del archivo a verificar: "))
    nombre_archivo = "ejemplo_valido.txt"
    return nombre_archivo
    
def leer_archivo(nombre):
    return controllerparser.load_data(nombre)

if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    while working:
        print("Bienvenido")
        nombre = menu()
        resultado = leer_archivo(nombre)
        if resultado is True:
            print("Yes")
        elif resultado is False:
            print("No")
        continuacion = int(input("Desea verificar otro archivo (Si = 1 / No = 0): "))
        if continuacion == 0:
            working = False
            print("\nGracias por utilizar el programa")
        elif continuacion != (0 or 1):
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
        
        