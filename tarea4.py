import re
"""Funcion que quita los comentarios de un archivo de texto cuando haya /* */,
 requiere un archivo de entrada y otro de salida que creara una copia del original
 """
def quita_comentarios(archivoEnt, archivoSal):
    archivo = open(archivoEnt,"r")
    texto = []
    cad = ""
    for linea in archivo:
       for c in linea:
         texto.append(c)
    archivo.close()
    estado = "z";
    for c in texto:
         if estado=="z" and c=="/":
          estado="a";
         elif estado =="z" and c!="/":
          cad = cad + c
         elif estado =="a" and c=="*":
          estado = "b"
         elif estado =="a" and c!="*":
          estado = "z"
          cad = cad + "/"
         elif estado=="b"and c=="*":
          estado = "c"
         elif estado =="c" and c=="/":
          estado = "z";
         elif estado =="c" and c!="/":
          estado="b"
    archivo = open(archivoSal,"w")
    archivo.write(cad)
    return None
quita_comentarios("uno.txt", "dos.txt") # se quitan los comentarios
 
"""Explique que hizo el programa y muestre como quedó el contenido del archivo dos.txt."""

def es_simbolo_esp(caracter):
    return caracter in "+-*;,.:!=%&/()[]<><=>=:="

"""Funcion que retorna los separadores o espacios"""
def es_separador(caracter):
    return caracter in " \n\t"

"""Funcion que retornara un falso si­ en la cadena ingresada no se encuentra un numero entero,
de lo contrario retorna un verdadero"""
def es_entero(cad):
    valido = True
    for c in cad:
        if c not in "0123456789":
            valido = False
    return valido
"""Funcion que recibe una cadena, 
retornara¡ un verdadero si despues o antes de un punto se encuentra un numero entero"""
def es_flotante(cad):
    a=[]
    if cad[0]!= "." and cad[-1]!= "." and cad.count(".")==1:
        a = cad.split(".")
        if es_entero(a[0]) and es_entero(a[1]):
            return True
        else:
            return False
        return True
"""Funcion que retorna un verdadero sÃ­ en la cadena ingresada se encuentra un guion
o una letra del abecedario minuscula o mayuscula, de lo contrario un falso"""
def es_id(cad):
    if cad[0] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
        return True
    else:
        return False

"""Funcion que retorna las palabras reservadas"""
def es_pal_res(token):
    return token in ["main","var","if","else","for","print","read","int","float","char","string"]

"""Funcion que retorna los tipos de datos"""    
def es_tipo(token):
    return token in ["int","float","char","string"]

"""Funcion que separa los tokens, recive un tipo archivo.
Si­ no es un simbolo especial, separador y no esta dentro devuelve un verdadero y la cadena sera vacia,
en caso de no ser un simbolo especial, separador pero si esta dentro agreaga a la cadena lo que tiene contenido,
en caso de ser un simbolo especial y no estar dentro se agrega a los tokens,
si­ es un simbolo especial o separador y esta dentro agrega los tokens y dentro sera falso de ser simbolo especial tambien se agrega,
si­ es un simbolo especial compuesto se agrega a otro arreglo de tokens,
remueve todos los numeros flotantes  

 """
def separa_tokens(archivo):
    tokens = []
    tokens2 = []
    archivo = open(archivo, "r")
    dentro = False
    for linea in archivo:
        for l in linea:
            if not (es_simbolo_esp(l)) and not (es_separador(l)) and not (dentro):
                dentro = True
                cad = ""
            if not (es_simbolo_esp(l)) and not (es_separador(l)) and dentro:
                cad = cad + l
            if es_simbolo_esp(l) and not(dentro):
                tokens.append(l)
            if (es_simbolo_esp(l) or es_separador(l)) and dentro:
                tokens.append(cad)
                dentro = False
                if es_simbolo_esp(l):
                    tokens.append(l)
    archivo.close()
    compuesto = False
    for c in range(len(tokens)-1):
        if compuesto:
            compuesto = False
            continue
        if tokens[c] in ":<>!" and tokens[c+1]=="=":
            tokens2.append(tokens[c]+"=")
            compuesto = True
        else:
            tokens2.append(tokens[c])
    tokens2.append(tokens[-1])
    for c in range(1,len(tokens2)-1):
        if tokens2[c]== "." and es_entero(tokens2[c-1]) and es_entero(tokens2[c+1]):
            tokens2[c]=tokens2[c-1]+tokens2[c]+tokens2[c+1]
            tokens2[c-1]= "borrar"
            tokens2[c+1]= "borrar"
    porBorrar = tokens2.count("borrar")
    for c in range(porBorrar):
        tokens2.remove("borrar")
    return tokens2

def separa_tokens2(filename):
    # Leer el archivo y cargar su contenido en una cadena
    with open(filename, 'r') as f:
         contents = f.read()
    # Definir una expresión regular que capture los tokens de C
    token_regex = re.compile(r'''
        /\*.*?\*/|                # comentarios multilinea
        //[^\n]*|                 # comentarios de una línea
        ".*?"|                    # literales de cadena
        \d+\.\d+|\w+|             # números decimales y palabras
        !=|==|<=|>=|&&|\|\||      # operadores
        \+|\-|\*|/|%|             # operadores aritméticos
        =|,|;|\(|\)|\{|\}|\[|\]   # símbolos especiales
        ''', re.DOTALL | re.VERBOSE)
# Utilizar la expresión regular para dividir el contenido del archivo en tokens
    tokens = []
    for token in re.findall(token_regex, contents):
        if token.strip():
            tokens.append(token.strip())
    return tokens

"""Clase que usa el nombre y el tipo de variable"""
class Variable:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo


"""Funcion que retorna que tipo de dato es el token, en caso de no encontrarse retornara un pendiente"""
def get_etiqueta(token):
    etiqueta = ""
    if es_id (token):
        if es_pal_res(token):
            if es_tipo(token):
                etiqueta = "tipo"
            else:
                etiqueta = "palres"
        else:
            etiqueta = "id"
    elif es_simbolo_esp(token):
        etiqueta = "simbolo"
    elif es_entero(token):
        etiqueta = "entero"
    elif es_flotante(token):
        etiqueta = "flotante"
    else:
        etiqueta = "pendiente"
    return etiqueta

"""imprime los tokens"""
def imprime_tabla_tokens(tokens):    
    for t in tokens:
        print (t+ "\t" + get_etiqueta(t))        
        pass

"""si una variable no esta en la tabla de variables retorna un falso, si ya se encuentra retornara un verdadero"""
def existe_var(v, tabla_var):
    existe = False
    for variable in tabla_var:
        if v == variable.nombre :
            existe = True
    return existe

"""
Funcion que imprime si la sintaxis es correcta.
Si comienza con un "var" pasa al siguiente estado,
si­ lo que tenemos es un tipo pasa al siguiente estado, sino imprime 1
si­ lo que tenemos es un id pasa al siguiente estado, sino imprime 2
si­ lo que tenemos es un ";" pasa al siguiente estado, pero si es una "," se regresa al estado B, sino imprime 3
si­ lo que tenemos ees un main pasa al estado "z", si es un "tipo" regresa al estado B, sino imprime 4
si­ estamos en el estado "z" imprime un 0
si no aplica ningun caso imprime un 5
si la variable ya exste imprime un 6

"""
def verifica_declara_var(tokens):
    '''
    si todo es correcto devuelve 0, de lo contrario devuelve un número que corresponde a un código de error
    '''
    tipo = ""       #semántico
    tabla_var = []  #semántico
    estado = "Z"    
    for t in tokens:
        if estado == "Z" and t=="var":
            estado = "A"
        elif (estado =="A"):
            if get_etiqueta(t)=="tipo":
                estado = "B"
            else:
                print("error, se esperaba un tipo")
                return 1
        elif (estado =="B"):
            tipo = t  #parte del análisis semántico
            if get_etiqueta(t)=="id":
                estado = "C"
                # ----------------------------------------
                # esto es parte del análisis semantico               
                if existe_var(t, tabla_var): #variable repetida
                    print("error, variable redeclarada:",t)
                    return 6
                else:
                    tabla_var.append(Variable(t, tipo))
                #-----------------------------------------
            else:
                print("error, se esperaba ID")
                return 2
        elif (estado =="C"):
            if(t==";"):
                estado = "D"
            elif (t==","):
                estado = "B"
            else:
                print('error, se esperaba ";"')
                return 3
        elif (estado =="D"):
            if (t=="main"):
                estado = "Z"
            elif(get_etiqueta(t)=="tipo"):
                estado = "B"
            else:
                print("Error, se esperaba tipo")
                return 4
    if estado == "Z":
        return 0
    else:
        return 5
    
"""funcion que determina la prioridad de los operadores"""
def obtenerPrioridadOperador(o):
    # Función que trabaja con convertirInfijaA**.
    return {'(':1,')':2,'+':3,'-':3,'*':4,'/':4,'^':5}.get(o)

'''Convierte una expresión infija a una posfija, devolviendo una lista.'''
def infija2Posfija(infija):
    
    pila = []
    salida = []
    for e in infija:
        if e == '(':
            pila.append(e)
        elif e ==')':
            while pila[len(pila) - 1 ] != '(':
                salida.append(pila.pop())
            pila.pop()
        elif e in ['+','-','*','/','^']:
            while (len(pila) != 0) and (obtenerPrioridadOperador(e)) <= obtenerPrioridadOperador(pila[len(pila) - 1]):
                salida.append(pila.pop())
            pila.append(e)
        else:
            salida.append(e)
    while len(pila) != 0:
        salida.append(pila.pop())
    return salida

'''recibe una expresión posfija, la convierte en código intermedio'''
def posfija_a_intermedio(posfija):
    intermedio = []
    codigo = []
    pila = []
    temp = 1
    for e in posfija:
        if e in ['+','-','*','+']:
            op2 = pila.pop()
            op1 = pila.pop()
            intermedio.append('t'+str(temp).zfill(2)+"="+op1+e+op2)
            codigo.append('LDA ' +op1+';')
            if e=="+":
                codigo.append('ADD '+op2+';')
            if e=="-":
                codigo.append('SUB '+op2+";")
            if e=="*":
                codigo.append('MUL '+op2+";")
            if e=="/":
                codigo.append('SUB '+op2+";")
            codigo.append('STA '+'t'+str(temp).zfill(2)+';')
            pila.append('t'+str(temp).zfill(2))
            temp += 1
        else:
            pila.append(e)
    if (len(pila)==1): #solo debe quedar un elemento en la pila
        return intermedio, codigo
    else:
        print("expresión no válida")
        return None

'''recibe una expresión posfija, la convierte en código intermedio'''
def evalua_posfija(posfija):
    pila = []
    for e in posfija:
        if get_etiqueta(e)=='entero':
            pila.append(int(e))
        elif get_etiqueta(e)=='flotante':
            pila.append(float(e))
        elif e in ['+','-','*','+']:
            op2 = pila.pop()
            op1 = pila.pop()
            if e=='+':
                pila.append(op1+op2)
            elif e=='-':
                pila.append(op1-op2)
            elif e=='*':
                pila.append(op1*op2)
            elif e=='/':
                pila.append(op1/op2)
            else:
                print("error")
                return None
    if (len(pila)==1): #solo debe quedar un elemento en la pila
        return pila[0]
    else:
        print('expresión no válida')
        return None

p = infija2Posfija(["1","*","2","+","3","*","4"])
print(p)
print(evalua_posfija(p))

p = infija2Posfija(["a","*","b","+","c","*","d"])
cod_intermedio, codigo = posfija_a_intermedio(p)
print(cod_intermedio)
print()
print(codigo)
print()
quita_comentarios("uno.txt", "dos.txt")
tokens2=separa_tokens2("dos.txt")
imprime_tabla_tokens(tokens2)
variables_validas=verifica_declara_var(tokens2)
print("Variables validas si devuelve 0: ",variables_validas)
