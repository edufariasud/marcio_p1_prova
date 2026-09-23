from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Mesa, Prato, Combo, Comanda, ItemComanda
from .forms import ComandaForm, ItemComandaForm, PratoForm, ComboForm, MesaForm

def index(request):
    mesas = Mesa.objects.all()
    comandas_abertas = Comanda.objects.filter(status="aberta").select_related("mesa")
    total_abertas = comandas_abertas.count()
    mesas_livres = mesas.filter(status="livre").count()
    mesas_ocupadas = mesas.filter(status="ocupada").count()

    context = {
        "mesas": mesas,
        "comandas_abertas": comandas_abertas,
        "total_abertas": total_abertas,
        "mesas_livres": mesas_livres,
        "mesas_ocupadas": mesas_ocupadas,
    }
    return render(request, "cardapio/index.html", context)

def abrir_comanda(request, mesa_id=None):
    mesa_pre = None
    if mesa_id:
        mesa_pre = get_object_or_404(Mesa, id=mesa_id)

    if request.method == "POST":
        form = ComandaForm(request.POST)
        if form.is_valid():
            comanda = form.save(commit=False)
            comanda.status = "aberta"
            comanda.save()
            # Atualiza mesa para ocupada
            mesa = comanda.mesa
            mesa.status = "ocupada"
            mesa.save()
            messages.success(request, f"Comanda #{comanda.id} aberta com sucesso para a Mesa {mesa.numero}!")
            return redirect("comanda_detalhes", comanda_id=comanda.id)
    else:
        initial_data = {}
        if mesa_pre:
            initial_data["mesa"] = mesa_pre
        form = ComandaForm(initial=initial_data)

    return render(request, "cardapio/abrir_comanda.html", {"form": form, "mesa_pre": mesa_pre})

def comanda_detalhes(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id)
    itens = comanda.itens.select_related("prato", "combo").all()
    form_item = ItemComandaForm()

    if request.method == "POST" and comanda.status == "aberta":
        form_item = ItemComandaForm(request.POST)
        if form_item.is_valid():
            item = form_item.save(commit=False)
            item.comanda = comanda
            tipo = form_item.cleaned_data.get("tipo_item")
            if tipo == "prato":
                item.combo = None
                item.preco_unitario = item.prato.preco
            else:
                item.prato = None
                item.preco_unitario = item.combo.preco
            item.save()
            messages.success(request, f"Item adicionado à comanda #{comanda.id}!")
            return redirect("comanda_detalhes", comanda_id=comanda.id)

    context = {
        "comanda": comanda,
        "itens": itens,
        "form_item": form_item,
        "total_consumo": comanda.total_consumo,
    }
    return render(request, "cardapio/comanda_detalhe.html", context)

def remover_item(request, item_id):
    item = get_object_or_404(ItemComanda, id=item_id)
    comanda_id = item.comanda.id
    if item.comanda.status == "aberta":
        item.delete()
        messages.info(request, "Item removido da comanda.")
    else:
        messages.error(request, "Não é possível remover itens de uma comanda já fechada.")
    return redirect("comanda_detalhes", comanda_id=comanda_id)

def fechar_conta(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id)
    if request.method == "POST":
        if comanda.status == "aberta":
            comanda.fechar_conta()
            messages.success(request, f"Conta da Mesa {comanda.mesa.numero} fechada com sucesso! Mesa liberada.")
        return redirect("comanda_detalhes", comanda_id=comanda.id)

    itens = comanda.itens.all()
    total = comanda.total_consumo
    taxa_servico = round(float(total) * 0.10, 2)
    total_com_taxa = round(float(total) + taxa_servico, 2)

    context = {
        "comanda": comanda,
        "itens": itens,
        "total": total,
        "taxa_servico": taxa_servico,
        "total_com_taxa": total_com_taxa,
    }
    return render(request, "cardapio/fechar_conta.html", context)

def cardapio_lista(request):
    pratos = Prato.objects.filter(disponivel=True)
    combos = Combo.objects.filter(disponivel=True).prefetch_related("pratos")
    entradas = pratos.filter(categoria="entrada")
    principais = pratos.filter(categoria="principal")
    sobremesas = pratos.filter(categoria="sobremesa")
    bebidas = pratos.filter(categoria="bebida")

    context = {
        "entradas": entradas,
        "principais": principais,
        "sobremesas": sobremesas,
        "bebidas": bebidas,
        "combos": combos,
    }
    return render(request, "cardapio/cardapio_lista.html", context)

def novo_prato(request):
    if request.method == "POST":
        form = PratoForm(request.POST)
        if form.is_valid():
            prato = form.save()
            messages.success(request, f"Prato {prato.nome} cadastrado com sucesso!")
            return redirect("cardapio_lista")
    else:
        form = PratoForm()
    return render(request, "cardapio/form_generico.html", {"form": form, "titulo": "Cadastrar Novo Prato"})

def novo_combo(request):
    if request.method == "POST":
        form = ComboForm(request.POST)
        if form.is_valid():
            combo = form.save()
            messages.success(request, f"Combo {combo.nome} cadastrado com sucesso!")
            return redirect("cardapio_lista")
    else:
        form = ComboForm()
    return render(request, "cardapio/form_generico.html", {"form": form, "titulo": "Cadastrar Novo Combo"})
