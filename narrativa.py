import random


class MotorNarrativo:

    def __init__(self):
        self.estado_actual = "q0"

        self.estados = {
            "q0": "Inicio de la aventura",
            "q1": "Pueblo de Arden",
            "q2": "Bosque Sombrío",
            "q3": "Campamento abandonado",
            "q4": "Ruinas antiguas",
            "q5": "Castillo de Valdoria",
            "q6": "Mazmorra",
            "q7": "Sala del trono",
            "q8": "Final del Héroe",
            "q9": "Final del Abandono",
            "q10": "Final Oscuro"
        }

        self.estados_finales = ["q8", "q9", "q10"]

    def mostrar_estado(self):
        print("\n----------------------------")
        print("Estado actual:", self.estado_actual)
        print("Escena:", self.estados[self.estado_actual])
        print("----------------------------")

    def transicion(self, accion):

        if self.estado_actual == "q0" and accion == "iniciar":
            self.estado_actual = "q1"

        elif self.estado_actual == "q1" and accion == "aceptar":
            self.estado_actual = "q2"

        elif self.estado_actual == "q1" and accion == "abandonar":
            self.estado_actual = "q9"

        elif self.estado_actual == "q2" and accion == "explorar":
            opciones = ["q3", "q4"]
            self.estado_actual = random.choice(opciones)

        elif self.estado_actual == "q3" and accion == "regresar":
            self.estado_actual = "q2"

        elif self.estado_actual == "q4" and accion == "ir_castillo":
            self.estado_actual = "q5"

        elif self.estado_actual == "q5" and accion == "entrar":
            self.estado_actual = "q6"

        elif self.estado_actual == "q6" and accion == "avanzar":
            self.estado_actual = "q7"

        elif self.estado_actual == "q7" and accion == "luchar":
            self.estado_actual = "q7"

        elif self.estado_actual == "q7" and accion == "ganar":
            self.estado_actual = "q8"

        elif self.estado_actual == "q7" and accion == "perder":
            self.estado_actual = "q10"

        elif self.estado_actual == "q7" and accion == "entregar":
            self.estado_actual = "q10"

        else:
            print("Esa acción no es válida en este estado.")

    def es_estado_final(self):
        return self.estado_actual in self.estados_finales