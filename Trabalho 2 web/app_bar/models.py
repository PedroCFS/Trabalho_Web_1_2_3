from django.db import models

class Area(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.CharField(max_length=200, default='images/default.jpg')
    
    def __str__(self):
        return self.nome

class Jogo(models.Model):
    DISPONIVEL = 'D'
    EM_USO = 'U'
    MANUTENCAO = 'M'
    
    STATUS_CHOICES = [
        (DISPONIVEL, 'Disponível'),
        (EM_USO, 'Em uso'),
        (MANUTENCAO, 'Em manutenção'),
    ]
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.CharField(max_length=200, default='images/jogos/default.jpg')
    copias_totais = models.IntegerField(default=1)
    copias_disponiveis = models.IntegerField(default=1)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DISPONIVEL)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nome} ({self.copias_disponiveis}/{self.copias_totais} disponíveis)"

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