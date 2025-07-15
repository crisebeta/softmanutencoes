from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count, Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Servico, ProdutoServico
from produtos.models import Produto
from .forms import ServicoForm, ProdutoServicoForm
from django.db.models.functions import ExtractYear, ExtractMonth
from despesas.models import Despesa
from datetime import datetime
import json
from django.db import transaction
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Create your views here.

@login_required
def lista_servicos(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    sort = request.GET.get('sort', 'data_entrada')  # campo padrão de ordenação
    order = request.GET.get('order', 'desc')  # direção padrão

    # Inicializa o queryset
    servicos = Servico.objects.all()

    # Aplica os filtros
    if query:
        servicos = servicos.filter(
            Q(cliente__nome__icontains=query) |
            Q(equipamento__icontains=query) |
            Q(marca__icontains=query)
        )
    
    if status:
        servicos = servicos.filter(status=status)

    # Aplica a ordenação
    order_by = sort
    if order == 'desc':
        order_by = f'-{sort}'
    servicos = servicos.order_by(order_by)

    # Paginação
    paginator = Paginator(servicos, 10)
    page = request.GET.get('page')
    try:
        servicos = paginator.get_page(page)
    except PageNotAnInteger:
        servicos = paginator.get_page(1)
    except EmptyPage:
        servicos = paginator.get_page(paginator.num_pages)

    context = {
        'servicos': servicos,
        'query': query,
        'status_atual': status,
        'status_choices': Servico.STATUS_CHOICES,
        'sort': sort,    # Adiciona sort ao contexto
        'order': order,  # Adiciona order ao contexto
    }
    return render(request, 'servicos/lista_servicos.html', context)

@login_required
def detalhe_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    return render(request, 'servicos/detalhe_servico.html', {'servico': servico})

@login_required
def novo_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    servico = form.save()
                    
                    # Processa os produtos
                    produtos_data = request.POST.getlist('produtos[][produto]')
                    quantidades = request.POST.getlist('produtos[][quantidade]')
                    valores = request.POST.getlist('produtos[][valor_unitario]')
                    
                    for i in range(len(produtos_data)):
                        if produtos_data[i]:  # Se um produto foi selecionado
                            ProdutoServico.objects.create(
                                servico=servico,
                                produto_id=produtos_data[i],
                                quantidade=quantidades[i],
                                valor_unitario=valores[i]
                            )
                    
                    messages.success(request, 'Serviço cadastrado com sucesso!')
                    return redirect('servicos:lista_servicos')
            except Exception as e:
                messages.error(request, f'Erro ao salvar o serviço: {str(e)}')
    else:
        form = ServicoForm()
    
    produtos = Produto.objects.all()
    return render(request, 'servicos/form_servico.html', {
        'form': form,
        'titulo': 'Novo Serviço',
        'produtos': produtos
    })

@login_required
def editar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            try:
                with transaction.atomic():
                    servico = form.save()
                    
                    # Remove produtos existentes
                    ProdutoServico.objects.filter(servico=servico).delete()
                    
                    # Processa os novos produtos
                    produtos_data = request.POST.getlist('produtos[][produto]')
                    quantidades = request.POST.getlist('produtos[][quantidade]')
                    valores = request.POST.getlist('produtos[][valor_unitario]')
                    
                    for i in range(len(produtos_data)):
                        if produtos_data[i]:  # Se um produto foi selecionado
                            ProdutoServico.objects.create(
                                servico=servico,
                                produto_id=produtos_data[i],
                                quantidade=quantidades[i],
                                valor_unitario=valores[i]
                            )
                    
                    messages.success(request, 'Serviço atualizado com sucesso!')
                    return redirect('servicos:lista_servicos')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar o serviço: {str(e)}')
    else:
        form = ServicoForm(instance=servico)
    
    produtos = Produto.objects.all()
    produtos_servico = ProdutoServico.objects.filter(servico=servico)
    
    return render(request, 'servicos/form_servico.html', {
        'form': form,
        'titulo': 'Editar Serviço',
        'servico': servico,
        'produtos': produtos,
        'produtos_servico': produtos_servico
    })

@login_required
def excluir_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        servico.delete()
        messages.success(request, 'Serviço excluído com sucesso!')
        return redirect('servicos:lista_servicos')
    return render(request, 'servicos/confirmar_exclusao.html', {'servico': servico})

def dashboard(request):
    # Obtém o ano selecionado do request, ou usa o ano atual como padrão
    ano_selecionado = int(request.GET.get('ano', datetime.now().year))
    
    # Define as datas padrão (primeiro e último dia do ano selecionado)
    data_inicio_padrao = f"{ano_selecionado}-01-01"
    data_fim_padrao = f"{ano_selecionado}-12-31"
    
    # Obtém as datas do request ou usa as datas padrão
    data_inicio = request.GET.get('data_inicio', data_inicio_padrao)
    data_fim = request.GET.get('data_fim', data_fim_padrao)
    
    # Query base para serviços
    servicos_query = Servico.objects.annotate(
        ano=ExtractYear('data_entrada')
    ).filter(ano=ano_selecionado)
    
    # Se houver filtro de período
    if data_inicio and data_fim:
        servicos_query = servicos_query.filter(data_entrada__range=[data_inicio, data_fim])
    
    # 1. Dados para o gráfico de pizza (Serviços vs Despesas)
    total_servicos = servicos_query.aggregate(total=Sum('valor_pago'))['total'] or 0
    total_despesas = Despesa.objects.filter(
        data_compra__range=[data_inicio, data_fim]
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    # 2. Dados para o gráfico de colunas (valor total por mês)
    valores_mensais = servicos_query.annotate(
        mes=ExtractMonth('data_entrada')
    ).values('mes').annotate(
        total=Sum('valor_pago')
    ).order_by('mes')
    
    # 3. Dados para o gráfico de colunas (valor total por ano)
    valores_anuais = Servico.objects.annotate(
        ano=ExtractYear('data_entrada')
    ).values('ano').annotate(
        total=Sum('valor_pago')
    ).order_by('ano')
    
    # 4. Dados para o ticket médio mensal
    ticket_medio_mensal = servicos_query.annotate(
        mes=ExtractMonth('data_entrada')
    ).values('mes').annotate(
        media=Avg('valor_pago')
    ).order_by('mes')
    
    # 5. Dados para quantidade de atendimentos por cliente (top 10)
     # 5. Dados para quantidade de atendimentos por cliente (top 10) - TODOS OS PERÍODOS
    atendimentos_cliente = Servico.objects.values(
        'cliente__nome'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:10]  # Limita aos 10 primeiros 
    
    # 6. Dados para Serviços vs Despesas de todos os períodos
    total_servicos_geral = Servico.objects.aggregate(total=Sum('valor_pago'))['total'] or 0
    total_despesas_geral = Despesa.objects.aggregate(total=Sum('valor'))['total'] or 0
    
    servicos_despesas_total = [{
        'servicos': float(total_servicos_geral),
        'despesas': float(total_despesas_geral)
    }]
    
    # Lista de anos para o seletor
    anos_servicos = set(Servico.objects.annotate(
        ano=ExtractYear('data_entrada')
    ).values_list('ano', flat=True))
    
    anos_despesas = set(Despesa.objects.annotate(
        ano=ExtractYear('data_compra')
    ).values_list('ano', flat=True))
    
    # Combina os anos de serviços e despesas e ordena
    anos_disponiveis = sorted(list(anos_servicos.union(anos_despesas)))
    
    # Convertendo Decimal para float para serialização JSON
    context = {
        'ano_selecionado': ano_selecionado,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'anos_disponiveis': anos_disponiveis,
        'dados_pizza': {
            'servicos': float(total_servicos),
            'despesas': float(total_despesas)
        },
        'valores_mensais': [
            {'mes': item['mes'], 'total': float(item['total'])}
            for item in valores_mensais
        ],
        'valores_anuais': [
            {'ano': item['ano'], 'total': float(item['total'])}
            for item in valores_anuais
        ],
        'ticket_medio_mensal': [
            {'mes': item['mes'], 'media': float(item['media'])}
            for item in ticket_medio_mensal
        ],
        'atendimentos_cliente': [
            {'cliente__nome': item['cliente__nome'], 'total': int(item['total'])}
            for item in atendimentos_cliente
        ],
        'servicos_despesas_total': servicos_despesas_total
    }
    
    return render(request, 'servicos/dashboard.html', context)

@login_required
def gerar_pdf_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    
    # Criar o response com content_type PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="servico_{servico.pk}.pdf"'
    
    # Criar o documento PDF com margens personalizadas menores
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=30,  # Reduzido de 50 para 30
        leftMargin=30,   # Reduzido de 50 para 30
        topMargin=30,    # Reduzido de 50 para 30
        bottomMargin=30  # Reduzido de 50 para 30
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para título com menos espaçamento
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,     # Reduzido de 24 para 20
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=15,   # Reduzido de 30 para 15
        alignment=1
    )
    
    # Estilo para subtítulos com menos espaçamento
    subtitulo_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=12,     # Reduzido de 14 para 12
        textColor=colors.HexColor('#34495E'),
        spaceBefore=10,  # Reduzido de 15 para 10
        spaceAfter=5    # Reduzido de 10 para 5
    )
    
    # Estilo para texto normal
    texto_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2C3E50')
    )
    
    # Cabeçalho com título e número do serviço
    title = Paragraph(f"Ordem de Serviço #{servico.pk}", titulo_style)
    elements.append(title)
    
    # Função auxiliar para criar seções de informação
    def criar_secao_info(titulo, dados, larguras=None):
        elements.append(Paragraph(titulo, subtitulo_style))
        if not larguras:
            larguras = [500]  # Aumentado de 400 para 500
        
        t = Table(dados, colWidths=larguras)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Reduzido de 11 para 10
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),  # Reduzido de 12 para 8
            ('TOPPADDING', (0, 0), (-1, -1), 8),     # Reduzido de 12 para 8
            ('LEFTPADDING', (0, 0), (-1, -1), 10),   # Reduzido de 15 para 10
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Reduzido de 15 para 10
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E9ECEF')),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#F8F9FA'), colors.HexColor('#FFFFFF')]),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 8))
    
    # Informações do Cliente com telefone e email na mesma linha
    cliente_info = [
        [Paragraph(f"<b>Cliente:</b> {servico.cliente.nome}", texto_style)],
        [
            Paragraph(f"<b>Telefone:</b> {servico.cliente.celular}", texto_style),
            Paragraph(f"<b>Email:</b> {servico.cliente.email}", texto_style)
        ]
    ]
    criar_secao_info("Informações do Cliente", cliente_info, [250, 250])
    
    # Datas na mesma linha
    data_saida = servico.data_saida.strftime('%d/%m/%Y') if servico.data_saida else 'Não definida'
    datas_info = [
        [
            Paragraph(f"<b>Data de Entrada:</b> {servico.data_entrada.strftime('%d/%m/%Y')}", texto_style),
            Paragraph(f"<b>Data de Saída:</b> {data_saida}", texto_style)
        ]
    ]
    criar_secao_info("Datas", datas_info, [250, 250])
    
    # Informações do Equipamento com marca, modelo e número de série na mesma linha
    equip_info = [
        [Paragraph(f"<b>Equipamento:</b> {servico.equipamento}", texto_style)],
        [
            Paragraph(f"<b>Marca:</b> {servico.marca}", texto_style),
            Paragraph(f"<b>Modelo:</b> {servico.modelo}", texto_style),
            Paragraph(f"<b>Nº Série:</b> {servico.numero_serie or 'Não informado'}", texto_style)
        ]
    ]
    criar_secao_info("Informações do Equipamento", equip_info, [170, 170, 160])
    
    # Descrições
    elements.append(Paragraph("Descrição do Problema", subtitulo_style))
    elements.append(Paragraph(servico.descricao_problema, texto_style))
    elements.append(Spacer(1, 10))  # Reduzido de 20 para 10
    
    if servico.servico_realizado:
        elements.append(Paragraph("Serviço Realizado", subtitulo_style))
        elements.append(Paragraph(servico.servico_realizado, texto_style))
        elements.append(Spacer(1, 10))  # Reduzido de 20 para 10
    
    # Produtos utilizados (nova seção)
    if servico.produtoservico_set.exists():
        elements.append(Paragraph("Produtos Utilizados", subtitulo_style))
        produtos_headers = [
            "Produto",
            "Quantidade",
            "Valor Unit.",
            "Total"
        ]
        produtos_data = [produtos_headers]
        
        for produto_servico in servico.produtoservico_set.all():
            produtos_data.append([
                produto_servico.produto.nome,
                str(produto_servico.quantidade),
                f"R$ {produto_servico.valor_unitario:.2f}",
                f"R$ {produto_servico.valor_total:.2f}"
            ])
        
        t = Table(produtos_data, colWidths=[250, 80, 85, 85])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E2E8F0')),  # Cabeçalho
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Cabeçalho em negrito
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E9ECEF')),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 10))
    
    # Valores (ajustado para maior largura)
    elements.append(Paragraph("Valores", subtitulo_style))
    valores_data = [
        ["Valor do Serviço", f"R$ {servico.valor_servico:.2f}"],
        ["Valor dos Produtos", f"R$ {servico.valor_total_produtos:.2f}"],
        ["Valor Total", f"R$ {servico.valor_total:.2f}"],
        ["Valor Pago", f"R$ {servico.valor_pago:.2f}"],
        ["Saldo a Pagar", f"R$ {servico.saldo_a_pagar:.2f}"]
    ]
    t = Table(valores_data, colWidths=[250, 250])  # Aumentado de 200 para 250
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Reduzido de 11 para 10
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),  # Reduzido de 12 para 8
        ('TOPPADDING', (0, 0), (-1, -1), 8),     # Reduzido de 12 para 8
        ('LEFTPADDING', (0, 0), (-1, -1), 10),   # Reduzido de 15 para 10
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Reduzido de 15 para 10
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E9ECEF')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#FEF9C3' if servico.saldo_a_pagar > 0 else '#DEF7EC')),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(t)
    
    # Rodapé com data de geração
    elements.append(Spacer(1, 15))  # Reduzido de 30 para 15
    data_geracao = datetime.now().strftime('%d/%m/%Y %H:%M')
    rodape_style = ParagraphStyle(
        'Rodape',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#94A3B8'),
        alignment=1  # Centralizado
    )
    elements.append(Paragraph(f"Documento gerado em {data_geracao}", rodape_style))
    
    # Gerar PDF
    doc.build(elements)
    return response
