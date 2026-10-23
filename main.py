from narrativa import MotorNarrativo
from pila_mundo import PilaMundo
from gramatica import Gramatica
from combate import Combate


juego = MotorNarrativo()
mundo = PilaMundo()
gramatica = Gramatica()

inventario = []

tiene_espada = False
tiene_llave = False
tiene_fragmento = False


def mostrar_inventario():
    print("\n--- INVENTARIO ---")

    if len(inventario) == 0:
        print("Inventario vacío.")
    else:
        for objeto in inventario:
            print("-", objeto)

    print("------------------")


print("==========================================")
print("   EL REINO DE VALDORIA")
print("      LA CORONA FRAGMENTADA")
print("==========================================")

print("\nEl reino se encuentra bajo el control de Malakar.")
print("Tu aventura comienza en el Pueblo de Arden.")

juego.transicion("iniciar")


while not juego.es_estado_final():



    if juego.estado_actual == "q1":

        juego.mostrar_estado()

        print("\nAnciano Eldran:")
        print(gramatica.generar_dialogo())

        print("\n1. Aceptar la misión")
        print("2. Abandonar la aventura")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            juego.transicion("aceptar")

        elif opcion == "2":
            juego.transicion("abandonar")

        else:
            print("\nOpción no válida.")



    elif juego.estado_actual == "q2":

        juego.mostrar_estado()

        print("\nTe encuentras en el Bosque Sombrío.")

        print("\n1. Explorar")
        print("2. Ver inventario")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            juego.transicion("explorar")

        elif opcion == "2":
            mostrar_inventario()

        else:
            print("\nOpción no válida.")



    elif juego.estado_actual == "q3":

        juego.mostrar_estado()

        print("\nHas encontrado un campamento abandonado.")

        if not tiene_espada:

            print("Encontraste una espada.")

            inventario.append("Espada")
            tiene_espada = True

        else:
            print("Ya recogiste la espada anteriormente.")

        mostrar_inventario()

        input("\nPresiona ENTER para regresar al bosque...")

        juego.transicion("regresar")


    elif juego.estado_actual == "q4":

        juego.mostrar_estado()

        print("\nHas encontrado las Ruinas Antiguas.")

        if not tiene_llave:

            print("\nEncontraste una Llave Antigua.")
            inventario.append("Llave Antigua")
            tiene_llave = True

        if not tiene_fragmento:

            print("Utilizas la llave para abrir una cámara secreta.")
            print("Dentro encuentras el Fragmento de la Corona.")

            inventario.append("Fragmento de la Corona")
            tiene_fragmento = True

        mostrar_inventario()

        print("\nMisión secundaria:")
        print(gramatica.generar_mision())

        print("\n1. Ir hacia el Castillo de Valdoria")
        print("2. Regresar al bosque")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            juego.transicion("ir_castillo")

        elif opcion == "2":
            juego.estado_actual = "q2"

        else:
            print("\nOpción no válida.")



    elif juego.estado_actual == "q5":

        juego.mostrar_estado()

        if tiene_fragmento:

            print("\nEl Fragmento de la Corona reacciona frente al castillo.")
            print("La entrada está disponible.")

            print("\n1. Entrar al castillo")
            print("2. Ver inventario")

            opcion = input("\nSelecciona una opción: ")

            if opcion == "1":

                mundo.entrar("Castillo")
                juego.transicion("entrar")

            elif opcion == "2":

                mostrar_inventario()

            else:

                print("\nOpción no válida.")

        else:

            print("\nNo puedes continuar.")
            print("Necesitas encontrar el Fragmento de la Corona.")

            juego.estado_actual = "q2"



    elif juego.estado_actual == "q6":

        juego.mostrar_estado()

        if mundo.ubicacion_actual() != "Mazmorra":
         mundo.entrar("Mazmorra")

        print("\nTe encuentras dentro de la mazmorra del castillo.")

        print("\nGuardia Rowan:")
        print(gramatica.generar_dialogo())

        print("\nUbicación actual:", mundo.ubicacion_actual())

        print("\n1. Avanzar hacia la Sala del Trono")
        print("2. Ver pila del mundo")
        print("3. Ver inventario")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":

            juego.transicion("avanzar")

        elif opcion == "2":

            mundo.mostrar_pila()

        elif opcion == "3":

            mostrar_inventario()

        else:

            print("\nOpción no válida.")



    elif juego.estado_actual == "q7":

        if mundo.ubicacion_actual() != "Sala del Trono":
         mundo.entrar("Sala del Trono")

        juego.mostrar_estado()

        print("\nFinalmente encuentras a Malakar.")

        print("\nMalakar:")
        print("Entrégame el Fragmento de la Corona y podrás marcharte.")

        print("\n1. Luchar contra Malakar")
        print("2. Entregar el Fragmento")
        print("3. Ver inventario")
        print("4. Ver pila del mundo")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":

            juego.transicion("luchar")

            combate = Combate(tiene_espada)

            resultado = combate.iniciar()

            if resultado == "ganar":
                juego.transicion("ganar")

            else:
                juego.transicion("perder")

        elif opcion == "2":

            juego.transicion("entregar")

        elif opcion == "3":

            mostrar_inventario()

        elif opcion == "4":

            mundo.mostrar_pila()

        else:

            print("\nOpción no válida.")




print("\n==========================================")

if juego.estado_actual == "q8":

    print("FINAL DEL HÉROE")
    print("\nHas derrotado a Malakar.")
    print("El Fragmento de la Corona queda protegido.")
    print("Valdoria comienza a recuperar la paz.")

elif juego.estado_actual == "q9":

    print("FINAL DEL ABANDONO")
    print("\nDecidiste abandonar la misión.")
    print("Malakar continúa controlando el castillo.")

elif juego.estado_actual == "q10":

    print("FINAL OSCURO")
    print("\nMalakar consigue el Fragmento de la Corona.")
    print("Su poder sobre Valdoria continúa creciendo.")

print("\nFIN DEL JUEGO")
print("==========================================")