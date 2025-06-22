# Archivo: criterios/criterio_minimo_faltante.py

from simulador import genera_demanda_diaria, COSTO_VP, COSTO_SB, BENEFICIO

DAYS = 30
PRODUCCION_INICIAL = 60  # 5 docenas

# Generamos la demanda de los próximos días
demanda_info = genera_demanda_diaria(DAYS)
demanda = [dia["demanda"] for dia in demanda_info]

produccion = []
sobrante_total = 0
faltante_total = 0
dias_con_sobrante = 0
dias_con_faltante = 0
dias_con_justo = 0

print("=== CRITERIO: Producción que minimiza el faltante ===")
print(f"Días simulados: {DAYS}\n")

# Este criterio recorre todo el rango posible y elige la producción diaria que da el menor faltante
for i in range(DAYS):
    D = demanda[i]

    # Para el primer día usamos una producción inicial
    if i == 0:
        P = PRODUCCION_INICIAL
    else:
        # Probamos todas las producciones entre 30 y 100 y elegimos la que minimiza el faltante
        min_faltante = float('inf')
        mejor_P = PRODUCCION_INICIAL

        for P_candidato in range(30, 101):
            faltante = max(0, D - P_candidato)
            if faltante < min_faltante:
                min_faltante = faltante
                mejor_P = P_candidato

        P = mejor_P

    produccion.append(P)

    if P > D:
        sobrante = P - D
        sobrante_total += sobrante
        dias_con_sobrante += 1
        print(f"Día {i+1}: Demanda={D}, Producción={P} → SOBRANTE de {sobrante} unidades")
    elif P < D:
        faltante = D - P
        faltante_total += faltante
        dias_con_faltante += 1
        print(f"Día {i+1}: Demanda={D}, Producción={P} → FALTANTE de {faltante} unidades")
    else:
        dias_con_justo += 1
        print(f"Día {i+1}: Demanda={D}, Producción={P} → Producción justa")

beneficio_ideal = sum(demanda) * BENEFICIO
costo_faltantes = faltante_total * COSTO_VP
costo_sobrantes = sobrante_total * COSTO_SB
beneficio_real = beneficio_ideal - costo_faltantes - costo_sobrantes

print(f"\nSobrante total (unidades): {sobrante_total} en {dias_con_sobrante} días")
print(f"Faltante total (unidades): {faltante_total} en {dias_con_faltante} días")
print(f"Días con producción justa: {dias_con_justo}")
print(f"Beneficio ideal (sin faltantes ni sobrantes): ${beneficio_ideal:.2f}")
print(f"Costo por faltantes: ${costo_faltantes:.2f}")
print(f"Costo por sobrantes: ${costo_sobrantes:.2f}")
print(f"Beneficio real: ${beneficio_real:.2f}")

ultimo_beneficio_real = beneficio_real
