# Analizador de Ventas
# Reto Semana 3: Analizador de Ventas

El programa agrupa todas las transacciones del mismo producto, calcula el total de unidades vendidas, el ingreso total y el precio promedio, y presenta los resultados ordenados de mayor a menor ingreso.

## Instruciones de uso:

### Requisitos:
- Asegúrate de tener Python instalado.
- Ejecutar los comandos desde la carpeta raíz del proyecto.

### Ejecución con archivo de entrada:
- Windows (PowerShell): Get-Content "tests\entrada.txt" | python .\main.py
- Windows (CMD): type "tests\entrada.txt" | python main.py
- Linux / Mac: python main.py < tests/entrada.txt

### Ejecución con entrada manual: python main.py
Puedes escribir los datos directamente en la terminal, línea por línea, sin necesitar un archivo.
- Linux / Mac: python main.py
- Windows (PowerShell): python .\main.py

Después de ejecutar el comando, escribe los datos manualmente:
fecha,producto,cantidad,precio_unitario   ← escribe esto y presiona Enter
2026-01-01,Laptop,2,15000.00             ← escribe cada transacción y presiona Enter
2026-01-02,Mouse,10,250.00

Cuando termines de ingresar todos los datos, presiona:
Linux / Mac: Ctrl + D
Windows: Ctrl + Z y luego Enter

### Guardar la salida en un archivo:
- Linux / Mac: python main.py < tests/entrada.txt > tests/salida.txt
- Windows (PowerShell): Get-Content "tests\entrada.txt" | python .\main.py | Out-File -FilePath "tests\salida.txt" -Encoding utf8
- Windows (CMD): type "tests\entrada.txt" | python main.py > "tests\salida.txt"

### Generar datos de prueba: 
Generar 100 registros sin errores
python generar_entrada.py 100 | python main.py

Generar 100 registros con 20% de errores
python generar_entrada.py 100 20 | python main.py

## Ejemplo:
Archivo entrada.txt:
fecha,producto,cantidad,precio_unitario
2026-01-01,Laptop,2,15000.00
2026-01-02,Mouse,10,250.00
2026-01-03,Laptop,1,14500.00
2026-01-04,Teclado,5,800.00
2026-01-05,Mouse,8,250.00
2026-01-06,Monitor,3,6000.00
2026-01-07,Laptop,2,15500.00
2026-01-08,Audifonos,20,350.00
2026-01-09,Mouse,5,275.00
2026-01-10,Monitor,2,5800.00

Archivo salida.txt:
producto,unidades_vendidas,ingreso_total,precio_promedio
Laptop,5,75500.00,15100.00
Monitor,5,29600.00,5920.00
Audifonos,20,7000.00,350.00
Mouse,23,5875.00,255.43
Teclado,5,4000.00,800.00

¿Por qué la salida tiene esos valores?
El programa toma todas las transacciones del archivo de entrada y las consolida por producto. Por ejemplo, Laptop aparece tres veces en la entrada con distintas cantidades y precios, por lo que el programa suma todas sus unidades y calcula el ingreso total multiplicando cada cantidad por su precio unitario. El resultado se ordena de mayor a menor ingreso, por eso Laptop aparece primero con el ingreso más alto.

Las líneas con datos inválidos como columnas faltantes o valores no numéricos se ignoran automáticamente, por lo que no afectan los cálculos ni aparecen en la salida.

El precio promedio no es el promedio simple de los precios, sino el ingreso total dividido entre las unidades vendidas. Esto refleja el valor real promedio por unidad considerando todas las transacciones del producto.

## Martinez Hernandez Jimena Michell 