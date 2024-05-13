tokens = []
index = 0
pila = []

def cargar_tokens():
    with open("programa.lex", "r") as archivo:
        global tokens
        tokens = archivo.readlines()

def pertenece_al_lenguaje():
    if token_actual() != "chuunbes":
        error("Se esperaba 'chuunbes' al inicio del programa")
        return False
    pila.append("xuul")  # Esperamos un 'xuul' al final
    siguiente_token()
    while token_actual() != "xuul":
        if not nueva_sentencia():
            return False
    siguiente_token()  # Pasar el 'xuul' de fin del programa
    if len(pila) == 0 and token_actual() == "":
        print("Compilación exitosa")
        return True
    else:
        error("Tokens sobrantes en pila o en el código")
        return False

def nueva_sentencia():
    if token_actual() == "waa":
        pila.append("xuul")  # Se espera 'xuul' al final del bloque condicional
        return condicional()
    elif token_actual() == "[id]":
        return asignacion()
    elif token_actual() == "tsiib":
        return imprimir()
    else:
        error("Sentencia desconocida o inesperada")
        return False

def condicional():
    siguiente_token()  # Pasar 'waa'
    if not comparacion():
        return False
    if token_actual() == "chuunbes":
        siguiente_token()
        while token_actual() != "xuul":
            if not nueva_sentencia():
                return False
        siguiente_token()  # Pasar el 'xuul'
        pila.pop()  # Eliminamos el 'xuul' esperado de la pila
        return True
    else:
        error("Se esperaba 'chuunbes' después de la condición")
        return False

def asignacion():
    siguiente_token()  # Pasar [id]
    if token_actual() != "antal":
        error("Se esperaba 'antal' para asignación")
        return False
    siguiente_token()  # Pasar 'antal'
    if token_actual() not in ["[num]", "[id]", "[txt]"]:
        error("Se esperaba un valor, variable o texto después de 'antal'")
        return False
    siguiente_token()  # Pasar valor/variable
    return True

def imprimir():
    siguiente_token()  # Pasar 'tsiib'
    if token_actual() not in ["[txt]", "[id]"]:
        error("Se esperaba un texto o identificador después de 'tsiib'")
        return False
    siguiente_token()  # Pasar texto o identificador
    return True

def comparacion():
    if token_actual() != "[id]":
        error("Se esperaba un identificador en la comparación")
        return False
    siguiente_token()  # Pasar [id]
    if token_actual() not in ["[op_rel]"]:
        error("Se esperaba un operador relacional en la comparación")
        return False
    siguiente_token()  # Pasar [op_rel]
    if token_actual() not in ["[id]", "[num]"]:
        error("Se esperaba un identificador o número en la comparación")
        return False
    siguiente_token()  # Pasar [id] o [num]
    return True

def token_actual():
    global index
    if index < len(tokens):
        return tokens[index].strip()
    return ""

def siguiente_token():
    global index
    index += 1

def error(mensaje):
    print(f"Error en la compilación: {mensaje} en el token '{token_actual()}' en la posición {index}")

# Cargar tokens desde el archivo y comenzar análisis
cargar_tokens()
pertenece_al_lenguaje()
