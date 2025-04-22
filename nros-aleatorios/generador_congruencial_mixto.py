# Generador de números aleatorios
# Descripción: Este script implementa un generador de números aleatorios utilizando el método congruencial mixto.

def generador_nros_aleatorios(seed, a, c, m, n):
    """
    Genera una lista de números aleatorios utilizando el método congruencial mixto.
    
    Parámetros:
    seed (int): Semilla inicial.
    a (int): Multiplicador.
    c (int): Incremento.
    m (int): Módulo.
    n (int): Cantidad de números aleatorios a generar.
    
    Retorna:
    list: Lista de números aleatorios generados.
    """
    
    numeros_aleatorios = []
    x = seed
    
    for _ in range(n):
        x = (a * x + c) % m
        x = x / m  # Normalizar el número aleatorio
        x = round(x, 4)
        numeros_aleatorios.append(x)
    
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
    seed = 68754
    a = 9745
    c = 7
    m = 100
    n = 100
    
    # Generar números aleatorios
    numeros_aleatorios = generador_nros_aleatorios(seed, a, c, m, n)
    
    # Guardar los números aleatorios en un archivo CSV
    guardar_nros_aleatorios_en_csv(numeros_aleatorios, 'numeros_aleatorios_metodo_mixto.csv')
    
    print("Números aleatorios generados y guardados en 'numeros_aleatorios_metodo_mixto.csv'")
