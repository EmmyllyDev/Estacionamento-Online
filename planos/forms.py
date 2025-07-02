from django import forms
from vagas.models import Vaga
from .models import PedidoPlano

class PedidoPlanoForm(forms.ModelForm):
    DIAS_VENCIMENTO = [
        (5, 'Dia 5'),
        (10, 'Dia 10'),
        (20, 'Dia 20'),
        (27, 'Dia 27'),
    ]

    vaga = forms.ModelChoiceField(
        queryset=Vaga.objects.filter(ocupada=False),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    dia_vencimento = forms.ChoiceField(
        choices=DIAS_VENCIMENTO,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Dia do Vencimento'
    )

    class Meta:
        model = PedidoPlano
        fields = ['plano', 'vaga']  # removido data_vencimento do form porque será calculado na view
        widgets = {
            'plano': forms.Select(attrs={'class': 'form-control'}),
        }