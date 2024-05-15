"""
<PROGRAMA> -> CHUUNBES <STMTS> XUUL
<STMTS> -> <STMT> <STMTS> | <STMT>
<STMT> -> VARIABLE ANTAL <OP>
<STMT> -> TSIIB TEXTO
<STMT> -> WAA <CONDICION> CHUUNBES <STMTS> XUUL
<STMT> -> WAA <CONDICION> CHUUNBES <STMTS> XUUL ACHAK WAA
<CONDICION> CHUUNBES <STMTS> XUUL
<STMT> IXTAK <CONDICION> CHUUNBES <STMTS> XUUL
<CONDICION> -> <EL> COMPARADOR <EL>
<EL> -> VARIABLE | NUMERO
<OP> -> NUMERO OPERADOR NUMERO | NUMERO | TEXTO
"""

tokens = []
index = 0

def cargar_tokens():
    with open("lenguajeTaan/tokens.lex", "r") as archivo:
        global tokens
        tokens = [line.strip() for line in archivo.readlines()]

def programa():
    if token_actual() != "chuunbes":
        error("Se esperaba 'chuunbes' al inicio del programa")
        return False
    siguiente_token()
    if not stmts():
        return False
    if token_actual() != "xuul":
        error("Se esperaba 'xuul' al final del programa")
        return False
    siguiente_token()
    return True

def stmts():
    if not stmt():
        return False
    if token_actual() == "xuul" or token_actual() == "":
        return True
    return stmts()

def stmt():
    if token_actual() == "[id]":
        return asignacion()
    elif token_actual() == "tsiib":
        return imprimir()
    elif token_actual() == "waa":
        return condicional()
    elif token_actual() == "ixtak":
        return loop()
    else:
        error("Sentencia desconocida o inesperada")
        return False

def asignacion():
    variable = token_actual()
    siguiente_token()
    if token_actual() != "antal":
        error(f"Se esperaba 'antal' después de la variable {variable}")
        return False
    siguiente_token()
    if not op():
        return False
    return True

def imprimir():
    siguiente_token()
    if token_actual() != "[txt]":
        error("Se esperaba un texto después de 'tsiib'")
        return False
    siguiente_token()
    return True

def condicional():
    """siguiente_token()
    if not condicion():
        return False
    if token_actual() == "chuunbes":
        siguiente_token()
        if not stmts():
            return False
        if token_actual() != "xuul":
            error("Se esperaba 'xuul' después de los enunciados de 'waa'")
            return False
        siguiente_token()
        if token_actual() == "achak":
            siguiente_token()
            if token_actual() != "waa":
                error("Se esperaba 'waa' después de 'achak'")
                return False
            siguiente_token()
            if not stmts():
                return False
            if token_actual() != "xuul":
                error("Se esperaba 'xuul' después de los enunciados de 'achak waa'")
                return False
            siguiente_token()
    elif token_actual() == "xuul":
        siguiente_token()
    else:
        error("Se esperaba 'chuunbes' o 'xuul' después de la condición")
        return False
    return True"""
    siguiente_token()
    if not condicion():
        return False
    if token_actual() != "tuun":
        error("Se esperaba 'tuun' después de la condición")
        return False
    siguiente_token()
    if token_actual() != "chuunbes":
        error("Se esperaba 'chuunbes' después de la condición")
        return False
    siguiente_token()
    if not stmts():
        return False
    if token_actual() != "xuul":
        error("Se esperaba 'xuul' después de los enunciados de 'waa'")
        return False
    siguiente_token()
    if token_actual() == "achak":
        siguiente_token()
        if token_actual() != "waa":
            error("Se esperaba 'waa' después de 'achak'")
            return False
        siguiente_token()
        if token_actual() != "chuunbes":
            error("Se esperaba 'chuunbes' después de la condición")
            return False
        siguiente_token()
        if not stmts():
            return False
        if token_actual() != "xuul":
            error("Se esperaba 'xuul' después de los enunciados de 'achak waa'")
            return False
        siguiente_token()
    return True

def loop():
    siguiente_token()
    if not condicion():
        return False
    if token_actual() != "chuunbes":
        error("Se esperaba 'chuunbes' después de la condición de 'lxtak'")
        return False
    siguiente_token()
    if not stmts():
        return False
    if token_actual() != "xuul":
        error("Se esperaba 'xuul' después de los enunciados de 'lxtak'")
        return False
    siguiente_token()
    return True

def condicion():
    if not el():
        return False
    if token_actual() not in ["[op_rel]"]:
        error("Se esperaba un operador relacional en la comparación")
        return False
    siguiente_token()
    if not el():
        return False
    return True

def el():
    if token_actual() not in ["[id]", "[num]"]:
        error("Se esperaba un identificador o número")
        return False
    siguiente_token()
    return True

def op():
    if token_actual() in ["[num]", "[id]", "[txt]"]:  # Permitir identificadores también, además de números y textos
        siguiente_token()
        if token_actual() in ["[op_ar]"]:  # Si hay un operador aritmético, espera otra parte de la expresión
            siguiente_token()
            if token_actual() not in ["[num]", "[id]", "[txt]"]:  # Permitir números, identificadores o textos
                error("Se esperaba un número, identificador o texto después del operador")
                return False
            siguiente_token()
        return True
    else:
        error("Se esperaba un número, identificador o texto después de 'antal'")
        return False

def token_actual():
    global index
    if index < len(tokens):
        return tokens[index]
    return ""

def siguiente_token():
    global index
    index += 1

def error(mensaje):
    print(f"Error en la compilación: {mensaje} en el token '{token_actual()}' en la posición {index+1}")

# Cargar tokens desde el archivo y comenzar análisis
def analizador_sintactico():
    cargar_tokens()
    if programa():
        print("Compilación exitosa")
    else:
        print("Error en la compilación")