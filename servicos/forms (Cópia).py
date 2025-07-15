from django import forms
from django.utils import timezone
from datetime import datetime
from .models import Servico, ProdutoServico
from produtos.models import Produto

class ProdutoServicoForm(forms.ModelForm):
    class Meta:
        model = ProdutoServico
        fields = ['produto', 'quantidade', 'valor_unitario']
        widgets = {
            'produto': forms.Select(attrs={'class': 'select2'}),
            'quantidade': forms.NumberInput(attrs={'min': 1}),
            'valor_unitario': forms.NumberInput(attrs={'step': '0.01'})
        }

class ServicoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se houver uma instância (edição), formata as datas
        if self.instance.pk:
            if self.instance.data_entrada:
                self.initial['data_entrada'] = self.instance.data_entrada.strftime('%Y-%m-%d')
            if self.instance.data_saida:
                self.initial['data_saida'] = self.instance.data_saida.strftime('%Y-%m-%d')
        
        # Define a data máxima como hoje
        hoje = timezone.localdate().strftime('%Y-%m-%d')
        self.fields['data_entrada'].widget.attrs['max'] = hoje
        self.fields['data_saida'].widget.attrs['max'] = hoje

    def clean_data_entrada(self):
        data_entrada = self.cleaned_data.get('data_entrada')
        if data_entrada and data_entrada > timezone.localdate():
            raise forms.ValidationError('A data de entrada não pode ser futura.')
        return data_entrada

    def clean_data_saida(self):
        data_saida = self.cleaned_data.get('data_saida')
        data_entrada = self.cleaned_data.get('data_entrada')
        
        if data_saida:
            if data_saida > timezone.localdate():
                raise forms.ValidationError('A data de saída não pode ser futura.')
            
            if data_entrada and data_saida < data_entrada:
                raise forms.ValidationError('A data de saída não pode ser anterior à data de entrada.')
        
        return data_saida

    class Meta:
        model = Servico
        fields = [
            'cliente',
            'data_entrada',
            'data_saida',
            'status',
            'equipamento',
            'marca',
            'modelo',
            'numero_serie',
            'descricao_problema',
            'servico_realizado',
            'valor_servico',
            'valor_pago',
            'observacoes'
        ]
        widgets = {
            'data_entrada': forms.DateInput(attrs={'type': 'date'}),
            'data_saida': forms.DateInput(attrs={'type': 'date'}),
            'descricao_problema': forms.Textarea(attrs={'rows': 3}),
            'servico_realizado': forms.Textarea(attrs={'rows': 3}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'equipamento': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_servico': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
            'valor_pago': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
        } 