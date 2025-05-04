# Generación de Números Pseudoaleatorios y Pruebas Estadísticas

Este proyecto implementa un generador de números pseudoaleatorios utilizando el método congruencial mixto y realiza cuatro pruebas estadísticas para verificar su validez:

1. Prueba de medias
2. Prueba de varianza
3. Prueba de uniformidad (Chi-cuadrada)
4. Prueba de independencia (Poker)

---

## Índice

- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Configuración del Entorno de Desarrollo](#configuración-del-entorno-de-desarrollo)
- [Fundamentación Teórica](#fundamentación-teórica)
  - [Método Congruencial Mixto](#método-congruencial-mixto)
  - [Ventajas del Método Congruencial Mixto](#ventajas-del-método-congruencial-mixto)
- [Pruebas Estadísticas](#pruebas-estadísticas)
  - [Prueba de Medias](#prueba-de-medias)
  - [Prueba de Varianza](#prueba-de-varianza)
  - [Prueba de Uniformidad (Chi-cuadrada)](#prueba-de-uniformidad-chi-cuadrada)
  - [Prueba de Independencia (Poker)](#prueba-de-independencia-poker)
- [Conclusiones de las Pruebas](#conclusiones-de-las-pruebas)
- [Guía de Uso](#guía-de-uso)
  - [Generación de Números Pseudoaleatorios](#generación-de-números-pseudoaleatorios)
  - [Ejecución de Pruebas Estadísticas](#ejecución-de-pruebas-estadísticas)

---

## Estructura del Proyecto

```
.
├── nros_aleatorios/
│   └── generador_congruencial_mixto.py
├── pruebas_estadisticas/
│   ├── prueba_de_independencia_poker.py
│   ├── prueba_de_medias.py
│   ├── prueba_de_uniformidad_chi_cuadrada.py
│   └── prueba_de_varianza.py
├── main.py
├── numeros_aleatorios_metodo_mixto.py
├── README.md
├── requirements.py
```

---

## Requisitos

- Python 3.12 o superior
- pip
- NumPy
- SciPy

---

## Configuración del Entorno de Desarrollo

Sigue los siguientes pasos para configurar tu entorno de desarrollo:

- **Clona el repositorio y navega al directorio del proyecto**

```sh
git clone https://github.com/marianoInsa/tpi-simulacion.git
cd tpi-simulacion
```

- **Crea un entorno virtual**

Crea un entorno virtual en tu máquina local, que llamaremos `env-tpi`.

```sh
python -m venv env-tpi
```

- **Activa el entorno virtual**

**En Windows:**

```sh
env-tpi\Scripts\activate
```

**En Linux/MacOS:**

```sh
source env-tpi/bin/activate
```

> [!NOTE]
> Si encuentras un error relacionado con la ejecución de scripts en Windows, puedes solucionarlo ejecutando el siguiente comando en PowerShell:

```sh
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego, intenta activar el entorno nuevamente.

- **Instala las dependencias**

Una vez que el entorno virtual esté activado, instala todas las dependencias necesarias utilizando el archivo `requirements.txt`.

```sh
pip install -r requirements.txt
```

- **Desactiva el entorno virtual**

Cuando termines de trabajar, puedes desactivar el entorno virtual usando el siguiente comando:

```sh
deactivate
```

- **Agregar una dependencia**

Para agregar una nueva dependencia al proyecto, puedes usar:

```sh
pip install nombre_dependencia
```

- **Eliminar una dependencia**

Para eliminar una dependencia existente:

```sh
pip uninstall nombre_dependencia
```

- **Actualizar `requirements.txt`**

Si has agregado o eliminado dependencias, asegúrate de actualizar el archivo requirements.txt ejecutando:

```sh
pip freeze > requirements.txt
```

> [!NOTE]
> Asegúrate de hacer esto antes de desactivar el entorno virtual.

---

## Fundamentación Teórica

### Método Congruencial Mixto

El método congruencial mixto (también conocido como generador congruencial lineal) es una técnica matemática para generar secuencias de números pseudoaleatorios. Su fórmula general es:

X<sub>n+1</sub> = (a·X<sub>n</sub> + c) mod m

Donde:

- X<sub>n</sub> es el número actual en la secuencia
- X<sub>n+1</sub> es el siguiente número en la secuencia
- a es el multiplicador
- c es el incremento
- m es el módulo
- X<sub>0</sub> es el valor inicial o semilla

Para obtener números pseudoaleatorios en el intervalo [0,1), se divide cada X<sub>n</sub> por m:

r<sub>n</sub> = X<sub>n</sub> / m

La calidad de los números generados depende significativamente de la elección adecuada de los parámetros a, c, m y X<sub>0</sub>. Para un período máximo (m), se recomienda:

1. c y m sean primos entre sí (no tengan factores comunes)
2. a - 1 sea divisible por todos los factores primos de m
3. a - 1 sea divisible por 4 si m es divisible por 4

### Ventajas del Método Congruencial Mixto

Este método es particularmente conveniente por varias razones:

1. **Simplicidad**: La implementación requiere solo operaciones aritméticas básicas (multiplicación, suma y módulo).
2. **Eficiencia computacional**: Consume pocos recursos, lo que lo hace ideal para aplicaciones donde el rendimiento es crítico.
3. **Comportamiento predecible**: Con los parámetros correctos, se puede garantizar un período largo antes de que la secuencia se repita.
4. **Reproducibilidad**: Al usar la misma semilla y parámetros, se obtiene exactamente la misma secuencia, lo que es útil para depuración.
5. **Base teórica sólida**: Es un método bien estudiado con propiedades estadísticas conocidas.

Si bien existen generadores más sofisticados, el método congruencial mixto ofrece un excelente equilibrio entre simplicidad de implementación y calidad de los números generados, lo que lo convierte en una opción ideal para muchas aplicaciones prácticas.

---

## Pruebas Estadísticas

Para verificar la calidad de los números pseudoaleatorios generados, se implementan cuatro pruebas estadísticas que evalúan diferentes aspectos de aleatoriedad:

### Prueba de Medias

La prueba de medias verifica si la media de los números generados se aproxima al valor esperado para una distribución uniforme en el intervalo [0,1), que es 0.5.

**Fundamento teórico**:

- Para una distribución uniforme en [0,1), la media teórica es μ = 0.5
- La desviación estándar teórica para n valores es σ = 1/√(12n)
- Se aplica la prueba Z para comprobar si la media observada está dentro de un intervalo de confianza aceptable

**Procedimiento**:

1. Calcular la media observada (x̄) de los números generados
2. Calcular el estadístico Z = |x̄ - 0.5| / (1/√(12n))
3. Para un nivel de confianza del 95%, se acepta la prueba si Z < 1.96

**Conclusión**:

- Si la prueba se acepta, la media de los números generados es estadísticamente similar a la esperada para números aleatorios
- Si la prueba se rechaza, existe un sesgo en la tendencia central de los números generados

### Prueba de Varianza

La prueba de varianza verifica si la varianza de los números generados se aproxima al valor esperado para una distribución uniforme en [0,1), que es 1/12 ≈ 0.0833.

**Fundamento teórico**:

- Para una distribución uniforme en [0,1), la varianza teórica es σ² = 1/12
- Se utiliza una prueba de chi-cuadrada para determinar si la varianza observada está dentro de los límites aceptables
- Para n números, el estadístico 12n·S² (donde S² es la varianza muestral) sigue aproximadamente una distribución chi-cuadrada con n-1 grados de libertad

**Procedimiento**:

1. Calcular la varianza muestral (S²) de los números generados
2. Calcular el estadístico V = 12n·S²
3. Para un nivel de confianza del 95%, se acepta la prueba si χ²<sub>α/2,n-1</sub> < V < χ²<sub>1-α/2,n-1</sub>

**Conclusión**:

- Si la prueba se acepta, la dispersión de los números generados es consistente con una verdadera secuencia aleatoria
- Si la prueba se rechaza, la dispersión es demasiado grande o demasiado pequeña para ser considerada aleatoria

### Prueba de Uniformidad (Chi-cuadrada)

La prueba de uniformidad chi-cuadrada evalúa si los números generados se distribuyen uniformemente en todo el intervalo [0,1), dividiendo este intervalo en subintervalos y analizando la frecuencia de ocurrencia en cada uno.

**Fundamento teórico**:

- Para números verdaderamente aleatorios, la frecuencia esperada en cada subintervalo debe ser aproximadamente igual
- El estadístico chi-cuadrado mide la discrepancia entre las frecuencias observadas y esperadas
- El estadístico sigue una distribución chi-cuadrada con k-1 grados de libertad, donde k es el número de subintervalos

**Procedimiento**:

1. Dividir el intervalo [0,1) en k subintervalos iguales
2. Contar la frecuencia observada (O<sub>i</sub>) en cada subintervalo
3. Calcular la frecuencia esperada (E<sub>i</sub> = n/k) para cada subintervalo
4. Calcular el estadístico χ² = Σ[(O<sub>i</sub> - E<sub>i</sub>)²/E<sub>i</sub>]
5. Para un nivel de confianza del 95%, se acepta la prueba si χ² < χ²<sub>α,k-1</sub>

**Conclusión**:

- Si la prueba se acepta, los números están distribuidos uniformemente en todo el intervalo
- Si la prueba se rechaza, existen sesgos en la distribución que hacen que algunos valores sean más probables que otros

### Prueba de Independencia (Poker)

La prueba de poker evalúa la independencia de los dígitos en los números generados, analizando patrones similares a las manos de poker (pares, tercias, etc.) en grupos de dígitos.

**Fundamento teórico**:

- Se agrupan los números en "manos" de d dígitos
- Se clasifican estas manos según los patrones (todos diferentes, un par, dos pares, tercia, etc.)
- Se comparan las frecuencias observadas con las probabilidades teóricas de cada patrón
- El estadístico sigue una distribución chi-cuadrada con k-1 grados de libertad, donde k es el número de categorías

**Procedimiento**:

1. Convertir cada número en una secuencia de d dígitos
2. Agrupar los números en "manos" de d dígitos
3. Clasificar cada mano según su patrón
4. Contar la frecuencia observada (O<sub>i</sub>) de cada patrón
5. Calcular la frecuencia esperada (E<sub>i</sub>) según la probabilidad teórica
6. Calcular el estadístico χ² = Σ[(O<sub>i</sub> - E<sub>i</sub>)²/E<sub>i</sub>]
7. Para un nivel de confianza del 95%, se acepta la prueba si χ² < χ²<sub>α,k-1</sub>

**Conclusión**:

- Si la prueba se acepta, los dígitos en los números generados son independientes entre sí
- Si la prueba se rechaza, existen patrones o dependencias entre los dígitos que no deberían estar presentes en números verdaderamente aleatorios

## Conclusiones de las Pruebas

La combinación de estas cuatro pruebas proporciona una evaluación integral de la calidad de los números pseudoaleatorios:

1. **Prueba de medias**: Evalúa si el generador produce valores centrados correctamente en 0.5.
2. **Prueba de varianza**: Confirma si la dispersión de los valores es adecuada.
3. **Prueba de uniformidad**: Verifica que los números cubran uniformemente todo el intervalo.
4. **Prueba de independencia**: Asegura que no haya patrones o correlaciones entre los valores.

Para considerar que un generador produce números con buenas propiedades aleatorias, debe pasar todas estas pruebas. Si falla en alguna:

- **Falla en prueba de medias**: Indica un sesgo hacia valores mayores o menores que 0.5.
- **Falla en prueba de varianza**: Revela que los números están demasiado agrupados o demasiado dispersos.
- **Falla en prueba de uniformidad**: Muestra que algunos subintervalos tienen más ocurrencias que otros.
- **Falla en prueba de independencia**: Señala la existencia de patrones reconocibles.

Es importante destacar que pasar estas pruebas no garantiza que el generador sea criptográficamente seguro, pero sí que posee propiedades estadísticas adecuadas para muchas aplicaciones prácticas como simulaciones, muestreos y experimentos numéricos.

---

## Guía de Uso

### Generación de Números Pseudoaleatorios

Para generar una secuencia de números pseudoaleatorios usando el método congruencial mixto:

```sh
python generador_congruencial_mixto.py
```

El script generador_congruencial_mixto.py tiene valores predeterminados configurados que puedes modificar directamente en el código:

```python
# Parámetros del generador
seed = 12345 # Semilla inicial
a = 16807 # Multiplicador
c = 0 # Incremento (en este caso usa generador multiplicativo puro)
m = 2**31 - 1 # Módulo (2^31 - 1 = 2,147,483,647)
n = 100 # Cantidad de números a generar
```

Los números generados se guardarán automáticamente en el archivo `numeros_aleatorios_metodo_mixto.csv`, un número por línea.

### Ejecución de Pruebas Estadísticas

Una vez generado el archivo con los números pseudoaleatorios, puedes ejecutar todas las pruebas estadísticas a la vez mediante:

```sh
python main.py
```

El script `main.py` realizará automáticamente:

1. Carga de números desde el archivo `numeros_aleatorios_metodo_mixto.csv`
2. Cálculo de estadísticas básicas (media, varianza, valores mínimo y máximo)
3. Ejecución de las cuatro pruebas estadísticas con un nivel de significancia `α = 0.05`:
   - Prueba de Medias
   - Prueba de Varianza
   - Prueba de Uniformidad (Chi-Cuadrada) con 10 intervalos
   - Prueba de Independencia (Poker) con 5 dígitos
4. Presentación de resultados y conclusiones en un formato claro.

---
