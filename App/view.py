"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
import sys
import controller

def menu():
    nombre_archivo = str(input("Introduzca el nombre del archivo a verificar: ")).lower
    return nombre_archivo
    
def leer_archivo(nombre):
    return controller.load_data(nombre)

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
        continuacion = str(input("Desea verificar otro archivo (Si / No): ")).lower
        if continuacion == "no":
            working = False
            print("\nGracias por utilizar el programa")
        elif continuacion != "si":
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
        
        