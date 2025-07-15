from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

class Produto(models.Model):
    ESTADO_CHOICES = [
        ('novo', 'Novo'),
        ('usado', 'Usado'),
        ('recondicionado', 'Recondicionado')
    ]
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    observacao = models.TextField(blank=True, verbose_name='Observação')
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço de Venda')
    preco_custo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Preço de Custo',
        null=True,
        blank=True
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='novo')
    quantidade = models.IntegerField(default=1)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_compra = models.DateField(verbose_name='Data da Compra', null=True, blank=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-data_cadastro']
