from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from clientes.models import Cliente
from django.db import IntegrityError

# Create your views here.

@login_required
def importar_clientes(request):
    if request.method == 'POST':
        arquivo_json = request.FILES.get('arquivo')
        if not arquivo_json:
            messages.error(request, 'Por favor, selecione um arquivo JSON para importar.')
            return redirect('importacoes:importar_clientes')
        
        if not arquivo_json.name.endswith('.json'):
            messages.error(request, 'Por favor, selecione um arquivo JSON válido.')
            return redirect('importacoes:importar_clientes')
        
        try:
            # Decodifica o arquivo JSON
            dados_json = json.loads(arquivo_json.read().decode('utf-8'))
            
            # Contador de clientes importados
            clientes_importados = 0
            clientes_atualizados = 0
            clientes_ignorados = 0
            
            # Procura pela lista de dados dos clientes no JSON
            dados_clientes = None
            for item in dados_json:
                if isinstance(item, dict) and item.get('type') == 'table' and item.get('name') == 'clientes':
                    dados_clientes = item.get('data', [])
                    break
            
            if not dados_clientes:
                messages.error(request, 'Estrutura do arquivo JSON inválida ou sem dados de clientes.')
                return redirect('importacoes:importar_clientes')
            
            # Processa cada cliente
            for cliente_json in dados_clientes:
                # Mapeamento dos campos do JSON para os campos do modelo
                dados_cliente = {
                    'nome': cliente_json.get('nome_cliente', ''),
                    'telefone': cliente_json.get('campo_fixo', ''),
                    'celular': cliente_json.get('campo_celular', ''),
                    'email': cliente_json.get('email', ''),
                    'cpf_cnpj': cliente_json.get('campo_cpf', ''),
                    'cep': cliente_json.get('cep', ''),
                    'endereco': cliente_json.get('endereco', ''),
                    'complemento': cliente_json.get('numero', ''),
                    'bairro': cliente_json.get('bairro', ''),
                    'cidade': cliente_json.get('cidade', ''),
                    'uf': cliente_json.get('uf', '')
                }
                
                if not dados_cliente['nome']:  # Ignora registros sem nome
                    clientes_ignorados += 1
                    continue

                try:
                    if dados_cliente['cpf_cnpj']:  # Se tem CPF/CNPJ, usa como chave única
                        cliente, criado = Cliente.objects.update_or_create(
                            cpf_cnpj=dados_cliente['cpf_cnpj'],
                            defaults=dados_cliente
                        )
                    else:  # Se não tem CPF/CNPJ, usa o nome como identificador
                        cliente, criado = Cliente.objects.update_or_create(
                            nome=dados_cliente['nome'],
                            defaults=dados_cliente
                        )
                    
                    if criado:
                        clientes_importados += 1
                    else:
                        clientes_atualizados += 1
                        
                except IntegrityError:
                    clientes_ignorados += 1
                    continue
            
            mensagem = f'Importação concluída: {clientes_importados} novos clientes, {clientes_atualizados} atualizados'
            if clientes_ignorados > 0:
                mensagem += f', {clientes_ignorados} ignorados'
            messages.success(request, mensagem)
            
        except json.JSONDecodeError:
            messages.error(request, 'Erro ao decodificar o arquivo JSON. Verifique se o formato está correto.')
        except Exception as e:
            messages.error(request, f'Erro ao importar clientes: {str(e)}')
            
        return redirect('importacoes:importar_clientes')
    
    return render(request, 'importacoes/importar_clientes.html')
