# Archivo: simulador.py

import time
import numpy as np
import math
from datetime import datetime, date, timedelta
import random
# --- 0. DEFINICION DE CONSTANTES ---
#venta perdida
COSTO_VP = 10
#sobrante
COSTO_SB = 7
BENEFICIO = 10



# --- 1. IMPORTAR TUS MÓDULOS (Sin cambios) ---
from nros_aleatorios.generador_congruencial_mixto import generador_nros_aleatorios
from pruebas_estadisticas.prueba_de_medias import prueba_de_medias
from pruebas_estadisticas.prueba_de_varianza import prueba_de_varianza
from pruebas_estadisticas.prueba_de_uniformidad_chi_cuadrada import prueba_chi_cuadrada
from pruebas_estadisticas.prueba_de_independencia_poker import prueba_poker

# --- 2. FUNCIÓN DE PRUEBAS COMPLETAS  ---
def ejecutar_pruebas_completas(numeros, alpha=0.05):
    pasa_medias = prueba_de_medias(numeros, alpha, verbose=False)
    pasa_varianza = prueba_de_varianza(numeros, alpha, verbose=False)
    pasa_uniformidad = prueba_chi_cuadrada(numeros, num_intervalos=10, alpha=alpha, verbose=False)
    pasa_independencia = prueba_poker(numeros, tamano_grupo=5, alpha=alpha, verbose=False)
    return pasa_medias and pasa_varianza and pasa_uniformidad and pasa_independencia

# --- 3. GENERADOR MAESTRO AUTOMATIZADO  ---
def generar_numeros_aprobados(cantidad, alpha=0.05,verbose=False):
    #intentos = 0
    while True:
        #intentos += 1
        #if verbose:
            #print(f"\rIntento #{intentos}: Generando y probando un nuevo conjunto de {cantidad} números...", end="")
        semilla_dinamica = random.randint(10000, 99999)
        a, c, m = 16807, 0, 2**31 - 1
        numeros_candidatos = generador_nros_aleatorios(semilla_dinamica, a, c, m, cantidad)
        if ejecutar_pruebas_completas(numeros_candidatos, alpha):
            #if verbose:
                #print(f"\n¡Éxito! Se encontró un conjunto aprobado en el intento #{intentos}.")
            return numeros_candidatos

# --- 4. NUEVAS FUNCIONES DE GENERACIÓN DE DEMANDA ---

def generar_demanda_entresemana(random_num):
    """
    Genera la demanda para un día de semana (Lunes a Jueves).
    """
    demanda = math.floor(random_num*77)+4
    return demanda

def generar_demanda_fin_de_semana(random_num):
    """
    Genera la demanda para un día de fin de semana (Viernes a Domingo).
    """
    demanda = math.floor(random_num*90)+18
    return demanda

# --- 5. NUEVA FUNCIÓN 'gen_var_value' ---
def gen_var_value(num_aleatorio, fecha_actual):
    """
    Recibe un número aleatorio y la fecha, y decide qué función de demanda usar.
    
    Args:
        num_aleatorio (float): El número aleatorio validado entre 0 y 1.
        fecha_actual (date): El objeto de fecha para el día de la simulación.
        
    Returns:
        int: El valor de la demanda generada.
    """
    # weekday() devuelve: Lunes=0, Martes=1, ..., Viernes=4, Sábado=5, Domingo=6
    dia_semana = fecha_actual.weekday()
    
    # Consideramos fin de semana a Viernes, Sábado y Domingo
    if dia_semana in [4, 5, 6]: # Viernes, Sábado o Domingo
        tipo_dia = "Fin de Semana"
        demanda = generar_demanda_fin_de_semana(num_aleatorio)
    else: # Lunes, Martes, Miércoles o Jueves
        tipo_dia = "Entre Semana"
        demanda = generar_demanda_entresemana(num_aleatorio)
        
    return demanda, tipo_dia


# --- 6. FUNCIÓN PRINCIPAL DE LA SIMULACIÓN (ACTUALIZADA) ---
def genera_demanda_diaria(dias_a_simular):
    """
    Punto de entrada principal. Pide fechas, calcula duración, genera números
    y ejecuta la simulación día por día.
    """

    # --- OBTENER FECHAS Y CALCULAR DURACIÓN ---
    fecha_inicio = date.today()
    # --- OBTENER NÚMEROS ALEATORIOS VALIDADOS ---
    nivel_confianza = 0.95
    alpha = 1 - nivel_confianza
    numeros_aleatorios_validados = generar_numeros_aprobados(cantidad=dias_a_simular, alpha=alpha)
    
    if not numeros_aleatorios_validados:
        print("No se pudo generar un conjunto de números aleatorios válidos. Abortando simulación.")
        return

    resultados_simulacion = []
    
    for i in range(dias_a_simular):
        # Obtenemos la fecha y el número aleatorio para esta iteración
        fecha_actual = fecha_inicio + timedelta(days=i)
        num_aleatorio_del_dia = numeros_aleatorios_validados[i]
        
        # Usamos tu función para obtener la demanda
        demanda_generada, tipo_dia = gen_var_value(num_aleatorio_del_dia, fecha_actual)
        
        # Guardamos y mostramos los resultados del día
        dia_info = {
            "dia": i + 1,
            "fecha": fecha_actual.strftime('%d/%m/%Y'),
            "dia_semana": fecha_actual.strftime('%A'),
            "tipo_dia": tipo_dia,
            "r(i)": round(num_aleatorio_del_dia, 4),
            "demanda": demanda_generada
        }
        resultados_simulacion.append(dia_info)
    # Opcional: Mostrar un resumen final si lo deseas
    # print("\nResumen de resultados:")
    # for res in resultados_simulacion:
    #     print(res)
    return resultados_simulacion

if __name__ == "__main__":
    genera_demanda_diaria(50)
