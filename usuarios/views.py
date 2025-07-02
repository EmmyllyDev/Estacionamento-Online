from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from clientes.models import Cliente, Mensalista
from planos.models import PedidoPlano
from reserva.models import Reserva
from vagas.models import EntradaVeiculo, SaidaVeiculo

from .forms import CustomUserCreationForm, EditarPerfilForm
from .models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # redireciona após login bem-sucedido
        else:
            return render(request, 'usuarios/login.html', {'error': 'Credenciais inválidas'})
    return render(request, 'usuarios/login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('home') # redireciona após registro bem-sucedido
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

def sair_view(request):
    logout(request)
    return redirect ('home')

def perfil_usuario(request):
    cliente = get_object_or_404(Cliente, user=request.user)

    if cliente.tipo == 'mensalista':
        mensalista = get_object_or_404(Mensalista, cliente=cliente, contrato_ativo=True)
        pedido = PedidoPlano.objects.filter(cliente=cliente, pago=True).order_by('-data_pedido').first()
    else:
        mensalista = None
        pedido = None

    # Reservas do usuário
    reservas = Reserva.objects.filter(cliente=request.user).order_by('-data_prevista')

    # Entradas e saídas do usuário
    entradas = EntradaVeiculo.objects.filter(cliente=request.user).order_by('-data_entrada')
    saidas = SaidaVeiculo.objects.filter(cliente=request.user).order_by('-data_saida')

    if request.method == 'POST' and 'cancelar' in request.POST:
        if mensalista:
            mensalista.contrato_ativo = False
            if mensalista.vaga:
                mensalista.vaga.ocupada = False
                mensalista.vaga.save()
            mensalista.vaga = None
            mensalista.save()

            cliente.tipo = 'avulso'
            cliente.save()
        return redirect('home')

    context = {
        'cliente': cliente,
        'mensalista': mensalista,
        'pedido': pedido,
        'reservas': reservas,
        'entradas': entradas,
        'saidas': saidas,
    }

    return render(request, 'usuarios/perfil.html', context)

@login_required
def editar_perfil(request):
    user = request.user

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        
            return redirect('perfil_usuario')
    else:
        form = EditarPerfilForm(instance=user)

    return render(request, 'usuarios/editar_perfil.html', {'form': form})