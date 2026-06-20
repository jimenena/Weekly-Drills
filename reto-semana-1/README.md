# Calculadora de Sumas
## Reto Semana 1 — Programación para Ciencia de Datos

Programa de línea de comandos que simula el procesamiento de reportes de ventas de diferentes sucursales. Cada sucursal envía un archivo de texto donde cada línea contiene los valores del día separados por comas; el programa calcula el total por línea e imprime el resultado en la salida estándar.

## Instrucciones de uso:

### Requisitos:
- Asegúrate de tener Python instalado. 
- Ejecutar los comandos desde la carpeta raíz del proyecto.

### Ejecución con archivo de entrada:
- Windows (PowerShell): Get-Content tests\entrada.txt | python main.py
- Windows (CMD): type tests\entrada.txt | python main.py
- Linux / Mac: python main.py < tests/entrada.txt

### Ejecución con entrada manual: python main.py
También es posible proporcionar los datos manualmente desde la terminal. 
Después de ejecutar el comando:
- Escribe cada línea de datos y presiona Enter.
- Para finalizar la entrada:
  - Windows: Ctrl + Z y luego Enter.
  - Linux/macOS: Ctrl + D.

### Guardar la salida en un archivo:
- En Windows (PowerShell): Get-Content tests\entrada.txt | python main.py > salida.txt
- En Linux/ Mac: python main.py < tests/entrada.txt > salida.txt

## Ejemplo:
Archivo entrada.txt:
1,2,3
abc
$2,00
3.99
-0.14

Archivo salida.txt:
6
0
2
3
0

## Martinez Hernandez Jimena Michell 