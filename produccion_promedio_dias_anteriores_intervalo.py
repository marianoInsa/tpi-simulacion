import math
import itertools
from simulador import genera_demanda_diaria, COSTO_VP, COSTO_SB, BENEFICIO
from scipy.stats import t 
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

    return resultado_neto

def generar_replicas(cant_replicas, n_dias):
    for __ in range(1, cant_replicas + 1):
            # 1. Generamos el cronograma completo de demanda desde el simulador
            cronograma_completo = genera_demanda_diaria(n_dias)
            # 2. Ejecutamos la simulación con la nueva función y los nuevos parámetros
            beneficios_obtenidos.append(simular_politica_produccion(
                dias_anteriores,
                cronograma_completo
            ))
    

# --- Bloque de ejecución de ejemplo ---
if __name__ == "__main__":
    n_dias = 30
    cant_replicas = 10000


    intervalos = {}

    for i in range(1,29):
        # Define el promedio de días para la política de producción
        dias_anteriores = i
        beneficios_obtenidos = []
        for j in range(1, 10001):
            # 1. Generamos el cronograma completo de demanda desde el simulador
            cronograma_completo = genera_demanda_diaria(n_dias)
            # 2. Ejecutamos la simulación con la nueva función y los nuevos parámetros
            beneficios_obtenidos.append(simular_politica_produccion(
                dias_anteriores,
                cronograma_completo
            ))
        alpha = 0.05
        length = len(beneficios_obtenidos)
        beneficio_prom = sum(beneficios_obtenidos) / length
        stddev = math.sqrt(sum((x - beneficio_prom) ** 2 for x in beneficios_obtenidos) / (length - 1))
        t_critical = t.ppf(1 - alpha / 2, df=length - 1)
        delta = t_critical * (stddev / math.sqrt(length))
        lower = beneficio_prom - delta
        upper = beneficio_prom + delta

        intervalos[i] = {
            "lower": lower,
            "upper": upper,
            "dias_anteriores": dias_anteriores
        }

        #print(f"Intervalo de Beneficio Prom con {dias_anteriores} dias anteriores: [{lower:.2f}, {upper:.2f}]")
    
    # Imprimir los resultados finales
    top5 = sorted(
        intervalos.values(),
        key=lambda x: (x["lower"] + x["upper"]) / 2,
        reverse=True
    )[:5]
    print("\nTOP 5 de intervalos con mayor beneficio promedio:")
    for idx, res in enumerate(top5, 1):
        print(f"{idx}. Días anteriores: {res['dias_anteriores']} | "
              f"Promedio: {((res['lower'] + res['upper']) / 2):.2f} | "
              f"IC: [{res['lower']:.2f}, {res['upper']:.2f}] (longitud {(res['upper'] - res['lower']):.2f}) ")
