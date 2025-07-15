from django import forms
from .models import Despesa
from datetime import date

class DespesaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se houver uma instância (edição), formata a data para o campo
        if self.instance.pk and self.instance.data_compra:
            self.initial['data_compra'] = self.instance.data_compra.strftime('%Y-%m-%d')

    def clean_valor(self):
        """
        Limpa e valida o campo valor, convertendo de formato brasileiro para decimal
        """
        valor = self.cleaned_data.get('valor')
        
        if isinstance(valor, str):
            # Remove pontos (separadores de milhares) e substitui vírgula por ponto
            valor_limpo = valor.replace('.', '').replace(',', '.')
            try:
                valor = float(valor_limpo)
            except (ValueError, TypeError):
                raise forms.ValidationError("Valor inválido. Use o formato: 1.234,56")
        
        if valor is not None and valor < 0:
            raise forms.ValidationError("O valor não pode ser negativo.")
            
        return valor

    class Meta:
        model = Despesa
        fields = ['descricao', 'fornecedor', 'data_compra', 'valor', 
                 'categoria', 'condicao', 'observacoes']
        widgets = {
            'data_compra': forms.DateInput(
                attrs={
                    'type': 'date',
                    'max': date.today().isoformat(),
                    'class': 'form-control'
                }
            ),
            'valor': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0,00',
                    'autocomplete': 'off'
                }
            ),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }