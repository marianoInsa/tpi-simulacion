# Archivo: analisis_estadistico.py

import importlib
import numpy as np
from scipy import stats

# --- Parámetros de simulación ---
N_CORRIDAS = 30  # Cantidad de repeticiones por criterio
CRITERIOS = [
    "criterio_produccion_constante",
    "criterio_demanda_anterior",
    "criterio_promedio_dias_anteriores",
    "criterio_minimo_faltante"
]

# --- Función para ejecutar un criterio y extraer el beneficio real ---
def ejecutar_y_extraer_beneficio(nombre_modulo):
    modulo = importlib.import_module(f"criterios.{nombre_modulo}")
    return getattr(modulo, "ultimo_beneficio_real", None)

# --- Función para calcular y mostrar estadística con t de Student ---
def calcular_estadisticas(nombre_criterio, beneficios):
    n = len(beneficios)
    media = np.mean(beneficios)
    std = np.std(beneficios, ddof=1)  # Desvío estándar muestral
    alpha = 0.05
    t_val = stats.t.ppf(1 - alpha/2, df=n-1)
    margen_error = t_val * (std / np.sqrt(n))

    print(f"\n=== Análisis para {nombre_criterio} ===")
    print(f"Media de beneficio real: ${media:.2f}")
    print(f"Intervalo de confianza al 95%: ${media - margen_error:.2f} a ${media + margen_error:.2f}")
    print(f"Desvío estándar muestral: ${std:.2f}")

# --- Ejecución principal ---
if __name__ == "__main__":
    for criterio in CRITERIOS:
        beneficios = []
        for i in range(N_CORRIDAS):
            importlib.invalidate_caches()
            try:
                beneficio = ejecutar_y_extraer_beneficio(criterio)
                if beneficio is not None:
                    beneficios.append(beneficio)
            except Exception as e:
                print(f"Error en corrida #{i+1} del criterio '{criterio}': {e}")

        if beneficios:
            calcular_estadisticas(criterio, beneficios)
        else:
            print(f"No se pudieron obtener beneficios para el criterio: {criterio}")
