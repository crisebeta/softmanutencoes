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
            'preco': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'preco_custo': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'quantidade': forms.NumberInput(attrs={'min': '0'}),
            'data_compra': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        } 