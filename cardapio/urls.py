from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("comanda/abrir/", views.abrir_comanda, name="abrir_comanda"),
    path("comanda/abrir/mesa/<int:mesa_id>/", views.abrir_comanda, name="abrir_comanda_mesa"),
    path("comanda/<int:comanda_id>/", views.comanda_detalhes, name="comanda_detalhes"),
    path("comanda/<int:comanda_id>/fechar/", views.fechar_conta, name="fechar_conta"),
    path("comanda/item/<int:item_id>/remover/", views.remover_item, name="remover_item"),
    path("cardapio/", views.cardapio_lista, name="cardapio_lista"),
    path("cardapio/prato/novo/", views.novo_prato, name="novo_prato"),
    path("cardapio/combo/novo/", views.novo_combo, name="novo_combo"),
]
