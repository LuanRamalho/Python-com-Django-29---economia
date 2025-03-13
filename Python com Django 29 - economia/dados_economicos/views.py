from django.shortcuts import render, redirect, get_object_or_404
from .models import DadosEconomicos
from .forms import DadosEconomicosForm
import matplotlib.pyplot as plt
import io
import urllib, base64
import json

def lista_dados(request):
    # Obtém o ano da query string, se houver
    ano_busca = request.GET.get('ano', '')
    
    if ano_busca:
        dados = DadosEconomicos.objects.filter(ano=ano_busca)
    else:
        dados = DadosEconomicos.objects.all()
    
    return render(request, 'dados_economicos/lista.html', {'dados': dados})

def adicionar_dado(request):
    if request.method == "POST":
        form = DadosEconomicosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_dados')
    else:
        form = DadosEconomicosForm()
    return render(request, 'dados_economicos/form.html', {'form': form})

def editar_dado(request, pk):
    dado = get_object_or_404(DadosEconomicos, pk=pk)
    if request.method == "POST":
        form = DadosEconomicosForm(request.POST, instance=dado)
        if form.is_valid():
            form.save()
            return redirect('lista_dados')
    else:
        form = DadosEconomicosForm(instance=dado)
    return render(request, 'dados_economicos/form.html', {'form': form})

def excluir_dado(request, pk):
    dado = get_object_or_404(DadosEconomicos, pk=pk)
    if request.method == "POST":
        dado.delete()
        return redirect('lista_dados')
    return render(request, 'dados_economicos/confirmar_exclusao.html', {'dado': dado})

def visualizar_grafico(request, pk):
    dado = get_object_or_404(DadosEconomicos, pk=pk)
    
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    valores = [
        float(dado.janeiro), float(dado.fevereiro), float(dado.março), float(dado.abril),
        float(dado.maio), float(dado.junho), float(dado.julho), float(dado.agosto),
        float(dado.setembro), float(dado.outubro), float(dado.novembro), float(dado.dezembro)
    ]
    
    return render(request, 'dados_economicos/grafico.html', {'meses': meses, 'valores': valores, 'ano': dado.ano})


