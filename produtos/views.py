from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Produto, Categoria
from .forms import ProdutoForm, CategoriaForm

def lista_produtos(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'nome')  # campo padrão de ordenação
    order = request.GET.get('order', 'asc')  # direção padrão

    # Inicializa o queryset
    produtos = Produto.objects.all()

    # Aplica o filtro de pesquisa se houver query
    if query:
        produtos = produtos.filter(
            Q(nome__icontains=query) |
            Q(descricao__icontains=query)
        )

    # Aplica a ordenação
    order_by = sort
    if order == 'desc':
        order_by = f'-{sort}'
    produtos = produtos.order_by(order_by)

    # Paginação
    paginator = Paginator(produtos, 10)  # 10 produtos por página
    page = request.GET.get('page')
    try:
        produtos = paginator.get_page(page)
    except PageNotAnInteger:
        produtos = paginator.get_page(1)
    except EmptyPage:
        produtos = paginator.get_page(paginator.num_pages)

    context = {
        'produtos': produtos,
        'query': query,
        'sort': sort,    # Adiciona sort ao contexto
        'order': order,  # Adiciona order ao contexto
    }
    return render(request, 'produtos/lista_produtos.html', context)

def detalhe_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'produtos/detalhe_produto.html', {'produto': produto})

@login_required
def novo_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.usuario = request.user
            produto.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('produtos:lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/form_produto.html', {'form': form, 'titulo': 'Novo Produto'})

@login_required
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if produto.usuario != request.user:
        messages.error(request, 'Você não tem permissão para editar este produto.')
        return redirect('produtos:lista_produtos')
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('produtos:detalhe_produto', pk=produto.pk)
    else:
        form = ProdutoForm(instance=produto)
        if produto.data_compra:
            form.initial['data_compra'] = produto.data_compra.strftime('%Y-%m-%d')
    
    return render(request, 'produtos/form_produto.html', {'form': form, 'titulo': 'Editar Produto'})

@login_required
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if produto.usuario != request.user:
        messages.error(request, 'Você não tem permissão para excluir este produto.')
        return redirect('produtos:lista_produtos')
    
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('produtos:lista_produtos')
    return render(request, 'produtos/confirmar_exclusao.html', {'produto': produto})

@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'produtos/lista_categorias.html', {'categorias': categorias})

@login_required
def nova_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('produtos:lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'produtos/form_categoria.html', {'form': form, 'titulo': 'Nova Categoria'})
