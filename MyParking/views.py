from django.shortcuts import render
from vagas.models import Vaga

def home(request):
    vagas = Vaga.objects.all().order_by('numero')

    context =  {
        'vagas' :vagas
    }
    
    return render(request, 'home.html', context)

def precos_view(request):
    return render(request, 'preco/precos.html')

def contato(request):
    return render(request, 'contato/contato.html')

