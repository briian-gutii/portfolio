from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Esta es la URL para la página principal
    path('projects/', views.project_index, name='project_index'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('new-data-project/', views.new_data_project, name='new_data_project'),
    path('flight-project/', views.flight_project, name='flight_project'),
    path('incidentes-project/', views.incidentes_project, name='incidentes_project'),
    path('nuevo-proyecto/', views.nuevo_proyecto, name='nuevo_proyecto'),
]
