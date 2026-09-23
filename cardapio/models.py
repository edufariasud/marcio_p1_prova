from django.db import models
from django.utils import timezone
from decimal import Decimal

class Mesa(models.Model):
    STATUS_CHOICES = [
        ("livre", "Livre"),
        ("ocupada", "Ocupada"),
        ("reservada", "Reservada"),
    ]

    numero = models.PositiveIntegerField(unique=True, verbose_name="Número da Mesa")
    capacidade = models.PositiveIntegerField(default=4, verbose_name="Capacidade de Pessoas")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="livre", verbose_name="Status")

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        ordering = ["numero"]

    def __str__(self):
        return f"Mesa {self.numero} - {self.get_status_display()}"


class Prato(models.Model):
    CATEGORIAS = [
        ("entrada", "Entrada"),
        ("principal", "Prato Principal"),
        ("sobremesa", "Sobremesa"),
        ("bebida", "Bebida"),
    ]

    nome = models.CharField(max_length=150, verbose_name="Nome do Prato")
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default="principal", verbose_name="Categoria")
    preco = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço (R$)")
    descricao = models.TextField(blank=True, verbose_name="Descrição dos Ingredientes")
    disponivel = models.BooleanField(default=True, verbose_name="Disponível para Pedido")

    class Meta:
        verbose_name = "Prato"
        verbose_name_plural = "Pratos"
        ordering = ["categoria", "nome"]

    def __str__(self):
        return f"{self.nome} (R$ {self.preco})"


class Combo(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome do Combo")
    descricao = models.TextField(blank=True, verbose_name="Descrição do Combo")
    preco = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço Especial (R$)")
    pratos = models.ManyToManyField(Prato, related_name="combos", verbose_name="Pratos Inclusos")
    disponivel = models.BooleanField(default=True, verbose_name="Ativo no Cardápio")

    class Meta:
        verbose_name = "Combo Promocional"
        verbose_name_plural = "Combos Promocionais"
        ordering = ["nome"]

    def __str__(self):
        return f"Combo: {self.nome} (R$ {self.preco})"


class Comanda(models.Model):
    STATUS_COMANDA = [
        ("aberta", "Aberta"),
        ("fechada", "Fechada"),
        ("cancelada", "Cancelada"),
    ]

    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name="comandas", verbose_name="Mesa")
    cliente_nome = models.CharField(max_length=100, blank=True, verbose_name="Nome do Cliente / Responsável")
    status = models.CharField(max_length=20, choices=STATUS_COMANDA, default="aberta", verbose_name="Status da Comanda")
    data_abertura = models.DateTimeField(auto_now_add=True, verbose_name="Abertura")
    data_fechamento = models.DateTimeField(null=True, blank=True, verbose_name="Fechamento")
    observacoes = models.TextField(blank=True, verbose_name="Observações do Atendimento")

    class Meta:
        verbose_name = "Comanda"
        verbose_name_plural = "Comandas"
        ordering = ["-data_abertura"]

    def __str__(self):
        return f"Comanda #{self.id} - Mesa {self.mesa.numero} ({self.get_status_display()})"

    @property
    def total_consumo(self):
        total = sum(item.subtotal for item in self.itens.all())
        return total

    def fechar_conta(self):
        self.status = "fechada"
        self.data_fechamento = timezone.now()
        self.save()
        # Libera a mesa automaticamente se não houver outras comandas abertas nela
        outras_abertas = Comanda.objects.filter(mesa=self.mesa, status="aberta").exclude(id=self.id).exists()
        if not outras_abertas:
            self.mesa.status = "livre"
            self.mesa.save()


class ItemComanda(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, related_name="itens", verbose_name="Comanda")
    prato = models.ForeignKey(Prato, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Prato Escolhido")
    combo = models.ForeignKey(Combo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Combo Escolhido")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço Unitário (R$)")
    observacao = models.CharField(max_length=200, blank=True, verbose_name="Observação (ex: sem cebola)")

    class Meta:
        verbose_name = "Item da Comanda"
        verbose_name_plural = "Itens da Comanda"

    def __str__(self):
        item_nome = self.prato.nome if self.prato else (self.combo.nome if self.combo else "Item Indefinido")
        return f"{self.quantidade}x {item_nome} (Comanda #{self.comanda.id})"

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def save(self, *args, **kwargs):
        # Auto-preenche o preco unitario se nao for informado
        if not self.preco_unitario:
            if self.prato:
                self.preco_unitario = self.prato.preco
            elif self.combo:
                self.preco_unitario = self.combo.preco
            else:
                self.preco_unitario = Decimal("0.00")
        super().save(*args, **kwargs)
