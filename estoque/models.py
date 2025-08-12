from django.db import models


class Unidade(models.Model):
    nome = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Unidade",
        help_text="Ex.: UN, CX, KG"
    )

    class Meta:
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"
        ordering = ['nome']

    def __str__(self):
        return self.nome



class TipoProduto(models.Model):
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Tipo de Produto"
    )

    class Meta:
        verbose_name = "Tipo de Produto"
        verbose_name_plural = "Tipos de Produtos"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código"
    )
    descricao = models.CharField(
        max_length=255,
        verbose_name="Descrição"
    )
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço Unitário"
    )
    quantidade_estoque = models.PositiveIntegerField(
        verbose_name="Quantidade em Estoque"
    )
    tipo_produto = models.ForeignKey(
        TipoProduto,
        on_delete=models.PROTECT,
        related_name="produtos",
        verbose_name="Tipo de Produto"
    )
    unidade = models.ForeignKey(
        Unidade,
        on_delete=models.PROTECT,
        related_name="unidades",
        verbose_name="Unidade"
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['descricao']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"



class Cliente(models.Model):
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código"
    )
    nome = models.CharField(
        max_length=255,
        verbose_name="Nome"
    )
    endereco = models.CharField(
        max_length=255,
        verbose_name="Endereco",
        help_text="Endereço completo (Lograduro, N.Imovel, Bairro, Cidade, CEP)"
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    

class Fornecedor(models.Model):
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código"
    )
    nome = models.CharField(
        max_length=255,
        verbose_name="Nome"
    )
    endereco = models.CharField(
        max_length=255,
        verbose_name="Endereco",
        help_text="Endereço completo (Lograduro, N.Imovel, Bairro, Cidade, CEP)"
    )

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"