from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Despesa
from .forms import DespesaForm

# Create your views here.

@login_required
def lista_despesas(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'data_compra')  # campo padrão de ordenação
    order = request.GET.get('order', 'desc')  # direção padrão

    # Inicializa o queryset
    despesas = Despesa.objects.all()

    # Aplica o filtro de pesquisa se houver query
    if query:
        despesas = despesas.filter(
            Q(descricao__icontains=query) |
            Q(fornecedor__icontains=query)
        )

    # Aplica a ordenação
    order_by = sort
    if order == 'desc':
        order_by = f'-{sort}'
    despesas = despesas.order_by(order_by)

    # Paginação
    paginator = Paginator(despesas, 10)  # 10 despesas por página
    page = request.GET.get('page')
    try:
        despesas = paginator.get_page(page)
    except PageNotAnInteger:
        despesas = paginator.get_page(1)
    except EmptyPage:
        despesas = paginator.get_page(paginator.num_pages)

    context = {
        'despesas': despesas,
        'query': query,
        'sort': sort,    # Adiciona sort ao contexto
        'order': order,  # Adiciona order ao contexto
    }
    return render(request, 'despesas/lista_despesas.html', context)

@login_required
def nova_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save()
            messages.success(request, 'Despesa cadastrada com sucesso!')
            return redirect('despesas:lista_despesas')
    else:
        form = DespesaForm()
    return render(request, 'despesas/form_despesa.html', {'form': form, 'titulo': 'Nova Despesa'})

@login_required
def editar_despesa(request, pk):
    despesa = get_object_or_404(Despesa, pk=pk)
    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Despesa atualizada com sucesso!')
            return redirect('despesas:lista_despesas')
    else:
        form = DespesaForm(instance=despesa)
    return render(request, 'despesas/form_despesa.html', {'form': form, 'titulo': 'Editar Despesa'})

@login_required
def excluir_despesa(request, pk):
    despesa = get_object_or_404(Despesa, pk=pk)
    if request.method == 'POST':
        despesa.delete()
        messages.success(request, 'Despesa excluída com sucesso!')
        return redirect('despesas:lista_despesas')
    return render(request, 'despesas/confirmar_exclusao.html', {'despesa': despesa})

@login_required
def detalhe_despesa(request, pk):
    despesa = get_object_or_404(Despesa, pk=pk)
    return render(request, 'despesas/detalhe_despesa.html', {'despesa': despesa})
