class PilaMundo:

    def __init__(self):
        
        self.pila = ["Mundo"]

    def entrar(self, lugar):
        self.pila.append(lugar)
        print(f"\nEntraste a: {lugar}")

    def salir(self):
        if len(self.pila) > 1:
            lugar = self.pila.pop()
            print(f"\nSaliste de: {lugar}")
        else:
            print("\nNo puedes salir del Mundo.")

    def ubicacion_actual(self):
        return self.pila[-1]

    def mostrar_pila(self):
        print("\n--- PILA DEL MUNDO ---")

        for lugar in reversed(self.pila):
            print(lugar)

        print("----------------------")