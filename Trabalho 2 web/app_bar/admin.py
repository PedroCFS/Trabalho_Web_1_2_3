from django.contrib import admin
from .models import Area, Jogo, CategoriaItem, ItemCardapio
class JogoInline(admin.TabularInline):
    """Inline para adicionar jogos diretamente na área"""
    model = Jogo
    extra = 1
    fields = ['nome', 'estilo', 'jogadores_min', 'jogadores_max', 'copias_totais', 'copias_disponiveis', 'imagem']
    verbose_name = 'Jogo'
    verbose_name_plural = 'Jogos'
class ItemCardapioInline(admin.TabularInline):
    """Inline para adicionar itens do cardápio diretamente na categoria"""
    model = ItemCardapio
    extra = 1
    fields = ['nome', 'descricao', 'preco', 'disponivel', 'imagem']
    verbose_name = 'Item do Cardápio'
    verbose_name_plural = 'Itens do Cardápio'
@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    """Admin customizado para Áreas"""
    list_display = ['nome', 'descricao_curta', 'quantidade_jogos']
    list_filter = ['nome']
    search_fields = ['nome', 'descricao']
    fields = ['nome', 'descricao', 'imagem']
    
    def descricao_curta(self, obj):
        return obj.descricao[:50] + '...' if len(obj.descricao) > 50 else obj.descricao
    descricao_curta.short_description = 'Descrição'
    
    def quantidade_jogos(self, obj):
        return obj.jogos.count()
    quantidade_jogos.short_description = 'Quantidade de Jogos'
@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    """Admin customizado para Jogos com funcionalidade de disponibilidade"""
    list_display = ['nome', 'area', 'estilo', 'jogadores_display', 'copias_disponiveis', 'copias_totais', 'disponibilidade_status']
    list_filter = ['area', 'estilo']
    search_fields = ['nome', 'descricao']
    list_editable = ['copias_disponiveis']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'area', 'estilo')
        }),
        ('Jogadores', {
            'fields': ('jogadores_min', 'jogadores_max')
        }),
        ('Disponibilidade', {
            'fields': ('copias_totais', 'copias_disponiveis')
        }),
        ('Imagem', {
            'fields': ('imagem',)
        }),
    )
    
    def jogadores_display(self, obj):
        return obj.get_jogadores_display()
    jogadores_display.short_description = 'Jogadores'
    
    def disponibilidade_status(self, obj):
        if obj.copias_disponiveis > 0:
            return f"✅ {obj.copias_disponiveis} disponível(eis)"
        return "❌ Indisponível"
    disponibilidade_status.short_description = 'Status'
@admin.register(CategoriaItem)
class CategoriaItemAdmin(admin.ModelAdmin):
    """Admin customizado para Categorias de Itens do Cardápio"""
    list_display = ['nome', 'ordem', 'quantidade_itens']
    list_editable = ['ordem']
    list_filter = ['ordem']
    search_fields = ['nome']
    ordering = ['ordem', 'nome']
    
    def quantidade_itens(self, obj):
        count = obj.itemcardapio_set.count()
        disponiveis = obj.itemcardapio_set.filter(disponivel=True).count()
        return f"{disponiveis}/{count} disponíveis"
    quantidade_itens.short_description = 'Itens no Cardápio'
@admin.register(ItemCardapio)
class ItemCardapioAdmin(admin.ModelAdmin):
    """Admin customizado para Itens do Cardápio"""
    list_display = ['nome', 'preco', 'categoria', 'preco_formatado', 'disponivel']
    list_filter = ['categoria', 'disponivel']
    search_fields = ['nome', 'descricao']
    list_editable = ['preco', 'disponivel']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'categoria')
        }),
        ('Preço e Disponibilidade', {
            'fields': ('preco', 'disponivel')
        }),
        ('Imagem', {
            'fields': ('imagem',)
        }),
    )
    
    def preco_formatado(self, obj):
        return f"R$ {obj.preco:.2f}"
    preco_formatado.short_description = 'Preço'