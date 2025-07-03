from django.utils import timezone
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.urls import reverse

from usuarios.models import User
from .models import EntradaVeiculo, SaidaVeiculo, Vaga

def lista_vagas(request):
    liberar_vagas_expiradas()

    todas_as_vagas = Vaga.objects.all().order_by('numero')
    vagas_ocupadas_numeros = list(todas_as_vagas.filter(ocupada=True).values_list('numero', flat=True))

    vaga_do_mensalista = None
    if request.user.is_authenticated:
        try:
            user = request.user
            if user.mensalista and user.vaga_mensalista:
                vaga_do_mensalista = user.vaga_mensalista
        except User.DoesNotExist:
            pass

    context = {
        'todas_as_vagas': todas_as_vagas,
        'vagas_ocupadas_json': json.dumps(vagas_ocupadas_numeros),
        'total_vagas_count': todas_as_vagas.count(),
        'vaga_do_mensalista': vaga_do_mensalista,
    }
    return render(request, 'vagas/lista_vagas.html', context)

@login_required
def confirmar_vaga(request):
    if request.method == 'POST':
        vagas = request.POST.get('vagas')
        tipo_cobranca = request.POST.get('tipo_cobranca')
        entrada = request.POST.get('entrada')
        saida = request.POST.get('saida')

        if not tipo_cobranca:
            return render(request, 'vagas/confirmar_vaga.html', {
                'vagas': vagas,
                'erro': 'Selecione o tipo de cobrança',
                'tipo_cobranca': tipo_cobranca,
                'entrada': entrada,
                'saida': saida,
            })
        
        vagas_selecionadas = [v.strip() for v in vagas.split(',') if v.strip()]
        quantidade_vagas = len(vagas_selecionadas)

        # Valida entrada e saída caso cobrança por hora
        if tipo_cobranca == 'hora':
            if not entrada or not saida:
                return render(request, 'vagas/confirmar_vaga.html', {
                    'vagas': vagas,
                    'erro': 'Horários são obrigatórios para cobrança por hora.'
                })
            entrada_dt = parse_datetime(entrada)
            saida_dt = parse_datetime(saida)
            if not entrada_dt or not saida_dt or entrada_dt >= saida_dt:
                return render(request, 'vagas/confirmar_vaga.html', {
                    'vagas': vagas,
                    'erro': 'Horários inválidos. Verifique entrada e saída.'
                })
        else:
            # Para diária, pode colocar entrada como agora e saída 24h depois, por exemplo
            entrada_dt = timezone.now()
            saida_dt = entrada_dt + timezone.timedelta(days=1)

        # Cálculo do valor (sua lógica aqui)
        if tipo_cobranca == 'diaria':
            valor_total = 60 * quantidade_vagas
        else:
            tempo = saida_dt - entrada_dt
            total_minutos = tempo.total_seconds() / 60
            if total_minutos <= 60:
                valor_total = 10 * quantidade_vagas
            else:
                minutos_restantes = total_minutos - 60
                fracoes = (minutos_restantes + 29) // 30
                valor_total = (10 + (fracoes * 5)) * quantidade_vagas

        for numero in vagas_selecionadas:
            vaga = Vaga.objects.get(numero=int(numero))
            vaga.ocupada = True
            vaga.save()

            # Cria registro de entrada e saída
            EntradaVeiculo.objects.create(
                cliente=request.user,
                vaga=vaga,
                data_entrada=entrada_dt
            )
            SaidaVeiculo.objects.create(
                cliente=request.user,
                vaga=vaga,
                data_saida=saida_dt
            )

        # Salva na sessão para usar depois no pagamento, etc
        request.session['vagas'] = vagas
        request.session['tipo_cobranca'] = tipo_cobranca
        request.session['entrada'] = entrada_dt.isoformat()
        request.session['saida'] = saida_dt.isoformat()
        request.session['saida'] = saida_dt.isoformat()
        request.session['valor_total'] = valor_total

        return redirect(reverse('pagamentos:pagamento'))

    return redirect(reverse('vagas:lista_vagas'))

def liberar_vagas_expiradas():
    agora = timezone.now()
    # Busca todas as vagas que estão ocupadas
    vagas_ocupadas = Vaga.objects.filter(ocupada=True)

    for vaga in vagas_ocupadas:
        # Verifica se existe uma saída para essa vaga com data_saida menor ou igual a agora
        saida = SaidaVeiculo.objects.filter(vaga=vaga, data_saida__lte=agora).order_by('-data_saida').first()

        if saida:
            # Se saiu e a data já passou, libera a vaga
            vaga.ocupada = False
            vaga.save()

