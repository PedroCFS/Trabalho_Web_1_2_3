from django.shortcuts import render
from .models import Area, Jogo, CategoriaItem, ItemCardapio


def index(request):
    """View para a página inicial"""
    areas = Area.objects.all()
    jogos_destaque = Jogo.objects.all()[:4]  # Primeiros 4 jogos
    cardapio_destaque = ItemCardapio.objects.filter(disponivel=True)[:4]  # Primeiros 4 itens disponíveis
    
    context = {
        'areas': areas,
        'jogos': jogos_destaque,
        'cardapio': cardapio_destaque,
    }
    return render(request, 'app_bar/index.html', context)


def jogos(request):
    """View para a página de jogos com disponibilidade"""
    jogos = Jogo.objects.select_related('area').all().order_by('nome')
    
    context = {
        'jogos': jogos,
    }
    return render(request, 'app_bar/jogos.html', context)


def cardapio(request):
    """View para a página do cardápio"""
    cardapio = ItemCardapio.objects.filter(disponivel=True).select_related('categoria').order_by('categoria__ordem', 'nome')
    
    context = {
        'cardapio': cardapio,
    }
    return render(request, 'app_bar/cardapio.html', context)