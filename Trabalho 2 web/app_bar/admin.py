from django.contrib import admin
from .models import Area, Jogo, CategoriaItem, ItemCardapio

class JogoInline(admin.TabularInline):
    model = Jogo
    extra = 1
    fields = ['nome', 'copias_totais', 'copias_disponiveis', 'status']

class ItemCardapioInline(admin.TabularInline):
    model = ItemCardapio
    extra = 1
    fields = ['nome', 'preco', 'disponivel']

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta']
    list_filter = ['nome']
    search_fields = ['nome', 'descricao']
    inlines = [JogoInline]
    
    def descricao_curta(self, obj):
        return obj.descricao[:50] + '...' if len(obj.descricao) > 50 else obj.descricao
    descricao_curta.short_description = 'Descrição'

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'area', 'copias_disponiveis', 'copias_totais', 'status']
    list_filter = ['area', 'status']
    search_fields = ['nome', 'descricao']
    list_editable = ['copias_disponiveis', 'status']

@admin.register(CategoriaItem)
class CategoriaItemAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ordem', 'quantidade_itens']
    list_editable = ['ordem']
    inlines = [ItemCardapioInline]
    
    def quantidade_itens(self, obj):
        return obj.itemcardapio_set.count()
    quantidade_itens.short_description = 'Itens no Cardápio'

@admin.register(ItemCardapio)
class ItemCardapioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'disponivel']
    list_filter = ['categoria', 'disponivel']
    search_fields = ['nome', 'descricao']
    list_editable = ['preco', 'disponivel']