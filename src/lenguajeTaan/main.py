import Analex
import Anasin
import Traductor
import runpy
path = "lenguajeTaan/programa.taan"

lenguaje_aceptado = Analex.analizador_lexico(path)
compilacion_exitosa=Anasin.analizador_sintactico()

if(lenguaje_aceptado and compilacion_exitosa):
    print("\nSalida del programa:")
    Traductor.traducir_archivo_taan(path, "traduccion.py")
    runpy.run_path("traduccion.py")
    