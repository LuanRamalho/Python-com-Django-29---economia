from django.shortcuts import render, redirect, get_object_or_404
from .models import DadosEconomicos
from .forms import DadosEconomicosForm
import matplotlib.pyplot as plt
import io
import urllib, base64

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
    valores = [dado.janeiro, dado.fevereiro, dado.março, dado.abril, dado.maio, dado.junho,
               dado.julho, dado.agosto, dado.setembro, dado.outubro, dado.novembro, dado.dezembro]

    plt.figure(figsize=(8, 4))
    plt.plot(meses, valores, marker='o', linestyle='-', color='b', label=f"Ano {dado.ano}")
    
    # Adiciona os valores acima dos pontos
    for i, valor in enumerate(valores):
        plt.text(meses[i], valor, f"{valor:.2f}%", ha='center', va='bottom', fontsize=10, color='black')

    plt.xlabel("Meses")
    plt.ylabel("Percentual Econômico (%)")
    plt.title(f"Dados Econômicos - {dado.ano}")
    plt.legend()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode()
    uri = f"data:image/png;base64,{string}"
    
    return render(request, 'dados_economicos/grafico.html', {'grafico': uri, 'dado': dado})

