# Escape room difuso: explicación línea a línea

Archivo: `escape_room_difuso.py`. Se ejecuta con `python escape_room_difuso.py`. Usa solo `tkinter`, que viene con Python (en Linux puede hacer falta `sudo apt install python3-tk`).

## La idea del juego

Hay 10 puertas. Cada una tiene una **regla difusa** (por ejemplo, `A AND B`) y un **umbral**. La puerta se abre si el resultado de la regla es igual o mayor que el umbral.

Tú controlas dos palancas, A y B, con valores de 0 a 1. Hay un límite: **A + B no puede pasar de la energía disponible**. Por eso hay que pensar cómo repartir la energía según el operador:

- Con **AND mínimo**, gana el valor más débil, así que conviene repartir parejo.
- Con **OR máximo**, basta una palanca alta, así que conviene concentrar toda la energía en una.
- Con **NOT**, conviene poner en la palanca negada un valor bajo.

## 1. Importar y operadores (líneas 1 a 8)

| Línea | Qué hace |
|---|---|
| 1 | Importa `tkinter` (la librería de ventanas) y le pone el apodo `tk`. |
| 3 | Comentario que separa la sección de operadores. |
| 4 | `y_min`: el AND clásico. Devuelve el menor de los dos valores. |
| 5 | `y_prod`: el AND alternativo. Multiplica los dos valores. |
| 6 | `o_max`: el OR clásico. Devuelve el mayor. |
| 7 | `o_suma`: el OR alternativo (suma probabilística): `a + b − a·b`. |
| 8 | `no`: el NOT. Devuelve `1 − a`. |

## 2. Las puertas (líneas 10 a 22)

| Línea | Qué hace |
|---|---|
| 10 | Comentario con el orden de los datos de cada puerta. |
| 11 | Abre la lista `PUERTAS`. |
| 12 a 21 | Cada línea es una puerta, con 6 datos: **nombre**, **texto de la regla** (lo que ve el jugador), **función** que calcula el resultado, **plantilla del cálculo** (para mostrar la cuenta), **umbral** y **energía**. |
| 12 a 15 | Puertas 1 a 4: AND y OR simples con mínimo y máximo. |
| 16 a 18 | Puertas 5 a 7: aparece NOT. Se usa `lambda`, una función corta escrita en una línea, para combinar `y_min` con `no`. |
| 19 a 21 | Puertas 8 a 10: operadores alternativos (producto y suma probabilística). |
| 22 | Cierra la lista. |

Las plantillas como `"mín({a}, {b})"` tienen huecos `{a}` y `{b}` que después se rellenan con los valores reales.

## 3. Colores (líneas 24 a 26)

| Línea | Qué hace |
|---|---|
| 25 | Define `FONDO` (azul oscuro), `PANEL` (azul grisáceo) y `LATON` (dorado, el color de acento). |
| 26 | Define `ABIERTA` (verde), `ALARMA` (rojo), `TEXTO` (crema) y `APAGADO` (gris para textos secundarios). |

El estilo es de bóveda: fondo oscuro, detalles dorados, verde cuando abres y rojo cuando fallas.

## 4. La clase `Juego` y su arranque (líneas 29 a 41)

| Línea | Qué hace |
|---|---|
| 29 | Crea la clase `Juego`, que guarda todo el estado y la interfaz. |
| 30 | `__init__` se ejecuta al crear el juego. Recibe la ventana `root`. |
| 31 | Guarda la ventana en `self.root`. |
| 32 | Pone el título de la ventana. |
| 33 | Pinta el fondo de la ventana. |
| 34 | Impide cambiar el tamaño de la ventana, para que el diseño no se rompa. |
| 35 | Crea `va` y `vb`, las variables que guardan el valor de cada palanca (empiezan en 0). |
| 36 | Llama a `construir()`, que crea todos los elementos visuales. |
| 37 | Fija la fase inicial en `"inicio"`. |
| 38 | Llama a `reiniciar()` para dejar todo listo. |
| 40 y 41 | `etiqueta`: función auxiliar que crea un texto (`Label`) con el fondo y color de texto ya puestos, para no repetir código. |

## 5. Construir la interfaz (líneas 43 a 76)

| Línea | Qué hace |
|---|---|
| 43 | Define `construir`. |
| 44 | Crea una barra horizontal (`Frame`) para la parte de arriba. |
| 45 | La coloca ocupando todo el ancho, con márgenes. |
| 46 y 47 | Crea el texto del nivel ("Puerta 3 de 10…") y lo pone a la izquierda. |
| 48 y 49 | Crea el texto de puntos, en dorado, y lo pone a la derecha. |
| 50 y 51 | Crea el texto de vidas (corazones), en rojo, junto a los puntos. |
| 53 | Muestra el título del juego en letra grande. |
| 54 | Crea el `Canvas`, el lienzo donde se dibuja la puerta (760 × 200 píxeles). |
| 55 | Lo coloca en la ventana. |
| 57 y 58 | Crea el texto de la regla de la puerta actual y lo coloca. |
| 59 y 60 | Crea el texto del umbral y la energía, en gris, y lo coloca. |
| 62 | Recorre las dos palancas (nombre y variable). Así no escribo el mismo bloque dos veces. |
| 63 y 64 | Crea una fila para cada palanca y la coloca. |
| 65 | Escribe el nombre de la palanca ("Palanca A") a la izquierda de la fila. |
| 66 a 68 | Crea el deslizador (`Scale`) de 0 a 1 con pasos de 0.1. Está conectado a la variable de esa palanca, tiene colores propios y llama a `al_mover` cada vez que se mueve. |
| 70 y 71 | Crea el texto que muestra la energía usada y lo coloca. |
| 72 y 73 | Crea el cuadro de mensajes (resultados y explicaciones). `wraplength` parte el texto largo en varias líneas y `height=4` reserva espacio para que no salte el diseño. |
| 74 a 76 | Crea el botón principal, con color dorado. Al presionarlo llama a `boton()`. |

## 6. Estado del juego (líneas 78 a 113)

| Línea | Qué hace |
|---|---|
| 79 | Define `reiniciar`, que deja el juego como nuevo. |
| 80 | Pone en cero el nivel, los puntos y los fallos, y en 3 las vidas. |
| 81 | Fase `"inicio"`: la pantalla de bienvenida. |
| 82 | La puerta se dibuja cerrada. |
| 83 | El botón dice "Comenzar". |
| 84 a 86 | Muestra las instrucciones en el cuadro de mensajes. |
| 87 | Llama a `refrescar()` para actualizar los textos. |
| 89 | Define `cargar_puerta`, que prepara una puerta nueva. |
| 90 | Pasa a la fase `"jugando"`, cierra la puerta y borra los fallos de esa puerta. |
| 91 y 92 | Regresa las dos palancas a 0. |
| 93 | Muestra un mensaje corto de ayuda. |
| 94 | El botón cambia a "Probar puerta". |
| 95 | Actualiza los textos. |
| 97 | Define `refrescar`, que actualiza todo lo que se ve. |
| 98 | Toma los datos de la puerta actual. Los guiones bajos `_` son datos que aquí no se necesitan. `min(self.nivel, 9)` evita salirse de la lista al terminar. |
| 99 | Actualiza el texto del nivel y el nombre de la puerta. |
| 100 | Actualiza los puntos. |
| 101 | Dibuja los corazones: `♥` por cada vida que queda y `♡` por cada vida perdida. |
| 102 | Muestra la regla. |
| 103 | Muestra el umbral y la energía disponible. `:g` quita ceros sobrantes (1.0 se ve como 1). |
| 104 | Llama a `al_mover()` para actualizar energía y dibujo. |
| 106 | Define `al_mover`, que se ejecuta cada vez que mueves una palanca. |
| 107 | Toma la energía disponible de la puerta actual (el dato en la posición 5). |
| 108 | Suma A + B y lo redondea a 1 decimal para evitar errores de coma flotante (como 0.30000000000000004). |
| 109 y 110 | Muestra la energía usada; el texto se pone rojo si te pasaste y verde si no. `1e-9` es una tolerancia mínima. |
| 111 y 112 | Si la puerta estaba en rojo por un fallo y mueves una palanca, vuelve a dorado (cerrada). |
| 113 | Vuelve a dibujar la puerta con los valores nuevos. |

## 7. Dibujar la puerta (líneas 115 a 129)

| Línea | Qué hace |
|---|---|
| 116 | Define `dibujar`. |
| 117 | Guarda el lienzo en una variable corta, `c`. |
| 118 | Borra todo lo dibujado antes. |
| 119 | Elige el color según el estado: dorado (cerrada), verde (abierta) o rojo (fallo). |
| 120 | `hueco` es cuánto se separan las hojas de la puerta: 48 píxeles si está abierta, 0 si no. |
| 121 | Dibuja el marco de la puerta. Si está abierta, el fondo es verde oscuro (luz al otro lado). |
| 122 | Dibuja la hoja izquierda; su borde derecho se mueve hacia la izquierda si hay hueco. |
| 123 | Dibuja la hoja derecha; su borde izquierdo se mueve hacia la derecha si hay hueco. |
| 124 | Recorre los dos círculos de las palancas: posición, letra y variable. |
| 125 | Dibuja el círculo. |
| 126 | Escribe "Palanca A" o "Palanca B" dentro. |
| 127 | Escribe el valor actual de la palanca con 1 decimal. |
| 128 y 129 | Dibujan las líneas que conectan cada palanca con la puerta. |

## 8. Botón principal (líneas 131 a 141)

El mismo botón hace cosas distintas según la **fase** del juego.

| Línea | Qué hace |
|---|---|
| 132 | Define `boton`. |
| 133 y 134 | Si estás en `"inicio"`, carga la primera puerta. |
| 135 y 136 | Si estás `"jugando"`, prueba la puerta. |
| 137 a 139 | Si la puerta ya `"abierta"`, sube un nivel y carga la siguiente. |
| 140 y 141 | En cualquier otro caso (`"fin"`), reinicia el juego. |

## 9. Probar la puerta (líneas 143 a 172)

| Línea | Qué hace |
|---|---|
| 143 | Define `probar`, la parte central del juego. |
| 144 | Toma de la lista la función, la plantilla de cálculo, el umbral y la energía. |
| 145 | Lee las dos palancas y las redondea a 1 decimal. |
| 146 a 148 | Si A + B pasa de la energía, muestra un aviso en rojo y termina con `return`. **No quita vida.** |
| 149 | Calcula el resultado difuso llamando a la función de la puerta, redondeado a 2 decimales. |
| 150 | Rellena la plantilla con los valores reales, por ejemplo `mín(0.6, 0.6)`. |
| 151 | Compara el resultado con el umbral. Si llega o lo supera, la puerta se abre. |
| 152 | Suma 100 puntos si abriste sin fallar, o 50 si antes fallaste en esa puerta. |
| 153 | Cambia el estado y la fase a `"abierta"`. |
| 154 | Muestra en verde el mensaje con la cuenta completa. |
| 155 | Revisa si esta era la última puerta. |
| 156 a 158 | Si era la última, la fase es `"fin"` y se muestra el mensaje de victoria con el puntaje. |
| 159 | El botón dice "Jugar de nuevo" si terminó, o "Siguiente puerta" si no. |
| 160 | Si el resultado no llegó al umbral, entra este bloque. |
| 161 y 162 | Resta una vida y suma un fallo. |
| 163 | Marca el estado como `"fallo"` (la puerta se pinta roja). |
| 164 | Prepara el mensaje con la cuenta y el umbral, para que veas por qué falló. |
| 165 a 168 | Si no quedan vidas, el juego termina y el botón pasa a "Jugar de nuevo". |
| 169 y 170 | Si quedan vidas, te invita a ajustar las palancas. |
| 171 | Muestra el mensaje en rojo. |
| 172 | Actualiza puntos, vidas y dibujo. |
| 174 a 177 | `refrescar_sin_reset`: actualiza puntos, corazones y dibujo sin tocar el mensaje ni el botón (si usara `refrescar`, se borrarían los textos de resultado). |

## 10. Arranque (líneas 180 a 183)

| Línea | Qué hace |
|---|---|
| 180 | Solo ejecuta lo de abajo si corres este archivo directamente (no si lo importas). |
| 181 | Crea la ventana principal. |
| 182 | Crea el juego dentro de esa ventana. |
| 183 | `mainloop()` mantiene la ventana abierta y atenta a los clics hasta que la cierres. |

## Soluciones de cada puerta (para probar el juego)

| Puerta | Regla | Umbral | Energía | Una solución |
|---|---|---|---|---|
| 1 | A AND B (mín) | 0.5 | 1.2 | A = 0.5, B = 0.5 |
| 2 | A OR B (máx) | 0.7 | 0.8 | A = 0.7, B = 0 |
| 3 | A AND B (mín) | 0.6 | 1.4 | A = 0.6, B = 0.6 |
| 4 | A OR B (máx) | 0.9 | 1.0 | A = 0.9, B = 0 |
| 5 | A AND NOT B | 0.6 | 1.0 | A = 0.6, B = 0.4 |
| 6 | NOT A AND B | 0.6 | 1.0 | A = 0.4, B = 0.6 |
| 7 | A AND NOT B | 0.7 | 1.0 | A = 0.7, B = 0.3 |
| 8 | A AND B (producto) | 0.36 | 1.2 | A = 0.6, B = 0.6 |
| 9 | A OR B (suma prob.) | 0.8 | 0.9 | A = 0.8, B = 0 |
| 10 | A AND B (producto) | 0.49 | 1.4 | A = 0.7, B = 0.7 |

## Cosas que puedes cambiar fácil

- **Dificultad:** cambia el umbral o la energía en `PUERTAS` (líneas 12 a 21).
- **Colores:** cambia los valores de las líneas 25 y 26.
- **Más puertas:** agrega una línea a `PUERTAS`. Recuerda cambiar el `9` de las líneas 98 y 107, y el "de 10" de la línea 99.
- **Vidas:** cambia el `3` de la línea 80 (y el `3` de las líneas 101 y 176).

En macOS, tkinter ignora el color de fondo de los botones, así que el botón principal se verá con el estilo del sistema. El juego funciona igual.
