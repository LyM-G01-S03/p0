"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
import config as cf
import model


def load_data(nombre):
    archivo = cf.data_dir + nombre
    with open(archivo) as file:
        verificacion = True
        longitud = True
        while (verificacion == True) and (longitud == True):
            linea = file.readline
            if len(linea) == 0:
                longitud = False
            resultado = model.verificar(linea)
            if resultado ==False:
                verificacion = False
    return verificacion
