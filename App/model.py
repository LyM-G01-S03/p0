"""
El modelo se encarga de la creacion de funciones y manejo de 
logica del programa
"""

variables=[]

def verificar(linea:str)->bool:
    if "defvar" in linea:
        parametros = linea.split()
        defvar(parametros[1], parametros[3])
        return True
    #otras funciones   
    else:
        return False


   

def defvar(name:str, n:int )->bool:
    variables.append(name)
    
    
    syntax = True
    return  syntax

    
    