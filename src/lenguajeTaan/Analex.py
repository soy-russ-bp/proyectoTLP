archivo = open("lenguajeTaan/programa2.taan", "r")

reservadas = ["chuunbes", "xuul", "antal", "waa", "tuun", "achak", "lxtak", "tsiib" ]
operadoresA = ["+", "-", "*", "/"]  # Asumimos operadores aritméticos básicos
operadoresR = ["<", ">", "==", "<=", ">="]  # Agregar operadores de comparación completos
asignacion = ["antal"]  # Uso de 'antal' como asignación, similar a 'es'

tokensSeñalados = []
tokens_NA = []
tabla_datos = [[], [], []]

def separar_tokens():
    contenidos = archivo.readlines()
    global tokens 
    tokens = []
    for s in contenidos:
        if s.strip() and not s.startswith("#"):  # Ignora líneas vacías y comentarios
            if '"' in s:
                lineaDiv = s.split('"')
                tokens.append(lineaDiv[0].strip())
                tokens.append('"' + lineaDiv[1] + '"')
            else:
                tokens += s.split()

def es_identificador(s):
    return s[0].isalpha()

def es_numero(s):
    # Verifica si el string es un número según la representación especial
    return set(s).issubset(set('.|,0'))

def convertir_numero(s):
    # Convierte el string del número especial a un número decimal
    partes = s.split(',')
    valor_total = 0
    for i, parte in enumerate(reversed(partes)):
        valor_base = 0
        for ch in parte:
            if ch == '.':
                valor_base += 1
            elif ch == '|':
                valor_base += 5
            elif ch == '0':
                valor_base += 0
        valor_total += valor_base * (20 ** i)
    return valor_total

def es_texto(s):
    return s.startswith('"') and s.endswith('"')

def identificar_tipo():
    num_linea = 1
    for t in tokens:
        num_linea += 1
        if t in reservadas:
            tokensSeñalados.append(t)
        elif t in operadoresA:
            tokensSeñalados.append("[op_ar]")
        elif t in operadoresR:
            tokensSeñalados.append("[op_rel]")
        elif t in asignacion:
            tokensSeñalados.append("[asignacion]")
        elif es_identificador(t):
            tokensSeñalados.append("[id]")
            if t not in tabla_datos[0]:
                tabla_datos[0].append(t)
        elif es_numero(t):
            tokensSeñalados.append("[num]")
            num_decimal = convertir_numero(t)
            tabla_datos[1].append(num_decimal)
        elif es_texto(t):
            tokensSeñalados.append("[txt]")
            if t not in tabla_datos[2]:
                tabla_datos[2].append(t)
        else:
            tokensSeñalados.append(t + "<NA>")
            tokens_NA.append(f"{t}, línea {num_linea}")

def imprimir_resultados():
    print("Tokens Señalados:")
    for token in tokensSeñalados:
        print(token)
    if tokens_NA:
        print("\nTokens No Reconocidos:")
        for token in tokens_NA:
            print(token)
            
def escribir_resultados_en_archivo():
    archivo = open("lenguajeTaan/tokens.lex", "w")
    for token in tokensSeñalados:
        archivo.write(token + "\n")
    if tokens_NA:
        archivo.write("\nTokens No Reconocidos:\n")
        for token in tokens_NA:
            archivo.write(token + "\n")
    archivo.close()
    
    
tabla_simbolos = [ [], [], [] ]
 
def Tabla():
    i = 1
    j = 1
    k = 1
    for fila in tabla_datos:
        for posicion in fila:
            if isinstance(posicion, str):  # Asegurarte de que la posición es una cadena
                if es_identificador(posicion):
                    tabla_simbolos[0].append(posicion + ', ' + "ID" + str(i))
                    #print(f"Añadiendo identificador: {posicion}")
                    i += 1
                elif es_texto(posicion):
                    tabla_simbolos[1].append(posicion + ', ' + "TX" + str(j))
                    #print(f"Añadiendo texto: {posicion}")
                    j += 1
            elif isinstance(posicion, int):  # Asegurarte de que la posición es un entero
                tabla_simbolos[2].append(str(posicion) + ', ' + "VAL" + str(k))
                #print(f"Añadiendo valor numérico: {posicion}")
                k += 1

def archivo_tabla_datos(path):
    with open(path, 'w') as archivo:
        # Identificadores
        archivo.write("IDS\n")
        archivo.write('\n'.join(tabla_simbolos[0]) + '\n\n')

        # Textos
        archivo.write("TXT\n")
        archivo.write('\n'.join(tabla_simbolos[1]) + '\n\n')

        # Números
        archivo.write("VAL\n")
        archivo.write('\n'.join(tabla_simbolos[2]) + '\n')

# Ejecutar funciones
def analizador_lexico():
    separar_tokens()
    identificar_tipo()
    imprimir_resultados()
    escribir_resultados_en_archivo()
    Tabla()
    archivo_tabla_datos("lenguajeTaan/tabla_datos.txt")
