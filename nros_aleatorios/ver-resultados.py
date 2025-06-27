
import csv
from generador_congruencial_mixtov2 import main

csv_file = 'resultados.csv'

rows = []

print("generating stuff")
main()  # Call the main function to generate the CSV file
print("reading results from CSV")

# Read CSV and compute interval length
with open(csv_file, newline='') as f:
    reader = csv.reader(f)
    headers = next(reader)  # Skip header

    for row in reader:
        try:
            p = int(row[0])
            beneficio_prom = float(row[1])
            lower = float(row[4])
            upper = float(row[5])
            interval_length = upper - lower

            rows.append({
                'p': p,
                'beneficio_prom': beneficio_prom,
                'interval_length': interval_length,
                'lower': lower,
                'upper': upper
            })
        except ValueError:
            continue  # skip bad rows

# Sort by beneficio_prom DESC, then by interval length ASC
# rows.sort(key=lambda x: (-x['beneficio_prom'], x['interval_length']))
rows.sort(key=lambda x: (-x['beneficio_prom']))

# Print top 5
print("Top 5 valores de p por beneficio_prom y menor intervalo:\n")
for i, row in enumerate(rows[:5], start=1):
    print(f"{i}. p = {row['p']}, beneficio_prom = {row['beneficio_prom']:.2f}, "
          f"intervalo = [{row['lower']:.2f}, {row['upper']:.2f}] "
          f"(longitud = {row['interval_length']:.2f})")
