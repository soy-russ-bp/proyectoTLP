'''
Reglas:
<PROG> → PROGRAMA [id] <SENTS> FINPROG
<SENTS> → <SENT> <SENTS>
<SENTS> → <SENT>
<SENT> → [id] = <ELEM> [op_ar] <ELEM>
<SENT> → [id] = <ELEM>
<SENT> → SI <COMPARA> ENTONCES <SENTS> SINO <SENTS> FINSI
<SENT> → SI <COMPARA> ENTONCES <SENTS> FINSI
<SENT> → REPITE <ELEM> VECES <SENTS> FINREP
<SENT> → IMPRIME <ELEM>
<SENT> → IMPRIME [txt]
<SENT> → LEE [id]
<SENT> → # [comentario]
<ELEM> → [id]
<ELEM> → [val]
<COMPARA> → [id] [op_rel] <ELEM>
'''
'''
<PROGRAMA> -> CHUUNBES <STMTS> XUUL

<STMTS> -> <STMT> <STMTS> | <STMT>

<STMT> -> VARIABLE ANTAL <OP>

<STMT> -> TSIIB TEXTO

<STMT> -> WAA <CONDICION> CHUUNBES <STMTS> XUUL 

<STMT> -> WAA <CONDICION> CHUUNBES <STMTS> XUUL ACHAK WAA <CONDICION> CHUUNBES <STMTS>

<STMT> LXTAK <CONDICION> CHUUNBES <STMTS> XUUL

<CONDICION> ->  <EL> COMPARADOR <EL> 
<EL> -> VARIABLE | NUMERO
<OP> -> NUMERO OPERADOR NUMERO | NUMERO | TEXTO

Palabras reservadas del lenguaje (cada una es un token)
•	chuunbes (inicio)
•	xuul (fin)
•	antal (es)
•	waa (si)
•	tuun (entonces)
•	achak (sino)
•	lxtak (desde)
•	COMPARADOR
•	OPERADOR
•	(
•	)
•	TEXTO
•	VARIABLE
•	NUMERO

'''
#Cambiar nombre de archivo
tokens = open("factorial.lex", "r").readlines()

pila = []
index = 0

def PerteneceAlLenguaje():
    pila.append("FINPROG") #xull
    if Token() != "PROGRAMA\n": #chuunbes
        print(Token())
        Error("Error en Programa")
        return
    Next()
    if Token() != "[id]\n": #VARIABLE/numero
        Error("Error en Programa 2")
        return
    Next()
    nuevaSentencia()

def nuevaSentencia():
    if Token() == "SI\n": #WAA
        pila.append("FINSI") # Considerando que en las reglas se con pone chuunbes y xuul (inicio y fin) cuando se usa el si<condicion>entonces (waa <condicion> tuun) y el sino, significa que despues de el si y el
                            #sino se usa un chuunbes y xuul
        Si()
        return

    elif Token() == "[id]\n": #VARIABLE/NUMERO
        Id()
        return

    elif Token() == "IMPRIME\n": #TSIIB
        Imprime()
        return

    elif Token() == "LEE\n": #???
        Lee()
        return

    elif Token() == "REPITE\n": #lxtak (desde)?
        pila.append("FINREP")
        Repite()
        return

    elif Token() == "SINO\n": #ACHAK
        if UltimoDePila() == "FINSI":
            Next()
            nuevaSentencia()
            return
        else:
            Error("Error en sino")
            return

    elif Token() == "FINSI\n":# Considerando que en las reglas se con pone chuunbes y xuul (inicio y fin) cuando se usa el si<condicion>entonces (waa <condicion> tuun) y el sino, significa que despues de el si y el
                            #sino se usa un chuunbes y xuul
        if UltimoDePila() == "FINSI":
            SacarDePila()
            Next()
            nuevaSentencia()
            return
        else:
            Error("Error en finsi")
            return

    elif Token() == "FINREP\n": #Ver la misma cuestion que en el si (se usa chuunbes y xul)
        if UltimoDePila() == "FINREP":
            SacarDePila()
            Next()
            nuevaSentencia()
            return
        else:
            Error("Error en finrep")
            return

    elif Token() == "FINPROG\n": #xuul,  pero considerar que no es exclusivo para finalizar el programa
        if UltimoDePila() == "FINPROG":
            SacarDePila()
            print("Compilacion exitosa")
            return
        else:
            Error("Error en finprog")
            return
        
    Error("FALLO EN LA DETECCION")
    
    

def Id():
    Next()
    if Token() != "=\n":
        Error("Error en id, deberia ser =")
        return
    Next()

    if Token() != "[id]\n":
        if Token() != "[val]\n":
            Error("Error en id, deberia ser id o val")
            return
    Next()

    if Token() != "[op_ar]\n":
        nuevaSentencia()
        return
    Next()

    if Token() != "[id]\n":
         if Token() != "[val]\n":
            Error("Error en id")
            return
    Next()
    nuevaSentencia()

def Si():
    Next()
    if Token() != "[id]\n":
        Error("Error en Si")
        return
    Next()
    if Token() != "[op_rel]\n":
        Error("Error en Si")
        return
    Next()

    if Token() != "[id]\n":
        if Token != "[val]\n":
            Error("Error en Si")
            return
    Next()
    if Token() != "ENTONCES\n":
        Error("Error en Si")
        return
    Next()
    nuevaSentencia()

def Repite():
    Next()
    if Token() != "[id]\n":
        if Token() != "[val]\n":
            Error("Error en Repite")
            return
    Next()
    if Token() != "VECES\n":
        Error("Error en Repite")
        return
    Next()
    nuevaSentencia()

def Imprime():
    Next()
    if Token() != "[id]\n":
        if Token() != "[val]\n":
            if Token() != "[txt]\n":
                Error("Error en Imprime")
                return
    Next()
    nuevaSentencia()

def Lee():
    Next()
    if Token() != "[id]\n":
        Error("Error en lee")
        return
    Next()
    nuevaSentencia()

def SacarDePila():
    pila.pop()

def UltimoDePila():
    return pila[len(pila)-1]

def Token():
    global index
    return tokens[index]

def SigToken():
    global index
    return tokens[index + 1]

def Next():
    global index
    index = index + 1

def Error(debugText):
    print(Token(), index)
    print("Error en compilacion")
    print(debugText)

PerteneceAlLenguaje()