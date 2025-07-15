from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'cpf_cnpj', 'cidade', 'uf', 'celular', 'email']
    list_filter = ['tipo', 'uf', 'cidade']
    search_fields = ['nome', 'cpf_cnpj', 'email']
    list_per_page = 20
    ordering = ['nome']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('tipo', 'nome', 'data_nascimento', 'cpf_cnpj')
        }),
        ('Endereço', {
            'fields': ('endereco', 'complemento', 'bairro', 'cidade', 'uf', 'cep')
        }),
        ('Contato', {
            'fields': ('celular', 'telefone', 'email', 'email_empresarial', 'rede_social')
        }),
        ('Informações Adicionais', {
            'fields': ('observacoes',)
        }),
    )
