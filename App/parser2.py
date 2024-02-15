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
OPERATORS = {"+": OPERATOR, "-": OPERATOR, "*": OPERATOR, "/": OPERATOR}
SEPARATORS = {",": SEPARATOR, "(": SEPARATOR, ")": SEPARATOR, ";": SEPARATOR}

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
                tokens.append(Token(VARIABLE if current_token in KEYWORDS else STRING, current_token))
            tokens.append(Token(SEPARATOR, char))
            current_token = ""
        elif char in "+-*/":
            if current_token:
                tokens.append(Token(VARIABLE if current_token in KEYWORDS else STRING, current_token))
            tokens.append(Token(OPERATOR, char))
            current_token = ""
        else:
            current_token += char
    if current_token:
        tokens.append(Token(VARIABLE if current_token in KEYWORDS else STRING, current_token))
    return tokens

# Define functions to check syntax and consistency
def is_valid_variable(name):
    return name.isalpha() and not name in KEYWORDS

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

def check_syntax(tokens):
    defined_variables = set()
    defined_functions = {}
    current_block = []
    for token in tokens:
        if token.type == SEPARATOR:
            continue
        if token.type == KEYWORD:
            if token.value == "defvar":
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

def main():
    archivo = cf.data_dir + 'ejemplo_valido.txt'
    with open(archivo, "r") as f:
        text = f.read()
    tokens = tokenize(text)
    if check_syntax(tokens):
        print("yes")
    else:
        print("no")

if __name__ == "__main__":
    main()
