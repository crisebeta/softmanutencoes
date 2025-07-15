from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Cliente
from servicos.models import Servico
from .forms import ClienteForm

# Create your views here.

@login_required
def lista_clientes(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'nome')  # campo padrão de ordenação
    order = request.GET.get('order', 'asc')  # direção padrão

    # Inicializa o queryset
    clientes = Cliente.objects.all()

    # Aplica o filtro de pesquisa se houver query
    if query:
        clientes = clientes.filter(
            Q(nome__icontains=query) |
            Q(cidade__icontains=query) |
            Q(email__icontains=query) |
            Q(celular__icontains=query)
        )

    # Aplica a ordenação
    order_by = sort
    if order == 'desc':
        order_by = f'-{sort}'
    clientes = clientes.order_by(order_by)

    # Paginação
    paginator = Paginator(clientes, 10)  # 10 clientes por página
    page = request.GET.get('page')
    try:
        clientes = paginator.get_page(page)
    except PageNotAnInteger:
        clientes = paginator.get_page(1)
    except EmptyPage:
        clientes = paginator.get_page(paginator.num_pages)

    context = {
        'clientes': clientes,
        'query': query,
        'sort': sort,    # Adiciona sort ao contexto
        'order': order,  # Adiciona order ao contexto
    }
    return render(request, 'clientes/lista_clientes.html', context)

@login_required
def detalhe_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    servicos = Servico.objects.filter(cliente=cliente).order_by('-data_entrada')
    
    context = {
        'cliente': cliente,
        'servicos': servicos,
    }
    return render(request, 'clientes/detalhe_cliente.html', context)

@login_required
def novo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('clientes:detalhe_cliente', pk=cliente.pk)
    else:
        form = ClienteForm()
    return render(request, 'clientes/form_cliente.html', {'form': form, 'titulo': 'Novo Cliente'})

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('clientes:detalhe_cliente', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/form_cliente.html', {'form': form, 'titulo': 'Editar Cliente'})

@login_required
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('clientes:lista_clientes')
    return render(request, 'clientes/confirmar_exclusao.html', {'cliente': cliente})
