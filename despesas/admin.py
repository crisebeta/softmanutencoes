from django.contrib import admin
from .models import Despesa

@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'fornecedor', 'data_compra', 'valor', 'categoria', 'condicao')
    list_filter = ('categoria', 'condicao', 'data_compra')
    search_fields = ('descricao', 'fornecedor', 'observacoes')
    date_hierarchy = 'data_compra'
    readonly_fields = ('data_cadastro', 'data_atualizacao')
