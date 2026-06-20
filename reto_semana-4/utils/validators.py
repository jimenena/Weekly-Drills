import math

def es_nan_o_inf(valor):
    try:
        num = float(valor)
        return math.isnan(num) or math.isinf(num)
    except (ValueError, TypeError):
        return False


def validar_sku(sku):
    if not sku or not str(sku).strip():
        return False
    return True


def validar_precio(precio):
    try:
        precio_num = float(precio)
        if math.isnan(precio_num) or math.isinf(precio_num):
            return False
        return precio_num >= 0
    except (ValueError, TypeError):
        return False


def validar_stock(stock):
    try:
        valor = float(stock)
        if math.isnan(valor) or math.isinf(valor):
            return False
        return int(valor) >= 0
    except (ValueError, TypeError):
        return False


def validar_producto(sku, nombre, categoria, precio, stock, stock_minimo):
    if not validar_sku(sku):
        return False, "SKU vacio o invalido"

    if not nombre or not str(nombre).strip():
        return False, "Nombre vacio"

    if not categoria or not str(categoria).strip():
        return False, "Categoria vacia"

    for campo, valor in [("precio", precio), ("stock", stock), ("stock_minimo", stock_minimo)]:
        if es_nan_o_inf(valor):
            return False, f"{campo} contiene NaN o infinito: '{valor}'"

    if not validar_precio(precio):
        return False, f"Precio invalido: '{precio}'"

    if not validar_stock(stock):
        return False, f"Stock invalido: '{stock}'"

    if not validar_stock(stock_minimo):
        return False, f"Stock minimo invalido: '{stock_minimo}'"

    return True, None