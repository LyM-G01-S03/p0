from collections import namedtuple
import config as cf
# Define tokens
Token = namedtuple("Token", ["type", "value"])
KEYWORD = "KEYWORD"
NUMBER = "NUMBER"
VARIABLE = "VARIABLE"
STRING = "STRING"
OPERATOR = "OPERATOR"
SEPARATOR = "SEPARATOR"

# Define keywords and operators
KEYWORDS = {
    "defvar": KEYWORD,
    "=": KEYWORD,
    "move": KEYWORD,
    "skip": KEYWORD,
    "turn": KEYWORD,
    "face": KEYWORD,
    "put": KEYWORD,
    "pick": KEYWORD,
    "move-dir": KEYWORD,
    "run-dirs": KEYWORD,
    "move-face": KEYWORD,
    "null": KEYWORD,
    "if": KEYWORD,
    "loop": KEYWORD,
    "repeat": KEYWORD,
    "defun": KEYWORD,
    "facing?": KEYWORD,
    "blocked?": KEYWORD,
    "can-put?": KEYWORD,
    "can-pick?": KEYWORD,
    "can-move?": KEYWORD,
    "isZero?": KEYWORD,
    "not": KEYWORD,
}
NUMBER = {1: NUMBER, 2: NUMBER, 3: NUMBER, 4: NUMBER, 5: NUMBER, 6: NUMBER, 7: NUMBER, 8: NUMBER, 9: NUMBER, 0: NUMBER}
OPERATORS = {"+": OPERATOR, "-": OPERATOR, "*": OPERATOR, "/": OPERATOR}
SEPARATORS = {",": SEPARATOR, "(": SEPARATOR, ")": SEPARATOR, ";": SEPARATOR}
 

def keywords_verification(current_token: str) -> str:
    for keyword in KEYWORDS.keys():
        if keyword in current_token:
            return KEYWORD
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
        elif char in "+-*/":
            if current_token:
                tokens.append(Token(keywords_verification(current_token), current_token))
            tokens.append(Token(OPERATOR, char))
            current_token = ""
        else:
            current_token += char
    if current_token:
        tokens.append(Token(keywords_verification(current_token), current_token))
    return tokens



# Define functions to check syntax and consistency
def is_valid_variable(name):
    if name in defined_variables:
        return True
    else:
        return False

def is_valid_function_call(name, params):
    if name not in defined_functions:
        return False
    expected_params = defined_functions[name]["params"]
    return len(expected_params) == len(params) and all(is_valid_variable(p) for p in params)


def is_valid_condition(condition):
    if condition[0] in KEYWORDS:
        if condition[0] == "facing?":
            return len(condition) == 2 and condition[1] in ["north", "south", "east", "west"]
        elif condition[0] == "blocked?":
            return len(condition) == 1
        elif condition[0] in ["can-put?", "can-pick?", "can-move?"]:
            return len(condition) == 3 and condition[1] in ["chips", "balloons"] and is_valid_variable(condition[2])
        elif condition[0] == "isZero?":
            return len(condition) == 2 and is_valid_variable(condition[1])
        elif condition[0] == "not":
            return len(condition) == 2 and is_valid_condition(condition[1])
    return False

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

defined_variables = {}
defined_functions = {}
    
def save_funcionts_variables(tokens):
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
        if token.type == KEYWORD or COMMAND:
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
    print(defined_functions) 
    print(defined_variables)       
            
def check_syntax(tokens):
    current_block = []
    for token in tokens:
        if token.type == SEPARATOR:
            continue
        if token.type == KEYWORD:
            if "defvar" or 'defun' in token.value:
                save_funcionts_variables(tokens)
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
            elif token.value in ["if", "loop", "repeat"]:
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
        elif token.type == OPERATOR:
            if len(current_block) <= 1:
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
    linea = '(defvarrotate300)'
    tokenlinea = tokenize(linea)
    print(tokenlinea)
    if check_syntax(tokenlinea)is False:
            bandera = False

            #break

    if bandera == True:
        return True
    else:
        return False
