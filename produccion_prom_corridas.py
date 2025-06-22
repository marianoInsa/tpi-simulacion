from simulador import genera_demanda_diaria, COSTO_VP, COSTO_SB, BENEFICIO

def simular_politica_produccion(
        produccion_semana: int, 
        produccion_finde: int,
        dias_promedio: int,
        cronograma_demanda: list[dict]
) -> dict:
    """
    Simula una política de producción teniendo en cuenta el promedio de producción de los últimos `dias_promedio` días.
    Criterio: Los primeros dias se produce con la producción fija de los argumentos produccion_semana y produccion_finde.
    Luego, se calcula el promedio de los últimos `dias_promedio` días y se utiliza para la producción diaria.
    LOS SOBRANTES DE AYER NO AFECTAN A LA PRODUCCION DE HOY, es indistinto!

    Args:
        produccion_semana (int): La cantidad producida en un día de semana (L-J).
        produccion_finde (int): La cantidad producida en un día de fin de semana (V-S-D).
        dias_promedio (int): El número de días a considerar para calcular el promedio de producción.
        cronograma_demanda (list[dict]): La lista de diccionarios generada por el simulador,
                                         que contiene la demanda y los detalles de cada día.

    Returns:
        dict: Un diccionario con los resultados finales de la simulación.
    """

    historial_demanda = []
    # Acumuladores finales
    ganancias_totales = 0
    costo_total_desperdicio = 0
    costo_total_faltantes = 0

    i = 0
    # El bucle itera sobre la lista de diccionarios que tiene los datos de la demanda diaria.
    for dia_simulado in cronograma_demanda:
        
        demanda_real = dia_simulado["demanda"]

        # Si son los primeros dias, utilizamos la producción fija
        if i < dias_promedio:
            
            tipo_dia_hoy = dia_simulado["tipo_dia"] # "Entre Semana" o "Fin de Semana"
            # --- Seleccionar la producción del día de acuerdo al tipo de dia ---
            if tipo_dia_hoy == "Fin de Semana":
                produccion = produccion_finde
            else: # "Entre Semana"
                produccion = produccion_semana

        # Si ya tenemos suficientes datos, calculamos el promedio
        else:
            produccion = round(sum(historial_demanda[-dias_promedio:]) / dias_promedio)

        # --- Calcular ventas, sobrantes y faltantes ---
        sobrante = max(produccion - demanda_real, 0)
        faltante = max(demanda_real - produccion, 0)
        ventas = min(produccion, demanda_real)

        # ACTUALIZAR TOTALES
        ganancia = ventas * BENEFICIO
        desperdicio = sobrante * COSTO_VP
        faltantes = faltante * COSTO_SB

        ganancias_totales += ganancia
        costo_total_desperdicio += desperdicio
        costo_total_faltantes += faltantes

        # Actualizar el historial de demanda
        historial_demanda.append(demanda_real)
        i += 1

    # --- Resultados finales ---
    costo_total = costo_total_desperdicio + costo_total_faltantes
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
    resultados_finales = []
    
    # Producción fija para días de semana y fines de semana
    produccion_dias_semana = 50
    produccion_fines_semana = 70

    # Define el promedio de días para la política de producción
    dias_promedio = 7
    costo_global = 0
    neto_global = 0

    # Simulamos 10 corridas para obtener un resultado más robusto
    for i in range(1, 11):
        print("="*60)
        print(f"\nSimulación {i} de {dias_a_simular} días:")
        
        # 1. Generamos el cronograma completo de demanda desde el simulador
        cronograma_completo = genera_demanda_diaria(dias_a_simular)

        # 2. Ejecutamos la simulación con la nueva función y los nuevos parámetros
        resultados = simular_politica_produccion(
            produccion_dias_semana,
            produccion_fines_semana,
            dias_promedio,
            cronograma_completo
        )

        # 3. Guardamos los resultados
        resultados_finales.append(resultados)

    print("\nResultados de la simulación:")
    for idx, resultado in enumerate(resultados_finales, 1):
        print(f"Simulación {idx}:")
        print(f"  Ganancia total: ${resultado['ganancia_total']:.2f}")        
        print(f"  Costo total: ${resultado['costo_total']:.2f}")
        costo_global += resultado['costo_total']
        print(f"  Resultado neto: ${resultado['resultado_neto']:.2f}")
        neto_global += resultado['resultado_neto']
        print("-" * 40)
    print("="*60)

    print("CONCLUSIÓN DE REALIZAR 10 CORRIDAS:")
    print(f"Costo total: ${(costo_global):.2f}")
    print(f"Resultado neto global: ${(neto_global):.2f}")