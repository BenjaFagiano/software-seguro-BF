import pyzipper
from itertools import permutations

SECUENCIA = "abccdaddddec"
ARCHIVO_ZIP = "secreto.zip"

# Los 9 dígitos posibles del teclado
DIGITOS = "123456789"

# Las 5 teclas que aparecen en el video
TECLAS = ["a", "b", "c", "d", "e"]

total = 0

print(f"Secuencia: {SECUENCIA}")
print(f"Teclas utilizadas: {TECLAS}")
print("Total de combinaciones: 15120")
print()

for asignacion in permutations(DIGITOS, 5):

    total += 1

    # Crear correspondencia tecla -> dígito
    mapa = dict(zip(TECLAS, asignacion))

    # Transformar la secuencia de teclas en la contraseña
    password = "".join(mapa[tecla] for tecla in SECUENCIA)

    try:
        with pyzipper.AESZipFile(ARCHIVO_ZIP, "r") as z:
            z.setpassword(password.encode())
            z.read("secreto.txt")

        print("=" * 40)
        print("¡CONTRASEÑA ENCONTRADA!")
        print(f"Password: {password}")
        print(f"Intento: {total}")
        print(f"Correspondencia: {mapa}")
        print("=" * 40)

        with open("resultado.txt", "w") as f:
            f.write(password)

        break

    except RuntimeError:
        pass

else:
    print("No se encontró una contraseña válida.")
    print(f"Intentos realizados: {total}")
