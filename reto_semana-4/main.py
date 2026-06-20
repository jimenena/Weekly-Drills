#!/usr/bin/env python3

from models.producto import Producto
from utils.validators import validar_producto
from utils.io import leer_inventario, escribir_reporte

ARCHIVO_INVENTARIO = "data/inventario.csv"
ARCHIVO_REPORTE = "outputs/reporte_inventario.csv"

def crear_productos(datos_raw):
    productos = []
    skus_vistos = set()

    for datos in datos_raw:
        sku = datos.get("sku", "")
        nombre = datos.get("nombre", "")
        categoria = datos.get("categoria", "")
        precio = datos.get("precio", "")
        stock = datos.get("stock", "")
        stock_minimo = datos.get("stock_minimo", "")

        es_valido, error = validar_producto(sku, nombre, categoria, precio, stock, stock_minimo)

        if not es_valido:
            print(f"  [Advertencia] Registro '{sku}' ignorado: {error}")
            continue

        if sku in skus_vistos:
            print(f"  [Advertencia] SKU duplicado '{sku}' ignorado.")
            continue

        skus_vistos.add(sku)
        producto = Producto(
            sku=sku,
            nombre=nombre,
            categoria=categoria,
            precio=float(precio),
            stock=int(float(stock)),
            stock_minimo=int(float(stock_minimo)),
        )
        productos.append(producto)

    return productos

def filtrar_necesitan_reorden(productos):
    return [p for p in productos if p.necesita_reorden()]

def ordenar_por_faltantes(productos):
    return sorted(productos, key=lambda p: p.unidades_faltantes(), reverse=True)

def mostrar_resumen(productos_reorden):
    print("\n" + "-" * 60)
    print("PRODUCTOS QUE NECESITAN REORDEN:")
    print("-" * 60)

    if not productos_reorden:
        print("  (Ningun producto necesita reorden en este momento)")
        return

    for p in productos_reorden:
        print(p)
        print(
            f"   Faltan: {p.unidades_faltantes()} uds. | "
            f"Valor actual en inventario: ${p.valor_inventario():,.2f}"
        )

def main():
    print("=" * 60)
    print("  SISTEMA DE INVENTARIO - Reporte de Reorden")
    print("=" * 60)

    print(f"\n[1] Leyendo inventario desde: {ARCHIVO_INVENTARIO}")
    try:
        datos_raw = leer_inventario(ARCHIVO_INVENTARIO)
    except FileNotFoundError as e:
        print(f"  ERROR: {e}")
        return
    print(f"  Registros leidos del CSV: {len(datos_raw)}")

    print("\n[2] Validando y creando objetos Producto...")
    productos = crear_productos(datos_raw)
    print(f"  Productos validos procesados: {len(productos)}")

    print("\n[3] Filtrando productos con stock bajo...")
    necesitan_reorden = filtrar_necesitan_reorden(productos)
    necesitan_reorden = ordenar_por_faltantes(necesitan_reorden)
    print(f"  Productos que necesitan reorden: {len(necesitan_reorden)}")

    mostrar_resumen(necesitan_reorden)

    print(f"\n[4] Generando reporte en: {ARCHIVO_REPORTE}")
    escribir_reporte(necesitan_reorden, ARCHIVO_REPORTE)
    print(f"  Reporte guardado correctamente ({len(necesitan_reorden)} registros).")

    print("\n" + "=" * 60)
    print("  Proceso completado exitosamente.")
    print("=" * 60)


if __name__ == "__main__":
    main()