"""
    
Proyecto 0 LYM, 202410_ISIS-1106_S03
Alejandra Fruto - 00000000, Daniel Vargas 202123892
a.fruto@uniandes.edo.co, d.vargasl2@uniandes.edu.co
    
El programa debe leer un archivo txt con una sitaxis,
y programa debe verificar si la sintaxis de este es correcta 
y devolver "yes" o "no" como respuesta de la verificacion de la sintaxis.
    
"""
import os
import sys
file_path = os.path.join(os.path.dirname(__file__), '..')
file_dir = os.path.dirname(os.path.realpath('__file__'))
sys.path.insert(0, os.path.abspath(file_path))
data_dir = file_dir + '/Data/'