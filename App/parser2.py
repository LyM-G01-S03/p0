from collections import namedtuple
import config as cf
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
    return STRING

defined_functions = {}

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
    print(tokens)
    return tokens



# Define functions to check syntax and consistency
def is_valid_variable(name):
    return name.isalpha() and not name in KEYWORDS

def is_valid_function_call(name, params):
    if name not in defined_functions:
        return False
    expected_params = defined_functions[name]["params"]
    return len(expected_params) == len(params) and all(is_valid_variable(p) for p in params)


def is_valid_condition(condition, tokens):
    lista_dir = [":north", ":south", ":west", ":east"]
    lista_c_p = ["chips", "balloons"]
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
        if info[0] in lista_c_p and n.isdigit():
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
        if info[0] in lista_c_p and n.isdigit():
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
        if parts[0].isdigit():
            return True
        else:
            return False
        
    if "not" in condition: 
        return True
                    
            
        


defined_variables = {}
defined_functions = {}
    
def save_functions_variables(tokens):
    lista_constantes = ['Dim', 'myXpos', 'myYpos', 'myChips', 'myBaloons', 'ballonsHere', 'ChipsHere', 'Spaces']
    for token in tokens:
        if token.type == KEYWORD:
            
            if "defvar" in token.value:
                for caracter in token.value[6:-1]:
                    if caracter.isdigit():
                        posicion = token.value[6:-1].find(caracter)
                        n = token.value[posicion:-1]
                    else:    
                        for constante in lista_constantes:
                            if constante in token.value[6:-1]:
                                posicion = token.value[6:-1].find(constante)
                                n = constante
                    name = token.value[7:posicion]
            defined_variables[name] = n

            
def verificar_condicion_if(tokens):
    verificados = []
    for token in tokens:
        if token.type == CONDITION:
            if is_valid_condition(token.value, tokens) == True:
                verificados.append(True)
            else:
                verificados.append(False)
    if False in verificados:
        return False
    else:
        return True
                
            

def check_syntax(tokens):
    current_block = []
    for token in tokens:
     
        if token.type == SEPARATOR:
            continue
        if token.type == KEYWORD:
            if "defvar" in token.value:
                if len(current_block) > 0:
                    return False  # Defvar should be at the beginning of a block
                next_token = next(iter(tokens))
                if not is_valid_variable(next_token.value):
                    return False
                defined_variables.add(next_token.value)
             
                continue
            elif token.value == "defun":
                if len(current_block) > 0:
                    return False  # Defun should be at the beginning of a block
                next_token = next(iter(tokens))
                if not is_valid_variable(next_token.value):
                    return False
                params = []
                while True:
                    next_token = next(iter(tokens))
                    if next_token.type == SEPARATOR and next_token.value == ")":
                        break
                    if not is_valid_variable(next_token.value):
                        return False
                    params.append(next_token.value)
                defined_functions[next_token.value] = {"params": params}
                continue
            elif token.value == "if":
                verificar_condicion_if(tokens)
                
            elif token.value in ["loop", "repeat"]:
                if not check_syntax(current_block):
                    return False
                current_block = []
            elif token.value == "null":
                continue
            else:
                if token.value not in defined_variables and token.value not in defined_functions:
                    return False
        elif token.type == VARIABLE:
            if token.value not in defined_variables and token.value not in defined_functions:
                return False
        elif token.type == STRING:
            if token.value not in ["north", "south", "east", "west", "chips", "balloons"]:
                return False
        current_block.append(token)
  
    if len(current_block) > 0 and not check_syntax(current_block):
        return False
    return True

def iniciar(lista):
    return main(lista)

def main(lista):
    bandera = True
    #for linea in lista:
    linea = "((if(not(blocked?))(move1)(null))(turn:left))"
    tokenlinea = tokenize(linea)
    if check_syntax(tokenlinea)is False:
            bandera = False
          
            #break
      
    if bandera == True:
        return True
    else:
        return False
