from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

def validar_data_nao_futura(value):
    if value > timezone.localdate():
        raise ValidationError('A data da compra não pode ser uma data futura.')

class Despesa(models.Model):
    CATEGORIA_CHOICES = [
        ('insumos', 'Insumos'),
        ('pecas', 'Peças'),
        ('produtos', 'Produtos'),
        ('servicos', 'Serviços'),
        ('outros', 'Outros'),
    ]
    
    CONDICAO_CHOICES = [
        ('novo', 'Novo'),
        ('usado', 'Usado'),
        ('recondicionado', 'Recondicionado'),
        ('nao_se_aplica', 'Não se aplica'),
    ]
    
    id_despesa = models.AutoField(primary_key=True)
    descricao = models.CharField('Descrição', max_length=200)
    fornecedor = models.CharField('Fornecedor', max_length=100)
    data_compra = models.DateField('Data da Compra', validators=[validar_data_nao_futura])
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    categoria = models.CharField(
        'Categoria',
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='insumos'
    )
    condicao = models.CharField(
        'Condição',
        max_length=20,
        choices=CONDICAO_CHOICES,
        default='novo'
    )
    observacoes = models.TextField('Observações', blank=True, null=True)
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização', auto_now=True)

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'
        ordering = ['-data_cadastro']

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor} ({self.data_compra})"
