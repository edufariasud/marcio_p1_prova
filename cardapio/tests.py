from django.test import TestCase, Client
from django.urls import reverse
from .models import Mesa, Prato, Combo, Comanda, ItemComanda

class CardapioP1TestesCompletos(TestCase):
    def setUp(self):
        self.client = Client()
        self.mesa = Mesa.objects.create(numero=1, capacidade=4, status="livre")
        self.prato = Prato.objects.create(
            nome="Filé Parmegiana", categoria="principal", preco=50.00, descricao="Prato clássico", disponivel=True
        )
        self.combo = Combo.objects.create(
            nome="Combo Casal", preco=90.00, descricao="Para duas pessoas", disponivel=True
        )
        self.combo.pratos.add(self.prato)

    def test_str_das_entidades(self):
        self.assertIn("Mesa 1", str(self.mesa))
        self.assertIn("Filé Parmegiana", str(self.prato))
        self.assertIn("Combo Casal", str(self.combo))

    def test_rotas_get_principais(self):
        for rota in ["index", "cardapio_lista", "abrir_comanda", "novo_prato", "novo_combo"]:
            res = self.client.get(reverse(rota))
            self.assertEqual(res.status_code, 200, f"Falha na rota {rota}")

    def test_cadastro_novo_prato_e_combo(self):
        res_prato = self.client.post(reverse("novo_prato"), {
            "nome": "Pudim Caseiro",
            "categoria": "sobremesa",
            "preco": 15.00,
            "descricao": "Delicioso",
            "disponivel": True,
        })
        self.assertEqual(res_prato.status_code, 302)
        self.assertTrue(Prato.objects.filter(nome="Pudim Caseiro").exists())

        pudim = Prato.objects.get(nome="Pudim Caseiro")
        res_combo = self.client.post(reverse("novo_combo"), {
            "nome": "Combo Doce",
            "preco": 25.00,
            "descricao": "Sobremesas",
            "pratos": [pudim.id],
            "disponivel": True,
        })
        self.assertEqual(res_combo.status_code, 302)
        self.assertTrue(Combo.objects.filter(nome="Combo Doce").exists())

    def test_ciclo_completo_comanda_itens_remover_fechar(self):
        # 1. Abertura
        self.client.post(reverse("abrir_comanda"), {
            "mesa": self.mesa.id,
            "cliente_nome": "Eduardo Faria",
        })
        self.mesa.refresh_from_db()
        self.assertEqual(self.mesa.status, "ocupada")

        comanda = Comanda.objects.get(mesa=self.mesa, status="aberta")

        # 2. Adicionar 2 itens
        self.client.post(reverse("comanda_detalhes", args=[comanda.id]), {
            "tipo_item": "prato",
            "prato": self.prato.id,
            "quantidade": 1,
        })
        self.client.post(reverse("comanda_detalhes", args=[comanda.id]), {
            "tipo_item": "combo",
            "combo": self.combo.id,
            "quantidade": 1,
        })
        self.assertEqual(comanda.itens.count(), 2)
        self.assertEqual(comanda.total_consumo, 140.00)

        # 3. Remover um item
        item_para_remover = comanda.itens.first()
        res_remove = self.client.get(reverse("remover_item", args=[item_para_remover.id]))
        self.assertEqual(res_remove.status_code, 302)
        self.assertEqual(comanda.itens.count(), 1)

        # 4. Tela de Fechamento de Conta
        res_fechamento_tela = self.client.get(reverse("fechar_conta", args=[comanda.id]))
        self.assertEqual(res_fechamento_tela.status_code, 200)

        # 5. Confirmar Fechamento
        res_fechar = self.client.post(reverse("fechar_conta", args=[comanda.id]))
        self.assertEqual(res_fechar.status_code, 302)

        comanda.refresh_from_db()
        self.mesa.refresh_from_db()

        self.assertEqual(comanda.status, "fechada")
        self.assertIsNotNone(comanda.data_fechamento)
        self.assertEqual(self.mesa.status, "livre")
