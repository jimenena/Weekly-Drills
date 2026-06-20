# Clasificador de Temperaturas 
## Reto Semana 2 — Programación para Ciencia de Datos

Programa de línea de comandos que recibe un archivo CSV con temperaturas de ciudades del mundo (en Celsius o Fahrenheit), unifica todas las temperaturas a Celsius, clasifica cada ciudad según su clima y genera un reporte estandarizado.

## Instruciones de uso:

### Requisitos:
- Asegúrate de tener Python instalado. 
- Ejecutar los comandos desde la carpeta raíz del proyecto.

### Ejecución con archivo de entrada:
- Windows (PowerShell): Get-Content "tests\entrada 1.txt" | python .\main.py
- Windows (CMD): type "tests\entrada 1.txt" | python main.py
- Linux / Mac: python main.py < tests/entrada 1.txt

### Ejecución con entrada manual: python main.py
Puedes escribir los datos directamente en la terminal, línea por línea, sin necesitar un archivo.
- Linux / Mac: python main.py
- Windows (PowerShell): python .\main.py

Después de ejecutar el comando, escribe los datos manualmente:
ciudad,temperatura,unidad     ← escribe esto y presiona Enter
CDMX,22,C                     ← escribe cada ciudad y presiona Enter

- Cuando termines de ingresar todos los datos, presiona:
- Linux / Mac: Ctrl + D
- Windows: Ctrl + Z y luego Enter

### Guardar la salida en un archivo:
- Linux / Mac: python main.py < tests/entrada.txt > tests/salida.txt
- Windows (PowerShell): Get-Content "tests\entrada 1.txt" | python .\main.py | Out-File -FilePath "tests\salida.txt" -Encoding utf8
- Windows (CMD): type "tests\entrada 1.txt" | python main.py > "tests\salida 1.txt"

## Ejemplo:
Archivo entrada 1.txt:
ciudad,temperatura,unidad
CDMX,22,C
Nueva York,50,F
Moscu,-10,C
Miami,95,F
Cancun,30,C
Chicago,14,F
Phoenix,104,F
Error,abc,C
Lima,25,C
Bangkok,36,C

Archivo salida 1.txt:
ciudad,temperatura_celsius,clasificacion
CDMX,22.0,Templado
Nueva York,10.0,Frio
Moscu,-10.0,Congelante
Miami,35.0,Calido
Cancun,30.0,Calido
Chicago,-10.0,Congelante
Phoenix,40.0,Extremo
Lima,25.0,Templado
Bangkok,36.0,Extremo

La línea Error,abc,C no aparece en la salida porque abc no es un número válido y se ignora automáticamente.

## Martinez Hernandez Jimena Michell 