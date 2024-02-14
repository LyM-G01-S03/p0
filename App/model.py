"""
El modelo se encarga de la creacion de funciones y manejo de 
logica del programa
"""

variables={}


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


def verificar(subcadenas:list)->bool:
    lista_numeros = ['0','1','2','3','4','5','6','7','8','9']
    lista_constantes = ['Dim', 'myXpos', 'myYpos', 'myChips', 'myBaloons', 'ballonsHere', 'ChipsHere', 'Spaces']
    for cadena in subcadenas:
        if '(defvar' in cadena:
            for caracter in cadena[7:-1]:
                if caracter in lista_numeros:
                    posicion = cadena[7:-1].find(caracter)
                    n = cadena[posicion:-1]
                    name = cadena[7:posicion]
            for constante in lista_constantes:
                if constante in cadena[7:-1]:
                    if constante == 'Dim':
                        posicion = cadena[7:-1].find('Dim')
                        n = 'Dim'
                        name = cadena[7:posicion]
                    if constante == 'myXpos':
                        posicion = cadena[7:-1].find('myXpos')
                        n = 'myXpos'
                        name = cadena[7:posicion]
                    if constante == 'myYpos':
                        posicion = cadena[7:-1].find('myYpos')
                        n = 'myYpos'
                        name = cadena[7:posicion]
                    if constante == 'myChips':
                        posicion = cadena[7:-1].find('myChips')
                        n = 'myChips'
                        name = cadena[7:posicion]
                    if constante == 'myBaloons':
                        posicion = cadena[7:-1].find('myBaloons')
                        n = 'myBaloons'
                        name = cadena[7:posicion]
                    if constante == 'ballonsHere':
                        posicion = cadena[7:-1].find('ballonsHere')
                        n = 'ballonsHere'
                        name = cadena[7:posicion]
                    if constante == 'ChipsHere':
                        posicion = cadena[7:-1].find('ChipsHere')
                        n = 'ChipsHere'
                        name = cadena[7:posicion]
                    if constante == 'Spaces':
                        posicion = cadena[7:-1].find('Spaces')
                        n = 'Spaces'
                        name = cadena[7:posicion]            
            variables[name] = n
        if '(defun' in cadena:
            numeroparentesis = 1
            sec_com = []
            parentesiscerrado1 = 0
            for parentesis in cadena[6:-1]:
                if numeroparentesis == 1:
                    if parentesis =='(' :
                        posicion = cadena[6:-1].find(parentesis)
                        name = cadena[6:parentesis]
                        if ')' in cadena[parentesis:-1]:
                            posicion2 = cadena[parentesis:-1].find(')')
                            parentesiscerrado1 = posicion2
                            parametros = cadena[posicion+1, posicion2].split(',')
                            numeroparentesis +=1
                if numeroparentesis > 1:
                    
                    if parentesis =='(' :
                        posicion = cadena[parentesiscerrado1:-1].find(parentesis)
                        name = cadena[6:parentesis]
                    
                            
                
                            
                    
                    
                    
                
                
    
    
    # if "defvar" in linea:
    #     parametros = linea.split()
    #     defvar(parametros[1], parametros[3])
    #     return True
    # #otras funciones   
    # else:
    #     return False


   

def defvar(name:str, n:int )->bool:
    variables.append(name)
    
    
    syntax = True
    return  syntax

    
    