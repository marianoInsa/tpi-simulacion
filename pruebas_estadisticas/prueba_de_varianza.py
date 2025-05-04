# Prueba estadística para números aleatorios
# Descripción: Este script implementa la prueba estadística llamada "Prueba de Varianza" para determinar la validez de un conjunto de números aleatorios.

import numpy as np
from scipy import stats

def prueba_de_varianza(numeros_aleatorios, alpha=0.05):
    """
    Realiza la prueba de varianza para determinar si un conjunto de números aleatorios
    tiene una varianza consistente con una distribución uniforme entre 0 y 1.
    
    Parámetros:
    numeros_aleatorios (list): Lista de números aleatorios entre 0 y 1.
    alpha (float): Nivel de significancia. Por defecto es 0.05.
    
    Retorna:
    bool: True si se acepta la hipótesis nula (los números son aleatorios), False en caso contrario.
    """
    
    # Número de observaciones
    n = len(numeros_aleatorios)
    
    # Calcular la varianza muestral
    varianza_muestral = np.var(numeros_aleatorios, ddof=1)  # ddof=1 para varianza muestral insesgada
    
    # Varianza teórica para una distribución uniforme entre 0 y 1
    varianza_teorica = 1/12
    
    # Grados de libertad
    df = n - 1
    
    # Valores críticos de chi-cuadrado para el nivel de significancia alpha
    chi2_inferior = stats.chi2.ppf(alpha/2, df)
    chi2_superior = stats.chi2.ppf(1 - alpha/2, df)
    
    # Calcular los límites de aceptación para la varianza
    limite_inferior = (df * varianza_teorica) / chi2_superior
    limite_superior = (df * varianza_teorica) / chi2_inferior
    
    # Estadístico de prueba
    estadistico = df * varianza_muestral / varianza_teorica
    
    print("\n=== PRUEBA DE VARIANZA ===")
    print("Hipótesis nula: La secuencia de números aleatorios tiene una varianza consistente con una distribución uniforme.")
    print("Hipótesis alternativa: La secuencia de números aleatorios no tiene una varianza consistente con una distribución uniforme.")
    print(f"Varianza muestral: {varianza_muestral}")
    print(f"Varianza teórica: {varianza_teorica}")
    print(f"Estadístico de prueba: {estadistico}")
    print(f"Grados de libertad: {df}")
    print(f"Valores críticos chi-cuadrado: [{chi2_inferior:.4f}, {chi2_superior:.4f}]")
    print(f"Límite inferior de varianza: {limite_inferior:.6f}")
    print(f"Límite superior de varianza: {limite_superior:.6f}")
    
    # Verificar si la varianza está dentro de los límites de aceptación
    if limite_inferior <= varianza_muestral <= limite_superior:
        print(f"\nCONCLUSIÓN PRUEBA DE VARIANZA: La secuencia pasa la prueba de varianza y puede considerarse aleatoria en términos de su dispersión (nivel de confianza {(1-alpha)*100}%).")
        print(f"Se acepta la hipótesis nula {varianza_teorica} ≈ {varianza_muestral}.")
        resultado = True
    else:
        print(f"\nCONCLUSIÓN PRUEBA DE VARIANZA: La secuencia no pasa la prueba de varianza. La dispersión no es consistente con una distribución uniforme. (nivel de confianza {(1-alpha)*100}%).")
        print(f"Se rechaza la hipótesis nula {varianza_teorica} ≠ {varianza_muestral}.")
        resultado = False
        
    # Verificación alternativa con p-valor
    print("\n=== VERIFICACIÓN CON P-VALOR ===")
    p_valor = 2 * min(stats.chi2.cdf(estadistico, df), 1 - stats.chi2.cdf(estadistico, df))
    print(f"P-valor de la prueba: {p_valor:.6f}")
    print(f"Interpretación p-valor: {f'Se acepta la hipótesis nula ({p_valor:.6f} > {alpha})' if p_valor > alpha else f'Se rechaza la hipótesis nula ({p_valor:.6f} <= {alpha})'}")
    print("=== FIN DE LA PRUEBA DE VARIANZA ===")
    return resultado

# Ejemplo de uso
if __name__ == "__main__":
    try:
        # Cargar los números aleatorios desde el archivo CSV
        with open('numeros_aleatorios_metodo_mixto.csv', 'r') as f:
            numeros_aleatorios = [float(line.strip()) for line in f]
        
        # Realizar la prueba de varianza
        resultado = prueba_de_varianza(numeros_aleatorios)
            
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'numeros_aleatorios_metodo_mixto.csv'.")
        print("Primero genera los números aleatorios con el script generador.")
    except Exception as e:
        print(f"Error al ejecutar la prueba: {str(e)}")