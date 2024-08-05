import numpy as np
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Project
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from django.conf import settings
from statsmodels.tsa.arima.model import ARIMA  # 
import matplotlib.pyplot as plt
import seaborn as sns

def project_index(request):
    projects = Project.objects.all()
    skills = [
        {'name': 'Python', 'level': 90},
        {'name': 'Django', 'level': 85},
        {'name': 'JavaScript', 'level': 80},
        {'name': 'HTML/CSS', 'level': 85},
        {'name': 'php', 'level': 95},
        {'name': 'SQL', 'level': 80},
        {'name': 'Data Analysis', 'level': 85},
        {'name': 'Machine Learning', 'level': 70},
    ]
    
    # Datos de ejemplo para los vuelos
    df = pd.DataFrame({
        'Airline': ['Avianca', 'Copa Airlines', 'Delta', 'American Airlines', 'United Airlines'] * 4,
        'Destination': ['Mexico City', 'San Salvador', 'Panama City', 'Miami', 'Los Angeles'] * 4,
        'Price': [250, 180, 320, 400, 550, 270, 200, 350, 420, 580, 240, 190, 310, 390, 540, 260, 195, 330, 410, 560],
        'Duration': [150, 70, 200, 170, 310, 160, 75, 210, 180, 320, 155, 72, 205, 175, 315, 158, 73, 208, 178, 318],
        'Passengers': [100, 80, 150, 200, 180, 110, 85, 160, 210, 190, 105, 82, 155, 205, 185, 108, 83, 158, 208, 188],
        'Month': ['Jan', 'Feb', 'Mar', 'Apr'] * 5
    })
    
    # Gráfico 1: Scatter plot de Precio vs Duración
    fig1 = px.scatter(df, x='Duration', y='Price', color='Airline', size='Passengers',
                      hover_data=['Destination'], title='Precio vs Duración de Vuelos')
    chart1 = fig1.to_html(full_html=False)
    
    # Gráfico 2: Bar chart de Precios por Aerolínea
    fig2 = px.bar(df, x='Airline', y='Price', color='Destination', 
                  title='Precios por Aerolínea y Destino')
    chart2 = fig2.to_html(full_html=False)
    
    # Gráfico 3: Pie chart de Distribución de Pasajeros por Aerolínea
    fig3 = px.pie(df, values='Passengers', names='Airline', 
                  title='Distribución de Pasajeros por Aerolínea')
    chart3 = fig3.to_html(full_html=False)
    
    # Gráfico 4: Line chart de Precios y Duración por Destino
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_trace(go.Scatter(x=df['Destination'].unique(), y=df.groupby('Destination')['Price'].mean(), name="Precio Promedio"), secondary_y=False)
    fig4.add_trace(go.Scatter(x=df['Destination'].unique(), y=df.groupby('Destination')['Duration'].mean(), name="Duración Promedio"), secondary_y=True)
    fig4.update_layout(title_text="Precios y Duración Promedio por Destino")
    fig4.update_xaxes(title_text="Destino")
    fig4.update_yaxes(title_text="Precio Promedio", secondary_y=False)
    fig4.update_yaxes(title_text="Duración Promedio (minutos)", secondary_y=True)
    chart4 = fig4.to_html(full_html=False)
    
    # Gráfico 5: Heatmap de Correlación (solo para columnas numéricas)
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    fig5 = px.imshow(corr, text_auto=True, aspect="auto", title="Mapa de Calor de Correlación")
    chart5 = fig5.to_html(full_html=False)
    
    # Gráfico 6: Box plot de Precios por Aerolínea
    fig6 = px.box(df, x='Airline', y='Price', color='Airline',
                  title='Distribución de Precios por Aerolínea')
    chart6 = fig6.to_html(full_html=False)
    
    # Gráfico 7: Línea de tiempo de Precios por Mes
    fig7 = px.line(df.groupby('Month')['Price'].mean().reset_index(), 
                   x='Month', y='Price', title='Tendencia de Precios por Mes')
    chart7 = fig7.to_html(full_html=False)
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            try:
                send_mail(
                    f"Nuevo mensaje de {name}",
                    f"Has recibido un nuevo mensaje de {name} ({email}):\n\n{message}",
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Tu mensaje ha sido enviado con éxito. ¡Gracias por contactarme!')
            except Exception as e:
                messages.error(request, 'Hubo un problema al enviar tu mensaje. Por favor, intenta nuevamente más tarde.')
            
            return redirect('project_index')
    else:
        form = ContactForm()
    
    context = {
        'projects': projects,
        'skills': skills,
        'form': form,
        'chart1': chart1,
        'chart2': chart2,
        'chart3': chart3,
        'chart4': chart4,
        'chart5': chart5,
        'chart6': chart6,
        'chart7': chart7,
    }
    return render(request, 'main/project_index.html', context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'main/project_detail.html', {'project': project})

def new_data_project(request):
    # Generamos datos de ejemplo más complejos para este nuevo proyecto
    np.random.seed(0)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    df = pd.DataFrame({
        'Date': dates,
        'Temperature': np.random.normal(25, 5, len(dates)),
        'Humidity': np.random.normal(60, 10, len(dates)),
        'Wind_Speed': np.random.normal(15, 5, len(dates)),
        'Rainfall': np.random.exponential(5, len(dates))
    })
    df['Season'] = pd.cut(df['Date'].dt.month, bins=[0,3,6,9,12], labels=['Winter', 'Spring', 'Summer', 'Fall'])
    
    # Gráfico 1: Serie temporal de temperatura
    fig1 = px.line(df, x='Date', y='Temperature', title='Temperatura a lo largo del año')
    chart1 = fig1.to_html(full_html=False)
    
    # Gráfico 2: Histograma de temperaturas
    fig2 = px.histogram(df, x='Temperature', nbins=30, title='Distribución de Temperaturas')
    chart2 = fig2.to_html(full_html=False)
    
    # Gráfico 3: Scatter plot de Temperatura vs Humedad
    fig3 = px.scatter(df, x='Temperature', y='Humidity', color='Season', 
                      title='Relación entre Temperatura y Humedad')
    chart3 = fig3.to_html(full_html=False)
    
    # Gráfico 4: Box plot de Temperatura por Estación
    fig4 = px.box(df, x='Season', y='Temperature', title='Distribución de Temperatura por Estación')
    chart4 = fig4.to_html(full_html=False)
    
    # Gráfico 5: Heatmap de correlación
    corr = df[['Temperature', 'Humidity', 'Wind_Speed', 'Rainfall']].corr()
    fig5 = px.imshow(corr, text_auto=True, aspect="auto", title="Mapa de Calor de Correlación")
    chart5 = fig5.to_html(full_html=False)
    
    context = {
        'chart1': chart1,
        'chart2': chart2,
        'chart3': chart3,
        'chart4': chart4,
        'chart5': chart5,
    }
    return render(request, 'main/new_data_project.html', context)


def flight_project(request):
    csv_path = os.path.join(settings.BASE_DIR, 'main', 'data', 'ORIGEN_Y_DESTINO_2024_CLEANED.csv')
    # Cargar los datos
    df = pd.read_csv(csv_path)
    
    # Diccionario para mapear ciudades a países
    city_to_country = {
        'EL SALVADOR': 'El Salvador',
        'COSTA RICA': 'Costa Rica',
        'LOS ANGELES': 'Estados Unidos',
        'BOGOTA, COLOMBIA': 'Colombia',
        'JOHN F. KENNEDY': 'Estados Unidos',
        'CANCUN': 'México',
        'COMAYAGUA HONDURAS': 'Honduras',
        'WASHINGTON': 'Estados Unidos',
        'HOUSTON': 'Estados Unidos',
        'ORLANDO': 'Estados Unidos',
        'SAN PEDRO SULA, HONDURAS': 'Honduras',
        'HONDURAS': 'Honduras',
        'FUERZA AEREA CANADIENCE': 'Canadá',
        'Massachusetts': 'Estados Unidos',
        'NEWARK': 'Estados Unidos',
        'LAS VEGAS': 'Estados Unidos',
        'MANAGUA': 'Nicaragua',
        'RAMON VILLA MORALES HONDURA': 'Honduras'
    }

    # Mapear las ciudades a sus respectivos países
    df['PAIS'] = df['PAIS'].apply(lambda x: city_to_country.get(x, x))
    
    # Agrupar los datos por país y sumar los valores de vuelos
    df = df.groupby('PAIS').sum().reset_index()
    
    # Preparar los datos
    df_melted = df.melt(id_vars=['PAIS'], 
                        value_vars=[col for col in df.columns if 'ATE' in col or 'DESP' in col],
                        var_name='Mes_Tipo', value_name='Vuelos')
    df_melted['Mes'] = df_melted['Mes_Tipo'].apply(lambda x: x.split('_')[0])
    df_melted['Tipo'] = df_melted['Mes_Tipo'].apply(lambda x: 'Aterrizajes' if 'ATE' in x else 'Despegues')
    
    # Gráfico 1: Total de vuelos por país
    fig1 = px.bar(df_melted.groupby('PAIS')['Vuelos'].sum().reset_index().sort_values('Vuelos', ascending=False),
                  x='PAIS', y='Vuelos', title='Total de Vuelos por País')
    chart1 = fig1.to_html(full_html=False)
    
    # Gráfico 2: Comparación de aterrizajes y despegues por país
    fig2 = px.bar(df_melted.groupby(['PAIS', 'Tipo'])['Vuelos'].sum().reset_index(),
                  x='PAIS', y='Vuelos', color='Tipo', barmode='group',
                  title='Comparación de Aterrizajes y Despegues por País')
    chart2 = fig2.to_html(full_html=False)
    
    # Gráfico 3: Tendencia de vuelos a lo largo de los meses
    fig3 = px.line(df_melted.groupby(['Mes', 'Tipo'])['Vuelos'].sum().reset_index(),
                   x='Mes', y='Vuelos', color='Tipo',
                   title='Tendencia de Vuelos a lo Largo de los Meses')
    chart3 = fig3.to_html(full_html=False)
    
    # Gráfico 4: Mapa de calor de vuelos por país y mes
    pivot_df = df_melted.pivot_table(values='Vuelos', index='PAIS', columns='Mes', aggfunc='sum')
    fig4 = px.imshow(pivot_df, title='Mapa de Calor: Vuelos por País y Mes')
    chart4 = fig4.to_html(full_html=False)
    
    # Gráfico 5: Distribución de vuelos por tipo (aterrizajes vs despegues)
    fig5 = px.pie(df_melted.groupby('Tipo')['Vuelos'].sum().reset_index(),
                  values='Vuelos', names='Tipo',
                  title='Distribución de Vuelos: Aterrizajes vs Despegues')
    chart5 = fig5.to_html(full_html=False)

    context = {
        'chart1': chart1,
        'chart2': chart2,
        'chart3': chart3,
        'chart4': chart4,
        'chart5': chart5,
    }
    return render(request, 'main/flight_project.html', context)



def incidentes_project(request):
    incidentes_csv_path = os.path.join(settings.BASE_DIR, 'main', 'data', 'incidentes-2022.csv')
    
    # Cargar los datos
    incidentes_df = pd.read_csv(incidentes_csv_path, delimiter=';')
    
    # Procesar los datos según sea necesario
    # Convertir las fechas y agregar una columna de mes
    incidentes_df['Fecha_Incidente'] = pd.to_datetime(incidentes_df['Fecha_Incidente'], dayfirst=True, errors='coerce')
    incidentes_df['Mes'] = incidentes_df['Fecha_Incidente'].dt.month
    
    # Gráfico 1: Total de incidentes por mes
    incidentes_por_mes = incidentes_df.groupby('Mes').size().reset_index(name='Total_Incidentes')
    fig1 = px.bar(incidentes_por_mes, x='Mes', y='Total_Incidentes', title='Total de Incidentes por Mes', width=600, height=400)
    chart1 = fig1.to_html(full_html=False)
    
    # Gráfico 2: Top 10 tipos de incidentes
    incidentes_por_tipo = incidentes_df['Incidente_Tipo_Incidente'].value_counts().reset_index(name='Total').rename(columns={'index': 'Incidente_Tipo_Incidente'})
    incidentes_por_tipo_top10 = incidentes_por_tipo.head(10)
    fig2 = px.pie(incidentes_por_tipo_top10, values='Total', names='Incidente_Tipo_Incidente', title='Top 10 Tipos de Incidentes', width=600, height=400)
    chart2 = fig2.to_html(full_html=False)
    
    # Gráfico 3: Top 10 municipios con más incidentes
    incidentes_por_municipio = incidentes_df['Municipio'].value_counts().reset_index(name='Total').rename(columns={'index': 'Municipio'})
    incidentes_por_municipio_top10 = incidentes_por_municipio.head(10)
    fig3 = px.bar(incidentes_por_municipio_top10, x='Municipio', y='Total', title='Top 10 Municipios con Más Incidentes', width=600, height=400)
    chart3 = fig3.to_html(full_html=False)
    
    # Gráfico 4: Incidentes por día de la semana
    incidentes_df['Dia_Semana'] = incidentes_df['Fecha_Incidente'].dt.day_name()
    incidentes_por_dia = incidentes_df['Dia_Semana'].value_counts().reset_index(name='Total').rename(columns={'index': 'Dia_Semana'})
    fig4 = px.bar(incidentes_por_dia, x='Dia_Semana', y='Total', title='Incidentes por Día de la Semana', width=600, height=400)
    chart4 = fig4.to_html(full_html=False)
    
    # Gráfico 5: Mapa de calor de correlación entre variables numéricas
    numeric_df = incidentes_df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    fig5 = px.imshow(corr, text_auto=True, aspect="auto", title="Mapa de Calor de Correlación", width=600, height=400)
    chart5 = fig5.to_html(full_html=False)
    
    # Gráfico 6: Predicción de incidentes para los próximos meses
    incidentes_ts = incidentes_df.groupby('Fecha_Incidente').size()
    incidentes_ts = incidentes_ts.resample('M').sum()

    model = ARIMA(incidentes_ts, order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=6)
    
    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(x=incidentes_ts.index, y=incidentes_ts.values, mode='lines', name='Datos Históricos'))
    fig6.add_trace(go.Scatter(x=forecast.index, y=forecast.values, mode='lines', name='Predicción'))
    fig6.update_layout(title='Predicción de Incidentes para los Próximos Meses', xaxis_title='Fecha', yaxis_title='Número de Incidentes', width=600, height=400)
    chart6 = fig6.to_html(full_html=False)
    
    context = {
        'chart1': chart1,
        'chart2': chart2,
        'chart3': chart3,
        'chart4': chart4,
        'chart5': chart5,
        'chart6': chart6,
    }
    return render(request, 'main/incidentes_project.html', context)


def nuevo_proyecto(request):
    csv_path = os.path.join(settings.BASE_DIR, 'main', 'data', 'Supresion-2022.csv')
    
    try:
        data = pd.read_csv(csv_path, on_bad_lines='skip')
    except pd.errors.ParserError as e:
        return render(request, 'main/nuevo_proyecto.html', {'error': str(e)})
    
    # Imprimir los nombres de las columnas para depuración
    print("Columnas del DataFrame:", data.columns)
    
    # Verificar si las columnas necesarias existen en el DataFrame
    required_columns = ['Fecha Reporte', 'Hora Reporte', 'Tipo', 'Departamento', 'Municipio', 'Lugar', 'Latitud', 'Longitud', 'Hectáreas']
    for col in required_columns:
        if col not in data.columns:
            return render(request, 'main/nuevo_proyecto.html', {'error': f"La columna '{col}' no existe en los datos."})
    
    # Generar las gráficas
    # Gráfica de líneas
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data, x='Fecha Reporte', y='Hectáreas', marker='o')
    plt.title('Tendencia de Valores a lo Largo del Tiempo')
    plt.xlabel('Fecha Reporte')
    plt.ylabel('Hectáreas')
    plt.xticks(rotation=45)
    plt.tight_layout()
    line_plot = 'static/images/line_plot.png'
    plt.savefig(os.path.join(settings.BASE_DIR, line_plot))
    
    # Gráfica de barras
    plt.figure(figsize=(10, 6))
    sns.barplot(data=data, x='Tipo', y='Hectáreas')
    plt.title('Comparación de Valores entre Categorías')
    plt.xlabel('Tipo')
    plt.ylabel('Hectáreas')
    plt.xticks(rotation=45)
    plt.tight_layout()
    bar_plot = 'static/images/bar_plot.png'
    plt.savefig(os.path.join(settings.BASE_DIR, bar_plot))
    
    # Gráfica de dispersión
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x='Latitud', y='Longitud', hue='Tipo')
    plt.title('Relación entre Variable1 y Variable2')
    plt.xlabel('Latitud')
    plt.ylabel('Longitud')
    plt.tight_layout()
    scatter_plot = 'static/images/scatter_plot.png'
    plt.savefig(os.path.join(settings.BASE_DIR, scatter_plot))
    
    # Mapa de calor
    plt.figure(figsize=(10, 6))
    corr = data.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Mapa de Calor de Correlaciones')
    plt.tight_layout()
    heatmap = 'static/images/heatmap.png'
    plt.savefig(os.path.join(settings.BASE_DIR, heatmap))
    
    context = {
        'line_plot': line_plot,
        'bar_plot': bar_plot,
        'scatter_plot': scatter_plot,
        'heatmap': heatmap
    }
    
    return render(request, 'main/nuevo_proyecto.html', context)

def home(request):
    return redirect('project_index')