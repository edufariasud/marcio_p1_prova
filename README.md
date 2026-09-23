# 🍽️ Cardápio Digital — Sistema de Gestão de Salão e Comandas

**Disciplina:** Laboratório de Programação Full Stack  
**Professor:** Márcio Garrido  
**Aluno:** Eduardo Augusto Figueiredo de Faria  
**Matrícula:** 202413235  
**Avaliação:** P1 — MVP Funcional (Aula 12)  
**Tema Escolhido:** Opção 9 — Cardápio Digital  

---

## 📌 1. Visão Geral do Projeto (P1)

Este projeto implementa o MVP funcional completo do sistema de **Cardápio Digital** para restaurantes, bares e lanchonetes. O sistema permite o gerenciamento do salão de mesas, o cardápio de pratos e combos promocionais, e o ciclo completo de atendimento por comanda com fechamento de conta.

### As 5 Entidades da Rubrica
1. **`Mesa`**: Controle físico do salão com número, capacidade e status dinâmico (`Livre`, `Ocupada`, `Reservada`).
2. **`Prato`**: Itens do cardápio categorizados (`Entrada`, `Prato Principal`, `Sobremesa`, `Bebida`), preço, ingredientes e disponibilidade.
3. **`Combo`**: Combos promocionais que agrupam múltiplos pratos via relação N:N (`ManyToManyField`) com precificação especial.
4. **`Comanda`**: Registro do atendimento vinculado à mesa, data/hora de abertura, status (`Aberta`, `Fechada`), responsável e data de fechamento.
5. **`ItemComanda` (Item)**: Lançamento de pedidos na comanda, suportando tanto pratos avulsos quanto combos, com controle de quantidade, preço unitário congelado no momento do pedido, subtotal e observações da cozinha.

### Regra de Negócio Central da P1
- **Abertura de Comanda:** Ao abrir uma comanda para uma mesa livre, a mesa tem seu status alterado automaticamente para `Ocupada`.
- **Lançamento de Itens:** Garçons/atendentes lançam pratos e combos com quantidades e observações personalizadas. O total parcial é recalculado dinamicamente.
- **Fechamento de Conta & Liberação:** Ao solicitar o fechamento, o sistema exibe o extrato discriminado com subtotal, sugestão de 10% de taxa de serviço e total geral. Ao confirmar, a comanda recebe o status `Fechada`, a data de encerramento é gravada e a mesa é liberada automaticamente para o status `Livre`.

---

## 🚀 2. Como Executar o Projeto

### Pré-requisitos
- Python 3.10+
- Gerenciador de pacotes `pip`

### Passo 1: Clonar ou Acessar a Pasta do Projeto
```bash
cd "Laboratório de Programação Full Stack/p1_prova/eduardo"
```

### Passo 2: Ativar o Ambiente Virtual
O ambiente virtual já se encontra criado na pasta `venv/`:
```bash
source venv/bin/activate
```
*(Caso deseje recriar do zero: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`)*

### Passo 3: Configurar o Arquivo .env
O arquivo `.env` já está pré-configurado:
```ini
SECRET_KEY=django-insecure-eduardo-faria-cardapio-digital-p1-202413235
DEBUG=True
```

### Passo 4: Executar as Migrações
```bash
python manage.py migrate
```

### Passo 5: Iniciar o Servidor de Desenvolvimento
```bash
python manage.py runserver
```

Acesse no navegador: **`http://127.0.0.1:8000/`**

---

## 🔑 3. Acesso Administrativo (Django Admin)

O banco já está populado com dados de teste e superusuário:
- **URL Admin:** `http://127.0.0.1:8000/admin/`
- **Usuário:** `admin`
- **Senha:** `admin123`

---

## 🧭 4. Rotas e Telas do Sistema

| Rota | Descrição |
|---|---|
| `/` | **Painel Principal:** Monitoramento do salão de mesas, status (Livre/Ocupada) e comandas ativas |
| `/cardapio/` | **Cardápio Completo:** Pratos divididos por categorias e combos promocionais ativos |
| `/comanda/abrir/` | **Abertura de Comanda:** Seleção de mesa livre e abertura de novo atendimento |
| `/comanda/<id>/` | **Detalhes da Comanda:** Visualização de itens consumidos, total acumulado e formulário para lançar novos itens |
| `/comanda/<id>/fechar/` | **Fechamento de Conta:** Extrato final com taxa de serviço e liberação automática da mesa |
| `/cardapio/prato/novo/` | **Cadastro de Prato:** Adicionar novos itens ao cardápio via ModelForm |
| `/cardapio/combo/novo/` | **Cadastro de Combo:** Montagem de combo promocional vinculando múltiplos pratos |

---

## 📋 5. Estrutura do Código-Fonte

```
eduardo/
├── cardapio/
│   ├── admin.py          # Registro das 5 entidades no Django Admin
│   ├── apps.py
│   ├── forms.py          # ModelForms para Mesas, Comandas, Itens, Pratos e Combos
│   ├── models.py         # As 5 entidades: Mesa, Prato, Combo, Comanda, ItemComanda
│   ├── urls.py           # Rotas do app
│   └── views.py          # Lógica de controle do salão, comanda e fechamento
├── restaurante/
│   ├── settings.py       # Configurações com python-dotenv, pt-br e templates
│   ├── urls.py           # Roteamento principal
│   └── wsgi.py
├── static/
│   └── css/style.css     # Folha de estilo limpa, moderna e responsiva
├── templates/
│   ├── base.html         # Template mestre com identificação do aluno
│   └── cardapio/         # Telas de salão, cardápio, comanda e fechamento
├── db.sqlite3            # Banco de dados pré-populado com dados de teste
├── manage.py
├── requirements.txt
├── .env
└── README.md
```
