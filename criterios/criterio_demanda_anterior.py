import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nros_aleatorios.generador_congruencial_mixto import generador_nros_aleatorios

dias = 30
costo_faltante = 3.0
costo_sobrante = 1.0
precio_venta = 5.0
produccion_inicial = 60

# Generar demanda
seed = 12345
a = 16807
c = 0
m = 2**31 - 1

numeros_aleatorios = generador_nros_aleatorios(seed, a, c, m, dias)
demanda = [int(num * 20 + 40) for num in numeros_aleatorios]

produccion = [produccion_inicial]
for i in range(1, dias):
    produccion.append(demanda[i - 1])

faltante_total = 0
sobrante_total = 0
dias_con_faltante = 0
dias_con_sobrante = 0
dias_con_justo = 0

print("=== CRITERIO: Producción igual a la demanda del día anterior ===")
print(f"Días simulados: {dias}")
print()

for i in range(dias):
    P = produccion[i]
    D = demanda[i]
    estado = ""
    if P > D:
        sobrante_total += (P - D)
        dias_con_sobrante += 1
        estado = f"SOBRANTE de {P - D} unidades"
    elif P < D:
        faltante_total += (D - P)
        dias_con_faltante += 1
        estado = f"FALTANTE de {D - P} unidades"
    else:
        dias_con_justo += 1
        estado = "Producción justa"

    print(f"Día {i+1}: Demanda={D}, Producción={P} → {estado}")

beneficio_ideal = sum(demanda) * precio_venta
costo_total = (sobrante_total * costo_sobrante) + (faltante_total * costo_faltante)
beneficio_real = beneficio_ideal - costo_total

print()
print(f"Sobrante total (unidades): {sobrante_total} en {dias_con_sobrante} días")
print(f"Faltante total (unidades): {faltante_total} en {dias_con_faltante} días")
print(f"Días con producción justa: {dias_con_justo}")
print(f"Beneficio ideal (sin faltantes ni sobrantes): ${beneficio_ideal:.2f}")
print(f"Costo por faltantes: ${faltante_total * costo_faltante:.2f}")
print(f"Costo por sobrantes: ${sobrante_total * costo_sobrante:.2f}")
print(f"Beneficio real: ${beneficio_real:.2f}")

ultimo_beneficio_real = beneficio_real
