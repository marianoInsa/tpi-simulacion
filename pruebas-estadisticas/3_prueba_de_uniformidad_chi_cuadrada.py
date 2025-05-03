# Prueba estadística para números aleatorios
# Descripción: Este script implementa la prueba estadística "Chi-Cuadrada" para verificar 
# la uniformidad de un conjunto de números aleatorios.

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def prueba_chi_cuadrada(numeros_aleatorios, num_intervalos=10, alpha=0.05, mostrar_grafico=True):
    """
    Realiza la prueba Chi-Cuadrada para determinar si un conjunto de números aleatorios
    sigue una distribución uniforme.
    
    Parámetros:
    numeros_aleatorios (list): Lista de números aleatorios entre 0 y 1.
    num_intervalos (int): Número de intervalos (clases) para la prueba. Por defecto es 10.
    alpha (float): Nivel de significancia. Por defecto es 0.05.
    mostrar_grafico (bool): Si es True, muestra un histograma de la distribución. Por defecto es True.
    
    Retorna:
    bool: True si se acepta la hipótesis nula (distribución uniforme), False en caso contrario.
    """
    # Número total de observaciones
    n = len(numeros_aleatorios)
    
    # Verificar que tenemos suficientes datos para el número de intervalos
    if n < 5 * num_intervalos:
        print(f"ADVERTENCIA: Se recomienda tener al menos {5 * num_intervalos} observaciones para {num_intervalos} intervalos.")
        if n < num_intervalos:
            print("ERROR: Número insuficiente de datos para realizar la prueba.")
            return False
    
    # Frecuencia esperada en cada intervalo (distribución uniforme)
    frecuencia_esperada = n / num_intervalos
    
    # Crear histograma para contar frecuencias observadas
    frecuencias_observadas, bordes = np.histogram(numeros_aleatorios, bins=num_intervalos, range=(0, 1))
    
    # Calcular el estadístico Chi-Cuadrado
    chi_cuadrado = np.sum((frecuencias_observadas - frecuencia_esperada) ** 2 / frecuencia_esperada)
    
    # Grados de libertad (k-1-m, donde k es el número de intervalos y m es el número de parámetros estimados)
    # Para una distribución uniforme sin parámetros estimados, los grados de libertad son num_intervalos - 1
    df = num_intervalos - 1
    
    # Valor crítico de chi-cuadrado
    chi_cuadrado_critico = stats.chi2.ppf(1 - alpha, df)
    
    # Calcular p-valor
    p_valor = 1 - stats.chi2.cdf(chi_cuadrado, df)
    
    # Mostrar resultados
    print(f"\n=== Prueba Chi-Cuadrada de Uniformidad ===")
    print(f"Número de datos: {n}")
    print(f"Número de intervalos: {num_intervalos}")
    print(f"Frecuencia esperada por intervalo: {frecuencia_esperada:.2f}")
    print(f"Estadístico Chi-Cuadrado: {chi_cuadrado:.4f}")
    print(f"Grados de libertad: {df}")
    print(f"Valor crítico (alpha={alpha}): {chi_cuadrado_critico:.4f}")
    print(f"P-valor: {p_valor:.6f}")
    
    # Mostrar tabla de frecuencias
    print("=== Tabla de frecuencias ===")
    print(f"{'Intervalo':<15} {'Frec. Observada':<20} {'Frec. Esperada':<20} {'Diferencia':<15} {'Contribución a Chi²':<20}")
    for i in range(num_intervalos):
        intervalo = f"[{bordes[i]:.2f}, {bordes[i+1]:.2f})"
        contribucion = ((frecuencias_observadas[i] - frecuencia_esperada) ** 2) / frecuencia_esperada
        print(f"{intervalo:<15} {frecuencias_observadas[i]:<20} {frecuencia_esperada:.2f} {' '*10} "
              f"{frecuencias_observadas[i] - frecuencia_esperada:+.2f} {' '*10} {contribucion:.4f}")
    print("="*80)
    # Verificar si la prueba pasa o no
    resultado = chi_cuadrado <= chi_cuadrado_critico
    
    if resultado:
        print(f"\nRESULTADO: Se acepta la hipótesis nula (p-valor = {p_valor:.6f} > {alpha}).")
        print("=== FIN DE LA PRUEBA DE UNIFORMIDAD ===")

    else:
        print(f"\nRESULTADO: Se rechaza la hipótesis nula (p-valor = {p_valor:.6f} < {alpha}).")
        print("=== FIN DE LA PRUEBA DE UNIFORMIDAD ===")
    
    # Crear un gráfico para visualizar la distribución
    if mostrar_grafico:
        plt.figure(figsize=(10, 6))
        
        # Histograma de frecuencias observadas
        plt.hist(numeros_aleatorios, bins=num_intervalos, range=(0, 1), alpha=0.7, color='blue', edgecolor='black')
        
        # Línea horizontal para la frecuencia esperada
        plt.axhline(y=frecuencia_esperada, color='r', linestyle='-', label=f'Frecuencia esperada: {frecuencia_esperada:.2f}')
        
        plt.title('Distribución de números aleatorios')
        plt.xlabel('Valor')
        plt.ylabel('Frecuencia')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Añadir texto con resultados de la prueba
        texto_resultado = f"Chi² = {chi_cuadrado:.4f}\nValor crítico = {chi_cuadrado_critico:.4f}\np-valor = {p_valor:.6f}"
        plt.annotate(texto_resultado, xy=(0.70, 0.85), xycoords='axes fraction', 
                     bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.5))
        
        plt.tight_layout()
        plt.savefig('prueba_chi_cuadrada_resultado.png')
        print("> Nota: Se ha guardado un gráfico de la distribución como 'prueba_chi_cuadrada_resultado.png'")
        plt.close()
    
    return resultado

# Ejemplo de uso
if __name__ == "__main__":
    try:
        # Cargar los números aleatorios desde el archivo CSV
        with open('numeros_aleatorios_metodo_mixto.csv', 'r') as f:
            numeros_aleatorios = [float(line.strip()) for line in f]
        
        # Realizar la prueba Chi-Cuadrada de uniformidad
        # Se puede ajustar el número de intervalos (10 por defecto)
        resultado = prueba_chi_cuadrada(numeros_aleatorios, num_intervalos=10)

        if resultado:
            print("CONCLUSIÓN: La secuencia pasa la prueba Chi-Cuadrada de uniformidad, siguiendo una distribución uniforme.")
        else:
            print("CONCLUSIÓN: La secuencia NO pasa la prueba Chi-Cuadrada de uniformidad, y no sigue una distribución uniforme.")
        
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'numeros_aleatorios_metodo_mixto.csv'.")
        print("Primero genera los números aleatorios con el script generador.")
    except Exception as e:
        print(f"Error al ejecutar la prueba: {str(e)}")