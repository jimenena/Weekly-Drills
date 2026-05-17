# Validador de Códigos con Expresiones Regulares
## Reto Semana 6 — Programación para Ciencia de Datos

Script de línea de comandos desarrollado en Python que valida códigos de productos,
envíos, empleados y facturas de una empresa de logística usando expresiones regulares.

El código está organizado de forma clara y modular, separando cada responsabilidad
en funciones independientes dentro de main.py, lo que facilita su mantenimiento
y extensión a futuro.

## Instrucciones de uso:

### Requisitos:
- Asegúrate de tener Python instalado.
- Ejecutar los comandos desde la carpeta raíz del proyecto.
- Contar con el archivo de entrada con un código por línea.

### Reglas de validación:

producto: categoría y país deben estar en MAYÚSCULAS.
envio: año entre 2020-2030, mes entre 01-12, día entre 01-31.
empleado: departamento debe ser VEN, ADM, TEC, LOG o RHH; número no puede empezar con 0.
factura: serie debe ser A, B, C, D o E en MAYÚSCULA.
desconocido: cualquier código que no encaje en los formatos anteriores; siempre INVALIDO.

### Ejecución:
- Windows (PowerShell): Get-Content tests\codigos.txt | python main.py 
- Windows (CMD): python main.py < tests\codigos.txt
- Linux / Mac: python3 main.py < tests/codigos.txt

### Para guardar la salida en un archivo:

- Windows (PowerShell): Get-Content tests\codigos.txt | python main.py | Out-File -Encoding utf8 resultados.csv
- Windows (CMD): python main.py < tests\codigos.txt > resultados.csv
- Linux / Mac: python3 main.py < tests/codigos.txt > resultados.csv

El programa lee los códigos automáticamente línea por línea, detecta el tipo de cada uno y escribe el resultado en formato CSV. No requiere ninguna entrada manual del usuario.

## Ejemplo:
Entrada archivo 'codigos.txt':
TEC-0001-MX
ALI-9999-US
ROB-1234-CA
tec-0001-MX
TEC-001-MX
TECH-0001-MX
ENV-2024-03-15-001234
ENV-2025-12-01-999999
ENV-2019-03-15-001234
ENV-2024-13-15-001234
ENV-2024-03-32-001234
EMP-VEN-1234
EMP-TEC-9999
EMP-ADM-1000
EMP-VEN-0123
EMP-XXX-1234
EMP-VEN-123
FAC-A-123456
FAC-E-000001
FAC-B-999999
FAC-F-123456
FAC-A-12345
FAC-a-123456
XXX-1234
RANDOM-CODE


Salida archivo:
codigo,tipo,valido
TEC-0001-MX,producto,VALIDO
ALI-9999-US,producto,VALIDO
ROB-1234-CA,producto,VALIDO
tec-0001-MX,producto,INVALIDO
TEC-001-MX,desconocido,INVALIDO
TECH-0001-MX,desconocido,INVALIDO
ENV-2024-03-15-001234,envio,VALIDO
ENV-2025-12-01-999999,envio,VALIDO
ENV-2019-03-15-001234,envio,INVALIDO
ENV-2024-13-15-001234,envio,INVALIDO
ENV-2024-03-32-001234,envio,INVALIDO
EMP-VEN-1234,empleado,VALIDO
EMP-TEC-9999,empleado,VALIDO
EMP-ADM-1000,empleado,VALIDO
EMP-VEN-0123,empleado,INVALIDO
EMP-XXX-1234,empleado,INVALIDO
EMP-VEN-123,desconocido,INVALIDO
FAC-A-123456,factura,VALIDO
FAC-E-000001,factura,VALIDO
FAC-B-999999,factura,VALIDO
FAC-F-123456,factura,INVALIDO
FAC-A-12345,desconocido,INVALIDO
FAC-a-123456,factura,INVALIDO
XXX-1234,desconocido,INVALIDO


## Manejo de errores:
El sistema detecta e informa automáticamente:
- Líneas vacías en la entrada (se ignoran sin producir salida)
- Códigos con estructura incorrecta (se clasifican como desconocido)
- Códigos con formato correcto pero valores inválidos (tipo correcto, marcados como INVALIDO)

Cada código se reporta en la salida CSV con su tipo y estado sin detener la ejecución.

## Martinez Hernandez Jimena Michell 