import random


class Gramatica:

    def __init__(self):
        self.acciones = [
            "Busca",
            "Encuentra",
            "Lleva"
        ]

        self.objetos = [
            "la espada",
            "la poción"
        ]

        self.npcs = [
            "el anciano Eldran",
            "el guardia Rowan"
        ]

        self.saludos = [
            "Saludos aventurero.",
            "Escucha con atención.",
            "Necesito tu ayuda."
        ]

        self.mensajes = [
            "El bosque es peligroso.",
            "Malakar controla el castillo.",
            "Debes proteger el fragmento.",
            "Ten cuidado durante tu camino."
        ]

    def generar_mision(self):
        accion = random.choice(self.acciones)
        objeto = random.choice(self.objetos)
        npc = random.choice(self.npcs)

        return f"{accion} {objeto} para {npc}."

    def generar_dialogo(self):
        saludo = random.choice(self.saludos)
        mensaje = random.choice(self.mensajes)

        return f"{saludo} {mensaje}"