# VERSIÓN CON PRODUCCIÓN DIFERENCIADA
# Asumiendo que las constantes están en un archivo config.py o en simulador.py
from simulador import genera_demanda_diaria, COSTO_VP, COSTO_SB, BENEFICIO
import itertools
from scipy.stats import t 
import math
def simular_politica_produccion(
    produccion_semana: int, 
    produccion_finde: int, 
    cronograma_demanda: list[dict]
) -> dict:
    """
    Simula una política de producción diferenciada para días de semana y fines de semana,
    con una vida útil de producto de 2 días.
    Criterio: Se produce todos los dias las cantidades recibidas en los argumentos produccion_semana
    y produccion_finde para cada caso. LOS SOBRANTES DE AYER NO AFECTAN A LA PRODUCCION DE HOY, es indistinto!

    Args:
        produccion_semana (int): La cantidad producida en un día de semana (L-J).
        produccion_finde (int): La cantidad producida en un día de fin de semana (V-S-D).
        cronograma_demanda (list[dict]): La lista de diccionarios generada por el simulador,
                                         que contiene la demanda y los detalles de cada día.

    Returns:
        dict: Un diccionario con los resultados finales de la simulación.
    """
    # Acumuladores finales
    ganancias_totales = 0
    costo_total_desperdicio = 0
    costo_total_faltantes = 0
    
    # Variable de estado: representa los sobrantes de ayer
    sobrantes_de_ayer = 0

    #print("\n" + "="*60)
    #print("INICIANDO SIMULACIÓN CON POLÍTICA DE PRODUCCIÓN DIFERENCIADA")
    #print(f"Producción L-J: {produccion_semana} | Producción V-S-D: {produccion_finde}")
    #print("="*60)

    # El bucle itera sobre la lista de diccionarios que tiene los datos de la demanda diaria y el dia de la semana.
    for dia_simulado in cronograma_demanda:
        
        demanda_hoy = dia_simulado["demanda"]
        tipo_dia_hoy = dia_simulado["tipo_dia"] # "Entre Semana" o "Fin de Semana"

        # --- Seleccionar la producción del día de acuerdo al tipo de dia ---
        produccion_de_hoy = 0
        if tipo_dia_hoy == "Fin de Semana":
            produccion_de_hoy = produccion_finde
        else: # "Entre Semana"
            produccion_de_hoy = produccion_semana
        

        unidades_vendidas_hoy = 0
        demanda_restante = demanda_hoy

        # 1. GESTIONAR SOBRANTES DEL DÍA ANTERIOR
        if sobrantes_de_ayer > 0:
            if demanda_restante >= sobrantes_de_ayer:
                unidades_vendidas_hoy += sobrantes_de_ayer
                demanda_restante -= sobrantes_de_ayer
            else: 
                unidades_vendidas_hoy += demanda_restante
                unidades_desperdiciadas = sobrantes_de_ayer - demanda_restante
                costo_total_desperdicio += unidades_desperdiciadas * COSTO_SB
                demanda_restante = 0

        # 2. GESTIONAR PRODUCCIÓN DEL DÍA
        sobrantes_para_manana = 0
        if demanda_restante > 0:
            if demanda_restante >= produccion_de_hoy:
                unidades_vendidas_hoy += produccion_de_hoy
                unidades_perdidas = demanda_restante - produccion_de_hoy
                costo_total_faltantes += unidades_perdidas * COSTO_VP
                sobrantes_para_manana = 0
            else:
                unidades_vendidas_hoy += demanda_restante
                sobrantes_para_manana = produccion_de_hoy - demanda_restante
        else:
            sobrantes_para_manana = produccion_de_hoy

        # 3. ACTUALIZAR TOTALES Y ESTADO
        ganancias_totales += unidades_vendidas_hoy * BENEFICIO
        sobrantes_de_ayer = sobrantes_para_manana

    # --- Resultados Finales ---
    costo_total = costo_total_faltantes + costo_total_desperdicio
    resultado_neto = ganancias_totales - costo_total
    
    return {
        "ganancia_total": ganancias_totales,
        "costo_desperdicio": costo_total_desperdicio,
        "costo_faltantes": costo_total_faltantes,
        "costo_total": costo_total,
        "resultado_neto": resultado_neto
    }

def generar_replicas(cant_replicas,cant_dias):
    produccion = list(itertools.product([x*6 for x in range(1,20)], repeat=2))
    acum_benef = {combi: [] for combi in produccion}
        
    for _ in range(cant_replicas):
        demanda_diaria = genera_demanda_diaria(cant_dias)
        for combi in produccion:
            resultado = simular_politica_produccion(combi[0],combi[1],demanda_diaria)
            acum_benef[combi].append(resultado["resultado_neto"])
    return acum_benef

def generar_intervalos(cant_replicas,acum_benef,alpha = 0.05):
    produccion = list(itertools.product([x*6 for x in range(1, 20)], repeat=2))
    result = {
    combi: {
        'beneficio_prom': 0,
        'stddev': 0,
        'delta': 0,
        'lower': 0,
        'upper': 0
    } for combi in produccion}
    
    for combi in acum_benef:
        result[combi]['beneficio_prom'] = sum(acum_benef[combi]) / cant_replicas
        result[combi]['stddev'] = math.sqrt(sum((x - result[combi]['beneficio_prom']) ** 2 for x in acum_benef[combi]) / (cant_replicas - 1))
        t_critical = t.ppf(1 - alpha / 2, df=cant_replicas - 1)
        result[combi]['delta'] = t_critical * (result[combi]['stddev'] / math.sqrt(cant_replicas))
        result[combi]['lower'] = result[combi]['beneficio_prom'] - result[combi]['delta']
        result[combi]['upper'] = result[combi]['beneficio_prom'] + result[combi]['delta']
        
    return result

def mostrar_resultados(resultados_intervalos):
    lista_ordenada = []
    for key in resultados_intervalos:
        dic_aux = {
            'produccion':f'semama {key[0]}, finde {key[1]}',
            'beneficio_prom':resultados_intervalos[key]['beneficio_prom'] ,
            'stddev': resultados_intervalos[key]['stddev'],
            'delta': resultados_intervalos[key]['delta'],
            'lower': resultados_intervalos[key]['lower'],
            'upper': resultados_intervalos[key]['upper']
        }
        lista_ordenada.append(dic_aux)
    lista_ordenada.sort(key=lambda x: -x['beneficio_prom'])
    print("\n--- Top 5 mejores valores de 'p' (combinando Weekday y Weekend) ---\n")
    for i, lista in enumerate(lista_ordenada[:5], start=1):
        intervalo_longitud = lista['upper'] - lista['lower']
        print(f"{i}.  p = {lista['produccion']:<3} | Beneficio Prom: {lista['beneficio_prom']:>9.2f} | "
              f"Intervalo de Confianza = [{lista['lower']:.2f}, {lista['upper']:.2f}] (longitud = {intervalo_longitud:.2f})")
# --- Bloque de ejecución de ejemplo ---
if __name__ == "__main__":
    dias_a_simular = 30
    cant_replicas = 10000
    beneficios_acumulados = generar_replicas(cant_replicas,dias_a_simular)
    lista_intervalos = generar_intervalos(cant_replicas,beneficios_acumulados)
    mostrar_resultados(lista_intervalos)