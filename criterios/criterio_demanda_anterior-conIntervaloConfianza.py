import numpy as np
import sys
import os
from scipy import stats

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nros_aleatorios.generador_congruencial_mixto import generador_nros_aleatorios

def simular_beneficio(seed, dias=30, costo_faltante=3.0, costo_sobrante=1.0, precio_venta=5.0, produccion_inicial=60):
    a = 16807
    c = 0
    m = 2**31 - 1
    
    numeros_aleatorios = generador_nros_aleatorios(seed, a, c, m, dias)
    demanda = [int(num * 20 + 40) for num in numeros_aleatorios]
    
    produccion = [produccion_inicial]
    for i in range(1, dias):
        produccion.append(demanda[i - 1])
    
    sobrante_total = 0
    faltante_total = 0
    dias_con_faltante = 0
    dias_con_sobrante = 0
    dias_con_justo = 0
    
    print(f"Simulación con semilla {seed}:")
    for i in range(dias):
        P = produccion[i]
        D = demanda[i]
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
        print(f"  Día {i+1}: Demanda={D}, Producción={P} → {estado}")

    beneficio_ideal = sum(demanda) * precio_venta
    costo_total = (sobrante_total * costo_sobrante) + (faltante_total * costo_faltante)
    beneficio_real = beneficio_ideal - costo_total
    
    print(f"  Sobrante total: {sobrante_total} en {dias_con_sobrante} días")
    print(f"  Faltante total: {faltante_total} en {dias_con_faltante} días")
    print(f"  Días producción justa: {dias_con_justo}")
    print(f"  Beneficio ideal: ${beneficio_ideal:.2f}")
    print(f"  Costo faltantes: ${faltante_total * costo_faltante:.2f}")
    print(f"  Costo sobrantes: ${sobrante_total * costo_sobrante:.2f}")
    print(f"  Beneficio real: ${beneficio_real:.2f}")
    print("-" * 50)
    
    return beneficio_real

N = 10  # Cambié a 10 para que no imprima demasiado, poné 1000 o más para análisis real
beneficios = []

for i in range(N):
    beneficio = simular_beneficio(seed=12345 + i)
    beneficios.append(beneficio)

beneficios = np.array(beneficios)

media = np.mean(beneficios)
std = np.std(beneficios, ddof=1)
alpha = 0.05
t_crit = stats.t.ppf(1 - alpha/2, df=N-1)
margen_error = t_crit * (std / np.sqrt(N))
IC_inferior = media - margen_error
IC_superior = media + margen_error

print(f"Simulaciones realizadas: {N}")
print(f"Beneficio medio: ${media:.2f}")
print(f"Intervalo de confianza al {100*(1-alpha):.1f}%: (${IC_inferior:.2f}, ${IC_superior:.2f})")
