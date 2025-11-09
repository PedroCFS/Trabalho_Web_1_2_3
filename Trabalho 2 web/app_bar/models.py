from django.db import models

class Area(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.CharField(max_length=200, default='images/default.jpg')
    
    def __str__(self):
        return self.nome

class Jogo(models.Model):
    ESTILO_CHOICES = [
        ('Sorte', 'Sorte'),
        ('Estrategia', 'Estrategia'),
        ('Cartas', 'Cartas'),
        ('Tabuleiro', 'Tabuleiro'),
    ]
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.CharField(max_length=200, default='images/jogos/default.jpg')
    estilo = models.CharField(max_length=20, choices=ESTILO_CHOICES, default='Tabuleiro')
    jogadores_min = models.IntegerField(default=2)
    jogadores_max = models.IntegerField(default=4)
    copias_totais = models.IntegerField(default=1)
    copias_disponiveis = models.IntegerField(default=1)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='jogos')
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Jogo'
        verbose_name_plural = 'Jogos'
    
    def __str__(self):
        return f"{self.nome} ({self.copias_disponiveis}/{self.copias_totais} disponíveis)"
    
    def get_jogadores_display(self):
        """Retorna string formatada com número de jogadores"""
        if self.jogadores_min == self.jogadores_max:
            return str(self.jogadores_min)
        return f"{self.jogadores_min}-{self.jogadores_max}"

class CategoriaItem(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome

class ItemCardapio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    imagem = models.CharField(max_length=200, default='images/alimentos/default.jpg')
    categoria = models.ForeignKey(CategoriaItem, on_delete=models.CASCADE)
    disponivel = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome