# # Prueba estadísitca para números aleatorios
# Descripción: Este script implementa la prueba estadística llamada "Prueba de Varianza" para determinar la validez de un conjunto de números aleatorios.

import numpy as np

def prueba_de_varianza(numeros_aleatorios, alpha=0.05):
    """
    Realiza la prueba de varianza para determinar si un conjunto de números aleatorios tiene una varianza diferente de 1/12.
    
    Parámetros:
    numeros_aleatorios (list): Lista de números aleatorios.
    alpha (float): Nivel de significancia. Por defecto es 0.05.
    
    Retorna:
    bool: True si se rechaza la hipótesis nula, False en caso contrario.
    """
    
    # Calcular la varianza
    varianza = np.var(numeros_aleatorios)
    
    # Calcular los valores de Chi cuadrado (tomados de la tabla)
    chi2_inferior = 91.0234 # v = 99 y alpha = 0,475
    chi2_superior = 118.1359 # v = 99 y alpha = 0,025

    # Calcular los limites de aceptacion
    limite_inferior = chi2_inferior / 12 * (len(numeros_aleatorios) - 1)
    limite_superior = chi2_superior / 12 + 12 * (len(numeros_aleatorios) - 1)
    
    print(f"Varianza: {varianza}")
    print(f"Limite inferior: {limite_inferior}")
    print(f"Limite superior: {limite_superior}")
    
    # Verificar si la varianza está dentro de los límites de aceptación
    if limite_inferior > varianza or varianza > limite_superior:
        print("No cumple la prueba de varianza.")
        return False
    else:
        print("Cumple la prueba de varianza.")
        return True

# Ejemplo de uso
if __name__ == "__main__":
    # Cargar los números aleatorios desde el archivo CSV
    with open('numeros_aleatorios_metodo_mixto.csv', 'r') as f:
        numeros_aleatorios = [float(line.strip()) for line in f]
    
    # Realizar la prueba de varianza
    resultado = prueba_de_varianza(numeros_aleatorios)
    
    if resultado:
        print("Los números aleatorios cumplen con la prueba de varianza.")
    else:
        print("Los números aleatorios no cumplen con la prueba de varianza.")