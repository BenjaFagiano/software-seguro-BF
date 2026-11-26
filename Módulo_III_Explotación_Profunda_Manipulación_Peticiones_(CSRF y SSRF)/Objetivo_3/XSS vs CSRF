Comparación Técnica: XSS vs. CSRF

Aunque ambos ataques se dirigen al navegador web de la víctima para comprometer su cuenta o sesión, sus vectores de explotación y mecánicas de confianza operan de forma opuesta:

- Diferencia fundamental de mecánica

Cross-Site Scripting (XSS): Es un ataque de inyección de código del lado del cliente. Ocurre cuando la aplicación no sanitiza o codifica las entradas del usuario, permitiendo que un atacante inyecte scripts arbitrarios (usualmente JavaScript) que se ejecutan directamente en el navegador de la víctima.
Cross-Site Request Forgery (CSRF): Es un ataque de falsificación de peticiones. Ocurre cuando un sitio malicioso logra que el navegador de la víctima emita una solicitud HTTP no deseada hacia la aplicación objetivo, aprovechando que el navegador adjunta de forma automática las cookies de sesión activas.

- Dirección de la confianza

En XSS (El cliente confía en la aplicación): El navegador de la víctima confía ciegamente en el código que proviene del servidor web vulnerable y ejecuta los scripts maliciosos creyendo que forman parte legítima de la página.
En CSRF (El servidor confía en el cliente): El servidor objetivo confía ciegamente en la petición HTTP recibida porque incluye las cookies de autenticación legítimas del usuario, sin poder verificar si la acción fue iniciada voluntariamente por el usuario o inducida desde otro sitio.

- Capacidades y alcance del atacante

Capacidad en XSS: Otorga al atacante la ejecución directa de comandos JavaScript en el origen de la víctima. Permite robar tokens de sesión (si no cuentan con la bandera `HttpOnly`), rediseñar la interfaz (phishing interno/defacement), capturar eventos de teclado y leer datos directamente del DOM.
Capacidad en CSRF: No permite al atacante ejecutar código JavaScript en el sitio objetivo ni leer las respuestas de las peticiones (debido a las restricciones impuestas por la Same-Origin Policy). Su alcance se limita exclusivamente a forzar acciones de escritura o cambio de estado (como modificar la contraseña, cambiar el correo o transferir fondos).
