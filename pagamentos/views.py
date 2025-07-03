from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404
from planos.models import PedidoPlano
from django.utils.dateparse import parse_datetime


def pagamento(request):
    valor_total = request.session.get('valor_total')
    vagas = request.session.get('vagas')

    if not valor_total or not vagas:
        return redirect('vagas:lista_vagas')

    erro = None
    forma_pagamento = None

    if request.method == 'POST':
        forma_pagamento = request.POST.get('forma_pagamento')
        numero_cartao = request.POST.get('numero_cartao')
        validade = request.POST.get('validade')
        cvc = request.POST.get('cvc')

        # Validação para débito e crédito
        if forma_pagamento in ['debito', 'credito']:
            if not numero_cartao or not validade or not cvc:
                erro = 'Por favor, preencha todos os dados do cartão para pagamento no débito ou crédito.'
            else:
                # Aqui você pode incluir validações adicionais do cartão se quiser

                # Se válido, salvar na sessão e redirecionar
                request.session['forma_pagamento'] = forma_pagamento
                request.session['numero_cartao'] = numero_cartao
                request.session['validade'] = validade
                request.session['cvc'] = cvc
                return redirect(reverse('pagamentos:recibo'))
        else:
            # Para PIX, não precisa de dados do cartão
            request.session['forma_pagamento'] = forma_pagamento
            return redirect(reverse('pagamentos:recibo'))

    contexto = {
        'valor_total': valor_total,
        'vagas': vagas,
        'erro': erro,
        'forma_pagamento': forma_pagamento,
        'numero_cartao': request.POST.get('numero_cartao', ''),
        'validade': request.POST.get('validade', ''),
        'cvc': request.POST.get('cvc', ''),
    }

    return render(request, 'pagamentos/pagamento.html', contexto)


def recibo(request):
    vagas = request.session.get('vagas')
    entrada = request.session.get('entrada')
    saida = request.session.get('saida')   

    entrada_dt = parse_datetime(entrada) if entrada else None
    saida_dt = parse_datetime(saida) if saida else None  

    contexto = {
        'vagas': vagas,
        'entrada': entrada_dt,
        'saida': saida_dt,
        'valor_total': request.session.get('valor_total'),
        'forma_pagamento': request.session.get('forma_pagamento'),
        'tipo_cobranca': request.session.get('tipo_cobranca'),
    }

    return render(request, 'pagamentos/recibo.html', contexto)

@login_required
def pagamento_mensalista(request):
    if request.method == 'POST':
        # Simulando pagamento confirmado
        pedido_id = request.session.get('pedido_id')
        if not pedido_id:
            return redirect('clientes:solicitar_plano')

        return redirect('pagamentos:confirmar_pagamento', pedido_id=pedido_id)

    return render(request, 'pagamentos/pagamento_mensalista.html')

def confirmar_pagamento(request, pedido_id):
    pedido = get_object_or_404(PedidoPlano, id=pedido_id, cliente__user=request.user)

    if not pedido.pago:
        pedido.pago = True
        pedido.save()

        mensalista = pedido.mensalista
        mensalista.contrato_ativo = True
        mensalista.data_inicio = timezone.now().date()
        mensalista.data_vencimento = pedido.data_vencimento

        # Bloquear a vaga vinculada ao mensalista
        if mensalista.vaga:
            mensalista.vaga.ocupada = True
            mensalista.vaga.save()

        mensalista.save()

        cliente = pedido.cliente
        cliente.tipo = 'mensalista'
        cliente.save()

    return render(request, 'pagamentos/confirmado.html', {'pedido': pedido})