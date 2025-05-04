# Generador de números aleatorios
# Descripción: Este script implementa un generador de números aleatorios utilizando el método congruencial mixto.

def generador_nros_aleatorios(seed, a, c, m, n):
    """
    Genera una lista de números aleatorios utilizando el método congruencial mixto.
    
    Parámetros:
    seed (int): Semilla inicial.
      - Rango: Cualquier entero entre 0 y m-1
      - Recomendación: Usar un valor que sea primo relativo con m (no tengan factores comunes)
    a (int): Multiplicador.
      - Rango: 0 < a < m
      - Condiciones óptimas:
        - a mod 4 = 1 si m es potencia de 2
        - a debe ser relativamente grande
    c (int): Incremento.
      - Rango: 0 ≤ c < m
      - Condiciones óptimas:
        - c debe ser primo relativo con m (no tienen factores comunes)
        - Si c = 0, es un generador multiplicativo puro (requiere otras condiciones)
        - Si c ≠ 0, es un generador mixto
    m (int): Módulo.
      - Rango: m > 0, preferiblemente grande
      - Recomendación: Usar una potencia de 2 (2³¹-1 o 2⁴⁸) o un número primo grande
      - El valor de m determina el período máximo posible
    n (int): Cantidad de números aleatorios a generar.
    
    Retorna:
    list: Lista de números aleatorios generados.
    """
    
    numeros_aleatorios = []
    x = seed
    
    for _ in range(n):
        x = (a * x + c) % m
        
        numeros_aleatorios.append(round(x / m, 4))
    
    return numeros_aleatorios

# Crear un archivo csv y almacenar los números aleatorios generados
def guardar_nros_aleatorios_en_csv(numeros_aleatorios, nombre_archivo):
    """
    Guarda una lista de números aleatorios en un archivo CSV.
    
    Parámetros:
    numeros_aleatorios (list): Lista de números aleatorios.
    nombre_archivo (str): Nombre del archivo CSV donde se guardarán los números.
    """
    
    with open(nombre_archivo, 'w') as f:
        for numero in numeros_aleatorios:
            f.write(f"{numero}\n")

# Ejemplo de uso
if __name__ == "__main__":
    # Parámetros del generador
    seed = 12345
    a = 16807
    c = 0
    m = 2**31 - 1
    n = 100
    
    # Generar números aleatorios
    numeros_aleatorios = generador_nros_aleatorios(seed, a, c, m, n)
    
    # Guardar los números aleatorios en un archivo CSV
    guardar_nros_aleatorios_en_csv(numeros_aleatorios, 'numeros_aleatorios_metodo_mixto.csv')
    
    print("Números aleatorios generados y guardados en 'numeros_aleatorios_metodo_mixto.csv'")
