# El Reino de Valdoria: La Corona Fragmentada

El objetivo fue crear un juego RPG narrativo donde se pudieran aplicar de forma práctica varios de los temas vistos en clase, como los autómatas, las pilas, las gramáticas y las transiciones entre estados.

El juego fue desarrollado en **Python** y utiliza **Tkinter** para mostrar una interfaz gráfica sencilla y fácil de utilizar.

## Historia

El juego se desarrolla en el Reino de Valdoria.

La Corona de Valdoria fue fragmentada y Malakar, antiguo guardián del reino, intenta conseguir sus fragmentos para aumentar su poder.

El jugador comienza su aventura en el Pueblo de Arden, donde el anciano Eldran le entrega la misión de encontrar uno de los fragmentos antes que Malakar.

Durante la aventura se pueden visitar diferentes lugares, conseguir objetos y tomar decisiones que pueden llevar a distintos finales.

## Lugares del juego

Durante la aventura se pueden visitar las siguientes zonas:

- Pueblo de Arden
- Bosque Sombrío
- Campamento abandonado
- Ruinas antiguas
- Castillo de Valdoria
- Mazmorra
- Sala del Trono

Cada lugar representa un estado importante dentro del recorrido del jugador.

## Autómata Finito No Determinista

La historia principal se controla mediante un **Autómata Finito No Determinista (AFN)**.

Cada estado representa una escena o lugar del juego y las decisiones del jugador permiten pasar de un estado a otro.

Uno de los ejemplos principales ocurre en el Bosque Sombrío.

Al seleccionar la opción de explorar, el jugador puede llegar al Campamento abandonado o a las Ruinas antiguas.

Esto permite representar el comportamiento no determinista del autómata.

## Pila del mundo

También se utilizó una pila para representar las zonas que se encuentran dentro de otras.

Por ejemplo:

```text
Mundo
Castillo
Mazmorra
Sala del Trono
```

Cuando el jugador entra a una nueva zona, esta se agrega a la pila.

De esta manera se puede conocer cuál es la ubicación más interna en la que se encuentra el jugador.

## Gramática Libre de Contexto

El proyecto utiliza una Gramática Libre de Contexto para generar algunos diá
