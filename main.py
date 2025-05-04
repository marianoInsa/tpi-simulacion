"""
Pruebas Estadísticas de Números Pseudoaleatorios
=======================================================================

Este script ejecuta un conjunto de pruebas estadísticas para verificar la calidad
de un conjunto de números pseudoaleatorios almacenados en un archivo .csv.

Pruebas implementadas:
1. Prueba de Medias - Verifica que la media sea aproximadamente 0.5
2. Prueba de Varianza - Verifica que la varianza sea aproximadamente 1/12
3. Prueba de Uniformidad (Chi-Cuadrada) - Verifica distribución uniforme
4. Prueba de Independencia (Poker) - Verifica independencia entre dígitos
"""

import sys
import numpy as np
from datetime import datetime

# Importar las pruebas
try:
    from pruebas_estadisticas.prueba_de_medias import prueba_de_medias
    from pruebas_estadisticas.prueba_de_varianza import prueba_de_varianza
    from pruebas_estadisticas.prueba_de_uniformidad_chi_cuadrada import prueba_chi_cuadrada
    from pruebas_estadisticas.prueba_de_independencia_poker import prueba_poker
except ImportError:
    print("\nError al importar los módulos de pruebas estadísticas.")
    print("Verificando estructura de directorios y archivos...")
    print("Asegúrese de que la carpeta existe y contiene los archivos de pruebas.")

def cargar_numeros_aleatorios(archivo):
    """
    Carga los números aleatorios desde un archivo CSV.
    
    Parámetros:
    archivo (str): Ruta al archivo CSV con los números aleatorios.
    
    Retorna:
    list: Lista de números aleatorios.
    """
    try:
        with open(archivo, 'r') as f:
            numeros = [float(line.strip()) for line in f if line.strip()]
        return numeros
    except Exception as e:
        print(f"Error al cargar el archivo: {str(e)}")
        sys.exit(1)

def mostrar_encabezado():
    """Muestra un encabezado estilizado para el informe de pruebas."""
    print("\n" + "="*80)
    print(" "*25 + "ANÁLISIS DE NÚMEROS PSEUDOALEATORIOS")
    print("="*80)
    print(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("-"*80)

def mostrar_estadisticas_basicas(numeros):
    """
    Muestra estadísticas básicas de los números cargados.
    
    Parámetros:
    numeros (list): Lista de números aleatorios.
    """
    n = len(numeros)
    if n == 0:
        print("No se encontraron números en el archivo.")
        return

    print(f"\n{'ESTADÍSTICAS BÁSICAS':-^80}")
    print(f"Cantidad de números analizados: {n}")
    print(f"Rango de valores: [{min(numeros):.6f}, {max(numeros):.6f}]")
    print(f"Media: {np.mean(numeros):.6f}")
    print(f"Desviación estándar: {np.std(numeros):.6f}")
    print(f"Varianza: {np.var(numeros):.6f}")
    
    # Verificar si hay valores fuera del rango [0,1]
    valores_invalidos = [x for x in numeros if x < 0 or x > 1]
    if valores_invalidos:
        print(f"\n¡ADVERTENCIA! Se encontraron los siguientes {len(valores_invalidos)} valores fuera del rango [0,1].")
        print(valores_invalidos[:5])

def ejecutar_pruebas(numeros, alpha=0.05):
    """
    Ejecuta todas las pruebas estadísticas y recopila resultados.
    
    Parámetros:
    numeros (list): Lista de números aleatorios.
    alpha (float): Nivel de significancia para las pruebas.
    
    Retorna:
    dict: Diccionario con los resultados de cada prueba.
    """
    resultados = {}
    
    print(f"\n{'EJECUCIÓN DE PRUEBAS ESTADÍSTICAS':-^80}")
    
    # 1. Prueba de Medias
    print("\n[1/4] Ejecutando Prueba de Medias...")
    try:
        resultado_medias = prueba_de_medias(numeros, alpha)
        resultados["medias"] = resultado_medias
    except Exception as e:
        print(f"Error al ejecutar la prueba de medias: {str(e)}")
        resultados["medias"] = None
    
    # 2. Prueba de Varianza
    print("\n[2/4] Ejecutando Prueba de Varianza...")
    try:
        resultado_varianza = prueba_de_varianza(numeros, alpha)
        resultados["varianza"] = resultado_varianza
    except Exception as e:
        print(f"Error al ejecutar la prueba de varianza: {str(e)}")
        resultados["varianza"] = None
    
    # 3. Prueba de Uniformidad (Chi-Cuadrada)
    print("\n[3/4] Ejecutando Prueba de Uniformidad (Chi-Cuadrada)...")
    try:
        resultado_uniformidad = prueba_chi_cuadrada(numeros, 10, alpha)
        resultados["uniformidad"] = resultado_uniformidad
    except Exception as e:
        print(f"Error al ejecutar la prueba de uniformidad: {str(e)}")
        resultados["uniformidad"] = None
    
    # 4. Prueba de Independencia (Poker)
    print("\n[4/4] Ejecutando Prueba de Independencia (Poker)...")
    try:
        resultado_poker = prueba_poker(numeros, 5, alpha)
        resultados["independencia"] = resultado_poker
    except Exception as e:
        print(f"Error al ejecutar la prueba de independencia: {str(e)}")
        resultados["independencia"] = None
    
    return resultados

def mostrar_conclusiones(resultados):
    """
    Muestra conclusiones generales basadas en los resultados de las pruebas.
    
    Parámetros:
    resultados (dict): Diccionario con los resultados de cada prueba.
    """
    print(f"\n{'CONCLUSIONES FINALES':-^80}")
    
    pruebas_exitosas = sum(1 for resultado in resultados.values() if resultado)
    pruebas_fallidas = sum(1 for resultado in resultados.values() if not resultado)
    pruebas_error = sum(1 for resultado in resultados.values() if resultado is None)
    
    print(f"\nResultados:")
    print(f"  - Pruebas aprobadas: {pruebas_exitosas}")
    print(f"  - Pruebas fallidas: {pruebas_fallidas}")
    if pruebas_error > 0:
        print(f"  - Pruebas con errores: {pruebas_error}")
    
    # Tabla de resultados
    print("\nResultados:")
    print(f"{'Prueba':<20} {'Resultado':<15}")
    print("-" * 35)
    
    nombres = {
        "medias": "Prueba de Medias",
        "varianza": "Prueba de Varianza",
        "uniformidad": "Prueba Chi-Cuadrada",
        "independencia": "Prueba de Poker"
    }
    
    for prueba, resultado in resultados.items():
        if resultado:
            status = "✓ APROBADA"
        elif not resultado:
            status = "✗ RECHAZADA"
        else:
            status = "! ERROR"
        print(f"{nombres.get(prueba, prueba):<20} {status:<15}")
    
    # Conclusión general
    print("\n")
    if pruebas_fallidas == 0 and pruebas_error == 0:
        print("  ✓ EXCELENTE - La secuencia de números pasa todas las pruebas estadísticas.")
        print("    Los números pseudoaleatorios pueden considerarse de buena calidad.")
    elif pruebas_fallidas <= 1 and pruebas_error == 0:
        print("  ⚠ ACEPTABLE - La secuencia pasa la mayoría de las pruebas estadísticas.")
        print("    Los números son aceptables para muchas aplicaciones, pero pueden tener algunas limitaciones.")
    else:
        print("  ✗ NO SATISFACTORIO - La secuencia no pasa múltiples pruebas estadísticas.")
        print("    Se recomienda revisar y ajustar los parámetros del generador.")

def main():
    """Función principal del script."""
    # Definir archivo de entrada
    archivo_entrada = "numeros_aleatorios_metodo_mixto.csv"
    
    # Mostrar encabezado
    mostrar_encabezado()
    
    # Cargar números aleatorios
    print(f"Cargando números aleatorios desde '{archivo_entrada}'...")
    numeros = cargar_numeros_aleatorios(archivo_entrada)
    
    # Mostrar estadísticas básicas
    mostrar_estadisticas_basicas(numeros)
    
    # Ejecutar pruebas estadísticas
    nivel_significancia = 0.05
    print(f"\nIniciando pruebas estadísticas con nivel de significancia α = {nivel_significancia}...")
    resultados = ejecutar_pruebas(numeros, alpha=nivel_significancia)
    
    # Mostrar conclusiones
    mostrar_conclusiones(resultados)
    
    print("\n" + "="*80)
    print(" "*15 + "FIN DEL ANÁLISIS DE NÚMEROS PSEUDOALEATORIOS")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        sys.exit(1)