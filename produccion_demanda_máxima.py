from simulador import genera_demanda_diaria, COSTO_VP, COSTO_SB, BENEFICIO

def simular_produccion_maxima(cronograma_demanda, N=5, produccion_inicial=60):
    """
    Simula una política de producción diferenciada para días de semana y fines de semana,
    con una vida útil de producto de 2 días.
    
    Criterio: Producir cada día lo mismo que la demanda máxima observada en los últimos N días,
    diferenciando entre días de semana y fines de semana.

    Args:
        cronograma_demanda (list[dict]): Lista de días simulados con demanda.
        N (int): Cantidad de días anteriores a considerar para calcular la producción.
        produccion_inicial (int): Producción fija para los primeros N días de cada tipo.
    
    Returns:
        dict: Resultados de la simulación.
    """
    ganancias_totales = 0
    costo_total_desperdicio = 0
    costo_total_faltantes = 0

    sobrantes_de_ayer = 0

    demandas_weekday = []
    demandas_weekend = []

    print("\n" + "="*60)
    print(f"INICIANDO SIMULACIÓN CON CRITERIO: MÁXIMO DE LOS ÚLTIMOS {N} DÍAS (SEGÚN TIPO DE DÍA)")
    print("="*60)

    for i, dia in enumerate(cronograma_demanda):
        demanda_hoy = dia["demanda"]
        tipo_dia_hoy = dia["tipo_dia"]

        # --- Determinar la producción de hoy según tipo de día ---
        if tipo_dia_hoy == "Entre Semana":
            historial = demandas_weekday
        else:
            historial = demandas_weekend

        if len(historial) < N:
            produccion_de_hoy = produccion_inicial
        else:
            produccion_de_hoy = max(historial[-N:])

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
            else:
                unidades_vendidas_hoy += demanda_restante
                sobrantes_para_manana = produccion_de_hoy - demanda_restante
        else:
            sobrantes_para_manana = produccion_de_hoy

        # 3. ACTUALIZAR ESTADO
        sobrantes_de_ayer = sobrantes_para_manana
        ganancias_totales += unidades_vendidas_hoy * BENEFICIO

        # 4. ACTUALIZAR HISTÓRICO CORRESPONDIENTE
        if tipo_dia_hoy == "Entre Semana":
            demandas_weekday.append(demanda_hoy)
        else:
            demandas_weekend.append(demanda_hoy)

    costo_total = costo_total_faltantes + costo_total_desperdicio
    resultado_neto = ganancias_totales - costo_total

    return {
        "ganancia_total": ganancias_totales,
        "costo_desperdicio": costo_total_desperdicio,
        "costo_faltantes": costo_total_faltantes,
        "costo_total": costo_total,
        "resultado_neto": resultado_neto
    }


if __name__ == "__main__":
    dias_a_simular = 30

    cronograma = genera_demanda_diaria(dias_a_simular)
    
    resultados = simular_produccion_maxima(
        cronograma_demanda=cronograma,
        N=5,
        produccion_inicial=60
    )

    print("\n" + "*"*40)
    print("      RESULTADOS FINALES DE LA SIMULACIÓN")
    print("*"*40)
    print(f"Período simulado: {dias_a_simular} días")
    print(f"Criterio: Producción igual al máximo de los últimos 5 días")
    print(f"Ganancia Bruta Total: ${resultados['ganancia_total']:,.2f}")
    print(f"Costo por Desperdicio: ${resultados['costo_desperdicio']:,.2f}")
    print(f"Costo por Ventas Perdidas: ${resultados['costo_faltantes']:,.2f}")
    print(f"Costo Total Combinado: ${resultados['costo_total']:,.2f}")
    print("-" * 40)
    print(f"RESULTADO NETO (Ganancia - Costo): ${resultados['resultado_neto']:,.2f}")
    print("*"*40)
