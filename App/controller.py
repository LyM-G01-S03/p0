"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
import config as cf
import model


def load_data(nombre):
    archivo = cf.data_dir + nombre
    with open(archivo) as file:
        verificacion = True
        while verificacion == True:
            linea = file.readline
            resultado = model.verificar(linea)
            if resultado ==False:
                verificacion = False
    return verificacion
