import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Load your CSV file
df = pd.read_csv('resultados_simulacion.csv')  # ← replace with the path to your file

# Remove thousands separators (spaces) and convert to integers
for col in ['beneficio_promedio', 'delta']:
    df[col] = df[col].astype(str).str.replace(' ', '').astype(int)

# Extract data
labels = df['nombre_criterio'].tolist()
means = df['beneficio_promedio'].tolist()
errors = df['delta'].tolist()

# Brown-ish color palette
colors = ['#cc8a63', '#d49d79', '#e9b9a6', '#f4d6c2', '#f4e3d7', '#f4f1ee']

# Plot
plt.figure(figsize=(10, 6))
plt.bar(labels, means, yerr=errors, capsize=10, color=colors[:len(labels)], edgecolor='none', alpha=0.95)

# Dark theme
plt.gca().set_facecolor('#2d2b2b')
plt.gcf().set_facecolor('#2d2b2b')
plt.grid(axis='y', linestyle='--', alpha=0.3, color='white')
plt.tick_params(colors='white', rotation=20)
plt.ylabel('Beneficio Promedio', color='white')
plt.title('Análisis de Resultados: Beneficio Obtenido por Criterio', color='peachpuff', fontsize=14)
plt.xticks(color='white')
plt.yticks(color='white')

# Format y-axis as currency
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

plt.tight_layout()
plt.savefig('beneficio_errorbar_from_csv.png', dpi=300)
plt.close()
