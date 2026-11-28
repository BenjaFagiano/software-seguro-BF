Una Condición de Carrera (Race Condition) de tipo TOCTOU (Time of Check to Time of Use) ocurre cuando un sistema realiza múltiples operaciones concurrentes sobre un recurso compartido y el resultado correcto depende de que se ejecuten en un orden secuencial estricto.
En flujos financieros o de e-commerce (como la aplicación de un cupón de descuento de un solo uso), esta falla permite a un atacante duplicar o multiplicar beneficios antes de que el servidor actualice el estado en la base de datos.

Un Repeater común envía una petición, espera la respuesta y recién después manda la siguiente. Eso nunca genera una carrera: el servidor termina el primer canje antes de empezar el segundo.

Turbo Intruder (extensión de Burp Suite) permite en cambio abrir muchas conexiones a la vez y dispararlas al mismo instante. El atacante:

Captura la petición de canje, por ejemplo:
POST /cart/apply-coupon
{"codigo":"DESCUENTO50"}
La carga en Turbo Intruder como plantilla.
Configura concurrencia alta (por ejemplo 50 peticiones) y un mecanismo de sincronización. El truco más usado es enviar todas las peticiones menos el último byte, retenerlas y liberarlas juntas (last-byte sync), o usar una "compuerta" (gate) que espera a que las 50 estén listas y las suelta simultáneamente.
Las 50 peticiones llegan al servidor casi al mismo tiempo.
Todas ven usado = False, porque ninguna todavía hizo el UPDATE. Las 50 pasan la verificación y las 50 aplican el descuento. Cuando finalmente se ejecutan los UPDATE, ya es tarde: el cupón se usó cincuenta veces.

Lo que observa el atacante son decenas de respuestas 200 OK en lugar de una sola y cuarenta y nueve rechazos. En un sistema financiero, el descuento se duplica hasta agotar el saldo o el stock.
