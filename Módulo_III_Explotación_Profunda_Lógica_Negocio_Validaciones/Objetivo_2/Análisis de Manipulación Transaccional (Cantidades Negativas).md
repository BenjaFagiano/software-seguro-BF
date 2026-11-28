Se trata de una falla de lógica de negocio por validación insuficiente de entrada (Business Logic Flaw / Improper Input Validation). El atacante no necesita inyectar código ni escalar privilegios: simplemente envía un valor que el servidor acepta aunque no debería, y se aprovecha de que la lógica de cálculo no contempla ese caso.
El campo cantidad viaja en el cuerpo de la petición (JSON o formulario) y el servidor lo toma como válido sin verificar su dominio. El frontend puede tener un min="1" en el input, pero eso es solo una restricción de interfaz: al interceptar la petición con Burp, ese límite desaparece y el atacante cambia 1 por -5.

El problema aparece en la aritmética. El servidor calcula:

total = precio × cantidad
saldo = saldo − total
Con cantidad = -5 y un producto de $100:

total = 100 × (-5) = -500
saldo = saldo − (-500) = saldo + 500
Restar un número negativo equivale a sumar. El signo se propaga desde la entrada hasta la operación contable, y lo que estaba pensado como un cobro se transforma en un abono. No hay ninguna excepción ni control que frene la operación porque, para el código, -5 es un entero perfectamente válido.

A esto se suman otros descuidos típicos: aceptar el precio o el total desde el cliente, usar float para dinero (que introduce errores de precisión) y no verificar stock de forma condicional, lo que además permite dejar existencias negativas.
