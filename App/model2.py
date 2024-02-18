variables = {}
funciones = {}

def separar_por_parentesis(texto: str) -> list:
    subcadenas = []
    nivel_parentesis = 0
    inicio_subcadena = 0

    for i, char in enumerate(texto):
        
        if char == '(':
            nivel_parentesis += 1
            if nivel_parentesis == 1:
                inicio_subcadena = i
        elif char == ')':
            nivel_parentesis -= 1
            if nivel_parentesis == 0:
                subcadenas.append(texto[inicio_subcadena:i+1])
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
    print(variables, funciones)
    return guardarvarfun(subcadenas)

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
                print(name)
            variables[name] = n
        if '(defun' in cadena:
            sec_com = []
            params = []
            name = cadena[6:posicion1]
            for parentesis in cadena[6:-1]:
                if parentesis =='(' :
                    posicion1 = cadena[6:-1].find(parentesis)
                    secuencia = parentesis_organizados(cadena[parentesis:-1])
                    parametros = secuencia[0]
                    params = parametros.split(" ")
                    for comando in secuencia[1:]:
                        sec_com.append(comando)
            funciones[name] = {'params': params, 'coms': sec_com}
    return True