import sys
import hashlib

def main():
    #Validamos que se pasen los 3 argumentos necesarios (inicio, fin, archivo)
    if len(sys.argv) != 4:
        print("Uso incorrecto.")
        print("Ejemplo de uso: python rango_MD5.py 1 100 hashes.txt")
        sys.exit(1)
    try:
        inicio = int(sys.argv[1])
        fin = int(sys.argv[2])
        archivo_salida = sys.argv[3]
    except ValueError:
        print("Error: El inicio y el fin del rango deben ser numeros enteros.")
        sys.exit(1)

    print(f"Generando hashes MD5 del rango {inicio} a {fin} en el archivo '{archivo_salida}'...")

    #Generamos y guardamos los hashes directamente en el archivo
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as archivo:
            for numero in range(inicio, fin + 1):
                hash_md5 = hashlib.md5(str(numero).encode('utf-8')).hexdigest()
                archivo.write(hash_md5 + "\n")

        print("Proceso completado con éxito.")
    except IOError as e:
        print(f"Error al escribir en el archivo: {e}")

if __name__ == "__main__":
    main()
