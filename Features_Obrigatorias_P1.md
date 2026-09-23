# UNIVERSIDADE DE VASSOURAS
## Curso de Graduação em Engenharia de Software
### FEATURES OBRIGATÓRIAS DA ENTREGA P1
**Disciplina:** Laboratório de Programação Full Stack — **Prof. Márcio Garrido**

---

### O que é este documento
Além do CRUD completo das entidades do seu projeto (visto nas Aulas 4 a 6), a entrega do P1 (Aula 12) exige a implementação de **DUAS features adicionais**, descritas abaixo. Elas se aplicam a qualquer um dos 10 projetos do catálogo — mas cada uma precisa ser **ADAPTADA** ao modelo de dados e à regra de negócio específica do projeto que você escolheu. Usam apenas o que já foi ensinado até a Aula 5: views, ORM, templates e ModelForm.

---

### Feature 1 — Busca e Filtro na Listagem
A página de listagem principal do seu projeto (a que você já construiu no CRUD) deve ganhar:
- Um campo de busca por texto, que filtra a lista por um campo textual relevante (ex.: nome, título, descrição).
- Um filtro por categoria ou status, usando um `<select>` ou botões, que restringe a lista a um subconjunto.
- Os dois filtros devem poder ser usados juntos ou separadamente.

#### Requisitos técnicos
- Ler os parâmetros da URL na view com `request.GET.get('...')`.
- Usar `.filter(campo__icontains=...)` do ORM para a busca textual (não é case-sensitive).
- Se nenhum resultado for encontrado, o template deve mostrar uma mensagem clara (reaproveite o `{% empty %}` que você já usa no `{% for %}`).
- O campo de busca deve permanecer preenchido com o termo digitado depois da pesquisa (atributo `value="{{ request.GET.q }}"` no input).

#### Sugestão de aplicação por projeto
| Projeto | O que buscar / filtrar |
|---|---|
| 1. Biblioteca / Acervo | Buscar por título ou autor do livro; filtrar por disponível/emprestado. |
| 2. Agenda de Consultas | Buscar por nome do paciente; filtrar por especialidade do profissional. |
| 3. Controle Financeiro | Buscar por descrição do lançamento; filtrar por categoria. |
| 4. Help Desk / Chamados | Buscar por título do chamado; filtrar por prioridade ou status. |
| 5. Mini E-commerce | Buscar por nome do produto; filtrar por categoria. |
| 6. Blog / Portal de Notícias | Buscar por título do post; filtrar por categoria ou tag. |
| 7. Gestão de Tarefas | Buscar por título da tarefa; filtrar por status (a fazer/fazendo/feito). |
| 8. Reserva de Salas | Buscar por nome da sala; filtrar por capacidade ou recurso disponível. |
| **9. Cardápio Digital** | **Buscar por nome do prato; filtrar por categoria.** |
| 10. Controle de Estoque | Buscar por nome do produto; filtrar por categoria ou fornecedor. |

#### Desafio extra (opcional, vale ponto adicional a critério do professor)
Combine busca por texto E filtro por categoria na **MESMA** consulta, usando `Q()` do Django (`from django.db.models import Q`). Isso não foi ensinado em aula até a Aula 5 — é uma pesquisa rápida que separa quem entende o problema de quem apenas copia um código pronto.

---

### Feature 2 — Validação Customizada no Formulário
O formulário de cadastro (ModelForm) do seu projeto deve ganhar **UMA** regra de validação própria do domínio do projeto — algo além de "campo obrigatório", que o Django já faz sozinho.

#### Requisitos técnicos
- Sobrescrever o método `clean()` (ou um `clean_<campo>()` específico) na classe do seu ModelForm.
- Usar `self.cleaned_data.get('...')` para ler o valor a ser validado.
- Levantar `forms.ValidationError("mensagem clara para o usuário")` quando a regra for violada.
- Confirmar que a mensagem de erro aparece no template (isso já acontece automaticamente com `{{ form.as_p }}`).

#### Sugestão de aplicação por projeto
| Projeto | Regra de validação sugerida |
|---|---|
| 1. Biblioteca / Acervo | O ano de publicação do livro não pode ser um ano futuro. |
| 2. Agenda de Consultas | A data da consulta não pode estar no passado. |
| 3. Controle Financeiro | O valor do lançamento deve ser maior que zero. |
| 4. Help Desk / Chamados | O prazo do SLA não pode ser anterior à data de abertura do chamado. |
| 5. Mini E-commerce | O preço do produto deve ser maior que zero; a quantidade em estoque não pode ser negativa. |
| 6. Blog / Portal de Notícias | Um post não pode ser publicado com um conteúdo abaixo de um tamanho mínimo (ex.: 50 caracteres). |
| 7. Gestão de Tarefas | O prazo de entrega da tarefa não pode ser anterior à data de criação do projeto. |
| 8. Reserva de Salas | O horário de término da reserva deve ser depois do horário de início. |
| **9. Cardápio Digital** | **O preço do prato deve ser maior que zero.** |
| 10. Controle de Estoque | Uma movimentação de saída não pode ser maior que o estoque atual do produto. |

---

### O Que Entregar
- As duas features funcionando no projeto, integradas ao CRUD já existente (não como telas separadas e soltas).
- Um parágrafo curto no relatório do P1 explicando: qual campo/categoria você escolheu para a Feature 1, e qual regra de negócio você escolheu para a Feature 2 — e por quê.
- Código versionado no Git, com pelo menos um commit específico para cada feature.

#### Por que o relatório importa
Colar um código pronto de uma IA sem entender resolve a tela, mas não explica a decisão. Se você não souber justificar por que escolheu aquele campo ou aquela regra — e o que aconteceria se ela não existisse — a feature não conta como compreendida, mesmo que o código rode.

*— Fim do documento —*
