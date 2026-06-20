# Sistema de Inventario Modular
## Reto Semana 4 — Programación para Ciencia de Datos

Sistema modular en Python que lee un inventario CSV, valida los datos, identifica productos con stock bajo y genera un reporte de reorden automáticamente.

El código está organizado de forma modular y profesional, separando
responsabilidades en carpetas `models/` y `utils/`, lo que facilita
su mantenimiento y extensión a futuro.

## Instrucciones de uso:

### Requisitos:
- Asegúrate de tener Python instalado.
- Ejecutar los comandos desde la carpeta raíz del proyecto.
- Contar con el archivo `data/inventario.csv` con el formato correcto.

### Ejecución:
- Windows (PowerShell): `python main.py`
- Linux / Mac: `python3 main.py`

El programa genera automáticamente el reporte en `outputs/reporte_inventario.csv`.
No requiere ninguna entrada manual del usuario.

### Registros que se descartan automáticamente:
- Precio, stock o stock mínimo con valor `inf`, `-inf` o `NaN`
- Columnas faltantes o con datos extra
- SKUs duplicados
- Precio no numérico 

## Ejemplo
Entrada:

Archivo `data/inventario.csv`:
```csv
SKU47845,Mouse Gaming MSI,Accesorios,inf,1,50
SKU47846,Audifonos SanDisk,Audio,674.50,0,10
SKU47847,SSD Externo Seagate,Almacenamiento,5346.05,146,50
SKU47848,Procesador WD,Componentes,9644.82,14,5
SKU47849,NAS Dell,Almacenamiento,18923.49,9,10,12..5,N/A
SKU47848,Procesador WD,Componentes,9644.82,14,5
SKU47849,NAS Dell,Almacenamiento,18923.49,9,10,12..5,N/A
SKU47850,HDD Dell,Almacenamiento,2211.39,,25
SKU47851,Audifonos Bluetooth Corsair,Audio,1664.06,inf,50
SKU47852,Touchpad Seagate,Accesorios,1886.44,59,30
SKU48582,Monitor Xiaomi,Electronica,13838.80,30,10
SKU48583,Teclado Mecanico Sony,Accesorios,2098.46,26,NaN
SKU48584,Teclado Gaming Apple,Accesorios,2968.53,0,5
SKU48585,Monitor Gaming Lenovo,Electronica,inf,31,15
SKU48586,MacBook TP-Link,Electronica,29063.93,15,10,inf,---,abc
SKU48587,SSD Externo Sony,Almacenamiento,2776.46
SKU48588,Laptop Logitech,Electronica,18748.16,23,10
SKU48589,Bocina HP,Audio,1012.22,59,25
SKU48590,MacBook LG,Electronica,35596.40,3,50
SKU48591,HDD Dell,Almacenamiento,2704.30,27,25
SKU48592,Monitor Asus,Electronica,TBD,96,50
```
Salida:

Archivo `outputs/reporte_inventario.csv`:
```csv
sku,nombre,categoria,stock_actual,stock_minimo,unidades_faltantes,valor_inventario
SKU48590,MacBook LG,Electronica,3,50,47,106789.20
SKU31368,NAS SanDisk,Almacenamiento,16,50,34,328124.32
SKU31371,Teclado WD,Accesorios,7,25,18,8465.24
SKU31366,SSD Seagate,Almacenamiento,34,50,16,52235.22
SKU47846,Audifonos SanDisk,Audio,0,10,10,0.00
SKU48584,Teclado Gaming Apple,Accesorios,0,5,5,0.00

```
Solo aparecen productos donde `stock < stock_minimo`, ordenados por unidades faltantes de mayor a menor.

## Manejo de errores
El sistema detecta e ignora automáticamente filas con:
- Precio no numérico
- Stock no numérico
- Columnas faltantes o extra

Cada error se reporta en consola sin detener la ejecución.

### Descripción de archivos

**`main.py`**
Punto de entrada del programa. Orquesta el flujo completo: lectura,
validación, filtrado, ordenamiento y generación del reporte.

**`models/producto.py`**
Define la clase `Producto` con toda la lógica de negocio encapsulada.
Contiene los métodos `necesita_reorden()`, `unidades_faltantes()` y
`valor_inventario()`.

**`models/__init__.py`**
Hace que la carpeta `models` sea reconocida como módulo de Python
y expone la clase `Producto` para importarla desde otros archivos.

**`utils/validators.py`**
Contiene las funciones de validación de datos: `validar_sku()`,
`validar_precio()`, `validar_stock()` y `validar_producto()`.
Detecta y descarta valores inválidos como `NaN`, `inf`, `-inf`,
textos no numéricos y campos vacíos.

**`utils/io.py`**
Maneja la lectura del archivo CSV de entrada y la escritura del
reporte de salida. Elimina automáticamente columnas vacías generadas
por Excel y descarta filas con número incorrecto de columnas.

**`utils/__init__.py`**
Hace que la carpeta `utils` sea reconocida como módulo de Python
y expone las funciones de validación y de entrada/salida.

**`data/inventario.csv`**
Archivo CSV de entrada con el inventario actual. Debe contener
las columnas: `sku`, `nombre`, `categoria`, `precio`, `stock` y `stock_minimo`.

**`outputs/reporte_inventario.csv`**
Archivo CSV generado automáticamente por el programa. Contiene
únicamente los productos que necesitan reorden, ordenados por
urgencia de mayor a menor.

**`.gitignore`**
Lista de archivos y carpetas que Git debe ignorar, como `__pycache__/`,
archivos `.pyc` y la carpeta `outputs/`.

## Martinez Hernandez Jimena Michell 
