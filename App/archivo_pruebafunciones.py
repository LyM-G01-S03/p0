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
                


tokens = [('SEPARATOR','('), ('STRING', 'foo1')]
print(funciones_arreglar(tokens))

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


print(is_valid_function_call('foo', ['1','3']))