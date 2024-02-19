lista_dir = [":north", ":south", ":west", ":east"]
lista_c_p = ["chips", "balloons"]
lista_move = [":left", ":right", ":around"]
command = "putballoons78"
defined_functions = {'foo': ['c', 'p'], 'fill':None, 'goend':None}
defined_variables = { "rotate" : "3", "one":"1"}
lista_constantes = ['Dim', 'myXpos', 'myYpos', 'myChips', 'myBaloons', 'ballonsHere', 'ChipsHere', 'Spaces']


def funciones_arreglar(tokens):
    parametros = []
    name = None
    for funcion in defined_functions:
#        if token.type == STRING:
            for token in tokens:
                if token[0] == 'STRING':
                    if 'defun' in token[1]:
                        return False, None, None 
                    if funcion in token[1]:
                        name = funcion
                        if len(funcion) == len(token[1]):
                            parametros = None
                            return True, name, None                        
                        else:
                            parametro = token[1][len(funcion):]
                            parametros.append(parametro)
                    if (funcion not in token[1])and (funcion == name) and((len(parametros) > 0) or (len(parametros) is not None)):
                        print(funcion)
                        print(token[1])
                        parametros.append(token[1])
                    return True, name, parametros
                



#print(funciones_arreglar(tokens))

def is_valid_param(parametro):
    if (parametro in defined_variables) or parametro.isdigit():
        return True
    else:
        return False

def is_valid_function_call(name, params=None):
    if name not in defined_functions:
        return False
    expected_params = defined_functions[name]
    return (len(expected_params) == len(params)) and all(is_valid_param(p) for p in params)


def is_valid_variable(name):
    if (name in defined_variables):
        return True
    else:
        return False


def verificar_repeat_times(tokens):
    for token in tokens:
        if token[0] == 'KEYWORD':
            if 'repeat' in token[1]:
                variable = token[1][6:]
                if is_valid_variable(variable) or variable in lista_constantes:
                    return True
                elif int(variable)>0:
                    return True
                else:
                    return False
#print(is_valid_function_call('foo', ['1','3']))

tokens = [('SEPARATOR', '('), ('KEYWORD', 'defunfill'), ('SEPARATOR', '('), ('SEPARATOR', ')'), 
          ('SEPARATOR', '('), ('KEYWORD', 'repeatSpaces'), ('SEPARATOR', '('), ('KEYWORD', 'if'),
          ('SEPARATOR', '('), ('CONDITION', 'not'), ('SEPARATOR', '('), ('CONDITION', 'isZero?myChips'), 
          ('SEPARATOR', ')'), ('SEPARATOR', ')'), ('SEPARATOR', '('), ('COMAND', 'put:chips1'), 
          ('SEPARATOR', ')'), ('SEPARATOR', '('), ('COMAND', 'null'), ('SEPARATOR', ')'), 
          ('SEPARATOR', ')'), ('SEPARATOR', ')'), ('SEPARATOR', ')')]


print(verificar_repeat_times(tokens))
