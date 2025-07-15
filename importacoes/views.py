from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from clientes.models import Cliente
from servicos.models import Servico
from despesas.models import Despesa
from django.db import IntegrityError
from datetime import datetime

# Create your views here.

@login_required
def importar_clientes(request):
    if request.method == 'POST':
        arquivo_json = request.FILES.get('arquivo')
        if not arquivo_json:
            messages.error(request, 'Por favor, selecione um arquivo JSON para importar.')
            return redirect('importacoes:importacoes')
        
        if not arquivo_json.name.endswith('.json'):
            messages.error(request, 'Por favor, selecione um arquivo JSON válido.')
            return redirect('importacoes:importacoes')
        
        try:
            # Decodifica o arquivo JSON
            conteudo = arquivo_json.read().decode('utf-8')
            dados_json = json.loads(conteudo)
            
            # Contador de clientes importados
            clientes_importados = 0
            clientes_atualizados = 0
            clientes_ignorados = 0
            erros = []
            
            # Procura pela lista de dados dos clientes no JSON
            dados_clientes = None
            for item in dados_json:
                if isinstance(item, dict) and item.get('type') == 'table' and item.get('name') == 'clientes':
                    dados_clientes = item.get('data', [])
                    break
            
            if not dados_clientes:
                messages.error(request, 'Estrutura do arquivo JSON inválida ou sem dados de clientes.')
                return redirect('importacoes:importacoes')
            
            total_registros = len(dados_clientes)
            messages.info(request, f'Iniciando importação de {total_registros} registros...')
            
            # Processa cada cliente
            for i, cliente_json in enumerate(dados_clientes, 1):
                # Mapeamento dos campos do JSON para os campos do modelo
                dados_cliente = {
                    'nome': cliente_json.get('nome_cliente', '').strip(),
                    'telefone': cliente_json.get('campo_fixo', '').strip(),
                    'celular': cliente_json.get('campo_celular', '').strip(),
                    'email': cliente_json.get('email', '').strip(),
                    'cpf_cnpj': cliente_json.get('campo_cpf', '').strip(),
                    'cep': cliente_json.get('cep', '').strip(),
                    'endereco': cliente_json.get('endereco', '').strip(),
                    'complemento': cliente_json.get('numero', '').strip(),
                    'bairro': cliente_json.get('bairro', '').strip(),
                    'cidade': cliente_json.get('cidade', '').strip(),
                    'uf': cliente_json.get('uf', '').strip()
                }
                
                if not dados_cliente['nome']:
                    clientes_ignorados += 1
                    erros.append(f'Registro {i}: Nome vazio')
                    continue

                try:
                    # Remove espaços extras do nome
                    nome = dados_cliente['nome'].strip()
                    if not nome:
                        clientes_ignorados += 1
                        erros.append(f'Registro {i}: Nome contém apenas espaços')
                        continue

                    # Verifica se já existe um cliente com o mesmo CPF/CNPJ
                    cpf_cnpj = dados_cliente.get('cpf_cnpj')
                    cliente_existente = None
                    
                    if cpf_cnpj:
                        try:
                            cliente_existente = Cliente.objects.get(cpf_cnpj=cpf_cnpj)
                        except Cliente.DoesNotExist:
                            pass
                    
                    if cliente_existente:
                        # Atualiza o cliente existente
                        for campo, valor in dados_cliente.items():
                            setattr(cliente_existente, campo, valor)
                        cliente_existente.save()
                        clientes_atualizados += 1
                    else:
                        # Tenta criar um novo cliente
                        try:
                            cliente = Cliente.objects.create(**dados_cliente)
                            clientes_importados += 1
                        except IntegrityError:
                            # Se der erro de integridade, remove o CPF/CNPJ e tenta criar
                            dados_cliente['cpf_cnpj'] = ''
                            cliente = Cliente.objects.create(**dados_cliente)
                            clientes_importados += 1
                            erros.append(f'Registro {i}: Cliente importado sem CPF/CNPJ devido a duplicidade')
                        
                except Exception as e:
                    clientes_ignorados += 1
                    erros.append(f'Registro {i}: Erro ao processar - {str(e)}')
            
            # Exibe mensagem principal
            mensagem = f'Importação concluída: {clientes_importados} novos clientes, {clientes_atualizados} atualizados'
            if clientes_ignorados > 0:
                mensagem += f', {clientes_ignorados} ignorados'
            messages.success(request, mensagem)
            
            # Exibe detalhes dos erros
            if erros:
                messages.warning(request, 'Detalhes dos registros ignorados:')
                for erro in erros[:10]:  # Mostra apenas os 10 primeiros erros
                    messages.warning(request, erro)
                if len(erros) > 10:
                    messages.warning(request, f'... e mais {len(erros) - 10} erros')
            
        except json.JSONDecodeError:
            messages.error(request, 'Erro ao decodificar o arquivo JSON. Verifique se o formato está correto.')
        except Exception as e:
            messages.error(request, f'Erro ao importar clientes: {str(e)}')
            
        return redirect('importacoes:importacoes')
    
    return redirect('importacoes:importacoes')

@login_required
def importar_servicos(request):
    if request.method == 'POST':
        arquivo_clientes = request.FILES.get('arquivo_clientes')
        arquivo_servicos = request.FILES.get('arquivo_servicos')
        
        if not arquivo_clientes or not arquivo_servicos:
            messages.error(request, 'Por favor, selecione ambos os arquivos JSON (clientes e serviços).')
            return redirect('importacoes:importacoes')
        
        if not arquivo_clientes.name.endswith('.json') or not arquivo_servicos.name.endswith('.json'):
            messages.error(request, 'Por favor, selecione arquivos JSON válidos.')
            return redirect('importacoes:importacoes')
        
        try:
            # Primeiro, tenta carregar o arquivo de clientes
            try:
                conteudo_clientes = arquivo_clientes.read().decode('utf-8-sig')  # Trata BOM se existir
                dados_clientes_json = json.loads(conteudo_clientes)
            except UnicodeDecodeError:
                messages.error(request, 'Erro ao decodificar o arquivo de clientes. Verifique se está no formato UTF-8.')
                return redirect('importacoes:importacoes')
            except json.JSONDecodeError as e:
                messages.error(request, f'Erro no arquivo de clientes: {str(e)}. Verifique se o formato JSON está correto.')
                return redirect('importacoes:importacoes')
            
            # Tenta carregar o arquivo de serviços
            try:
                conteudo_servicos = arquivo_servicos.read().decode('utf-8-sig')  # Trata BOM se existir
                dados_servicos_json = json.loads(conteudo_servicos)
            except UnicodeDecodeError:
                messages.error(request, 'Erro ao decodificar o arquivo de serviços. Verifique se está no formato UTF-8.')
                return redirect('importacoes:importacoes')
            except json.JSONDecodeError as e:
                messages.error(request, f'Erro no arquivo de serviços: {str(e)}. Verifique se o formato JSON está correto.')
                return redirect('importacoes:importacoes')
            
            # Cria um dicionário de mapeamento id_antigo -> nome_cliente
            mapeamento_clientes = {}
            clientes_encontrados = False
            
            for item in dados_clientes_json:
                if isinstance(item, dict) and item.get('type') == 'table' and item.get('name') == 'clientes':
                    clientes_encontrados = True
                    for cliente in item.get('data', []):
                        id_antigo = cliente.get('id')
                        nome_cliente = cliente.get('nome_cliente', '').strip()
                        if id_antigo and nome_cliente:
                            mapeamento_clientes[id_antigo] = nome_cliente
            
            if not clientes_encontrados:
                messages.error(request, 'O arquivo de clientes não contém a estrutura esperada. Verifique se é o arquivo correto.')
                return redirect('importacoes:importacoes')
            
            if not mapeamento_clientes:
                messages.error(request, 'Nenhum cliente encontrado no arquivo de clientes.')
                return redirect('importacoes:importacoes')
            
            # Procura pela lista de dados dos serviços
            dados_servicos = None
            servicos_encontrados = False
            
            for item in dados_servicos_json:
                if isinstance(item, dict) and item.get('type') == 'table' and item.get('name') == 'servicos':
                    servicos_encontrados = True
                    dados_servicos = item.get('data', [])
                    break
            
            if not servicos_encontrados:
                messages.error(request, 'O arquivo de serviços não contém a estrutura esperada. Verifique se é o arquivo correto.')
                return redirect('importacoes:importacoes')
            
            if not dados_servicos:
                messages.error(request, 'Nenhum serviço encontrado no arquivo.')
                return redirect('importacoes:importacoes')
            
            # Contadores
            servicos_importados = 0
            servicos_ignorados = 0
            erros = []
            
            total_registros = len(dados_servicos)
            messages.info(request, f'Iniciando importação de {total_registros} registros...')
            
            # Processa cada serviço
            for i, servico_json in enumerate(dados_servicos, 1):
                try:
                    # Busca o cliente pelo ID antigo no mapeamento
                    fkcliente = servico_json.get('fkcliente')
                    nome_cliente = mapeamento_clientes.get(fkcliente)
                    
                    if not nome_cliente:
                        servicos_ignorados += 1
                        erros.append(f'Registro {i}: Cliente com ID {fkcliente} não encontrado no arquivo de clientes')
                        continue
                    
                    try:
                        cliente = Cliente.objects.get(nome=nome_cliente)
                    except Cliente.DoesNotExist:
                        servicos_ignorados += 1
                        erros.append(f'Registro {i}: Cliente "{nome_cliente}" não encontrado no banco de dados')
                        continue
                    
                    # Converte as datas
                    try:
                        data_entrada = datetime.strptime(servico_json.get('dataentrada', ''), '%Y-%m-%d').date() if servico_json.get('dataentrada') else None
                        data_saida = datetime.strptime(servico_json.get('datasaida', ''), '%Y-%m-%d').date() if servico_json.get('datasaida') else None
                    except ValueError as e:
                        servicos_ignorados += 1
                        erros.append(f'Registro {i}: Erro no formato da data - {str(e)}')
                        continue
                    
                    # Mapeamento dos campos do JSON para os campos do modelo
                    dados_servico = {
                        'cliente': cliente,
                        'data_entrada': data_entrada,
                        'data_saida': data_saida,
                        'descricao_problema': servico_json.get('defeito', '').strip(),
                        'equipamento': servico_json.get('equipamento', '').strip(),
                        'marca': servico_json.get('marca', '').strip(),
                        'modelo': servico_json.get('modelo', '').strip(),
                        'numero_serie': servico_json.get('nserie', '').strip(),
                        'servico_realizado': servico_json.get('servico', '').strip(),
                        'observacoes': servico_json.get('observacao', '').strip(),
                        'valor_servico': float(servico_json.get('valorservico', 0)),
                        'valor_pago': float(servico_json.get('valorpago', 0))
                    }
                    
                    # Define o status com base no valor pago
                    if float(servico_json.get('valorpago', 0)) > 0:
                        dados_servico['status'] = 'finalizado'  # Finalizado
                    else:
                        dados_servico['status'] = 'em_andamento'  # Em Andamento
                    
                    # Cria o serviço
                    servico = Servico.objects.create(**dados_servico)
                    servicos_importados += 1
                        
                except ValueError as e:
                    servicos_ignorados += 1
                    erros.append(f'Registro {i}: Erro ao converter valor numérico - {str(e)}')
                except Exception as e:
                    servicos_ignorados += 1
                    erros.append(f'Registro {i}: Erro ao processar - {str(e)}')
            
            # Exibe mensagem principal
            mensagem = f'Importação concluída: {servicos_importados} serviços importados'
            if servicos_ignorados > 0:
                mensagem += f', {servicos_ignorados} ignorados'
            messages.success(request, mensagem)
            
            # Exibe detalhes dos erros
            if erros:
                messages.warning(request, 'Detalhes dos registros ignorados:')
                for erro in erros[:10]:  # Mostra apenas os 10 primeiros erros
                    messages.warning(request, erro)
                if len(erros) > 10:
                    messages.warning(request, f'... e mais {len(erros) - 10} erros')
            
        except Exception as e:
            messages.error(request, f'Erro inesperado ao importar: {str(e)}')
            
        return redirect('importacoes:importacoes')
    
    return redirect('importacoes:importacoes')

@login_required
def importar_despesas(request):
    if request.method == 'POST':
        arquivo_json = request.FILES.get('arquivo_pecas')
        if not arquivo_json:
            messages.error(request, 'Por favor, selecione o arquivo JSON para importar.')
            return redirect('importacoes:importacoes')
        
        if not arquivo_json.name.endswith('.json'):
            messages.error(request, 'Por favor, selecione um arquivo JSON válido.')
            return redirect('importacoes:importacoes')
        
        try:
            # Decodifica o arquivo JSON
            conteudo = arquivo_json.read().decode('utf-8-sig')  # Trata BOM se existir
            dados_json = json.loads(conteudo)
            
            # Contadores
            despesas_importadas = 0
            despesas_ignoradas = 0
            erros = []
            
            # Procura pela lista de dados das peças
            dados_pecas = None
            for item in dados_json:
                if isinstance(item, dict) and item.get('type') == 'table' and item.get('name') == 'pecas':
                    dados_pecas = item.get('data', [])
                    break
            
            if not dados_pecas:
                messages.error(request, 'Estrutura do arquivo JSON inválida ou sem dados de peças.')
                return redirect('importacoes:importacoes')
            
            total_registros = len(dados_pecas)
            messages.info(request, f'Iniciando importação de {total_registros} registros...')
            
            # Processa cada peça
            for i, peca_json in enumerate(dados_pecas, 1):
                try:
                    # Prepara as informações adicionais para o campo observações
                    info_adicional = []
                    if peca_json.get('marca'):
                        info_adicional.append(f"Marca: {peca_json['marca']}")
                    if peca_json.get('modelo'):
                        info_adicional.append(f"Modelo: {peca_json['modelo']}")
                    if peca_json.get('nserie'):
                        info_adicional.append(f"N. de série: {peca_json['nserie']}")
                    
                    # Combina as observações originais com as informações adicionais
                    observacoes = peca_json.get('observacao', '').strip()
                    if info_adicional:
                        if observacoes:
                            observacoes += " - "
                        observacoes += ", ".join(info_adicional)
                    
                    # Converte a data
                    try:
                        data_compra = datetime.strptime(peca_json.get('datacompra', ''), '%Y-%m-%d').date() if peca_json.get('datacompra') and peca_json.get('datacompra') != '0000-00-00' else None
                    except ValueError:
                        data_compra = None
                    
                    # Converte o valor
                    try:
                        valor = float(peca_json.get('valor', 0))
                    except ValueError:
                        valor = 0
                    
                    # Mapeamento dos campos do JSON para os campos do modelo
                    dados_despesa = {
                        'descricao': peca_json.get('descricao', '').strip(),
                        'fornecedor': peca_json.get('fornecedor', '').strip(),
                        'data_compra': data_compra,
                        'valor': valor,
                        'condicao': peca_json.get('condicao', '').strip(),
                        'observacoes': observacoes
                    }
                    
                    # Cria a despesa
                    if dados_despesa['descricao']:  # Só importa se tiver descrição
                        despesa = Despesa.objects.create(**dados_despesa)
                        despesas_importadas += 1
                    else:
                        despesas_ignoradas += 1
                        erros.append(f'Registro {i}: Despesa sem descrição')
                        
                except Exception as e:
                    despesas_ignoradas += 1
                    erros.append(f'Registro {i}: Erro ao processar - {str(e)}')
            
            # Exibe mensagem principal
            mensagem = f'Importação concluída: {despesas_importadas} despesas importadas'
            if despesas_ignoradas > 0:
                mensagem += f', {despesas_ignoradas} ignoradas'
            messages.success(request, mensagem)
            
            # Exibe detalhes dos erros
            if erros:
                messages.warning(request, 'Detalhes dos registros ignorados:')
                for erro in erros[:10]:  # Mostra apenas os 10 primeiros erros
                    messages.warning(request, erro)
                if len(erros) > 10:
                    messages.warning(request, f'... e mais {len(erros) - 10} erros')
            
        except json.JSONDecodeError as e:
            messages.error(request, f'Erro ao decodificar o arquivo JSON: {str(e)}. Verifique se o formato está correto.')
        except Exception as e:
            messages.error(request, f'Erro ao importar despesas: {str(e)}')
            
        return redirect('importacoes:importacoes')
    
    return redirect('importacoes:importacoes')

@login_required
def importacoes(request):
    return render(request, 'importacoes/importacoes.html')
