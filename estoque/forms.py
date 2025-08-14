from django import forms
from .models import Produto, TipoProduto, Unidade, Cliente
from django.forms import inlineformset_factory
from .models import Cliente, Contato

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
        codigo = cleaned_data.get('codigo')
        tipo_produto = cleaned_data.get('tipo_produto')
        novo_tipo = cleaned_data.get('novo_tipo')

        if codigo and len(codigo) < 3:
            self.add_error('codigo', 'O código deve ter pelo menos 3 caracteres.')

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
            unidade, created = Unidade.objects.get_or_create(nome=nova_unidade_nome)
            self.instance.unidade = unidade
        return super().save(commit)


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['codigo', 'nome', 'endereco']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        codigo = cleaned_data.get('codigo')
        if codigo and len(codigo) < 3:
            self.add_error('codigo', 'O código deve ter pelo menos 3 caracteres.')

        return cleaned_data



class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }

ContatoFormSet = inlineformset_factory(
    Cliente,
    Contato,
    form=ContatoForm,
    extra=2,        # começa com 2 linha de contato
    can_delete=True # permite excluir contatos
)
