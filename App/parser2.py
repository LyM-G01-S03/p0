from collections import namedtuple
import config as cf
import sys
sys.setrecursionlimit(100000000)

# Define tokens
Token = namedtuple("Token", ["type", "value"])
KEYWORD = "KEYWORD"
COMAND = "COMAND"
CONDITION = "CONDITION"
NUMBER = "NUMBER"
VARIABLE = "VARIABLE"
STRING = "STRING"
SEPARATOR = "SEPARATOR"

# Define keywords and operators
KEYWORDS = {
    
    "if": KEYWORD,
    "loop": KEYWORD,
    "repeat": KEYWORD,
    "defun": KEYWORD,
}

COMANDS = {
    "defvar": COMAND,
    "=": COMAND,
    "move": COMAND,
    "skip": COMAND,
    "turn": COMAND,
    "face": COMAND,
    "put": COMAND,
    "pick": COMAND,
    "move-dir": COMAND,
    "run-dirs": COMAND,
    "move-face": COMAND,
    "null": COMAND,
}

NUMBERS = {1: NUMBER, 2: NUMBER, 3: NUMBER, 4: NUMBER, 5: NUMBER, 6: NUMBER, 7: NUMBER, 8: NUMBER, 9: NUMBER, 0: NUMBER}
SEPARATORS = {",": SEPARATOR, "(": SEPARATOR, ")": SEPARATOR, ";": SEPARATOR}
CONDITIONS = {    
    "facing?": CONDITION,
    "blocked?": CONDITION,
    "can-put?": CONDITION,
    "can-pick?": CONDITION,
    "can-move?": CONDITION,
    "isZero?": CONDITION,
    "not": CONDITION,}
 

def keywords_verification(current_token: str) -> str:
    for keyword in CONDITIONS.keys():
        if keyword in current_token:
            return CONDITION
    for keyword in KEYWORDS.keys():
        if keyword in current_token:
            return KEYWORD  
    for keyword in COMANDS.keys():
        if keyword in current_token:
            return COMAND
    return STRING

# Define function to tokenize input
def tokenize(text):
    tokens = []
    current_token = ""
    for char in text:
        if char.isalpha():
            current_token += char
        elif char.isdigit():
            current_token += char
        elif char in SEPARATORS:
            if current_token:
                tokens.append(Token(keywords_verification(current_token), current_token))
            tokens.append(Token(SEPARATOR, char))
            current_token = ""
        else:
            current_token += char
    if current_token:
        tokens.append(Token(keywords_verification(current_token), current_token))
    return tokens



# Define functions to check syntax and consistency

defined_variables = {}
defined_functions = {}
        
def is_valid_variable(name):
    if (name in defined_variables):
        return True
    else:
        return False
    
def is_valid_param(parametro):
   
    lista_nueva = []
    for defined_f in defined_functions.values():
            for param in defined_f:
                lista_nueva.append(param)
    if (parametro in lista_nueva) or parametro.isdigit() or (parametro in defined_variables):
        return True
    else:
        return False

def is_valid_function_call(name, params=None):
    if name not in defined_functions:
    
        return False
    expected_params = defined_functions[name]
   
    if params == None:
        return  True
    else:
        return (len(expected_params) == len(params)) and all(is_valid_param(p) for p in params)

def funciones_arreglar(tokens):
    parametros = []
    name = None
    for funcion in defined_functions:
        for token in tokens:
            if token.type == STRING:
                if 'defun' in token.value:
                    return False, None, None
                if funcion in token.value:
                    name = funcion
                    if len(funcion) == len(token.value):
                        parametros = None
                        return True, name, None                        
                    else:
                        parametro = token.value[len(funcion):]
                        parametros.append(parametro)
               
                if (funcion not in token.value)   and ((len(parametros) > 0) or (len(parametros) is not None)):
                   
                    parametros.append(token.value)
                
    return  True, name, parametros 
                
def is_valid_condition(condition):
    lista_dir = [":north", ":south", ":west", ":east"]
    lista_c_p = ["chips", "balloons"]
    lista_constantes = ['Dim', 'myXpos', 'myYpos', 'myChips', 'myBalloons', 'balloonsHere', 'ChipsHere', 'Spaces']
    
    if "facing?" in condition:
        parts = condition.split("facing?")
        for element in parts:
            if element == "":
                parts.remove(element)
        if parts[0] in lista_dir:
            return True
        else:
            return False
                
    if "blocked?" in condition:  
        return True
        
    if "can-put?" in condition: 
        info = []
        cadena_info = condition[8:]
        for caracter in cadena_info:
                    if caracter.isdigit():
                        posicion = cadena_info.find(caracter)
                        n = cadena_info[posicion:]
                        name = cadena_info[:posicion]
                        if len(info) < 2:
                            info.append(name)
                            info.append(n)
        if info[0] in lista_c_p and info[1].isdigit():
            return True
        else:
            return False
        
    if "can-pick?" in condition:
        info = []
        cadena_info = condition[9:]
        for caracter in cadena_info:
                    if caracter.isdigit():
                        posicion = cadena_info.find(caracter)
                        n = cadena_info[posicion:]
                        name = cadena_info[:posicion]
                        if len(info) < 2:
                            info.append(name)
                            info.append(n)
        if info[0] in lista_c_p and info[1].isdigit():
            return True
        else:
            return False
        
    if "can-move?" in condition:
        parts = condition.split("can-move?")
        for element in parts:
            if element == "":
                parts.remove(element)
        if parts[0] in lista_dir:
            return True
        else:
            return False
        
    if "isZero?" in condition:
        parts = condition.split("isZero?")
        for element in parts:
            if element == "":
                parts.remove(element)
        
        if parts[0].isdigit() or parts[0] in lista_constantes :
            return True
        else:
            return False
        
    if "not" in condition: 
        return True
                                   
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
                
def save_functions_variables(tokens):
    lista_constantes = ['Dim', 'myXpos', 'myYpos', 'myChips', 'myBaloons', 'ballonsHere', 'ChipsHere', 'Spaces']
    params = []
    for token1 in tokens:
        if (token1.type == KEYWORD) :
            if ('defun' in token1.value):
                count = 1
                while count < len(tokens):
                    if tokens[count].type == STRING:
                        parametro = tokens[count].value
                        params.append(parametro)
                    count = count +1
    for token in tokens:
        if token.type == KEYWORD or COMAND:
            if 'defvar' in token.value:
                cadena_info = token.value[6:]
                for caracter in cadena_info:
                    if caracter.isdigit():
                        posicion = cadena_info.find(caracter)
                        n = cadena_info[posicion:]
                        name = cadena_info[:posicion]
                        defined_variables[name]=n
                        break
                for constante in lista_constantes:
                    if constante in cadena_info:
                        posicion = cadena_info.find(constante)
                        n = cadena_info[posicion:]
                        if n!=None:
                            name = cadena_info[:posicion]
                            defined_variables[name] = n     
            if 'defun' in token.value:
                nombre = token.value[5:]
                defined_functions[nombre] = params
   
def is_valid_comand(command):
    lista_dir = [":north", ":south", ":east", ":west"]
    lista_move = [":left", ":right", ":around"]
    lista_constantes = ['Dim', 'myXpos', 'myYpos', 'myChips', 'myBalloons', 'balloonsHere', 'ChipsHere', 'Spaces']
    lista_c_p = [":chips", ":balloons"]
    lista_move_dir = [ ":front", ":right", ":left", ":back"]
    lista_move_dir2 = [ "front", "right", "left", "back"]
    
    if "defvar" in command:
        
        info = []
        cadena_info = command[6:]
        for caracter in cadena_info:
                            if caracter.isdigit():
                                posicion = cadena_info.find(caracter)
                                n = cadena_info[posicion:]
                                name = cadena_info[:posicion]
                                info = [name, n]
                                break
        for constante in lista_constantes:
                            if constante in cadena_info:
                                posicion = cadena_info.find(constante)
                                n = cadena_info[posicion:]
                                if n!=None:
                                    name = cadena_info[:posicion]
                                info = [name, n] 
                                
        if info[1].isdigit() or info[1] in lista_constantes:   
            return True
        else:
            return False 
        
    elif "run-dirs" in command:
        parts = command.split("run-dirs")
        for element in parts:
            if element == "":
                parts.remove(element)
                
        partss = parts[0].split(":")
        for element in partss:
            if element == "":
                partss.remove(element)
                
        visitados = []
        for element in partss:
            if element in lista_move_dir2:
                visitados.append(True)
            else: 
                visitados.append(False)
             
        if len(partss) != 0:
            if False in visitados:
                return False
            else:
                return True
        else:
            return False
        
    elif "=" in command:
        info = []
        cadena_info = command[1:]
        for caracter in cadena_info:
                            if caracter.isdigit():
                                posicion = cadena_info.find(caracter)
                                n = cadena_info[posicion:]
                                name = cadena_info[:posicion]
                                info = [name, n]
                                break
        for constante in lista_constantes:
                            if constante in cadena_info:
                                posicion = cadena_info.find(constante)
                                n = cadena_info[posicion:]
                                if n!=None:
                                    name = cadena_info[:posicion]
                                info = [name, n] 
                                
        if info[0]  in defined_variables:
            defined_variables[info[0]] = info[1]
            return True
        else:
            return False       
              
    elif "skip" in command:
        parts = command.split("skip")
        for element in parts:
            if element == "":
                parts.remove(element)
        if parts[0] in lista_constantes or parts[0] in defined_variables or parts[0].isdigit():
            return True
        else:
            return False
        
    elif "turn" in command:
        parts = command.split("turn")
        for element in parts:
            if element == "":
                parts.remove(element)
        if parts[0] in lista_move:
            return True
        else:
            return False
        
    elif "put" in command:
        info = []
        cadena_info = command[3:]
        for caracter in cadena_info:
                            if caracter.isdigit():
                                posicion = cadena_info.find(caracter)
                                n = cadena_info[posicion:]
                                name = cadena_info[:posicion]
                                info = [name, n]
                                break
        for constante in defined_variables:
                            if constante in cadena_info:
                                posicion = cadena_info.find(constante)
                                n = cadena_info[posicion:]
                                if n!=None:
                                    name = cadena_info[:posicion]
                                info = [name, n] 
                      
        
        for element in lista_c_p:
                                if element in cadena_info:
                                    cadena_par = cadena_info[len(element):]
  
                                    info = [element, cadena_par] 
        
       
        lista_nueva = []
        for defined_f in defined_functions.values():
            for param in defined_f:
                lista_nueva.append(param)
        if info[0] in lista_c_p and (info[1].isdigit() or info[1] in defined_variables or info[1]in lista_nueva):
                return True
        else:
               return False
     
       
            
        
    elif "pick" in command:
        info = []
        cadena_info = command[4:]
        for caracter in cadena_info:
                            if caracter.isdigit():
                                posicion = cadena_info.find(caracter)
                                n = cadena_info[posicion:]
                                name = cadena_info[:posicion]
                                info = [name, n]
                                break
        for constante in defined_variables:
                            if constante in cadena_info:
                                posicion = cadena_info.find(constante)
                                n = cadena_info[posicion:]
                                if n!=None:
                                    name = cadena_info[:posicion]
                                info = [name, n] 
        for constante in lista_constantes:
                            
                            if constante in cadena_info:
                                
                                posicion = cadena_info.find(constante)
                                n = cadena_info[posicion:]
                                if n!=None:
                                    name = cadena_info[:posicion]
                                info = [name, n] 
                                
               
        if info[0] in lista_c_p and (info[1].isdigit() or info[1] in defined_variables or info[1] in lista_constantes):
           return True
        else:
            return False
        
    elif "move-dir" in command:  
        info = []
        cadena_info = command[8:]
        for constante in lista_move_dir:
                                if constante in cadena_info:
                                    posicion = cadena_info.find(constante)
                                    n = cadena_info[posicion:]
                                    if n!=None:
                                        name = cadena_info[:posicion]
                                    info = [name, n] 
        if ( info[0] in defined_variables or info[0].isdigit() ) and info[1] in lista_move_dir:
                return True
        else:
               return False
        
    elif "move-face" in command:
        
        info = []
        cadena_info = command[9:]
        for constante in lista_dir:
                                if constante in cadena_info:
                                    posicion = cadena_info.find(constante)
                                    n = cadena_info[posicion:]
                                    if n!=None:
                                        name = cadena_info[:posicion]
                                    info = [name, n] 
        if ( info[0] in defined_variables or info[0].isdigit() ) and info[1] in lista_dir:
                return True
        else:
               return False
    
    elif "face" in command:
        parts = command.split("face")
        for element in parts:
            if element == "":
                parts.remove(element)
        if parts[0] in lista_dir:
            return True
        else:
            return False
        
    elif "move" in command:
        
        parts = command.split("move")
        for element in parts:
            if element == "":
                parts.remove(element)
        if parts[0] in lista_constantes or parts[0] in defined_variables or parts[0].isdigit():
            return True
        else:
            return False
        
    elif "null" in command:
        return True
    
def verificar_if_loop(tokens):
    verificados_condition = []
    verificados_command = []
    for token in tokens:
        if token.type == CONDITION:
            if is_valid_condition(token.value) == True:
                verificados_condition.append(True)
            else:
                verificados_condition.append(False)
                
        if token.type == COMAND:
            if is_valid_comand(token.value) == True:
                 verificados_command.append(True)
            else:
                verificados_command.append(False)
    

    if False in verificados_condition or False in verificados_command:
        return False
    else:
        return True
    
def verificar_repeat_times(tokens):
    lista_constantes = ['Dim', 'myXpos', 'myYpos', 'myChips', 'myBaloons', 'ballonsHere', 'ChipsHere', 'Spaces']
    for token in tokens:
        if token.type == KEYWORD:
            if 'repeat' in token.value:
                variable = token.value[6:]
                if is_valid_variable(variable) or variable in lista_constantes:
                    return True
                elif int(variable)>0:
                    return True
                else:
                    return False

def verificar_defun(tokens):
    verificados = []
    for token in (tokens):
        if token.type == KEYWORD:
            if 'defun' in token.value:
                if len(token.value) == 5:
                    
                    verificados.append(False)
                else: 
                    verificados.append(True)
        
       
                
                count = 1
                while count < len(tokens):
                        if tokens[count].type == STRING:
                            parametro = tokens[count].value
                            
                            paramver = is_valid_param(parametro)
                            verificados.append(paramver)
                        count = count +1
        if token.type == COMAND:
            verificados.append(is_valid_comand(token.value))  
            
    
    if False in verificados:
        return False
    else:
        return True       
                
                    
    
            
def check_syntax(tokens):
    verificados = []
    for token in tokens:
        if token.type == SEPARATOR:
            continue
        if token.type == COMAND:
            if "defvar" in token.value:
                save_functions_variables(tokens)
                verificados.append(is_valid_comand(token.value))
            else:
                verificados.append(is_valid_comand(token.value))
        if token.type == KEYWORD:
            if 'defun' in token.value:
                save_functions_variables(tokens)
                verificados.append(verificar_defun(tokens))
                continue
            if "if" in token.value or "loop" in token.value:
                verificados.append(verificar_if_loop(tokens))
            if "repeat" in token.value:
                verificados.append(verificar_repeat_times(tokens))
                
                
        if token.type == STRING:
            for element in defined_functions.values():
                if token.value in  element:
                    continue
                else:   
                    ver, name, par = funciones_arreglar(tokens)
                    if ver is True:
                     
                        ver2 = is_valid_function_call(name, par)
                        verificados.append(ver2)
 
    if False in verificados:
        return False
    else:
        return True
                


def iniciar(lista):
    return main(lista)

def main(lista):
    bandera = True
    for linea in lista:
        tokenlinea = tokenize(linea)
        
        if check_syntax(tokenlinea)is False:
            bandera = False
            
            break
       
    if bandera == True:
        return True
    else:
        return False
