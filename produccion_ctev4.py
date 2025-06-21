# VERSIÓN CON PRODUCCIÓN DIFERENCIADA
# Asumiendo que las constantes están en un archivo config.py o en simulador.py
from simulador import genera_demanda_diaria, COSTO_VP, COSTO_SB, BENEFICIO

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

    print("\n" + "="*60)
    print("INICIANDO SIMULACIÓN CON POLÍTICA DE PRODUCCIÓN DIFERENCIADA")
    print(f"Producción L-J: {produccion_semana} | Producción V-S-D: {produccion_finde}")
    print("="*60)

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


# --- Bloque de ejecución de ejemplo ---
if __name__ == "__main__":
    dias_a_simular = 30
    
    # Define los dos niveles de producción que quieres probar
    produccion_dias_semana = 50
    produccion_fines_semana = 70

    # 1. Generamos el cronograma completo de demanda desde el simulador
    cronograma_completo = genera_demanda_diaria(dias_a_simular)
    
    # 2. Ejecutamos la simulación con la nueva función y los nuevos parámetros
    resultados = simular_politica_produccion(
        produccion_semana=produccion_dias_semana, 
        produccion_finde=produccion_fines_semana,
        cronograma_demanda=cronograma_completo
    )

    print("\n" + "*"*40)
    print("      RESULTADOS FINALES DE LA SIMULACIÓN")
    print("*"*40)
    print(f"Período simulado: {dias_a_simular} días")
    print(f"Política de Producción:")
    print(f"  - Días de Semana (L-J): {produccion_dias_semana} unidades/día")
    print(f"  - Fines de Semana (V-S-D): {produccion_fines_semana} unidades/día")
    print(f"Ganancia Bruta Total: ${resultados['ganancia_total']:,.2f}")
    print(f"Costo por Desperdicio: ${resultados['costo_desperdicio']:,.2f}")
    print(f"Costo por Ventas Perdidas: ${resultados['costo_faltantes']:,.2f}")
    print(f"Costo Total Combinado: ${resultados['costo_total']:,.2f}")
    print("-" * 40)
    print(f"RESULTADO NETO (Ganancia - Costo): ${resultados['resultado_neto']:,.2f}")
    print("*"*40)