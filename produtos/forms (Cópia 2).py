from django import forms
from django.utils import timezone
from .models import Produto, Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

class ProdutoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define a data máxima como hoje
        hoje = timezone.localdate().strftime('%Y-%m-%d')
        self.fields['data_compra'].widget.attrs['max'] = hoje

    def clean_preco(self):
        """
        Limpa e valida o campo preço, convertendo de formato brasileiro para decimal
        """
        preco = self.cleaned_data.get('preco')
        
        if isinstance(preco, str):
            # Remove pontos (separadores de milhares) e substitui vírgula por ponto
            preco_limpo = preco.replace('.', '').replace(',', '.')
            try:
                preco = float(preco_limpo)
            except (ValueError, TypeError):
                raise forms.ValidationError("Preço inválido. Use o formato: 1.234,56")
        
        if preco is not None and preco < 0:
            raise forms.ValidationError("O preço não pode ser negativo.")
            
        return preco

    def clean_preco_custo(self):
        """
        Limpa e valida o campo preço de custo, convertendo de formato brasileiro para decimal
        """
        preco_custo = self.cleaned_data.get('preco_custo')
        
        if isinstance(preco_custo, str):
            # Remove pontos (separadores de milhares) e substitui vírgula por ponto
            preco_custo_limpo = preco_custo.replace('.', '').replace(',', '.')
            try:
                preco_custo = float(preco_custo_limpo)
            except (ValueError, TypeError):
                raise forms.ValidationError("Preço de custo inválido. Use o formato: 1.234,56")
        
        if preco_custo is not None and preco_custo < 0:
            raise forms.ValidationError("O preço de custo não pode ser negativo.")
            
        return preco_custo

    def clean_data_compra(self):
        data_compra = self.cleaned_data.get('data_compra')
        if data_compra and data_compra > timezone.localdate():
            raise forms.ValidationError('A data de compra não pode ser futura.')
        return data_compra

    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'observacao', 'preco_custo', 'preco', 'estado', 
                 'quantidade', 'imagem', 'data_compra']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'observacao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Informações adicionais sobre o produto'}),
            'preco': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0,00',
                    'autocomplete': 'off'
                }
            ),
            'preco_custo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0,00',
                    'autocomplete': 'off'
                }
            ),
            'quantidade': forms.NumberInput(attrs={'min': '0'}),
            'data_compra': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }