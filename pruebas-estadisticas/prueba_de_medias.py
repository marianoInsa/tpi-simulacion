# Prueba estadísitca para números aleatorios
# Descripción: Este script implementa la prueba estadística llamada "Prueba de Medias" para determinar la validez de un conjunto de números aleatorios.

import numpy as np

def prueba_de_medias(numeros_aleatorios, alpha=0.05):
    """
    Realiza la prueba de medias para determinar si un conjunto de números aleatorios tiene una media diferente de cero.
    
    Parámetros:
    numeros_aleatorios (list): Lista de números aleatorios.
    alpha (float): Nivel de significancia. Por defecto es 0.05.
    
    Retorna:
    bool: True si se rechaza la hipótesis nula, False en caso contrario.
    """
    
    # Calcular la media
    media = np.mean(numeros_aleatorios)
    
    # Calcular los limites de aceptacion
    limite_inferior = 0.5 - (1.96) * 1 / 12 * np.sqrt(len(numeros_aleatorios))
    limite_superior = 0.5 + (1.96) * 1 / 12 * np.sqrt(len(numeros_aleatorios))
    print(f"Media: {media}")
    print(f"Limite inferior: {limite_inferior}")
    print(f"Limite superior: {limite_superior}")
    # Verificar si la media está dentro de los límites de aceptación
    if limite_inferior > media or media > limite_superior:
        print("No cumple la prueba de medias.")
        return False
    else:
        print("Cumple la prueba de medias.")
        return True

# Ejemplo de uso
if __name__ == "__main__":
    # Cargar los números aleatorios desde el archivo CSV
    with open('numeros_aleatorios_metodo_mixto.csv', 'r') as f:
        numeros_aleatorios = [float(line.strip()) for line in f]
    
    # Realizar la prueba de medias
    resultado = prueba_de_medias(numeros_aleatorios)
    
    if resultado:
        print("Los números aleatorios cumplen con la prueba de medias.")
    else:
        print("Los números aleatorios no cumplen con la prueba de medias.")