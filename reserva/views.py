from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from reserva.forms import ReservaForm

@login_required
def reservar(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = request.user  # Associa o cliente logado
            reserva.save()

            reserva.vaga.status = 'Ocupada'
            reserva.vaga.save()

            # Enviar e-mail
            assunto = 'Confirmação de Reserva - MyParking'
            mensagem = render_to_string('reserva/email_reserva.html', {
                'reserva': reserva,
                'usuario': request.user,
            })
            send_mail(
                assunto,
                '',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                html_message=mensagem
            )

            return redirect('reserva_sucesso')
    else:
        form = ReservaForm()
    
    return render(request, 'reserva/reservar.html', {'form': form})

@login_required
def reserva_sucesso(request):
    return render(request, 'reserva/reserva_sucesso.html')

@login_required
def cancelar_reserva(request, reserva_id):
    reserva = request.user.reservas.filter(id=reserva_id).first()
    if reserva:
        reserva.delete()
    return redirect('perfil_usuario')

