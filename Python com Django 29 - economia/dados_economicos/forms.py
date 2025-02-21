from django import forms
from .models import DadosEconomicos

class DadosEconomicosForm(forms.ModelForm):
    class Meta:
        model = DadosEconomicos
        fields = '__all__'
