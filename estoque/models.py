from django.db import models

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
    unidade = models.CharField(
        max_length=10,
        verbose_name="Unidade de Medida",
        help_text="Ex.: UN, CX, KG"
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

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['descricao']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"
