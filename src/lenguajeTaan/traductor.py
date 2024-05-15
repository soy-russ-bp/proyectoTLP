def taan_a_python(archivo_taan, archivo_py):
    # Leer el archivo .taan
    with open(archivo_taan, "r") as file:
        lineas = file.readlines()

    # Analizar cada línea y construir el código Python
    codigo_python = []
    indentacion = 0
    for linea in lineas:
        tokens = linea.strip().split()
        if not tokens:
            continue
        if tokens[0] == "chuunbes":
            codigo_python.append("    " * indentacion + "def bloque():")
            indentacion += 1
        elif tokens[0] == "xuul":
            indentacion -= 1
        elif tokens[0] == "antal":
            # Convertir la asignación a Python
            var = tokens[1]
            valor = tokens[2]
            if "," in valor:
                valor = valor.replace(",", ".")  # Conversión simplificada
            codigo_python.append("    " * indentacion + f"{var} = {valor}")
        elif tokens[0] == "waa" and tokens[2] == "<":
            condicion = f"{tokens[1]} < {tokens[3]}"
            codigo_python.append("    " * indentacion + f"if {condicion}:")
            indentacion += 1
        elif tokens[0] == "tuun":
            indentacion -= 1
        elif tokens[0] == "tsiib":
            texto = ' '.join(tokens[1:])
            codigo_python.append("    " * indentacion + f"print({texto})")

    # Escribir el resultado en un archivo .py
    with open(archivo_py, "w") as file:
        file.write("\n".join(codigo_python))

# Ejemplo de uso:
taan_a_python("lenguajeTaan/programa.taan", "programa.py")
