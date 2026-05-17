import sys
import re

DEPARTAMENTOS_VALIDOS = ['VEN', 'ADM', 'TEC', 'LOG', 'RHH']
SERIES_VALIDAS        = ['A', 'B', 'C', 'D', 'E']

PATRON_TIPO_PRODUCTO  = re.compile(r'^[A-Za-z]{3}-\d{4}-[A-Za-z]{2}$')

PATRON_TIPO_ENVIO     = re.compile(r'^ENV-\d{4}-\d{2}-\d{2}-\d{6}$')

PATRON_TIPO_EMPLEADO  = re.compile(r'^EMP-[A-Za-z]{3}-\d{4}$')

PATRON_TIPO_FACTURA   = re.compile(r'^FAC-[A-Za-z]-\d{6}$')

PATRON_PRODUCTO_VALIDO = re.compile(r'^([A-Z]{3})-(\d{4})-([A-Z]{2})$')

PATRON_ENVIO_VALIDO    = re.compile(r'^ENV-(\d{4})-(\d{2})-(\d{2})-(\d{6})$')

PATRON_EMPLEADO_VALIDO = re.compile(r'^EMP-([A-Z]{3})-(\d{4})$')

PATRON_FACTURA_VALIDA  = re.compile(r'^FAC-([A-Z])-(\d{6})$')

def detectar_tipo(codigo: str) -> str:

    if PATRON_TIPO_ENVIO.match(codigo):
        return 'envio'
    if PATRON_TIPO_EMPLEADO.match(codigo):
        return 'empleado'
    if PATRON_TIPO_FACTURA.match(codigo):
        return 'factura'
    # El de producto es el más genérico: va al final
    if PATRON_TIPO_PRODUCTO.match(codigo):
        return 'producto'
    return 'desconocido'

def validar_producto(codigo: str) -> bool:
  
    return PATRON_PRODUCTO_VALIDO.match(codigo) is not None


def validar_envio(codigo: str) -> bool:
   
    match = PATRON_ENVIO_VALIDO.match(codigo)
    if not match:
        return False  

    anio = int(match.group(1))  
    mes  = int(match.group(2))  
    dia  = int(match.group(3))  

    anio_valido = 2020 <= anio <= 2030
    mes_valido  = 1 <= mes <= 12
    dia_valido  = 1 <= dia <= 31

    return anio_valido and mes_valido and dia_valido

def validar_empleado(codigo: str) -> bool:
   
    match = PATRON_EMPLEADO_VALIDO.match(codigo)
    if not match:
        return False

    departamento = match.group(1)  
    numero       = match.group(2)  

    depto_valido  = departamento in DEPARTAMENTOS_VALIDOS
    numero_valido = numero[0] != '0'  

    return depto_valido and numero_valido


def validar_factura(codigo: str) -> bool:

    match = PATRON_FACTURA_VALIDA.match(codigo)
    if not match:
        return False

    serie = match.group(1)  # ej. "A", "F"

    return serie in SERIES_VALIDAS

def validar_codigo(codigo: str) -> tuple:

    tipo = detectar_tipo(codigo)

    if tipo == 'producto':
        return tipo, validar_producto(codigo)
    elif tipo == 'envio':
        return tipo, validar_envio(codigo)
    elif tipo == 'empleado':
        return tipo, validar_empleado(codigo)
    elif tipo == 'factura':
        return tipo, validar_factura(codigo)
    else:
        return 'desconocido', False  

def main():

    print("codigo,tipo,valido")  

    for linea in sys.stdin:
        codigo = linea.strip()   

        if not codigo:          
            continue

        tipo, es_valido = validar_codigo(codigo)
        estado = 'VALIDO' if es_valido else 'INVALIDO'

        print(f"{codigo},{tipo},{estado}")  

if __name__ == "__main__":
    main()