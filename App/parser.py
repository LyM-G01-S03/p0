from ply import lex, yacc

# Lista de tokens
tokens = (
    'LPAREN', 'RPAREN', 'NAME', 'NUMBER', 'COLON', 'COMMA', 'CONSTANT',
    'DEFVAR', 'ASSIGN', 'MOVE', 'SKIP', 'TURN', 'FACE', 'PUT', 'PICK',
    'MOVE_DIR', 'RUN_DIRS', 'MOVE_FACE', 'NULL', 'IF', 'LOOP', 'REPEAT',
    'DEFUN', 'FACING', 'BLOCKED', 'CAN_PUT', 'CAN_PICK', 'CAN_MOVE', 'IS_ZERO',
    'NOT'
)

# Definición de las expresiones regulares para los tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_COMMA = r','
t_CONSTANT = r':[a-zA-Z]+'

# Definición de la regla para nombres (identificadores)
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')  # Check for reserved words
    return t

# Definición de la regla para números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para defvar
def t_DEFVAR(t):
    r'defvar'
    return t

# Regla para reserved keywords
reserved = {
    'defvar': 'DEFVAR',
    'if': 'IF',
    'loop': 'LOOP',
    'repeat': 'REPEAT',
    'defun': 'DEFUN',
    'facing': 'FACING',
    'blocked': 'BLOCKED',
    'can-put': 'CAN_PUT',
    'can-pick': 'CAN_PICK',
    'can-move': 'CAN_MOVE',
    'is-zero': 'IS_ZERO',
    'not': 'NOT'}

# Regla para ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# Función para manejar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Función para manejar errores de token
def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

# Definición de los tokens para operadores aritméticos
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_UMINUS = r'-'

# Reglas de la gramática
def p_program(p):
    '''program : 
               | instruction program'''
    pass


def p_instruction(p):
    '''instruction : command
                   | control_structure
                   | function_call'''
    pass

def p_command(p):
    '''command : LPAREN command_type params RPAREN'''
    pass

def p_command_type(p):
    '''command_type : DEFVAR
                    | ASSIGN
                    | MOVE
                    | SKIP
                    | TURN
                    | FACE
                    | PUT
                    | PICK
                    | MOVE_DIR
                    | RUN_DIRS
                    | MOVE_FACE
                    | NULL'''
    pass

def p_params(p):
    '''params : param
              | params COMMA param'''
    pass

def p_param(p):
    '''param : NAME
             | CONSTANT
             | NUMBER'''
    pass

def p_control_structure(p):
    '''control_structure : conditional
                         | repeat
                         | repeat_times
                         | function_definition
                         | command'''
    pass

def p_conditional(p):
    '''conditional : LPAREN IF condition instruction instruction RPAREN'''
    pass

def p_repeat(p):
    '''repeat : LPAREN LOOP condition instruction RPAREN'''
    pass

def p_repeat_times(p):
    '''repeat_times : LPAREN REPEAT param instruction RPAREN'''
    pass

def p_function_definition(p):
    '''function_definition : LPAREN DEFUN NAME LPAREN params RPAREN instruction RPAREN'''
    pass

def p_function_call(p):
    '''function_call : LPAREN NAME function_params RPAREN'''
    pass

def p_function_params(p):
    '''function_params : param
                       | function_params COMMA param'''
    pass

def p_condition(p):
    '''condition : facing
                 | blocked
                 | can_put
                 | can_pick
                 | can_move
                 | is_zero
                 | not_condition
                 | NAME
                 | CONSTANT
                 | NUMBER'''
    pass

def p_facing(p):
    '''facing : LPAREN FACING LPAREN COLON NAME RPAREN RPAREN'''
    pass

def p_blocked(p):
    '''blocked : LPAREN BLOCKED LPAREN RPAREN RPAREN'''
    pass

def p_can_put(p):
    '''can_put : LPAREN CAN_PUT COLON NAME param RPAREN'''
    pass

def p_can_pick(p):
    '''can_pick : LPAREN CAN_PICK COLON NAME param RPAREN'''
    pass

def p_can_move(p):
    '''can_move : LPAREN CAN_MOVE COLON NAME RPAREN'''
    pass

def p_is_zero(p):
    '''is_zero : LPAREN IS_ZERO COLON NAME RPAREN'''
    pass

def p_not_condition(p):
    '''not_condition : LPAREN NOT condition RPAREN'''
    pass

def p_error(p):
    print("Error de sintaxis en '%s'" % p.value)

# Construcción del parser
parser = yacc.yacc()

# Función para analizar la entrada
def parse_program(program):
    return parser.parse(program)

# Programa de ejemplo
program = "(defvarrotate3)(if(can-move?:north)(move-dir1:north)(null))((if(not(blocked?))(move1)(null))(turn:left))(defvarone1)(defunfoo(c,p)(put:chipsc)(put:balloonsp)(moverotate))(foo13)(defungoend()(if(not(blocked?))((moveone)(goend))(null)))(defunfill()(repeatSpaces(if(not(isZero?myChips))(put:chips1))))(defunpickAllB()(pick:balloonsballoonsHere))(run-dirs:left:up:left:down:right)"
result = parse_program(program)
print("Sintaxis correcta.")
