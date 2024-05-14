archivo = open("programa.taan", "r")

reservadas = ["chuunbes", "xuul", "antal", "waa", "tuun", "achak", "lxtak"]
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
            if num_decimal not in tabla_datos[1]:
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

# Ejecutar funciones
separar_tokens()
identificar_tipo()
imprimir_resultados()
