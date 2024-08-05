import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import os

# Datos de vuelos
data = '''Flight Number,Departure,Destination,Airline,Duration,Price
GT100,Guatemala City,Mexico City,Avianca,2h 30m,250
GT101,Guatemala City,San Salvador,Copa Airlines,1h 10m,180
GT102,Guatemala City,Panama City,Delta,3h 20m,320
GT103,Guatemala City,Miami,American Airlines,2h 50m,400
GT104,Guatemala City,Los Angeles,United Airlines,5h 10m,550'''

# Crear DataFrame
df = pd.read_csv(StringIO(data))

# Convertir duración a minutos
df['Duration'] = df['Duration'].apply(lambda x: int(x.split('h')[0]) * 60 + int(x.split('h')[1].split('m')[0]))

# Análisis básico
avg_price = df['Price'].mean()
max_price = df['Price'].max()
min_price = df['Price'].min()
longest_flight = df.loc[df['Duration'].idxmax()]
shortest_flight = df.loc[df['Duration'].idxmin()]

# Crear carpeta si no existe
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main', 'static', 'images')
os.makedirs(static_dir, exist_ok=True)

# Gráfico 1: Precio vs Duración
plt.figure(figsize=(10, 6))
plt.scatter(df['Duration'], df['Price'])
plt.xlabel('Duración (minutos)')
plt.ylabel('Precio (USD)')
plt.title('Precio vs Duración de Vuelos desde Guatemala')
for i, txt in enumerate(df['Destination']):
    plt.annotate(txt, (df['Duration'][i], df['Price'][i]))
plt.savefig(os.path.join(static_dir, 'price_vs_duration.png'))

# Gráfico 2: Precios por Destino
plt.figure(figsize=(10, 6))
plt.bar(df['Destination'], df['Price'], color='skyblue')
plt.xlabel('Destino')
plt.ylabel('Precio (USD)')
plt.title('Precios de Vuelos por Destino')
plt.savefig(os.path.join(static_dir, 'prices_by_destination.png'))

# Gráfico 3: Duración por Destino
plt.figure(figsize=(10, 6))
plt.bar(df['Destination'], df['Duration'], color='lightgreen')
plt.xlabel('Destino')
plt.ylabel('Duración (minutos)')
plt.title('Duración de Vuelos por Destino')
plt.savefig(os.path.join(static_dir, 'duration_by_destination.png'))

# Gráfico 4: Distribución de Precios
plt.figure(figsize=(10, 6))
plt.hist(df['Price'], bins=5, color='coral')
plt.xlabel('Precio (USD)')
plt.ylabel('Frecuencia')
plt.title('Distribución de Precios de Vuelos')
plt.savefig(os.path.join(static_dir, 'price_distribution.png'))

# Resultados del análisis
analysis_results = f"""
Análisis de Vuelos desde Guatemala:

1. Precio promedio: ${avg_price:.2f}
2. Precio máximo: ${max_price:.2f} ({df.loc[df['Price'].idxmax(), 'Destination']})
3. Precio mínimo: ${min_price:.2f} ({df.loc[df['Price'].idxmin(), 'Destination']})
4. Vuelo más largo: {longest_flight['Destination']} ({longest_flight['Duration']} minutos)
5. Vuelo más corto: {shortest_flight['Destination']} ({shortest_flight['Duration']} minutos)
"""

# Guardar los resultados en un archivo
with open(os.path.join(static_dir, 'flight_analysis_results.txt'), 'w') as f:
    f.write(analysis_results)

print("Análisis completado. Resultados guardados en 'main/static/images/flight_analysis_results.txt'")
print("Gráficos guardados en 'main/static/images/'")
