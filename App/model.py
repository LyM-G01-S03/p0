"""
El modelo se encarga de la creacion de funciones y manejo de 
logica del programa
"""

variables={}
funciones = {}

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

def parentesis_organizados(cadena):
    subcadenas = []
    nivel_parentesis = 0
    inicio_subcadena = 0
    for i, char in enumerate(cadena):
        if char == '(':
            nivel_parentesis += 1
            if nivel_parentesis == 1:
                inicio_subcadena = i
        elif char == ')':
            nivel_parentesis -= 1
            if nivel_parentesis == 0:
                subcadenas.append(cadena[inicio_subcadena:i+1])
                inicio_subcadena = i + 1
    return subcadenas

def verificar(subcadenas:list)->bool:
    guardarvarfun(subcadenas)

def guardarvarfun(subcadenas):
    lista_numeros = ['0','1','2','3','4','5','6','7','8','9']
    lista_constantes = ['Dim', 'myXpos', 'myYpos', 'myChips', 'myBaloons', 'ballonsHere', 'ChipsHere', 'Spaces']
    for cadena in subcadenas:
        if '(defvar' in cadena:
            for caracter in cadena[7:-1]:
                if caracter in lista_numeros:
                    posicion = cadena[7:-1].find(caracter)
                    n = cadena[posicion:-1]
                else:    
                    for constante in lista_constantes:
                        if constante in cadena[7:-1]:
                            posicion = cadena[7:-1].find(constante)
                            n = constante
                name = cadena[7:posicion]
            variables[name] = n
        if '(defun' in cadena:
            sec_com = []
            params = []
            for parentesis in cadena[6:-1]:
                if parentesis =='(' :
                    posicion1 = cadena[6:-1].find(parentesis)
                    name = cadena[6:posicion1]
                    secuencia = parentesis_organizados(cadena[parentesis:-1])
                    parametros = secuencia[0]
                    params = parametros.split(",")
                    for comando in secuencia[1:]:
                        sec_com.append(comando)
            funciones[name] = {'params': params, 'coms': sec_com}


    
    