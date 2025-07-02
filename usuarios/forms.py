from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from usuarios.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Seu melhor e-mail'})
    )
    telefone = forms.CharField(
        label='Telefone',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Seu telefone'})
    )
    cpf = forms.CharField(
        label='CPF',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Seu CPF'})
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'telefone', 'cpf') + UserCreationForm.Meta.fields[1:]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nome de usuário'}),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nome', 'email', 'username']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }