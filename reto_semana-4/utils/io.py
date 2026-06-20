import csv
import os

def leer_inventario(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"No se encontro el archivo: {ruta_archivo}")

    productos_raw = []
    columnas_esperadas = ["sku", "nombre", "categoria", "precio", "stock", "stock_minimo"]
    num_columnas = len(columnas_esperadas)

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        reader = csv.reader(archivo)
        next(reader, None)  # Saltar encabezados

        for num_linea, fila in enumerate(reader, start=2):
            # Eliminar columnas vacias del final
            fila = [campo for campo in fila if campo.strip() != ""]

            if not fila:
                continue

            if len(fila) != num_columnas:
                print(
                    f"  [Linea {num_linea}] Ignorada: se esperaban {num_columnas} "
                    f"columnas, se encontraron {len(fila)}."
                )
                continue

            producto_dict = dict(zip(columnas_esperadas, [campo.strip() for campo in fila]))
            productos_raw.append(producto_dict)

    return productos_raw


def escribir_reporte(productos, ruta_archivo):
    directorio = os.path.dirname(ruta_archivo)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    encabezados = [
        "sku", "nombre", "categoria", "stock_actual",
        "stock_minimo", "unidades_faltantes", "valor_inventario",
    ]

    with open(ruta_archivo, "w", encoding="utf-8", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(encabezados)

        for p in productos:
            writer.writerow([
                p.sku,
                p.nombre,
                p.categoria,
                p.stock,
                p.stock_minimo,
                p.unidades_faltantes(),
                f"{p.valor_inventario():.2f}",
            ])