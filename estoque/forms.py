from django import forms
from .models import Produto, TipoProduto

class ProdutoForm(forms.ModelForm):
    novo_tipo = forms.CharField(
        required=False,
        label="Novo Tipo de Produto",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite para criar um novo tipo'})
    )

    class Meta:
        model = Produto
        fields = ['codigo', 'descricao', 'unidade', 'preco', 'quantidade_estoque', 'tipo_produto', 'novo_tipo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'unidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: UN, CX, KG'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantidade_estoque': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_produto': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_produto = cleaned_data.get('tipo_produto')
        novo_tipo = cleaned_data.get('novo_tipo')

        # Se não escolheu tipo e não digitou novo tipo → erro
        if not tipo_produto and not novo_tipo:
            raise forms.ValidationError("Selecione um tipo existente ou informe um novo tipo.")

        return cleaned_data

    def save(self, commit=True):
        novo_tipo_nome = self.cleaned_data.get('novo_tipo')
        if novo_tipo_nome:
            tipo, created = TipoProduto.objects.get_or_create(nome=novo_tipo_nome)
            self.instance.tipo_produto = tipo
        return super().save(commit)
