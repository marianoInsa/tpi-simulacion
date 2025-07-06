from simulador import genera_demanda_diaria, COSTO_VP, COSTO_SB, BENEFICIO

def simular_politica_produccion(
        dias_anteriores: int,
        cronograma_demanda: list[dict]
) -> dict:
    """
    Simula una política de producción teniendo en cuenta el promedio de producción de los últimos `dias_anteriores` días.
    Criterio: Los primeros dias se produce con la producción fija de los argumentos produccion_semana y produccion_finde.
    Luego, se calcula el promedio de los últimos `dias_anteriores` días y se utiliza para la producción diaria.
    LOS SOBRANTES DE AYER NO AFECTAN A LA PRODUCCION DE HOY, es indistinto!

    Args:
        dias_anteriores (int): El número de días a considerar para calcular el promedio de producción.
        cronograma_demanda (list[dict]): La lista de diccionarios generada por el simulador,
                                         que contiene la demanda y los detalles de cada día.

    Returns:
        dict: Un diccionario con los resultados finales de la simulación.
    """

    historial_demanda_dia_semana = []
    historial_demanda_fin_de_semana = []
    # Acumuladores finales
    ganancias_totales = 0
    costo_total_desperdicio = 0
    costo_total_faltantes = 0

#    print("\n" + "="*60)
#    print("INICIANDO SIMULACIÓN CON POLÍTICA DE PRODUCCIÓN CON PROMEDIO DE LOS ÚLTIMOS DÍAS")
#    print(f"Producción igual al promedio de los últimos {(dias_anteriores)} días")
#    print("="*60)

    # El bucle itera sobre la lista de diccionarios que tiene los datos de la demanda diaria.
    for dia_simulado in cronograma_demanda:
        
        demanda_real = dia_simulado["demanda"]
        tipo_dia_hoy = dia_simulado["tipo_dia"] # "Entre Semana" o "Fin de Semana"
       
        if tipo_dia_hoy == "Fin de Semana":    
            # Si es el primer dia, utilizamos la producción fija
            if len(historial_demanda_fin_de_semana) == 0:
                produccion = 60 # Promedio [18-108] del fin de semana = 63. Para que sea múltiplo uso 60  
                historial_demanda_fin_de_semana.append(demanda_real)            
            
            elif len(historial_demanda_fin_de_semana) > 0 and len(historial_demanda_fin_de_semana) < dias_anteriores:
                # Si son los primeros dias, utilizamos el promedio de la cantidad de dias actuales
                produccion = (
                round((sum(historial_demanda_fin_de_semana) / len(historial_demanda_fin_de_semana)) / 6) * 6
                if historial_demanda_fin_de_semana else demanda_real)
                historial_demanda_fin_de_semana.append(demanda_real)
            # Si ya tenemos suficientes datos, calculamos el promedio
            else:
                produccion = round((sum(historial_demanda_fin_de_semana[-dias_anteriores:]) / dias_anteriores) / 6) * 6
                historial_demanda_fin_de_semana.append(demanda_real)
        
        else: # "Entre Semana"
            # Si es el primer dia, utilizamos la producción fija
            if len(historial_demanda_dia_semana) == 0:           
                produccion = 42 # Promedio [4-81] de la semana = 42,5
                historial_demanda_dia_semana.append(demanda_real)
            
            elif len(historial_demanda_dia_semana) > 0 and len(historial_demanda_dia_semana) < dias_anteriores:
            # Si son los primeros dias, utilizamos el promedio de los dias actuales
                produccion = (
                round((sum(historial_demanda_dia_semana) / len(historial_demanda_dia_semana)) / 6) * 6
                if historial_demanda_dia_semana else demanda_real)
                historial_demanda_dia_semana.append(demanda_real)
            # Si ya tenemos suficientes datos, calculamos el promedio
            else:
                produccion = round((sum(historial_demanda_dia_semana[-dias_anteriores:]) / dias_anteriores) / 6) * 6
                historial_demanda_dia_semana.append(demanda_real)
        
        # --- Calcular ventas, sobrantes y faltantes ---
        sobrante = max(produccion - demanda_real, 0)
        faltante = max(demanda_real - produccion, 0)
        ventas = min(produccion, demanda_real)

        # --- Calcular precios del dia ---
        precio_venta = ventas * BENEFICIO
        precio_sobrante = sobrante * COSTO_VP
        precio_faltante = faltante * COSTO_SB

        # ACTUALIZAR TOTALES
        ganancias_totales += precio_venta
        costo_total_desperdicio += precio_sobrante
        costo_total_faltantes += precio_faltante


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
    n_dias = 30

    # Define el promedio de días para la política de producción
    dias_anteriores = 3

    # 1. Generamos el cronograma completo de demanda desde el simulador
    cronograma_completo = genera_demanda_diaria(n_dias)

    # 2. Ejecutamos la simulación con la nueva función y los nuevos parámetros
    resultado = simular_politica_produccion(
                    dias_anteriores,
                    cronograma_completo) 

    print("\n" + "*"*40)
    print("      RESULTADOS FINALES DE LA SIMULACIÓN")
    print("*"*40)
    print(f"Período simulado: {n_dias} días")
    print("Política de Producción:")
    print(f"  - Se produce teniendo en cuenta el promedio de los últimos {(dias_anteriores)} días.")
    print(f"Ganancia Bruta Total: ${resultado['ganancia_total']:,.2f}")
    print(f"Costo por Desperdicio: ${resultado['costo_desperdicio']:,.2f}")
    print(f"Costo por Ventas Perdidas: ${resultado['costo_faltantes']:,.2f}")
    print(f"Costo Total Combinado: ${resultado['costo_total']:,.2f}")
    print("-" * 40)
    print(f"RESULTADO NETO (Ganancia - Costo): ${resultado['resultado_neto']:,.2f}")
    print("*"*40)