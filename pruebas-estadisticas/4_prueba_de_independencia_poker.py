# Prueba estadística para números aleatorios
# Descripción: Este script implementa la prueba de Poker para verificar la independencia
# de una secuencia de números aleatorios.

import numpy as np
from scipy import stats
import math
from collections import Counter

def obtener_patron_poker(grupo):
    """
    Determina el patrón de poker para un grupo de dígitos.
    
    Patrones:
    - TD (Todos Diferentes): Todos los dígitos son diferentes
    - 1P (Un Par): Exactamente un par de dígitos iguales
    - 2P (Dos Pares): Exactamente dos pares de dígitos iguales
    - T (Tercia): Exactamente tres dígitos iguales
    - TP (Tercia y Par/Full House): Una tercia y un par
    - P (Poker): Exactamente cuatro dígitos iguales
    - Q (Quintilla): Todos los dígitos son iguales
    
    Parámetros:
    grupo (str): Un grupo de dígitos (ej: '23452')
    
    Retorna:
    str: El patrón de poker identificado
    """
    # Contar ocurrencias de cada dígito
    conteo = Counter(grupo)
    valores = list(conteo.values())
    
    # Determinar el patrón según las frecuencias
    if len(valores) == 5:  # Todos diferentes
        return "TD"
    elif len(valores) == 4:  # Un par (1,1,1,2)
        return "1P"
    elif len(valores) == 3:
        if 3 in valores:  # Tercia (1,1,3)
            return "T"
        else:  # Dos pares (1,2,2)
            return "2P"
    elif len(valores) == 2:
        if 4 in valores:  # Poker (1,4)
            return "P"
        else:  # Full house / Tercia y par (2,3)
            return "TP"
    else:  # Todos iguales (5)
        return "Q"

def probabilidades_poker_teoricas(tamano_grupo=5):
    """
    Calcula las probabilidades teóricas para los patrones de poker.
    
    Parámetros:
    tamano_grupo (int): Tamaño del grupo de dígitos. Por defecto es 5.
    
    Retorna:
    dict: Diccionario con las probabilidades teóricas para cada patrón
    """
    if tamano_grupo == 5:
        # Probabilidades teóricas para grupos de 5 dígitos (base 10)
        return {
            "TD": 0.3024,  # Todos diferentes: 10*9*8*7*6 / 10^5
            "1P": 0.5040,  # Un par: 10C1 * 5C2 * 9^3 / 10^5
            "2P": 0.1080,  # Dos pares: 10C2 * (5C2 * 3C2) / (2! * 10^5)
            "T": 0.0720,   # Tercia: 10C1 * 5C3 * 9^2 / 10^5
            "TP": 0.0090,  # Full House: 10C1 * 5C3 * 9C1 * 3C2 / 10^5
            "P": 0.0045,   # Poker: 10C1 * 5C4 * 9 / 10^5
            "Q": 0.0001    # Quintilla: 10 * 1 / 10^5
        }
    else:
        # Para otros tamaños de grupo, sería necesario calcular las probabilidades
        raise ValueError(f"No hay probabilidades teóricas implementadas para grupos de tamaño {tamano_grupo}")

def prueba_poker(numeros_aleatorios, tamano_grupo=5, alpha=0.05):
    """
    Realiza la prueba de Poker para determinar la independencia de un conjunto de números aleatorios.
    
    Parámetros:
    numeros_aleatorios (list): Lista de números aleatorios entre 0 y 1.
    tamano_grupo (int): Tamaño del grupo de dígitos a analizar. Por defecto es 5.
    alpha (float): Nivel de significancia. Por defecto es 0.05.
    
    Retorna:
    bool: True si se acepta la hipótesis nula (independencia), False en caso contrario.
    """
    # Verificar que tenemos suficientes datos
    n = len(numeros_aleatorios)
    
    # Convertir números a cadenas con dígitos específicos
    # Necesitamos extraer los primeros 'tamano_grupo' dígitos de cada número
    grupos = []
    for num in numeros_aleatorios:
        # Convertir el número a string, quitar el '0.' y tomar los primeros dígitos
        digitos = str(num).replace("0.", "").ljust(tamano_grupo, '0')[:tamano_grupo]
        grupos.append(digitos)
    
    # Identificar el patrón de poker de cada grupo
    patrones = [obtener_patron_poker(grupo) for grupo in grupos]
    
    # Contar ocurrencias de cada patrón
    conteo_patrones = Counter(patrones)
    
    # Obtener probabilidades teóricas
    prob_teoricas = probabilidades_poker_teoricas(tamano_grupo)
    
    # Calcular frecuencias esperadas
    freq_esperadas = {patron: prob * n for patron, prob in prob_teoricas.items()}
    
    # Preparamos los datos para la prueba chi-cuadrado
    patrones_observados = []
    patrones_esperados = []
    nombres_patrones = []
    
    print("\n=== Prueba de Poker ===")
    print(f"Tamaño del grupo: {tamano_grupo} dígitos")
    print(f"Número de grupos analizados: {n}")
    print("\nTabla de frecuencias:")
    print(f"{'Patrón':<20} {'Descripción':<20} {'Frec. Observada':<20} {'Frec. Esperada':<20} {'Contribución a Chi²':<20}")
    
    descripciones = {
        "TD": "Todos Diferentes",
        "1P": "Un Par",
        "2P": "Dos Pares",
        "T": "Tercia",
        "TP": "Tercia y Par",
        "P": "Poker",
        "Q": "Quintilla"
    }
    
    # Calcular el estadístico chi-cuadrado
    chi_cuadrado = 0
    for patron, prob in prob_teoricas.items():
        observada = conteo_patrones.get(patron, 0)
        esperada = freq_esperadas[patron]
        
        # Solo incluimos categorías con frecuencia esperada >= 5
        if esperada >= 5:
            patrones_observados.append(observada)
            patrones_esperados.append(esperada)
            nombres_patrones.append(patron)
            
            # Contribución al estadístico chi-cuadrado
            contribucion = ((observada - esperada) ** 2) / esperada
            chi_cuadrado += contribucion
            
            print(f"{patron:<20} {descripciones.get(patron, ''):<20} {observada:<20} {esperada:.2f} {' '*10} {contribucion:.4f}")
        else:
            print(f"{patron:<20} {descripciones.get(patron, ''):<20} {observada:<20} {esperada:.2f} {' '*10} {'Agrupado* ':<20}")
    
    # Agrupar categorías con frecuencias esperadas pequeñas
    # En este ejemplo, agrupamos las categorías con esperados < 5
    total_agrupado_obs = sum(conteo_patrones.get(patron, 0) for patron, esp in freq_esperadas.items() if esp < 5)
    total_agrupado_esp = sum(esp for esp in freq_esperadas.values() if esp < 5)
    
    if total_agrupado_esp >= 5:
        print(f"{'Otros':<20} {'Categorías agrupadas':<20} {total_agrupado_obs:<20} {total_agrupado_esp:.2f} {' '*10} "
              f"{((total_agrupado_obs - total_agrupado_esp) ** 2) / total_agrupado_esp:.4f}")
        patrones_observados.append(total_agrupado_obs)
        patrones_esperados.append(total_agrupado_esp)
        nombres_patrones.append("Otros")
        chi_cuadrado += ((total_agrupado_obs - total_agrupado_esp) ** 2) / total_agrupado_esp
    
    print("> Nota: Las categorías con frecuencia esperada < 5 se han agrupado para la prueba Chi-Cuadrado.")

    # Grados de libertad (número de categorías - 1)
    df = len(patrones_observados) - 1
    
    # Valor crítico y p-valor
    chi_cuadrado_critico = stats.chi2.ppf(1 - alpha, df)
    p_valor = 1 - stats.chi2.cdf(chi_cuadrado, df)
    
    print(f"\nEstadístico Chi-Cuadrado: {chi_cuadrado:.4f}")
    print(f"Grados de libertad: {df}")
    print(f"Valor crítico (alpha={alpha}): {chi_cuadrado_critico:.4f}")
    print(f"P-valor: {p_valor:.6f}")
    
    # Verificar si la prueba pasa o no
    resultado = chi_cuadrado <= chi_cuadrado_critico
    
    if resultado:
        print(f"\nRESULTADO: Se acepta la hipótesis nula (p-valor = {p_valor:.6f} > {alpha}).")
        print("=== FIN DE LA PRUEBA DE POKER ===")
    else:
        print(f"\nRESULTADO: Se rechaza la hipótesis nula (p-valor = {p_valor:.6f} < {alpha}).")
        print("=== FIN DE LA PRUEBA DE POKER ===")
    
    return resultado

# Función auxiliar para mostrar ejemplos de patrones
def mostrar_ejemplos_patrones():
    """
    Muestra ejemplos de los diferentes patrones de poker para ayudar a entender la prueba.
    """
    ejemplos = {
        "TD": ["12345", "98765", "13579"],  # Todos Diferentes
        "1P": ["11234", "12234", "12334", "12344"],  # Un Par
        "2P": ["11224", "11233", "12233"],  # Dos Pares
        "T": ["11123", "12222", "33321"],  # Tercia
        "TP": ["11122", "22233", "33322"],  # Tercia y Par (Full House)
        "P": ["11112", "22221", "33334"],  # Poker
        "Q": ["11111", "22222", "33333"]   # Quintilla
    }
    
    print("\n=== Ejemplos de Patrones de Poker ===")
    for patron, ejemplos_lista in ejemplos.items():
        print(f"{patron} - {', '.join(ejemplos_lista)}")

# Ejemplo de uso
if __name__ == "__main__":
    try:
        # Cargar los números aleatorios desde el archivo CSV
        with open('numeros_aleatorios_metodo_mixto.csv', 'r') as f:
            numeros_aleatorios = [float(line.strip()) for line in f]
        
        # Mostrar ejemplos de patrones para mejor comprensión
        mostrar_ejemplos_patrones()
        
        # Realizar la prueba de Poker
        resultado = prueba_poker(numeros_aleatorios, tamano_grupo=5)

        if resultado:
            print("CONCLUSIÓN: La secuencia pasa la prueba de independencia de Poker, lo que sugiere que los números son aleatorios.")
        else:
            print("CONCLUSIÓN: La secuencia no pasa la prueba de independencia de Poker, lo que sugiere que los números no son aleatorios.")
        
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'numeros_aleatorios_metodo_mixto.csv'.")
        print("Primero genera los números aleatorios con el script generador.")
    except Exception as e:
        print(f"Error al ejecutar la prueba: {str(e)}")