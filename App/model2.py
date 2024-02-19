defined_variables = {}
defined_functions = {}

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
    return guardarvarfun(subcadenas)

def guardarvarfun(subcadenas):
    lista_constantes = ['Dim', 'myXpos', 'myYpos', 'myChips', 'myBaloons', 'ballonsHere', 'ChipsHere', 'Spaces']
    for cadena in subcadenas:
        if 'defvar' in cadena:
            cadena_info = cadena[7:-1]
            for caracter in cadena_info:
                if caracter.isdigit():
                    posicion = cadena_info.find(caracter)
                    n = cadena_info[posicion:]
                    name = cadena_info[:posicion]
                    defined_variables[name] = n
                    if n == None:
                        return False
            for constante in lista_constantes:
                if constante in cadena_info:
                    posicion = cadena_info.find(constante)
                    n = cadena_info[posicion:]
                    name = cadena_info[:posicion]
                    defined_variables[name] = n
                    if n == None:
                        return False
                        
        if 'defun' in cadena:
            cadena_info = cadena[6:-1]
            sec_com = []
            params = []
            posicion1 = cadena_info.find('(')
            name = cadena_info[:posicion1]
            secuencia = parentesis_organizados(cadena[posicion1:-1])  
            parametros = secuencia[0]
            params = parametros.split(",")
            params = [cadena.replace('(', '').replace(')', '').replace('()', '') for cadena in params]
            for comando in secuencia[1:]:
                sec_com.append(comando)
            defined_functions[name] = {'params': params, 'coms': sec_com}
    return True

verificar(['(defvarrotate300)', '(if(can-move?:north)(move-face1:north)(null))', 
           '((if(not(blocked?))(move1)(null))(turn:left))', '(defvarone1)', '(defunfoo(c,p)(put:chipsc)(put:balloonsp)(moverotate))', '(foo1,3)', 
           '(defungoend()(if(not(blocked?))((moveone)(goend))(null)))', '(defunfill()(repeatSpaces(if(not(isZero?myChips))(put:chips1)(null))))', 
           '(defunpickAllB()(pick:balloonsballoonsHere))', '(run-dirs:left:front:left:back:right)'])
print(defined_functions)