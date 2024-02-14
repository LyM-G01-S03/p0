"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
import config as cf
import model


def load_data(nombre):
    archivo = cf.data_dir + nombre
    with open(archivo, 'r') as file:
        lineas = file.readlines()
    lista_mod = []
    for posicion, linea in enumerate(lineas):
        if '(defun' in linea:
            posiciones = []
            posicion = 0  # Reiniciar la posición para cada línea
            while True:
                posicion = linea.find('defun', posicion)
                if posicion == -1:
                    break
                posiciones.append(posicion)
                posicion += 1
            for position in posiciones:
                indice_parentesis_abierto = linea.find("(", position)
                # Buscar la posición del siguiente paréntesis de cierre ')'
                indice_parentesis_cerrado = linea.find(")", indice_parentesis_abierto)
                if indice_parentesis_abierto != -1 and indice_parentesis_cerrado != -1:
                    # Extraer el contenido entre paréntesis
                    contenido_paréntesis = linea[indice_parentesis_abierto + 1:indice_parentesis_cerrado]
                    # Reemplazar los espacios por comas
                    contenido_modificado = contenido_paréntesis.replace(" ", ",")
                    # Construir la cadena modificada con los cambios
                    linea_modificada = linea[:indice_parentesis_abierto + 1] + contenido_modificado + linea[indice_parentesis_cerrado:]
                    # Actualizar la lista 'lineas' con la línea modificada
                    lista_mod.append(linea_modificada)
        else:
            lista_mod.append(linea)
                
    contenido = ''.join(linea.replace(' ', '').strip() for linea in lista_mod)
    print(contenido)
    if len(contenido) == 0:
        return False
    resultado = model.verificar(contenido)
    return resultado
