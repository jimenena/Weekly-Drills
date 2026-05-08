#!/usr/bin/env python3

import argparse
import csv
import sys
import os

def es_valor_nulo(valor):
    if valor is None:
        return True
    if isinstance(valor, str) and valor.strip() == "":
        return True
    return False

def es_numerico(valor):
    try:
        float(str(valor).replace(",", "").strip())
        return True
    except (ValueError, TypeError):
        return False


def es_fecha(valor):
    v = str(valor).strip()

    if len(v) >= 10 and v[4] == "-" and v[7] == "-":
        try:
            partes = v[:10].split("-")
            anio = int(partes[0])
            mes  = int(partes[1])
            dia  = int(partes[2])
            return 1900 <= anio <= 2100 and 1 <= mes <= 12 and 1 <= dia <= 31
        except (ValueError, IndexError):
            pass

    return False


def es_booleano(valor):
    v = str(valor).strip().lower()
    return v in {"true", "false", "yes", "no", "si", "1", "0", "t", "f"}

def inferir_tipo(valores):
    valores_validos = [v for v in valores if not es_valor_nulo(v)]

    if not valores_validos:
        return "texto"  

    total   = len(valores_validos)
    umbral  = 0.8

    num_fechas    = sum(1 for v in valores_validos if es_fecha(v))
    num_booleanos = sum(1 for v in valores_validos if es_booleano(v))
    num_numericos = sum(1 for v in valores_validos if es_numerico(v))

    if num_fechas / total >= umbral:
        return "fecha"
    elif num_booleanos / total >= umbral:
        return "booleano"
    elif num_numericos / total >= umbral:
        return "numerico"
    else:
        return "texto"

def calcular_porcentaje(parte, total):
    if total == 0:
        return 0.00
    return round((parte / total) * 100, 2)


def perfilar_columna(nombre, valores):
    total            = len(valores)
    nulos            = sum(1 for v in valores if es_valor_nulo(v))
    valores_no_nulos = [v for v in valores if not es_valor_nulo(v)]
    unicos           = len(set(valores_no_nulos))
    ejemplo          = valores_no_nulos[0] if valores_no_nulos else ""
    tipo             = inferir_tipo(valores)

    return {
        "nombre_columna"   : nombre,
        "tipo_inferido"    : tipo,
        "total_registros"  : total,
        "valores_nulos"    : nulos,
        "porcentaje_nulos" : calcular_porcentaje(nulos, total),
        "valores_unicos"   : unicos,
        "porcentaje_unicos": calcular_porcentaje(unicos, total),
        "ejemplo_valor"    : ejemplo,
    }

def leer_csv(ruta):
    encabezados = []
    filas       = []

    with open(ruta, "r", encoding="utf-8", newline="") as f:
        lector = csv.reader(f)

        for i, fila in enumerate(lector):
            if i == 0:
                encabezados = fila
            else:
                if any(campo.strip() for campo in fila):
                    filas.append(fila)

    return encabezados, filas


def escribir_csv(ruta, perfiles):
    directorio = os.path.dirname(ruta)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)

    columnas_salida = [
        "nombre_columna",
        "tipo_inferido",
        "total_registros",
        "valores_nulos",
        "porcentaje_nulos",
        "valores_unicos",
        "porcentaje_unicos",
        "ejemplo_valor",
    ]

    with open(ruta, "w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(columnas_salida)  # Encabezados

        for p in perfiles:
            escritor.writerow([
                p["nombre_columna"],
                p["tipo_inferido"],
                p["total_registros"],
                p["valores_nulos"],
                f"{p['porcentaje_nulos']:.2f}",
                p["valores_unicos"],
                f"{p['porcentaje_unicos']:.2f}",
                p["ejemplo_valor"],
            ])

def main():
    parser = argparse.ArgumentParser(
        description="Perfilador de Datasets CSV — analiza la calidad de cualquier CSV.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python main.py --input data/ventas.csv --output outputs/perfil_ventas.csv\n"
            "  python main.py -i data/empleados.csv -o outputs/perfil_empleados.csv\n"
        ),
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Ruta al archivo CSV de entrada a perfilar.",
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Ruta donde guardar el CSV de perfil generado.",
    )

    args = parser.parse_args()

    print(f"Perfilando: {args.input}")

    try:
        encabezados, filas = leer_csv(args.input)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{args.input}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        sys.exit(1)

    if not encabezados:
        print("Error: El archivo está vacío o no tiene encabezados.")
        sys.exit(1)

    print(f"Columnas encontradas : {len(encabezados)}")
    print(f"Registros encontrados: {len(filas)}")

    perfiles = []
    for i, nombre_col in enumerate(encabezados):
        valores = [fila[i] if i < len(fila) else "" for fila in filas]
        perfil  = perfilar_columna(nombre_col, valores)
        perfiles.append(perfil)

    try:
        escribir_csv(args.output, perfiles)
    except Exception as e:
        print(f"Error al escribir el archivo de salida: {e}")
        sys.exit(1)

    print(f"Perfil guardado en  : {args.output}")
    print("¡Completado!")


if __name__ == "__main__":
    main()