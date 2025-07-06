import numpy as np
import matplotlib.pyplot as plt
from simulador import genera_demanda_diaria
from produccion_demanda_máxima import simular_produccion_maxima

def ejecutar_analisis(resultados_netos):
    
    # Calcular intervalo de confianza simple
    minimo = min(resultados_netos)
    maximo = max(resultados_netos)
    media = np.mean(resultados_netos)
    
    # Generar gráfico
    plt.figure(figsize=(10, 6))
    
    # Grafico de línea con los valores
    plt.plot(resultados_netos, 'b-', alpha=0.7)
    plt.axhline(minimo, color='green', linestyle='--', label=f'Mínimo: {minimo:.2f}')
    plt.axhline(maximo, color='green', linestyle='--', label=f'Máximo: {maximo:.2f}')
    plt.axhline(media, color='red', linestyle='--', label=f'Media: {media:.2f}')
    
    plt.xlabel('Simulación')
    plt.ylabel('Resultado Neto')
    plt.title(f'Intervalo de Confianza - Resultado Neto ({num_corridas} simulaciones)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    print(f"\n=== Resultados ===")
    print(f"Mínimo: {minimo:.2f}")
    print(f"Máximo: {maximo:.2f}")
    print(f"Media: {media:.2f}")
    
    plt.savefig('IC_Demanda_Maxima.png', dpi=300, bbox_inches='tight')
    print("Gráfico guardado como 'intervalo_confianza.png'")
    plt.show()

if __name__ == "__main__":
    
    num_corridas = 100_000
    print(f"Ejecutando {num_corridas} simulaciones...")
    resultados_netos = []
    
    for i in range(num_corridas):
        dias_a_simular = 30
        cronograma = genera_demanda_diaria(dias_a_simular)
        resultado = simular_produccion_maxima(cronograma, N=3, produccion_inicial=60)
        resultados_netos.append(resultado['resultado_neto'])
        print(f"Simulación {i+1}/{num_corridas}: Resultado Neto = {resultado['resultado_neto']}")
        print("\n" + "*"*40)

    ejecutar_analisis(resultados_netos)