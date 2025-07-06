from simulador import genera_demanda_diaria, COSTO_VP, COSTO_SB, BENEFICIO
import math
from scipy.stats import t

def simular_criterio_demanda_anterior(p_cte: int, cronograma_demanda: list[dict]) -> dict:
    """
    Simula una política donde la producción diaria es la demanda del día anterior + constante.
    El primer día se produce p_cte solamente.

    Args:
        p_cte (int): Constante a sumar a la demanda del día anterior.
        cronograma_demanda (list[dict]): Datos diarios de demanda.

    Returns:
        dict: Resultados finales de la simulación.
    """
    ganancias_totales = 0
    costo_total_desperdicio = 0
    costo_total_faltantes = 0

    sobrantes_de_ayer = 0
    demanda_ayer = 0  # No se conoce la demanda anterior el primer día

    for i, dia_simulado in enumerate(cronograma_demanda):
        demanda_hoy = dia_simulado["demanda"]

        # Calcular producción de hoy
        if i == 0:
            produccion_de_hoy = p_cte  # Día inicial
        else:
            produccion_de_hoy = demanda_ayer + p_cte

        demanda_restante = demanda_hoy
        unidades_vendidas_hoy = 0

        # Gestionar sobrantes de ayer
        if sobrantes_de_ayer > 0:
            if demanda_restante >= sobrantes_de_ayer:
                unidades_vendidas_hoy += sobrantes_de_ayer
                demanda_restante -= sobrantes_de_ayer
            else:
                unidades_vendidas_hoy += demanda_restante
                unidades_desperdiciadas = sobrantes_de_ayer - demanda_restante
                costo_total_desperdicio += unidades_desperdiciadas * COSTO_SB
                demanda_restante = 0

        # Gestionar producción del día
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

        ganancias_totales += unidades_vendidas_hoy * BENEFICIO
        sobrantes_de_ayer = sobrantes_para_manana
        demanda_ayer = demanda_hoy  # actualizar para mañana

    costo_total = costo_total_faltantes + costo_total_desperdicio
    resultado_neto = ganancias_totales - costo_total

    return {
        "ganancia_total": ganancias_totales,
        "costo_desperdicio": costo_total_desperdicio,
        "costo_faltantes": costo_total_faltantes,
        "costo_total": costo_total,
        "resultado_neto": resultado_neto
    }


def generar_replicas(p_cte_valores, cant_replicas, cant_dias):
    acum_benef = {p: [] for p in p_cte_valores}
    for _ in range(cant_replicas):
        demanda_diaria = genera_demanda_diaria(cant_dias)
        for p_cte in p_cte_valores:
            resultado = simular_criterio_demanda_anterior(p_cte, demanda_diaria)
            acum_benef[p_cte].append(resultado["resultado_neto"])
    return acum_benef


def generar_intervalos(cant_replicas, acum_benef, alpha=0.05):
    result = {
        p_cte: {
            'beneficio_prom': 0,
            'stddev': 0,
            'delta': 0,
            'lower': 0,
            'upper': 0
        } for p_cte in acum_benef
    }

    for p_cte in acum_benef:
        prom = sum(acum_benef[p_cte]) / cant_replicas
        stddev = math.sqrt(sum((x - prom) ** 2 for x in acum_benef[p_cte]) / (cant_replicas - 1))
        t_critical = t.ppf(1 - alpha / 2, df=cant_replicas - 1)
        delta = t_critical * (stddev / math.sqrt(cant_replicas))
        result[p_cte].update({
            'beneficio_prom': prom,
            'stddev': stddev,
            'delta': delta,
            'lower': prom - delta,
            'upper': prom + delta
        })

    return result


def mostrar_resultados(resultados_intervalos):
    lista_ordenada = []
    for p_cte, datos in resultados_intervalos.items():
        dic_aux = {
            'p_cte': p_cte,
            'beneficio_prom': datos['beneficio_prom'],
            'stddev': datos['stddev'],
            'delta': datos['delta'],
            'lower': datos['lower'],
            'upper': datos['upper']
        }
        lista_ordenada.append(dic_aux)

    lista_ordenada.sort(key=lambda x: -x['beneficio_prom'])

    print("\n--- Top 5 mejores valores de p_cte ---\n")
    for i, item in enumerate(lista_ordenada[:5], start=1):
        longitud = item['upper'] - item['lower']
        print(f"{i}. p_cte = {item['p_cte']:>3} | Beneficio Prom: {item['beneficio_prom']:>9.2f} | "
              f"IC 95% = [{item['lower']:.2f}, {item['upper']:.2f}] (longitud = {longitud:.2f})")


# --- Ejecución ---
if __name__ == "__main__":
    dias_a_simular = 30
    cant_replicas = 50000
    valores_de_pcte = list(range(0, 61, 6))  # probamos desde 0 hasta 60 en pasos de 6
    beneficios = generar_replicas(valores_de_pcte, cant_replicas, dias_a_simular)
    intervalos = generar_intervalos(cant_replicas, beneficios)
    mostrar_resultados(intervalos)
