from django.contrib import admin
from .models import Mesa, Prato, Combo, Comanda, ItemComanda

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ("numero", "capacidade", "status")
    list_filter = ("status",)
    search_fields = ("numero",)

@admin.register(Prato)
class PratoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "preco", "disponivel")
    list_filter = ("categoria", "disponivel")
    search_fields = ("nome", "descricao")

@admin.register(Combo)
class ComboAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "disponivel")
    list_filter = ("disponivel",)
    search_fields = ("nome", "descricao")
    filter_horizontal = ("pratos",)

class ItemComandaInline(admin.TabularInline):
    model = ItemComanda
    extra = 1

@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = ("id", "mesa", "cliente_nome", "status", "data_abertura", "data_fechamento", "total_exibicao")
    list_filter = ("status", "data_abertura")
    search_fields = ("cliente_nome", "mesa__numero")
    inlines = [ItemComandaInline]

    def total_exibicao(self, obj):
        return f"R$ {obj.total_consumo:.2f}"
    total_exibicao.short_description = "Total Consumido"

@admin.register(ItemComanda)
class ItemComandaAdmin(admin.ModelAdmin):
    list_display = ("comanda", "prato", "combo", "quantidade", "preco_unitario", "subtotal")
    list_filter = ("comanda__status",)
