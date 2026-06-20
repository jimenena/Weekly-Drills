import sys


def limpiar_valor(valor):
    valor = valor.strip()
    caracteres_validos = "0123456789.-"
    resultado = ""
    for char in valor:
        if char in caracteres_validos:
            resultado += char
    return resultado


def convertir_a_entero(texto):
    if not texto:
        return 0
    try:
        numero = float(texto)
        return int(numero)
    except ValueError:
        return 0


def procesar_linea(linea):
    linea = linea.strip()

    if not linea:
        return 0

    valores = linea.split(",")

    total = 0
    for valor in valores:
        limpio = limpiar_valor(valor)
        total += convertir_a_entero(limpio)

    return total


def main():
    for linea in sys.stdin:
        resultado = procesar_linea(linea)
        print(resultado)


if __name__ == "__main__":
    main()