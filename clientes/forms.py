from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se houver uma instância (edição), formata a data para o campo
        if self.instance.pk and self.instance.data_nascimento:
            self.initial['data_nascimento'] = self.instance.data_nascimento.strftime('%Y-%m-%d')

    class Meta:
        model = Cliente
        fields = [
            'tipo', 'nome', 'data_nascimento', 'cpf_cnpj',
            'endereco', 'complemento', 'bairro', 'cidade', 'uf', 'cep',
            'celular', 'telefone', 'email', 'email_empresarial', 'rede_social',
            'observacoes'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
            'tipo': forms.RadioSelect(),
            'uf': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')
        tipo = self.cleaned_data.get('tipo')
        
        if not cpf_cnpj:
            return cpf_cnpj
            
        # Remove caracteres não numéricos
        cpf_cnpj = ''.join(filter(str.isdigit, cpf_cnpj))
        
        if tipo == 'PF' and len(cpf_cnpj) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos.')
        elif tipo == 'PJ' and len(cpf_cnpj) != 14:
            raise forms.ValidationError('CNPJ deve conter 14 dígitos.')
        
        # Formata CPF/CNPJ
        if tipo == 'PF':
            cpf_cnpj = f'{cpf_cnpj[:3]}.{cpf_cnpj[3:6]}.{cpf_cnpj[6:9]}-{cpf_cnpj[9:]}'
        else:
            cpf_cnpj = f'{cpf_cnpj[:2]}.{cpf_cnpj[2:5]}.{cpf_cnpj[5:8]}/{cpf_cnpj[8:12]}-{cpf_cnpj[12:]}'
        
        return cpf_cnpj

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if not cep:
            return cep
            
        cep = ''.join(filter(str.isdigit, cep))
        
        if len(cep) != 8:
            raise forms.ValidationError('CEP deve conter 8 dígitos.')
        
        return f'{cep[:5]}-{cep[5:]}'

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if not celular:
            return celular
            
        celular = ''.join(filter(str.isdigit, celular))
        
        if len(celular) != 11:
            raise forms.ValidationError('Celular deve conter 11 dígitos incluindo DDD.')
        
        return f'({celular[:2]}) {celular[2:7]}-{celular[7:]}'

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if not telefone:
            return telefone
            
        telefone = ''.join(filter(str.isdigit, telefone))
        
        if len(telefone) != 10:
            raise forms.ValidationError('Telefone deve conter 10 dígitos incluindo DDD.')
        
        return f'({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}' 