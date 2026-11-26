Explotación de SSRF en AWS: El Peligro del Servicio de Metadatos

En arquitecturas orientadas a la nube (como Amazon Web Services), un ataque de Server-Side Request Forgery (SSRF) adquiere una gravedad crítica debido a la existencia del Servicio de Metadatos de la Instancia (IMDS - Instance Metadata Service).
La dirección IP `169.254.169.254` es una dirección de enlace local (link-local) no enrutable en Internet, accesible exclusivamente desde el interior de la propia máquina virtual o servidor de la nube (por ejemplo, una instancia EC2).

¿Qué sucede cuando se fuerza una petición GET a 169.254.169.254?

Cuando la aplicación web contiene un SSRF y el backend procesa una URL hacia `http://169.254.169.254/`, el servidor actúa como un puente no autorizado hacia su propia interfaz de metadatos. Dado que las peticiones se originan dentro del perímetro de la instancia, la interfaz confía en el origen interno y responde con la información del entorno.

Información altamente sensible que el atacante busca extraer

- Credenciales Temporales de Seguridad del Rol IAM ( IAM Role Credentials):
  - Ruta de extracción: 169.254.169.254/latest/meta-data/iam/security-credentials/<nombre-del-rol>
  - Datos expuestos: El servidor devuelve una respuesta JSON en texto plano que contiene las claves `AccessKeyId`, `SecretAccessKey` y el `Token` de sesión asignados al rol IAM de esa instancia
  - Impacto: El atacante puede configurar estas credenciales en la AWS CLI de su propia computadora para autenticarse remotamente en la infraestructura cloud de la víctima con los mismos privilegios que la máquina comprometida.

- Scripts de Aprovisionamiento e Inicialización (User-Data):
  - Ruta de extracción: 169.254.169.254/latest/user-data
  - Datos expuestos: Frecuentemente almacena scripts de despliegue en texto plano con variables de entorno, claves de API, contraseñas de bases de datos o secretos hardcodeados

- Detalles de Red e Infraestructura:
  - Ruta de extracción: 169.254.169.254/latest/meta-data/
  - Datos expuestos: Direcciones IP privadas, claves públicas SSH, identificadores de cuenta de AWS, nombres de seguridad VPC y listas de subredes internas.
