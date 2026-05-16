import sys
import math


def leer_transacciones():
   
    transacciones = []

    for numero_linea, linea in enumerate(sys.stdin):
        linea = linea.strip()

        if numero_linea == 0 or not linea:
            continue

        columnas = linea.split(",")

        if len(columnas) != 4:
            continue

        fecha, producto, cantidad_str, precio_str = columnas

        try:
            cantidad = int(cantidad_str.strip())
            precio = float(precio_str.strip())
            if not math.isfinite(precio) or not math.isfinite(float(cantidad)):
                continue
        except ValueError:
            continue

        transacciones.append({
            "producto": producto.strip(),
            "cantidad": cantidad,
            "precio": precio,
        })

    return transacciones


def agrupar_por_producto(transacciones):
    
    productos = {}

    for t in transacciones:
        producto = t["producto"]

        # Si el producto no existe en el diccionario, lo inicializamos
        if producto not in productos:
            productos[producto] = {
                "unidades": 0,
                "ingreso": 0.0,
            }

        # Acumulamos unidades e ingreso
        productos[producto]["unidades"] += t["cantidad"]
        productos[producto]["ingreso"] += t["cantidad"] * t["precio"]

    return productos


def calcular_reporte(productos):
   
    filas = []

    for nombre, datos in productos.items():
        unidades = datos["unidades"]
        ingreso = datos["ingreso"]

        precio_promedio = ingreso / unidades if unidades > 0 else 0.0

        filas.append({
            "producto": nombre,
            "unidades_vendidas": unidades,
            "ingreso_total": ingreso,
            "precio_promedio": precio_promedio,
        })

    filas_ordenadas = sorted(
        filas,
        key=lambda fila: (-fila["ingreso_total"], fila["producto"])
    )

    return filas_ordenadas


def imprimir_reporte(filas):
    
    print("producto,unidades_vendidas,ingreso_total,precio_promedio")

    for fila in filas:
        print(
            f"{fila['producto']},"
            f"{fila['unidades_vendidas']},"
            f"{fila['ingreso_total']:.2f},"
            f"{fila['precio_promedio']:.2f}"
        )


def main():
    transacciones = leer_transacciones()
    productos = agrupar_por_producto(transacciones)
    reporte = calcular_reporte(productos)
    imprimir_reporte(reporte)


if __name__ == "__main__":
    main()