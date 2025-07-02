import calendar
from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from clientes.models import Cliente, Mensalista
from .forms import PedidoPlanoForm

def calcular_data_vencimento(dia_escolhido):
    hoje = date.today()
    ano = hoje.year
    mes = hoje.month

    if dia_escolhido < hoje.day:
        mes += 1
        if mes > 12:
            mes = 1
            ano += 1

    ultimo_dia_mes = calendar.monthrange(ano, mes)[1]
    dia = min(dia_escolhido, ultimo_dia_mes)

    return date(ano, mes, dia)

@login_required
def solicitar_plano(request):
    cliente = Cliente.objects.get(user=request.user)

    if request.method == 'POST':
        form = PedidoPlanoForm(request.POST)
        if form.is_valid():
            dia_vencimento_escolhido = int(form.cleaned_data['dia_vencimento'])
            data_vencimento = calcular_data_vencimento(dia_vencimento_escolhido)

            pedido = form.save(commit=False)
            pedido.cliente = cliente
            pedido.pago = False
            pedido.data_vencimento = data_vencimento
            pedido.save()

            # Criar o mensalista com base no pedido
            # e vincular a vaga selecionada
            vaga = form.cleaned_data['vaga']
            mensalista = Mensalista.objects.create(
                cliente=cliente,
                plano=pedido.plano,
                vaga=vaga,
                contrato_ativo=False
            )

            # vincula o pedido com o mensalita
            pedido.mensalista = mensalista
            pedido.save()

            # Armazenar o ID do pedido na sessão para uso posterior
            request.session['pedido_id'] = pedido.id
            return redirect('pagamentos:pagamento_mensalista')
    else:
        form = PedidoPlanoForm()

    return render(request, 'planos/solicitar_plano.html', {'form': form})
