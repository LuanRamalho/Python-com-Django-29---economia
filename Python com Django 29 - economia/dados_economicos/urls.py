from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_dados, name='lista_dados'),
    path('adicionar/', views.adicionar_dado, name='adicionar_dado'),
    path('editar/<int:pk>/', views.editar_dado, name='editar_dado'),
    path('excluir/<int:pk>/', views.excluir_dado, name='excluir_dado'),
    path('grafico/<int:pk>/', views.visualizar_grafico, name='visualizar_grafico'),
]
