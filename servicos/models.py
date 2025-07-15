from django.db import models
from clientes.models import Cliente
from produtos.models import Produto
from decimal import Decimal

class Servico(models.Model):
    STATUS_CHOICES = [
        ('em_andamento', 'Em Andamento'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='servicos',
        verbose_name='Cliente'
    )
    data_entrada = models.DateField('Data de Entrada')
    data_saida = models.DateField('Data de Saída', null=True, blank=True)
    status = models.CharField(
        'Status do Serviço',
        max_length=20,
        choices=STATUS_CHOICES,
        default='em_andamento'
    )
    equipamento = models.CharField('Equipamento', max_length=100, null=True, blank=True)
    marca = models.CharField('Marca', max_length=50, null=True, blank=True)
    modelo = models.CharField('Modelo', max_length=50, null=True, blank=True)
    numero_serie = models.CharField('Número de Série', max_length=50, blank=True, null=True)
    descricao_problema = models.TextField('Descrição do Problema')
    servico_realizado = models.TextField('Serviço Realizado', blank=True, null=True)
    valor_servico = models.DecimalField('Valor do Serviço', max_digits=10, decimal_places=2)
    valor_pago = models.DecimalField('Valor Pago', max_digits=10, decimal_places=2, default=0)
    observacoes = models.TextField('Observações', blank=True, null=True)
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    produtos = models.ManyToManyField(Produto, through='ProdutoServico')

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['-data_entrada']

    def __str__(self):
        return f'Serviço #{self.id} - {self.cliente.nome} - {self.equipamento or "Sem equipamento"}'

    @property
    def saldo_a_pagar(self):
        return self.valor_total - self.valor_pago

    @property
    def valor_total_produtos(self):
        return sum(ps.valor_total for ps in self.produtoservico_set.all())

    @property
    def valor_total(self):
        return self.valor_servico + self.valor_total_produtos

class ProdutoServico(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField(default=1)
    valor_unitario = models.DecimalField('Valor Unitário', max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Produto do Serviço'
        verbose_name_plural = 'Produtos do Serviço'
        
    def __str__(self):
        return f'{self.produto.nome} - {self.quantidade}x'
        
    @property
    def valor_total(self):
        return self.quantidade * self.valor_unitario
