import random


class Combate:

    def __init__(self, tiene_espada=False):
        self.vida_jugador = 20
        self.vida_enemigo = 20
        self.tiene_espada = tiene_espada

    def ataque_jugador(self):
        numero = random.randint(1, 100)

        if numero <= 70:
            dano = 7 if self.tiene_espada else 5
            return "normal", dano

        elif numero <= 90:
            dano = 12 if self.tiene_espada else 10
            return "critico", dano

        else:
            return "esquive", 0

    def ataque_enemigo(self):
        numero = random.randint(1, 100)

        if numero <= 70:
            return "normal", 5

        elif numero <= 90:
            return "critico", 10

        else:
            return "esquive", 0

    def turno_jugador(self):
        tipo, dano = self.ataque_jugador()

        if tipo == "normal":
            print("\nGolpe normal del jugador.")

        elif tipo == "critico":
            print("\n¡Golpe crítico del jugador!")

        else:
            print("\nMalakar esquivó el ataque.")

        self.vida_enemigo -= dano

        if self.vida_enemigo < 0:
            self.vida_enemigo = 0

        print("Vida de Malakar:", self.vida_enemigo)

    def turno_enemigo(self):
        tipo, dano = self.ataque_enemigo()

        if tipo == "normal":
            print("\nMalakar realizó un golpe normal.")

        elif tipo == "critico":
            print("\n¡Malakar realizó un golpe crítico!")

        else:
            print("\nEl jugador esquivó el ataque.")

        self.vida_jugador -= dano

        if self.vida_jugador < 0:
            self.vida_jugador = 0

        print("Vida del jugador:", self.vida_jugador)

    def iniciar(self):

        print("\n==============================")
        print("        COMBATE FINAL")
        print("==============================")

        if self.tiene_espada:
            print("\nLa Espada aumenta el daño de tus ataques.")

        while self.vida_jugador > 0 and self.vida_enemigo > 0:

            print("\nVida jugador:", self.vida_jugador)
            print("Vida Malakar:", self.vida_enemigo)

            input("\nPresiona ENTER para atacar...")

            self.turno_jugador()

            if self.vida_enemigo <= 0:
                print("\nHas derrotado a Malakar.")
                return "ganar"

            self.turno_enemigo()

            if self.vida_jugador <= 0:
                print("\nMalakar te ha derrotado.")
                return "perder"