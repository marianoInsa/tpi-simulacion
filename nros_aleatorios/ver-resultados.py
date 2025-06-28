# ver-resultados.py

import csv
from generador_congruencial_mixtov2 import main as ejecutar_simulaciones
import os

def analizar_resultados(archivos_csv):
    """
    Lee uno o más archivos CSV de resultados, los combina y muestra los 5 mejores.
    """
    rows = []
    
    print("\n--- Análisis de Resultados ---")

    for archivo in archivos_csv:
        if not os.path.exists(archivo):
            print(f"Advertencia: El archivo de resultados '{archivo}' no fue encontrado. Omitiendo.")
            continue
        
        print(f"Leyendo resultados de '{archivo}'...")
        with open(archivo, newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)  # Omitir cabecera

            for row in reader:
                try:
                    p = int(row[0])
                    beneficio_prom = float(row[1])
                    lower = float(row[4])
                    upper = float(row[5])
                    
                    # Añadimos el origen del dato para mayor claridad
                    tipo_simulacion = "Weekday" if "weekday" in archivo else "Weekend"

                    rows.append({
                        'p': p,
                        'beneficio_prom': beneficio_prom,
                        'lower': lower,
                        'upper': upper,
                        'tipo': tipo_simulacion
                    })
                except (ValueError, IndexError):
                    continue  # Omitir filas con formato incorrecto

    if not rows:
        print("No se encontraron datos para analizar.")
        return

    # Ordenar por beneficio_prom descendente
    rows.sort(key=lambda x: -x['beneficio_prom'])

    # Imprimir los 5 mejores resultados
    print("\n--- Top 5 mejores valores de 'p' (combinando Weekday y Weekend) ---\n")
    for i, row in enumerate(rows[:5], start=1):
        intervalo_longitud = row['upper'] - row['lower']
        print(f"{i}. Tipo: {row['tipo']:<8} | p = {row['p']:<3} | Beneficio Prom: {row['beneficio_prom']:>9.2f} | "
              f"Intervalo de Confianza = [{row['lower']:.2f}, {row['upper']:.2f}] (longitud = {intervalo_longitud:.2f})")

if __name__ == "__main__":
    # 1. Ejecutar las simulaciones optimizadas para generar los archivos CSV
    print("--- Iniciando Simulaciones (esto puede tardar) ---")
    ejecutar_simulaciones()
    
    # 2. Una vez terminadas, analizar los archivos generados
    archivos_a_analizar = ['resultados_weekday.csv', 'resultados_weekend.csv']
    analizar_resultados(archivos_a_analizar)