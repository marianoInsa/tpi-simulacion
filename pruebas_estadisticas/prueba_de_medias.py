# Prueba estadística para números aleatorios
# Descripción: Este script implementa la primera prueba estadística, "Prueba de Medias", para determinar la validez de un conjunto de números aleatorios.

import numpy as np
from scipy import stats

def prueba_de_medias(numeros_aleatorios, alpha=0.05, verbose=True):
    """
    Realiza la prueba de medias para determinar si un conjunto de números aleatorios
    sigue una distribución uniforme entre 0 y 1.
    
    Parámetros:
    numeros_aleatorios (list): Lista de números aleatorios entre 0 y 1.
    alpha (float): Nivel de significancia. Por defecto es 0.05.
    
    Retorna:
    bool: True si se acepta la hipótesis nula (los números son aleatorios), False en caso contrario.
    """
    
    # Calcular la media
    media = np.mean(numeros_aleatorios)
    
    # Valor esperado para una distribución uniforme entre 0 y 1
    media_esperada = 0.5
    
    # Desviación estándar teórica para una distribución uniforme entre 0 y 1
    desviacion_estandar = 1/np.sqrt(12)
    
    # Error estándar de la media
    error_estandar = desviacion_estandar / np.sqrt(len(numeros_aleatorios))
    
    # Valor crítico para el nivel de significancia alpha
    z_critico = stats.norm.ppf(1 - alpha/2)  # Para una prueba de dos colas
    
    # Calcular los límites de aceptación
    limite_inferior = media_esperada - z_critico * error_estandar
    limite_superior = media_esperada + z_critico * error_estandar
    if verbose:
        print("\n=== PRUEBA DE MEDIAS ===")
        print("Hipótesis nula: La secuencia de números aleatorios tiene una media igual a 0.5.")
        print("Hipótesis alternativa: La secuencia de números aleatorios no tiene una media igual a 0.5.")
        print(f"Media calculada: {media}")
        print(f"Media esperada: {media_esperada}")
        print(f"Límite inferior: {limite_inferior}")
        print(f"Límite superior: {limite_superior}")
    
    # Verificar si la media está dentro de los límites de aceptación
    if limite_inferior <= media <= limite_superior:
        if verbose:
            print(f"CONCLUSIÓN PRUEBA DE MEDIAS: La secuencia pasa la prueba de medias y puede considerarse aleatoria en términos de su media (nivel de confianza {(1-alpha)*100}%).")
            print(f"Se acepta la hipótesis nula {media_esperada} ≈ {media}.")
            print("=== FIN DE LA PRUEBA DE MEDIAS ===")
        return True
    else:
        if verbose:
            print(f"\nCONCLUSIÓN PRUEBA DE MEDIAS: La secuencia no pasa la prueba de medias. La distribución no es uniforme en términos de su media. (nivel de confianza {(1-alpha)*100}%).")
            print(f"Se rechaza la hipótesis nula {media_esperada} ≠ {media}.")
            print("=== FIN DE LA PRUEBA DE MEDIAS ===")
        return False

# Ejemplo de uso
if __name__ == "__main__":
    try:
        # Cargar los números aleatorios desde el archivo CSV
        with open('numeros_aleatorios_metodo_mixto.csv', 'r') as f:
            numeros_aleatorios = [float(line.strip()) for line in f]
        
        # Realizar la prueba de medias
        resultado = prueba_de_medias(numeros_aleatorios)
            
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'numeros_aleatorios_metodo_mixto.csv'.")
        print("Primero genera los números aleatorios con el script generador.")
    except Exception as e:
        print(f"Error al ejecutar la prueba: {str(e)}")