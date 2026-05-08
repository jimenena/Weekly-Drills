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

El programa lee el archivo automáticamente, muestra el resumen en consola y guarda el reporte en `outputs/reporte_inventario.csv`.
No requiere ninguna entrada manual del usuario.

## Ejemplo
Entrada:

Archivo `data/inventario.csv`:
```csv
sku,nombre,categoria,precio,stock,stock_minimo
SKU001,Laptop HP,Electronica,15000.00,5,10
SKU002,Mouse Logitech,Accesorios,350.00,3,15
```
Salida:

Archivo `outputs/reporte_inventario.csv`:
```csv
sku,nombre,categoria,stock_actual,stock_minimo,unidades_faltantes,valor_inventario
SKU002,Mouse Logitech,Accesorios,3,15,12,1050.00
SKU005,Audifonos Sony,Accesorios,2,10,8,2400.00
SKU001,Laptop HP,Electronica,5,10,5,75000.00
SKU007,SSD 1TB,Almacenamiento,0,5,5,0.00
```
Solo aparecen productos donde `stock < stock_minimo`, ordenados por unidades faltantes de mayor a menor.

## Manejo de errores
El sistema detecta e ignora automáticamente filas con:
- Precio no numérico
- Stock no numérico
- Columnas faltantes o extra

Cada error se reporta en consola sin detener la ejecución.

## Martinez Hernandez Jimena Michell 
