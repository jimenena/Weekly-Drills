import sys

def fahrenheit_a_celsius(f):
    """Convierte una temperatura de Fahrenheit a Celsius usando la fórmula (F - 32) * 5 / 9."""
    return (f - 32) * 5 / 9

def clasificar_temperatura(celsius):
    """Clasifica la temperatura en Celsius y devuelve su categoría climática."""
    if celsius < 0:
        return "Congelante"
    elif celsius <= 15:
        return "Frio"
    elif celsius <= 25:
        return "Templado"
    elif celsius <= 35:
        return "Calido"
    else:
        return "Extremo"

def main():
    """Lee el CSV desde stdin, procesa cada ciudad y escribe el reporte a stdout."""
    lineas = sys.stdin.readlines()
    print("ciudad,temperatura_celsius,clasificacion")

    for linea in lineas[1:]:       
        linea = linea.strip()
        if not linea:
            continue

        partes = linea.split(',')
        if len(partes) != 3:
            continue

        ciudad = partes[0].strip()
        temp_str = partes[1].strip()
        unidad = partes[2].strip().upper()

        if unidad not in ['C', 'F']:
            continue

        try:
            temperatura = float(temp_str)
        except ValueError:
            continue

        if unidad == 'F':
            celsius = fahrenheit_a_celsius(temperatura)
        else:
            celsius = temperatura

        clasificacion = clasificar_temperatura(celsius)
        print(f"{ciudad},{celsius:.1f},{clasificacion}")

if __name__ == "__main__":
    main()