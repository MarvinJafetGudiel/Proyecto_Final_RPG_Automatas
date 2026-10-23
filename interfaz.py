import tkinter as tk

from narrativa import MotorNarrativo
from pila_mundo import PilaMundo
from gramatica import Gramatica
from combate import Combate


class JuegoValdoria:

    def __init__(self, ventana):

        self.ventana = ventana
        self.ventana.title(
            "El Reino de Valdoria - La Corona Fragmentada"
        )

        self.ventana.configure(bg="#101319")
        self.ventana.resizable(False, False)

        ancho = 880
        alto = 560

        pantalla_ancho = self.ventana.winfo_screenwidth()
        pantalla_alto = self.ventana.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.ventana.geometry(
            f"{ancho}x{alto}+{x}+{y}"
        )


        self.FONDO = "#101319"
        self.PANEL = "#191D25"
        self.PANEL2 = "#232832"

        self.DORADO = "#D6B469"
        self.DORADO_CLARO = "#F0D58E"

        self.TEXTO = "#F3F3F3"
        self.SECUNDARIO = "#B8BEC9"

        self.VERDE_MAPA = "#263F2D"
        self.CAMINO = "#927553"

        self.AZUL = "#3D648F"
        self.ROJO = "#813A3A"


        self.narrativa = MotorNarrativo()
        self.mundo = PilaMundo()
        self.gramatica = Gramatica()

        self.inventario = []

        self.tiene_espada = False
        self.tiene_llave = False
        self.tiene_fragmento = False

        self.visito_campamento = False
        self.visito_ruinas = False

        self.ultima_ruta_bosque = None

        self.combate = None
        self.en_combate = False

        self.mensaje_combate = ""

        self.acciones_actuales = []

    

        self.crear_interfaz()

        self.ventana.bind(
            "1",
            self.tecla_1
        )

        self.ventana.bind(
            "2",
            self.tecla_2
        )

        self.narrativa.transicion(
            "iniciar"
        )

        self.actualizar_juego()



    def crear_interfaz(self):


        header = tk.Frame(
            self.ventana,
            bg="#151922",
            height=55
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="EL REINO DE VALDORIA",
            font=("Georgia", 17, "bold"),
            bg="#151922",
            fg=self.DORADO_CLARO
        ).pack(pady=(5, 0))

        tk.Label(
            header,
            text="LA CORONA FRAGMENTADA",
            font=("Arial", 8, "bold"),
            bg="#151922",
            fg=self.SECUNDARIO
        ).pack()




        principal = tk.Frame(
            self.ventana,
            bg=self.FONDO
        )

        principal.pack(
            fill="x",
            padx=10,
            pady=8
        )


        zona_mapa = tk.Frame(
            principal,
            bg=self.PANEL
        )

        zona_mapa.pack(
            side="left"
        )

        tk.Label(
            zona_mapa,
            text="MAPA DE VALDORIA",
            font=("Arial", 10, "bold"),
            bg=self.PANEL,
            fg=self.DORADO
        ).pack(pady=(6, 3))

        self.canvas = tk.Canvas(
            zona_mapa,
            width=560,
            height=300,
            bg=self.VERDE_MAPA,
            highlightthickness=0
        )

        self.canvas.pack(
            padx=6,
            pady=(0, 6)
        )


        derecha = tk.Frame(
            principal,
            bg=self.PANEL2,
            width=285,
            height=330
        )

        derecha.pack(
            side="right",
            padx=(8, 0)
        )

        derecha.pack_propagate(False)


        self.titulo_panel(
            derecha,
            "UBICACIÓN"
        )

        self.lbl_ubicacion = tk.Label(
            derecha,
            text="",
            font=("Arial", 9, "bold"),
            bg=self.PANEL2,
            fg=self.TEXTO
        )

        self.lbl_ubicacion.pack()


        self.titulo_panel(
            derecha,
            "OBJETIVO"
        )

        self.lbl_objetivo = tk.Label(
            derecha,
            text="",
            font=("Arial", 8),
            bg=self.PANEL2,
            fg=self.SECUNDARIO,
            wraplength=250,
            justify="left"
        )

        self.lbl_objetivo.pack(
            padx=10
        )


        self.titulo_panel(
            derecha,
            "INVENTARIO"
        )

        self.lbl_inventario = tk.Label(
            derecha,
            text="Vacío",
            font=("Arial", 8),
            bg=self.PANEL2,
            fg=self.TEXTO,
            justify="left"
        )

        self.lbl_inventario.pack()


        self.titulo_panel(
            derecha,
            "PILA DEL MUNDO"
        )

        self.lbl_pila = tk.Label(
            derecha,
            text="Mundo",
            font=("Courier New", 8),
            bg=self.PANEL2,
            fg="#9DD1A3",
            justify="left"
        )

        self.lbl_pila.pack()


        self.titulo_panel(
            derecha,
            "ACCIONES"
        )

        self.frame_botones = tk.Frame(
            derecha,
            bg=self.PANEL2
        )

        self.frame_botones.pack(
            fill="x",
            padx=10,
            pady=(0, 8)
        )


        marco_historia = tk.Frame(
            self.ventana,
            bg=self.DORADO
        )

        marco_historia.pack(
            fill="x",
            padx=10,
            pady=(0, 8)
        )

        self.lbl_historia = tk.Label(
            marco_historia,
            text="",
            bg="#20252E",
            fg=self.TEXTO,
            font=("Arial", 9),
            justify="left",
            anchor="w",
            wraplength=830,
            padx=12,
            pady=8,
            height=6
        )

        self.lbl_historia.pack(
            fill="x",
            padx=1,
            pady=1
        )


    def titulo_panel(self, padre, texto):

        tk.Label(
            padre,
            text=texto,
            font=("Arial", 8, "bold"),
            bg=self.PANEL2,
            fg=self.DORADO
        ).pack(
            pady=(7, 1)
        )

    def dibujar_mapa(self):

        self.canvas.delete("all")

        estado = self.narrativa.estado_actual

        # Fondo
        self.canvas.create_rectangle(
            0, 0,
            560, 300,
            fill=self.VERDE_MAPA,
            outline=""
        )

        # Luna
        self.canvas.create_oval(
            485, 15,
            525, 55,
            fill="#E6D7A6",
            outline=""
        )

        # Río
        self.canvas.create_line(
            10, 275,
            120, 250,
            230, 265,
            350, 255,
            550, 275,
            fill="#557D96",
            width=10,
            smooth=True
        )

        posiciones = {
            "q1": (65, 155),
            "q2": (170, 155),
            "q3": (280, 230),
            "q4": (280, 75),
            "q5": (400, 155),
            "q6": (500, 220),
            "q7": (500, 75)
        }

        conexiones = [
            ("q1", "q2"),
            ("q2", "q3"),
            ("q2", "q4"),
            ("q4", "q5"),
            ("q5", "q6"),
            ("q6", "q7")
        ]

        # Caminos
        for origen, destino in conexiones:

            x1, y1 = posiciones[origen]
            x2, y2 = posiciones[destino]

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=self.CAMINO,
                width=5
            )

        # Decoración
        for x, y in [
            (120, 55),
            (145, 80),
            (180, 60),
            (205, 85),
            (225, 45),
            (120, 225),
            (155, 250)
        ]:

            self.dibujar_arbol(
                x,
                y
            )

        # Pueblo
        self.dibujar_pueblo(
            *posiciones["q1"],
            estado == "q1"
        )

        # Bosque
        self.dibujar_bosque(
            *posiciones["q2"],
            estado == "q2"
        )

        # Campamento
        self.dibujar_campamento(
            *posiciones["q3"],
            estado == "q3"
        )

        # Ruinas
        self.dibujar_ruinas(
            *posiciones["q4"],
            estado == "q4"
        )

        # Castillo
        self.dibujar_castillo(
            *posiciones["q5"],
            estado == "q5"
        )

        # Mazmorra
        self.dibujar_mazmorra(
            *posiciones["q6"],
            estado == "q6"
        )

        # Trono
        self.dibujar_trono(
            *posiciones["q7"],
            estado == "q7"
        )

        # Personaje
        if estado in posiciones:

            x, y = posiciones[estado]

            self.dibujar_heroe(
                x,
                y - 55,
                "heroe_mapa"
            )


    def resaltar(self, x, y, activo):

        if activo:

            self.canvas.create_oval(
                x - 45,
                y - 40,
                x + 45,
                y + 40,
                fill="#9D762E",
                outline=self.DORADO_CLARO,
                width=3
            )


    def dibujar_pueblo(self, x, y, activo):

        self.resaltar(
            x,
            y,
            activo
        )

        # Casa
        self.canvas.create_rectangle(
            x - 25,
            y - 10,
            x + 25,
            y + 25,
            fill="#9A6941",
            outline="#3B2B20"
        )

        self.canvas.create_polygon(
            x - 32,
            y - 10,
            x,
            y - 38,
            x + 32,
            y - 10,
            fill="#763934",
            outline="#3B2020"
        )

        self.canvas.create_rectangle(
            x - 7,
            y + 5,
            x + 7,
            y + 25,
            fill="#4B3024",
            outline=""
        )

        self.canvas.create_text(
            x,
            y + 40,
            text="Pueblo de Arden",
            fill="white",
            font=("Arial", 7, "bold")
        )

    def dibujar_bosque(self, x, y, activo):

        self.resaltar(
            x,
            y,
            activo
        )

        self.dibujar_arbol(
            x - 18,
            y
        )

        self.dibujar_arbol(
            x + 15,
            y - 10
        )

        self.dibujar_arbol(
            x,
            y + 12
        )

        self.canvas.create_text(
            x,
            y + 43,
            text="Bosque Sombrío",
            fill="white",
            font=("Arial", 7, "bold")
        )


    def dibujar_arbol(self, x, y):

        self.canvas.create_rectangle(
            x - 3,
            y + 4,
            x + 3,
            y + 20,
            fill="#60442B",
            outline=""
        )

        self.canvas.create_polygon(
            x,
            y - 20,
            x - 14,
            y + 8,
            x + 14,
            y + 8,
            fill="#315A38",
            outline="#1F3B25"
        )

    def dibujar_campamento(self, x, y, activo):

        self.resaltar(
            x,
            y,
            activo
        )

        # Carpa
        self.canvas.create_polygon(
            x - 30,
            y + 18,
            x,
            y - 25,
            x + 30,
            y + 18,
            fill="#A78055",
            outline="#4B392A"
        )

        self.canvas.create_line(
            x,
            y - 25,
            x,
            y + 18,
            fill="#4B392A",
            width=2
        )

        # Fogata
        self.canvas.create_line(
            x + 32,
            y + 13,
            x + 48,
            y + 21,
            fill="#533B29",
            width=4
        )

        self.canvas.create_line(
            x + 48,
            y + 13,
            x + 32,
            y + 21,
            fill="#533B29",
            width=4
        )

        self.canvas.create_polygon(
            x + 40,
            y + 13,
            x + 34,
            y,
            x + 40,
            y + 5,
            x + 46,
            y,
            fill="#E88732",
            outline="#B95D20"
        )

        self.canvas.create_text(
            x,
            y + 39,
            text="Campamento",
            fill="white",
            font=("Arial", 7, "bold")
        )


    def dibujar_ruinas(self, x, y, activo):

        self.resaltar(
            x,
            y,
            activo
        )

        for columna in [
            x - 22,
            x,
            x + 22
        ]:

            self.canvas.create_rectangle(
                columna - 5,
                y - 22,
                columna + 5,
                y + 18,
                fill="#878B87",
                outline="#4D514D"
            )

        self.canvas.create_rectangle(
            x - 33,
            y - 28,
            x + 33,
            y - 20,
            fill="#9A9D99",
            outline="#4D514D"
        )

        self.canvas.create_text(
            x,
            y + 36,
            text="Ruinas Antiguas",
            fill="white",
            font=("Arial", 7, "bold")
        )


    def dibujar_castillo(self, x, y, activo):

        self.resaltar(
            x,
            y,
            activo
        )

        self.canvas.create_rectangle(
            x - 27,
            y - 12,
            x + 27,
            y + 25,
            fill="#555C65",
            outline="#292E35"
        )

        self.canvas.create_rectangle(
            x - 35,
            y - 30,
            x - 17,
            y + 25,
            fill="#616873",
            outline="#292E35"
        )

        self.canvas.create_rectangle(
            x + 17,
            y - 30,
            x + 35,
            y + 25,
            fill="#616873",
            outline="#292E35"
        )

        self.canvas.create_rectangle(
            x - 7,
            y + 3,
            x + 7,
            y + 25,
            fill="#24282E",
            outline=""
        )

        self.canvas.create_text(
            x,
            y + 42,
            text="Castillo",
            fill="white",
            font=("Arial", 7, "bold")
        )

    def dibujar_mazmorra(self, x, y, activo):

        self.resaltar(
            x,
            y,
            activo
        )

        self.canvas.create_rectangle(
            x - 30,
            y - 24,
            x + 30,
            y + 24,
            fill="#3E4148",
            outline="#181A1E"
        )

        for barra in [
            -18,
            -6,
            6,
            18
        ]:

            self.canvas.create_line(
                x + barra,
                y - 20,
                x + barra,
                y + 20,
                fill="#9A9EA6",
                width=3
            )

        self.canvas.create_text(
            x,
            y + 39,
            text="Mazmorra",
            fill="white",
            font=("Arial", 7, "bold")
        )


    def dibujar_trono(self, x, y, activo):

        self.resaltar(
            x,
            y,
            activo
        )

        self.canvas.create_rectangle(
            x - 20,
            y - 22,
            x + 20,
            y + 22,
            fill="#502D55",
            outline="#27152A"
        )

        self.canvas.create_rectangle(
            x - 27,
            y + 8,
            x + 27,
            y + 22,
            fill="#68406D",
            outline="#27152A"
        )

        # Corona
        self.canvas.create_polygon(
            x - 18,
            y - 28,
            x - 10,
            y - 40,
            x,
            y - 28,
            x + 10,
            y - 40,
            x + 18,
            y - 28,
            fill="#D8B252",
            outline="#866A28"
        )

        self.canvas.create_text(
            x,
            y + 40,
            text="Sala del Trono",
            fill="white",
            font=("Arial", 7, "bold")
        )

    def dibujar_heroe(self, x, y, tag):

        # Sombra
        self.canvas.create_oval(
            x - 15,
            y + 40,
            x + 15,
            y + 47,
            fill="#101510",
            outline="",
            tags=tag
        )

        # Capa
        self.canvas.create_polygon(
            x - 14,
            y + 8,
            x + 14,
            y + 8,
            x + 19,
            y + 36,
            x - 19,
            y + 36,
            fill="#752E3B",
            outline="#401921",
            tags=tag
        )

        # Armadura
        self.canvas.create_rectangle(
            x - 10,
            y + 7,
            x + 10,
            y + 31,
            fill="#48647E",
            outline="#202B36",
            tags=tag
        )

        # Cinturón
        self.canvas.create_rectangle(
            x - 10,
            y + 22,
            x + 10,
            y + 26,
            fill="#604226",
            outline="",
            tags=tag
        )

        # Cabeza
        self.canvas.create_oval(
            x - 9,
            y - 10,
            x + 9,
            y + 8,
            fill="#D8A574",
            outline="#222222",
            tags=tag
        )

        # Cabello
        self.canvas.create_arc(
            x - 10,
            y - 13,
            x + 10,
            y + 8,
            start=0,
            extent=180,
            style="pieslice",
            fill="#38271E",
            outline="#38271E",
            tags=tag
        )

        # Piernas
        self.canvas.create_line(
            x - 5,
            y + 31,
            x - 7,
            y + 42,
            fill="#222831",
            width=4,
            tags=tag
        )

        self.canvas.create_line(
            x + 5,
            y + 31,
            x + 7,
            y + 42,
            fill="#222831",
            width=4,
            tags=tag
        )

        # Espada
        if self.tiene_espada:

            self.canvas.create_line(
                x + 10,
                y + 9,
                x + 25,
                y - 10,
                fill="#E1E4E8",
                width=3,
                tags=tag
            )

            self.canvas.create_line(
                x + 7,
                y + 10,
                x + 14,
                y + 17,
                fill="#CAA04C",
                width=3,
                tags=tag
            )


    # =========================================================
    # MALAKAR
    # =========================================================

    def dibujar_malakar(self, x, y, tag):

        self.canvas.create_oval(
            x - 17,
            y + 40,
            x + 17,
            y + 47,
            fill="#0A0A0A",
            outline="",
            tags=tag
        )

        self.canvas.create_polygon(
            x - 14,
            y + 5,
            x + 14,
            y + 5,
            x + 20,
            y + 37,
            x - 20,
            y + 37,
            fill="#351D48",
            outline="#160C20",
            tags=tag
        )

        self.canvas.create_oval(
            x - 9,
            y - 10,
            x + 9,
            y + 8,
            fill="#B98C76",
            outline="#111111",
            tags=tag
        )

        self.canvas.create_arc(
            x - 14,
            y - 15,
            x + 14,
            y + 13,
            start=0,
            extent=180,
            style="pieslice",
            fill="#1C1025",
            outline="#1C1025",
            tags=tag
        )

        # Ojos
        self.canvas.create_oval(
            x - 5,
            y - 2,
            x - 2,
            y + 1,
            fill="#E04B4B",
            outline="",
            tags=tag
        )

        self.canvas.create_oval(
            x + 2,
            y - 2,
            x + 5,
            y + 1,
            fill="#E04B4B",
            outline="",
            tags=tag
        )

    def actualizar_juego(self):

        self.en_combate = False

        self.limpiar_botones()

        estado = self.narrativa.estado_actual

        self.dibujar_mapa()

        self.lbl_ubicacion.config(
            text=self.narrativa.estados[estado]
        )

        self.actualizar_inventario()
        self.actualizar_pila()

        if estado == "q1":

            self.lbl_objetivo.config(
                text="Acepta la misión de Eldran."
            )

            self.lbl_historia.config(
                text=
                "Llegaste al Pueblo de Arden.\n\n"
                "Eldran: "
                + self.gramatica.generar_dialogo()
                + "\n\n"
                "Debes encontrar el Fragmento de la Corona "
                "antes de que Malakar consiga apoderarse de él."
            )

            self.crear_boton(
                "1. ACEPTAR MISIÓN",
                self.aceptar
            )

            self.crear_boton(
                "2. ABANDONAR",
                self.abandonar,
                True
            )

        elif estado == "q2":

            self.lbl_objetivo.config(
                text="Explora los senderos del bosque."
            )

            self.lbl_historia.config(
                text=
                "Te encuentras en el Bosque Sombrío.\n\n"
                "Los senderos pueden llevarte hacia el "
                "Campamento Abandonado o hacia las Ruinas Antiguas."
            )

            self.crear_boton(
                "1. EXPLORAR",
                self.explorar
            )

        elif estado == "q3":

            self.visito_campamento = True

            if not self.tiene_espada:

                self.tiene_espada = True

                self.inventario.append(
                    "Espada"
                )

                texto = (
                    "Descubriste el Campamento Abandonado.\n\n"
                    "Junto a una vieja fogata encontraste una ESPADA.\n"
                    "La espada aumentará tu daño durante el combate."
                )

            else:

                texto = (
                    "Has regresado al Campamento Abandonado.\n\n"
                    "La espada ya fue recogida anteriormente."
                )

            self.actualizar_inventario()
            self.dibujar_mapa()

            self.lbl_objetivo.config(
                text="Regresa al bosque y continúa explorando."
            )

            self.lbl_historia.config(
                text=texto
            )

            self.crear_boton(
                "1. VOLVER AL BOSQUE",
                self.regresar
            )


        elif estado == "q4":

            self.visito_ruinas = True

            texto = (
                "Llegaste a las antiguas ruinas de Valdoria.\n\n"
            )

            if not self.tiene_llave:

                self.tiene_llave = True

                self.inventario.append(
                    "Llave Antigua"
                )

                texto += (
                    "Encontraste una LLAVE ANTIGUA.\n"
                )

            if not self.tiene_fragmento:

                self.tiene_fragmento = True

                self.inventario.append(
                    "Fragmento de la Corona"
                )

                texto += (
                    "La llave abre una cámara escondida.\n"
                    "¡Encontraste el FRAGMENTO DE LA CORONA!\n\n"
                    "Misión secundaria: "
                    + self.gramatica.generar_mision()
                )

            self.actualizar_inventario()

            self.lbl_objetivo.config(
                text="Puedes ir al Castillo o volver a explorar."
            )

            self.lbl_historia.config(
                text=texto
            )

            self.crear_boton(
                "1. IR AL CASTILLO",
                self.ir_castillo
            )

            self.crear_boton(
                "2. VOLVER AL BOSQUE",
                self.regresar_ruinas
            )


        elif estado == "q5":

            self.lbl_objetivo.config(
                text="Entra al Castillo de Valdoria."
            )

            self.lbl_historia.config(
                text=
                "El Castillo de Valdoria se alza frente a ti.\n\n"
                "El Fragmento de la Corona comienza a brillar "
                "y las enormes puertas se abren."
            )

            self.crear_boton(
                "1. ENTRAR AL CASTILLO",
                self.entrar_castillo
            )


        elif estado == "q6":

            if self.mundo.ubicacion_actual() != "Mazmorra":

                self.mundo.entrar(
                    "Mazmorra"
                )

            self.actualizar_pila()

            self.lbl_objetivo.config(
                text="Llega hasta la Sala del Trono."
            )

            self.lbl_historia.config(
                text=
                "Has descendido a las mazmorras del Castillo.\n\n"
                "El Guardia Rowan te advierte que Malakar "
                "se encuentra en la Sala del Trono."
            )

            self.crear_boton(
                "1. AVANZAR AL TRONO",
                self.avanzar
            )


        elif estado == "q7":

            if self.mundo.ubicacion_actual() != "Sala del Trono":

                self.mundo.entrar(
                    "Sala del Trono"
                )

            self.actualizar_pila()

            self.lbl_objetivo.config(
                text="Decide el destino del Fragmento."
            )

            self.lbl_historia.config(
                text=
                "Malakar te espera frente al trono.\n\n"
                "\"Entrégame el Fragmento de la Corona y podrás marcharte. "
                "Si te niegas, tendrás que enfrentarme.\"\n\n"
                "La decisión es tuya."
            )

            self.crear_boton(
                "1. LUCHAR",
                self.iniciar_combate
            )

            self.crear_boton(
                "2. ENTREGAR FRAGMENTO",
                self.entregar,
                True
            )


        elif estado == "q8":

            self.final(
                "FINAL DEL HÉROE",
                "Has derrotado a Malakar.\n"
                "El Fragmento queda protegido y Valdoria recupera la paz."
            )


        elif estado == "q9":

            self.final(
                "FINAL DEL ABANDONO",
                "Decidiste abandonar la aventura.\n"
                "Malakar continúa controlando Valdoria."
            )


        elif estado == "q10":

            self.final(
                "FINAL OSCURO",
                "Malakar obtiene el Fragmento de la Corona.\n"
                "Su poder continúa creciendo."
            )

    def explorar(self):

        if self.ultima_ruta_bosque is None:

            self.narrativa.transicion(
                "explorar"
            )

        else:

            if (
                self.visito_campamento
                and not self.visito_ruinas
            ):

                self.narrativa.estado_actual = "q4"

            elif (
                self.visito_ruinas
                and not self.visito_campamento
            ):

                self.narrativa.estado_actual = "q3"

            else:

                self.narrativa.transicion(
                    "explorar"
                )

        self.ultima_ruta_bosque = (
            self.narrativa.estado_actual
        )

        self.actualizar_juego()



    def crear_boton(
        self,
        texto,
        comando,
        peligro=False
    ):

        color = (
            "#763838"
            if peligro
            else "#395A7B"
        )

        activo = (
            "#914545"
            if peligro
            else "#4A7197"
        )

        boton = tk.Button(
            self.frame_botones,
            text=texto,
            command=comando,
            font=("Arial", 8, "bold"),
            bg=color,
            fg="white",
            activebackground=activo,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            height=1
        )

        boton.pack(
            fill="x",
            pady=3
        )

        self.acciones_actuales.append(
            comando
        )


    def limpiar_botones(self):

        self.acciones_actuales = []

        for widget in (
            self.frame_botones.winfo_children()
        ):

            widget.destroy()


    def tecla_1(self, evento=None):

        if len(self.acciones_actuales) >= 1:

            self.acciones_actuales[0]()


    def tecla_2(self, evento=None):

        if len(self.acciones_actuales) >= 2:

            self.acciones_actuales[1]()


    def actualizar_inventario(self):

        if not self.inventario:

            texto = "Vacío"

        else:

            texto = "\n".join(
                "• " + objeto
                for objeto in self.inventario
            )

        self.lbl_inventario.config(
            text=texto
        )


    def actualizar_pila(self):

        lugares = list(
            reversed(
                self.mundo.pila
            )
        )

        texto = ""

        for i, lugar in enumerate(lugares):

            if i == 0:

                texto += "► " + lugar

            else:

                texto += "\n   " + lugar

        self.lbl_pila.config(
            text=texto
        )


    def aceptar(self):

        self.narrativa.transicion(
            "aceptar"
        )

        self.actualizar_juego()


    def abandonar(self):

        self.narrativa.transicion(
            "abandonar"
        )

        self.actualizar_juego()


    def regresar(self):

        self.narrativa.transicion(
            "regresar"
        )

        self.actualizar_juego()


    def regresar_ruinas(self):

        self.narrativa.estado_actual = "q2"

        self.actualizar_juego()


    def ir_castillo(self):

        self.narrativa.transicion(
            "ir_castillo"
        )

        self.actualizar_juego()


    def entrar_castillo(self):

        if self.mundo.ubicacion_actual() != "Castillo":

            self.mundo.entrar(
                "Castillo"
            )

        self.narrativa.transicion(
            "entrar"
        )

        self.actualizar_juego()


    def avanzar(self):

        self.narrativa.transicion(
            "avanzar"
        )

        self.actualizar_juego()


    def entregar(self):

        self.narrativa.transicion(
            "entregar"
        )

        self.actualizar_juego()


    def iniciar_combate(self):

        self.narrativa.transicion(
            "luchar"
        )

        self.combate = Combate(
            self.tiene_espada
        )

        self.en_combate = True

        self.mensaje_combate = (
            "El combate ha comenzado."
        )

        self.dibujar_arena()

        self.actualizar_combate()

    def dibujar_arena(self):

        self.canvas.delete(
            "all"
        )

        self.canvas.create_rectangle(
            0,
            0,
            560,
            300,
            fill="#17151B",
            outline=""
        )

        # Piso
        for x in range(
            0,
            560,
            50
        ):

            self.canvas.create_line(
                x,
                220,
                x + 80,
                300,
                fill="#292630"
            )

        # Columnas
        for x in [
            35,
            510
        ]:

            self.canvas.create_rectangle(
                x - 14,
                35,
                x + 14,
                220,
                fill="#3A3940",
                outline="#202026"
            )

        self.canvas.create_text(
            280,
            28,
            text="SALA DEL TRONO",
            fill=self.DORADO_CLARO,
            font=("Georgia", 12, "bold")
        )

        # Personajes
        self.dibujar_heroe(
            145,
            180,
            "heroe_batalla"
        )

        self.dibujar_malakar(
            415,
            180,
            "malakar_batalla"
        )

        self.dibujar_vidas_combate()


    def dibujar_vidas_combate(self):

        self.canvas.delete(
            "hud_batalla"
        )

        # Jugador
        self.canvas.create_text(
            120,
            75,
            text="AVENTURERO",
            fill="white",
            font=("Arial", 8, "bold"),
            tags="hud_batalla"
        )

        self.dibujar_barra(
            60,
            88,
            self.combate.vida_jugador,
            "hud_batalla"
        )

        # Malakar
        self.canvas.create_text(
            440,
            75,
            text="MALAKAR",
            fill="white",
            font=("Arial", 8, "bold"),
            tags="hud_batalla"
        )

        self.dibujar_barra(
            380,
            88,
            self.combate.vida_enemigo,
            "hud_batalla"
        )


    def dibujar_barra(
        self,
        x,
        y,
        vida,
        tag
    ):

        vida = max(
            0,
            min(20, vida)
        )

        ancho = 120

        self.canvas.create_rectangle(
            x,
            y,
            x + ancho,
            y + 12,
            fill="#3C3C42",
            outline="#777777",
            tags=tag
        )

        self.canvas.create_rectangle(
            x,
            y,
            x + ancho * (vida / 20),
            y + 12,
            fill="#B34747",
            outline="",
            tags=tag
        )

        self.canvas.create_text(
            x + ancho / 2,
            y + 6,
            text=f"{vida}/20",
            fill="white",
            font=("Arial", 7, "bold"),
            tags=tag
        )


    def actualizar_combate(self):

        self.limpiar_botones()

        self.lbl_ubicacion.config(
            text="Sala del Trono"
        )

        self.lbl_objetivo.config(
            text="Derrota a Malakar."
        )

        espada = ""

        if self.tiene_espada:

            espada = (
                "\nEspada equipada: daño aumentado."
            )

        self.lbl_historia.config(
            text=
                "COMBATE FINAL\n"
                f"Jugador: {self.combate.vida_jugador} HP   |   "
                f"Malakar: {self.combate.vida_enemigo} HP"
                f"{espada}\n\n"
                f"{self.mensaje_combate}"
        )

        self.crear_boton(
            "1. ATACAR",
            self.atacar
        )


    def atacar(self):

        # Evitar doble clic
        self.limpiar_botones()

        tipo, dano = (
            self.combate.ataque_jugador()
        )

        self.animar_movimiento(
            "heroe_batalla",
            12,
            3,
            50,
            lambda: self.impacto_jugador(
                tipo,
                dano
            )
        )


    def impacto_jugador(
        self,
        tipo,
        dano
    ):

        # Efecto de espada
        self.canvas.create_line(
            220,
            150,
            260,
            200,
            fill="#F4E3A3",
            width=5,
            tags="efecto"
        )

        self.canvas.create_line(
            230,
            145,
            270,
            190,
            fill="white",
            width=2,
            tags="efecto"
        )

        self.combate.vida_enemigo -= dano

        if self.combate.vida_enemigo < 0:

            self.combate.vida_enemigo = 0

        self.dibujar_vidas_combate()

        if tipo == "normal":

            mensaje = (
                f"Golpeas a Malakar: {dano} de daño."
            )

        elif tipo == "critico":

            mensaje = (
                f"¡GOLPE CRÍTICO! {dano} de daño."
            )

        else:

            mensaje = (
                "Malakar esquivó tu ataque."
            )

        self.mensaje_combate = mensaje

        # Sacudir al enemigo
        if dano > 0:

            self.sacudir(
                "malakar_batalla",
                4
            )

        self.ventana.after(
            180,
            lambda: self.canvas.delete(
                "efecto"
            )
        )

        # Regresar al personaje
        self.ventana.after(
            220,
            lambda: self.animar_movimiento(
                "heroe_batalla",
                -12,
                3,
                50,
                self.despues_ataque_jugador
            )
        )


    def despues_ataque_jugador(self):

        if self.combate.vida_enemigo <= 0:

            self.ventana.after(
                400,
                self.ganar_combate
            )

            return

        self.ventana.after(
            350,
            self.ataque_malakar
        )


    def ataque_malakar(self):

        tipo, dano = (
            self.combate.ataque_enemigo()
        )

        self.animar_movimiento(
            "malakar_batalla",
            -12,
            3,
            50,
            lambda: self.impacto_malakar(
                tipo,
                dano
            )
        )


    def impacto_malakar(
        self,
        tipo,
        dano
    ):

        # Efecto mágico rojo
        self.canvas.create_oval(
            250,
            145,
            295,
            190,
            fill="#B53B4A",
            outline="#FF7782",
            width=3,
            tags="efecto"
        )

        self.combate.vida_jugador -= dano

        if self.combate.vida_jugador < 0:

            self.combate.vida_jugador = 0

        self.dibujar_vidas_combate()

        if tipo == "normal":

            mensaje = (
                f"\nMalakar te golpea: {dano} de daño."
            )

        elif tipo == "critico":

            mensaje = (
                f"\n¡CRÍTICO DE MALAKAR! {dano} de daño."
            )

        else:

            mensaje = (
                "\nLograste esquivar el ataque de Malakar."
            )

        self.mensaje_combate += mensaje

        if dano > 0:

            self.sacudir(
                "heroe_batalla",
                4
            )

        self.ventana.after(
            180,
            lambda: self.canvas.delete(
                "efecto"
            )
        )

        self.ventana.after(
            220,
            lambda: self.animar_movimiento(
                "malakar_batalla",
                12,
                3,
                50,
                self.despues_ataque_malakar
            )
        )


    def despues_ataque_malakar(self):

        if self.combate.vida_jugador <= 0:

            self.ventana.after(
                400,
                self.perder_combate
            )

            return

        self.actualizar_combate()


    def animar_movimiento(
        self,
        tag,
        dx,
        pasos,
        intervalo,
        callback
    ):

        if pasos <= 0:

            callback()
            return

        self.canvas.move(
            tag,
            dx,
            0
        )

        self.ventana.after(
            intervalo,
            lambda: self.animar_movimiento(
                tag,
                dx,
                pasos - 1,
                intervalo,
                callback
            )
        )


    def sacudir(
        self,
        tag,
        repeticiones
    ):

        if repeticiones <= 0:

            return

        direccion = (
            5
            if repeticiones % 2 == 0
            else -5
        )

        self.canvas.move(
            tag,
            direccion,
            0
        )

        self.ventana.after(
            45,
            lambda: self.sacudir(
                tag,
                repeticiones - 1
            )
        )

    def ganar_combate(self):

        self.en_combate = False

        self.narrativa.transicion(
            "ganar"
        )

        self.actualizar_juego()


    def perder_combate(self):

        self.en_combate = False

        self.narrativa.transicion(
            "perder"
        )

        self.actualizar_juego()



    def final(
        self,
        titulo,
        descripcion
    ):

        self.lbl_objetivo.config(
            text="La aventura ha terminado."
        )

        self.lbl_historia.config(
            text=
                titulo
                + "\n\n"
                + descripcion
        )

        self.limpiar_botones()

        self.crear_boton(
            "1. JUGAR DE NUEVO",
            self.reiniciar
        )

        self.crear_boton(
            "2. SALIR",
            self.ventana.destroy,
            True
        )


    def reiniciar(self):

        self.narrativa = MotorNarrativo()
        self.mundo = PilaMundo()
        self.gramatica = Gramatica()

        self.inventario = []

        self.tiene_espada = False
        self.tiene_llave = False
        self.tiene_fragmento = False

        self.visito_campamento = False
        self.visito_ruinas = False

        self.ultima_ruta_bosque = None

        self.combate = None
        self.en_combate = False

        self.narrativa.transicion(
            "iniciar"
        )

        self.actualizar_juego()


ventana = tk.Tk()

juego = JuegoValdoria(
    ventana
)

ventana.mainloop()