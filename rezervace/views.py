from django.db.models import Value
from django.db.models.functions import Concat
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Ubytovani, Rezervace, Klient


class seznamListView(ListView):
    model = Rezervace
    context_object_name = 'rezervace_context'
    template_name = 'list/rezervace.html'

    def data(request):
        context = {
            'rezervace': Rezervace.objects.all().order_by('ubytovani','-zacatek_pobytu')
        }
        return render(request, 'list/rezervace.html', context=context)

class seznamDetailView(DetailView):
    model = Rezervace
    context_object_name = 'rezervace_context2'
    template_name = 'list/rezervace_detail.html'

    def name(request):
        jmeno = Klient.objects.annotate(fullname=Concat('name', Value(' '), 'surname'))


        out2 = {
            'jmeno':jmeno
        }
        return render(request, 'list/rezervace_detail.html', context=out2)

def index(request):
    context = {
        'nadpis': 'Ubytovací zařízení',
        'mista': Ubytovani.objects.filter(pocet_pokoju__gt = 2)
    }
    return render(request, 'index.html', context=context)
