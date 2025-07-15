from django.db import models
from django.core.validators import RegexValidator

class Cliente(models.Model):
    TIPO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica')
    ]
    
    UF_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'),
        ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    ]

    # Campos básicos
    id_cliente = models.AutoField(primary_key=True)
    tipo = models.CharField('Tipo de Cliente', max_length=2, choices=TIPO_CHOICES, default='PF')
    nome = models.CharField('Nome', max_length=200)
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    #cpf_cnpj = models.CharField('CPF/CNPJ', max_length=18, unique=True, null=True, blank=True)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=18, null=True, blank=True)
    
    # Campos de endereço
    endereco = models.CharField('Endereço', max_length=200, null=True, blank=True)
    complemento = models.CharField('Complemento', max_length=100, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=100, null=True, blank=True)
    cidade = models.CharField('Cidade', max_length=100, null=True, blank=True)
    uf = models.CharField('UF', max_length=2, choices=UF_CHOICES, null=True, blank=True)
    cep = models.CharField('CEP', max_length=9, null=True, blank=True, validators=[
        RegexValidator(
            regex=r'^\d{5}-?\d{3}$',
            message='CEP deve estar no formato 00000-000'
        )
    ])
    
    # Campos de contato
    celular = models.CharField('Celular', max_length=15, validators=[
        RegexValidator(
            regex=r'^\(\d{2}\) \d{5}-\d{4}$',
            message='Celular deve estar no formato (00) 00000-0000'
        )
    ])
    telefone = models.CharField('Telefone', max_length=14, null=True, blank=True, validators=[
        RegexValidator(
            regex=r'^\(\d{2}\) \d{4}-\d{4}$',
            message='Telefone deve estar no formato (00) 0000-0000'
        )
    ])
    email = models.EmailField('E-mail', null=True, blank=True)
    email_empresarial = models.EmailField('E-mail Empresarial', null=True, blank=True)
    rede_social = models.URLField('Rede Social', null=True, blank=True)
    
    # Campos adicionais
    observacoes = models.TextField('Observações', null=True, blank=True)
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    
    def __str__(self):
        if self.cpf_cnpj:
            return f"{self.nome} - {'CPF' if self.tipo == 'PF' else 'CNPJ'}: {self.cpf_cnpj}"
        return self.nome
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']
