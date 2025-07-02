from .models import Reserva
from django import forms

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['vaga', 'data_prevista', 'hora_entrada', 'hora_saida', 'email', 'telefone']
        widgets = {
            'vaga': forms.Select(attrs={'class': 'form-control'}),
            'data_prevista': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_entrada': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_saida': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }