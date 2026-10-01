¿Qué es un CVE?
Un CVE es un diccionario o sistema de referencia que asigna un número único a vulnerabilidades conocidas den producto de software, este catálogo es mantenido por la MITRE Corporation.
Cada entrada de CVR tiene un número de identificación estándar, un estado, una descripción breve de la falla y referencias a avisos oficiales.

¿Qué es el catálogo CWE?
Es una lista formal de tipos, clases y categorías de debilidades de seguridad en la arquitectura, el diseño o el código fuente del software. Sirve como gúia para que los desarrolladores y arquitectos eviten cometer los mismos errores durante la creación de tecnología.

Diferencia entre CVE y CWE
La diferencia principal es que CVE registra una falla de seguridad concreta en un programa, software o versión específica, mientras que CWE categoriza el tipo de defecto o debilidad sin importar que programa o versión lo contenga, no con el objetivo de solucionar la vulnerabilidad sino para evitar cometer errores al escribir código nuevo.

Las CVE Numbering Authorities (CNAs) son organizaciones y empresas autorizadas para evaluar reportes de fallas y asignarles un identificador CVE único, incluyen a grandes fabricantes tecnológicos (Microsoft, Google, Apple), proyectos de código abierto (Red Hat), centros de respuesta a incidentes informáticos (INCIBE) y firmas especializadas en ciberseguridad. Suelen ser proveedores de software y tecnología, firmas de ciberseguridad, equipos de respuesta ante incidentes (CERTs) o bug bounty hunters.
Existen repositorios y bases de datos públicas para revisar los registros de CVE:
- Catálogo Oficial de CVE (MITRE)
- National Vulnerability Database (NVD)
- Plataformas de Inteligencia de Amenazas

Herramientas automatizadas
- Nuclei: Escáner modular y automatizado que envía peticiones basadas en plantillas (templates* en formato YAML)
- Prisma Cloud (Palo Alto Networks): Una plataforma de protección de aplicaciones nativas de la nube (CNAPP)
- OWASP Dependency-Check: Una herramienta de código abierto muy utilizada en la industria. Analiza las dependencias de un proyecto (Java, .NET, JavaScript, etc.) y determina si existen CVEs asociados mediante consultas directas a la base de datos de la NVD de NIST.
