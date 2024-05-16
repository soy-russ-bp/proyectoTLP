import Analex
import Anasin

# Diccionario de equivalencias de palabras reservadas de Taan a Python
traducciones = {
    'chuunbes': '',  # Inicialmente definido para definir una función, pero no usado aquí
    'xuul': '',  # No directamente utilizado, solo para controlar la indentación
    'antal': '=',  # Operador de asignación
    'waa': 'if',  # Instrucción condicional if
    'tuun': ':',  # Inicio de bloque de código
    'tsiib': 'print(',  # Inicio de la función print en Python
    'ixtak': 'while',  # Instrucción de bucle while
    'achak': 'elif',  # Instrucción condicional elif
}

def traducir_linea(linea, nivel_indentacion):
    tokens = linea.strip().split() 
    linea_traducida = []
    indentacion = '    ' * nivel_indentacion  # Crea una indentación basada en el nivel actual
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in traducciones:
            if token == 'tuun':  # 'tuun' indica un nuevo bloque de código
                linea_traducida.append(':')
                break  # Finaliza el procesamiento de la línea
            elif token == 'tsiib':  # Manejo especial para print
                linea_traducida.append(traducciones[token])  # Añade 'print('
                i += 1  # Avanza al siguiente token, que es el primer parámetro
                # Maneja múltiples parámetros hasta final de línea o xuul
                while i < len(tokens) and tokens[i] != 'xuul':
                    if tokens[i].startswith('"'):  # Si es una cadena literal
                        # Agrega el texto directamente
                        linea_traducida.append(tokens[i])
                    else:
                        # Añade el resto de tokens directamente, asumiendo que son variables o expresiones
                        linea_traducida.append(' ' + tokens[i])
                    i += 1
                linea_traducida.append(')')  # Cierra la función print
                continue
            elif token == 'ixtak':  # 'manejo especial para while'
                linea_traducida.append(traducciones[token])  # Añade 'while'
                i += 1  # Avanza al siguiente token, que es la condición
                # Añade la condición, pero si es número, lo convierte
                while i < len(tokens) and tokens[i] != '\n':
                    if Analex.es_numero(tokens[i]): # Si el token es un número
                        numero_traducido = Analex.convertir_numero(tokens[i])
                        linea_traducida.append(str(numero_traducido))
                    elif Analex.es_identificador(tokens[i]):  # Si el token es un identificador
                        linea_traducida.append(tokens[i])
                    elif tokens[i] in Analex.operadoresR:  # Si el token es un operador de comparación
                        linea_traducida.append(tokens[i])
                    i += 1
                linea_traducida.append(':')
            elif token == 'achak':  # 'manejo especial para elif'
                linea_traducida.append(traducciones[token])  # Añade 'elif'
                i += 1  # Avanza al siguiente token, que es la condición
                # Añade la condición, pero si es número, lo convierte
                while i < len(tokens) and tokens[i] != 'tuun':
                    if tokens[i] == 'waa': # Si el token es un if
                        pass
                    elif Analex.es_numero(tokens[i]): # Si el token es un número
                        numero_traducido = Analex.convertir_numero(tokens[i])
                        linea_traducida.append(str(numero_traducido))
                    elif Analex.es_identificador(tokens[i]):  # Si el token es un identificador
                        linea_traducida.append(tokens[i])
                    elif tokens[i] in Analex.operadoresR:  # Si el token es un operador de comparación
                        linea_traducida.append(tokens[i])
                    i += 1 
                if i < len(tokens) and tokens[i] == 'tuun':  # Verifica si el token actual es 'tuun'
                    linea_traducida.append(':')
                    
            else:
                linea_traducida.append(traducciones[token])
        elif Analex.es_numero(token):
            numero_traducido = Analex.convertir_numero(token)
            linea_traducida.append(str(numero_traducido))
        elif token in Analex.operadoresA or token in Analex.operadoresR:
            linea_traducida.append(token)
        else:
            linea_traducida.append(token)
        i += 1

    return indentacion + ' '.join(linea_traducida)

def traducir_archivo_taan(path_entrada, path_salida):
    nivel_indentacion = 0
    with open(path_entrada, 'r') as archivo_entrada, open(path_salida, 'w') as archivo_salida:
        for linea in archivo_entrada:
            if linea.strip() and not linea.startswith('#'):
                if 'tuun' in linea:
                    archivo_salida.write(traducir_linea(linea, nivel_indentacion) + '\n')
                    nivel_indentacion += 1
                elif 'ixtak' in linea:
                    archivo_salida.write(traducir_linea(linea, nivel_indentacion) + '\n')
                    nivel_indentacion += 1
                elif 'xuul' in linea:
                    nivel_indentacion -= 1
                else:
                    archivo_salida.write(traducir_linea(linea, nivel_indentacion) + '\n')
