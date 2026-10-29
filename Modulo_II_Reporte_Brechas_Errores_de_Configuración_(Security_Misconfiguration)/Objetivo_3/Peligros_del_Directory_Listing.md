El Directory Listing (o Listado de Directorios) es una falla de seguridad provocada por una configuración inadecuada en el servidor web. Ocurre cuando el servidor está instruido para mostrar una lista de todos los archivos y subcarpetas contenidos en un directorio si no encuentra un archivo de índice predeterminado.

Cuando un usuario navega a una ruta, el servidor busca automáticamente archivos como index.html, index.php o default.aspx. Si estos archivos no existen y la directiva de listado está activa, el servidor genera dinámicamente una página HTML que actúa como un "explorador de archivos" público. Esto permite que un atacante vea la estructura interna del servidor, descubra archivos ocultos y descargue información sin necesidad de adivinar sus nombres.
Archivos sensibles que podrían quedar expuestos:
Archivos de configuración: Archivos como .env o config.php, que suelen contener credenciales de bases de datos y llaves maestras de APIs.
Backups y archivos temporales: Copias de seguridad como respaldo.sql, web_vieja.zip o archivos de edición (script.php.bak) que contienen código fuente antiguo o datos sensibles.
Carpetas de control de versiones: La carpeta .git/, que permitiría a un atacante descargar y reconstruir el código fuente completo del proyecto.
Logs y registros: Archivos de error o acceso que pueden revelar rutas internas del servidor, IPs de otros usuarios o parámetros de depuración.
Mitigación (Cómo se soluciona): La forma más efectiva de mitigar este riesgo es deshabilitar la directiva desde la configuración del servidor web:
En Apache: Se debe modificar el archivo de configuración o el archivo .htaccess agregando la línea: Options -Indexes
En Nginx: Se debe asegurar que la directiva autoindex esté en off dentro del bloque del sitio: autoindex off;
Buenas prácticas: Como medida de seguridad adicional ("defensa en profundidad"), se recomienda colocar un archivo index.html vacío o un redireccionamiento en todas las carpetas públicas para evitar que el servidor intente listar el contenido.
