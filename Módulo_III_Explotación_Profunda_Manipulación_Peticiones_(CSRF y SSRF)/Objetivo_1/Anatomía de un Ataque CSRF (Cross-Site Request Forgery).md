Supongamos que la víctima tiene sesión activa en banco.com y el atacante controla sitio-malicioso.com.

La víctima se autentica. Ingresa a https://banco.com, el servidor valida credenciales y responde:
Set-Cookie: session=abc123; HttpOnly; Path=/
El navegador guarda la cookie y la asocia al dominio banco.com. De ahora en más, cada petición que el navegador haga a ese dominio la va a adjuntar automáticamente.
La víctima visita el sitio malicioso, por un link en un mail, un banner o una redirección. No hace falta que haga clic en nada más: basta con que cargue la página.
Esa página fuerza una petición hacia banco.com, por ejemplo con un formulario que se envía solo:
<form id="f" action="https://banco.com/transferir" method="POST">
  <input type="hidden" name="destino" value="atacante">
  <input type="hidden" name="monto" value="50000">
</form>
<script>document.getElementById('f').submit();</script>
También puede lograrse con <img src="...">, un <iframe>, un fetch() o un link.
El navegador envía la cookie de banco.com junto con esa petición, aunque el origen sea sitio-malicioso.com y la víctima no haya tenido intención de transferir nada.
El servidor de banco.com recibe la cookie válida, la considera prueba de sesión y ejecuta la transferencia.
La víctima no percibe nada: sigue en el sitio del atacante, a lo sumo ve una recarga o un error invisible.
Condiciones para que funcione:

Que exista una sesión activa (cookie vigente).
Que la acción sensible sea predecible: parámetros conocidos, sin token aleatorio, sin CAPTCHA y sin confirmación adicional.
Que el navegador adjunte la cookie automáticamente, que es justamente el comportamiento que habilita el ataque.


Por qué ocurre: el comportamiento automático de las cookies
Las cookies no identifican quién originó la petición, solo hacia dónde va. El navegador aplica una regla simple: si el destino coincide con el dominio dueño de la cookie, la manda.
No hay ninguna señal en una petición HTTP común que diga "esta transferencia fue intencional del usuario". El servidor ve:

POST /transferir HTTP/2
Cookie: session=abc123
destino=atacante&monto=50000
Para el backend eso es idéntico a una transferencia legítima heda desde el formulario del propio banco. El navegador hace exactamente lo que debe hacer (mandar la cookie al dominio correspondiente); el fallo está en que el servidor confía solo en esa cookie como prueba de intención.

HttpOnly no evita CSRF: solo impide que JavaScript lea la cookie. El navegador sigue enviándola igual.

Cómo SameSite mitiga el vector
El atributo SameSite le indica al navegador en qué contextos puede enviar la cookie. Es el mecanismo más directo contra CSRF porque ataca justo el eslabón que hace posible el ataque: el envío automático.
