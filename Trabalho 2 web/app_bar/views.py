from django.shortcuts import render
from .models import Area, Jogo, ItemCardapio


def index(request):
    """View para a página inicial"""
    areas = Area.objects.all()
    jogos_destaque = Jogo.objects.all()[:4]  # Primeiros 4 jogos
    cardapio_destaque = ItemCardapio.objects.all()[:4]  # Primeiros 4 itens
    
    context = {
        'areas': areas,
        'jogos': jogos_destaque,
        'cardapio': cardapio_destaque,
    }
    return render(request, 'app_bar/index.html', context)


def jogos(request):
    """View para a página de jogos com disponibilidade"""
    jogos = Jogo.objects.all().prefetch_related('disponibilidades')
    
    context = {
        'jogos': jogos,
    }
    return render(request, 'app_bar/jogos.html', context)


def cardapio(request):
    """View para a página do cardápio"""
    cardapio = ItemCardapio.objects.select_related('tipo').prefetch_related('ingredientes_items__ingrediente')
    
    context = {
        'cardapio': cardapio,
    }
    return render(request, 'app_bar/cardapio.html', context)

