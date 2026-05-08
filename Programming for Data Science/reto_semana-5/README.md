# Perfilador de Datasets
## Reto Semana 5 — Programación para Ciencia de Datos

Script de línea de comandos desarrollado en Python que analiza cualquier archivo CSV, infiere el tipo de dato de cada columna, detecta valores nulos y genera un reporte de calidad de datos automáticamente.

El código está organizado de forma clara y modular, separando cada responsabilidad
en funciones independientes dentro de `main.py`, lo que facilita su mantenimiento
y extensión a futuro.

## Instrucciones de uso:

### Requisitos:
- Asegúrate de tener Python instalado.
- Ejecutar los comandos desde la carpeta raíz del proyecto.
- Contar con el archivo CSV de entrada con encabezados en la primera fila.

### Ejecución:
- Windows (PowerShell): `python main.py --input data/ventas.csv --output outputs/perfil_ventas.csv`
- Linux / Mac: `python3 main.py --input data/ventas.csv --output outputs/perfil_ventas.csv`

El programa lee el archivo automáticamente, muestra el resumen en consola y guarda
el reporte en la ruta indicada. No requiere ninguna entrada manual del usuario.

## Ejemplo:
Entrada archivo `data/ventas.csv`:
fecha,producto,cantidad,precio,vendedor
2026-01-01,Laptop,2,15000.00,Ana
2026-01-02,Mouse,10,250.00,Bob
2026-01-03,Teclado,,800.00,Ana

Salida archivo `outputs/perfil_ventas.csv`: 
nombre_columna,tipo_inferido,total_registros,valores_nulos,porcentaje_nulos,valores_unicos,porcentaje_unicos,ejemplo_valor
fecha,fecha,5,0,0.00,5,100.00,2026-01-01
producto,texto,5,0,0.00,4,80.00,Laptop
cantidad,numerico,5,1,20.00,4,80.00,2
precio,numerico,5,1,20.00,3,60.00,15000.00
vendedor,texto,5,1,20.00,3,60.00,Ana

## Manejo de errores:
El sistema detecta e informa automáticamente:
- Archivo de entrada no encontrado
- Archivo vacío o sin encabezados
- Filas con menos columnas que el encabezado (se completan con vacío)
- Directorio de salida inexistente (se crea automáticamente)

Cada error se reporta en consola con un mensaje claro sin detener innecesariamente la ejecución.

## Martinez Hernandez Jimena Michell 