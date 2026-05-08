import sys
import math


def leer_transacciones():
    transacciones = []

    for numero_linea, linea in enumerate(sys.stdin):
        linea = linea.strip()

        if numero_linea == 0 or not linea:
            continue

        columnas = linea.split(",")

        if len(columnas) < 4:
            continue

        fecha, producto, cantidad_str, precio_str = columnas[:4]

        try:
            cantidad = int(cantidad_str)
            precio = float(precio_str)
            if not math.isfinite(precio):
                continue
        except ValueError:
            continue

        transacciones.append({
            "producto": producto,
            "cantidad": cantidad,
            "precio": precio,
        })

    return transacciones


def agrupar_por_producto(transacciones):
    productos = {}

    for t in transacciones:
        producto = t["producto"]

        if producto not in productos:
            productos[producto] = {
                "unidades": 0,
                "ingreso": 0.0,
            }

        productos[producto]["unidades"] += t["cantidad"]
        productos[producto]["ingreso"] += t["cantidad"] * t["precio"]

    return productos


def calcular_reporte(productos):  
    filas = []

    for nombre, datos in productos.items():
        unidades = datos["unidades"]
        ingreso = datos["ingreso"]

        # Regla: evitar división por cero
        precio_promedio = ingreso / unidades if unidades > 0 else 0.0

        filas.append({
            "producto": nombre,
            "unidades_vendidas": unidades,
            "ingreso_total": ingreso,
            "precio_promedio": precio_promedio,
        })

    filas_ordenadas = sorted(filas, key=lambda fila: fila["ingreso_total"], reverse=True)

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