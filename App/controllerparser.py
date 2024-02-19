"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
import config as cf
import parser2


def separar_por_parentesis(texto: str) -> list:
    subcadenas = []
    nivel_parentesis = 0
    inicio_subcadena = 0

    # Itera sobre cada carácter en el texto
    for i, char in enumerate(texto):
        
        if char == '(':
            # Si encontramos un paréntesis de apertura, incrementamos el nivel de paréntesis
            nivel_parentesis += 1
            # Si es el primer paréntesis de apertura, guardamos su posición como inicio de subcadena
            if nivel_parentesis == 1:
                inicio_subcadena = i
        elif char == ')':
            # Si encontramos un paréntesis de cierre, decrementamos el nivel de paréntesis
            nivel_parentesis -= 1
            # Si el nivel de paréntesis vuelve a 0, significa que hemos encontrado el cierre de una subcadena
            if nivel_parentesis == 0:
                # Guardamos la subcadena encontrada
                subcadenas.append(texto[inicio_subcadena:i+1])
                # Actualizamos el inicio de la próxima subcadena
                inicio_subcadena = i + 1
    return subcadenas

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
    
    for i, linea in enumerate(lista_mod):
        if linea == '\n':
            lista_mod.remove('\n')
        if '\n' in linea:
            lista_mod[i] = lista_mod[i].rstrip('\n')
            
    contenido = ''.join(linea.replace(' ', '').strip() for linea in lista_mod)
     
    lista_org = separar_por_parentesis(contenido)
    
    
    if len(lista_org) == 0:
        return False
    resultado = parser2.iniciar(lista_org)
    return resultado