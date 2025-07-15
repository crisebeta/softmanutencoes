from django.contrib import admin
from .models import Servico

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'equipamento', 'data_entrada', 'data_saida', 'status', 'valor_servico', 'valor_pago')
    list_filter = ('status', 'data_entrada', 'data_saida')
    search_fields = ('cliente__nome', 'equipamento', 'marca', 'modelo', 'numero_serie')
    date_hierarchy = 'data_entrada'
    readonly_fields = ('data_cadastro', 'data_atualizacao')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('cliente', 'data_entrada', 'data_saida', 'status')
        }),
        ('Equipamento', {
            'fields': ('equipamento', 'marca', 'modelo', 'numero_serie')
        }),
        ('Detalhes do Serviço', {
            'fields': ('descricao_problema', 'servico_realizado', 'valor_servico', 'valor_pago')
        }),
        ('Informações Adicionais', {
            'fields': ('observacoes', 'data_cadastro', 'data_atualizacao')
        }),
    )
