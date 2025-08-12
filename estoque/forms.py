from django import forms
from .models import Produto, TipoProduto, Unidade

class ProdutoForm(forms.ModelForm):
    novo_tipo = forms.CharField(
        required=False,
        label="Novo Tipo de Produto",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite para criar um novo tipo'})
    )

    nova_unidade = forms.CharField(
        required=False,
        label="Nova Unidade",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite para criar uma nova unidade'})
    )

    class Meta:
        model = Produto
        fields = ['codigo', 'descricao', 'preco', 'quantidade_estoque', 'tipo_produto', 'novo_tipo', 'unidade', 'nova_unidade']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantidade_estoque': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_produto': forms.Select(attrs={'class': 'form-control'}),
            'unidade': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_produto = cleaned_data.get('tipo_produto')
        novo_tipo = cleaned_data.get('novo_tipo')

        # Se não escolheu tipo e não digitou novo tipo → erro
        if not tipo_produto and not novo_tipo:
            raise forms.ValidationError("Selecione um tipo existente ou informe um novo tipo.")
        
        unidade = cleaned_data.get('unidade')
        nova_unidade = cleaned_data.get('nova_unidade')

        # Se não escolheu unidade e não digitou nova unidade → erro
        if not unidade and not nova_unidade:
            raise forms.ValidationError("Selecione uma unidade existente ou informe uma nova unidade.")

        return cleaned_data

    def save(self, commit=True):
        novo_tipo_nome = self.cleaned_data.get('novo_tipo')
        if novo_tipo_nome:
            tipo, created = TipoProduto.objects.get_or_create(nome=novo_tipo_nome)
            self.instance.tipo_produto = tipo

        nova_unidade_nome = self.cleaned_data.get('nova_unidade')
        if nova_unidade_nome:
            unidade, created = Unidade.objects.get_or_create(nome=nova_unidade)
            self.instance.unidade = unidade
        return super().save(commit)
