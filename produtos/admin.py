from django.contrib import admin
from .models import Produto, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estado', 'quantidade', 'usuario')
    list_filter = ('estado', 'data_cadastro')
    search_fields = ('nome', 'descricao')
    readonly_fields = ('data_cadastro', 'ultima_atualizacao')
    date_hierarchy = 'data_cadastro'
