from django.shortcuts import render
from .models import Area, Jogo, CategoriaItem, ItemCardapio

def index(request):
    areas = Area.objects.all()
    context = {
        'areas': areas
    }
    return render(request, 'app_bar/index.html', context)

def jogos(request):
    jogos = Jogo.objects.select_related('area').all()
    areas = Area.objects.all()
    
    context = {
        'jogos': jogos,
        'areas': areas
    }
    return render(request, 'app_bar/jogos.html', context)

def cardapio(request):
    categorias = CategoriaItem.objects.prefetch_related('itemcardapio_set').all()
    
    context = {
        'categorias': categorias
    }
    return render(request, 'app_bar/cardapio.html', context)