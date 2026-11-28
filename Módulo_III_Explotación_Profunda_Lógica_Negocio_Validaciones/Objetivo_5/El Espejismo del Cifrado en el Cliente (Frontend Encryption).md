El error de fondo es confundir confidencialidad en tránsito con protección frente al usuario que controla el navegador.

HTTPS/TLS ya cifra la comunicación entre el navegador y el servidor. Un proxy como Burp puede ver el contenido porque se coloca en el medio, però el punto clave es otro: el atacante es el dueño de su propio navegador. Todo el JavaScript que corre ahí —incluida la función que cifra— llega a su máquina y puede ser leído, modificado o simplemente ignorado.

Cifrar en el cliente agrega una capa de ofuscación, no una barrera de seguridad. Es security by obscurity: el código y la clave viajan en el mismo paquete que el atacante controla.

Dónde reside el fallo fundamental de diseño
En tres ideas equivocadas:

a) La clave está en el cliente. Si el navegador puede cifrar, necesita tener la clave o poder derivarla. Esa clave está en el bundle JavaScript (hardcodeada, ofuscada o generada a partir de datos públicos). El atacante la extrae con solo mirar el código. No existe secreto que el cliente necesite conocer y que el dueño del cliente no pueda leer.

b) Cifrar no equivale a autenticar. El cifrado da confidencialidad; no garantiza que el mensaje no haya sido modificado ni quién lo generó. Aunque se use AES-GCM con tag de integridad, el tag se calcula con la clave que el atacante ya tiene en el navegador, así que puede generar tags válidos para sus propios valores. Para que un MAC protegiera de verdad, la clave tendría que ser secreta para el cliente… y entonces el cliente no podría cifrar.

c) El backend vuelve a confiar en el cliente. Después de descifrar, el servidor procesa el valor como si viniera de un usuario legítimo. El cifrado no reemplaza la validación de esquema, la autorización ni los controles de integridad en servidor.

Pasos tácticos de un atacante
Paso 1 — Reconocer el mecanismo
Abre DevTools (F12) → Sources y busca el bundle que hace el cifrado. Síntomas típicos:

const key = CryptoJS.enc.Utf8.parse("clave1234567890");
const cipher = CryptoJS.AES.encrypt(JSON.stringify(payload), key, {
    mode: CryptoJS.mode.CBC,
    iv: ivFijo
}).toString();

fetch("/api/transferir", {
    method: "POST",
    body: JSON.stringify({ data: cipher })
});
También aparece con crypto.subtle, btoa() + XOR, RC4 casero o librerías tipo CryptoJS. En Network se ve el parámetro cifrado, por ejemplo data=U2FsdGVkX1+8J3m....

Paso 2 — Extraer clave, IV y algoritmo
Buscar literales de clave/IV en el JS ("clave123...", iv = ...).
Si están ofuscados, poner un breakpoint en la función de cifrado y leer las variables en la consola justo antes de que se ejecute.
Anotar algoritmo, modo, padding y codificación (Base64, Hex, etc.).
Paso 3 — Evadir la protección (tres variantes)
Variante A — manipular antes del cifrado (hook). Sobrescribir la función en la consola del navegador:

window.encrypt = function (payload) {
    payload.monto = -1000;          // valor manipulado
    return encryptOriginal(payload); // se cifra con la clave real
};
O interceptar el fetch y cambiar el objeto antes de que se cifre con un breakpoint. El navegador produce un ciphertext perfectamente válido, pero con datos del atacante.

Variante B — replicar el cifrado fuera del navegador. Con la clave extraída, armar el payload en Python y mandarlo desde Repeater:

import base64, json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

clave = b"clave1234567890"
iv = b"ivfijo1234567890"
payload = json.dumps({"monto": -1000, "destino": "atacante"}).encode()
cipher = AES.new(clave, AES.MODE_CBC, iv)
data = base64.b64encode(cipher.encrypt(pad(payload, 16))).decode()


Para el servidor es indistinguible de una petición generada por la web.
