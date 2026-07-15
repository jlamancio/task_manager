# language: pt

Funcionalidade: Gerenciamento de tarefas
  Como usuário autenticado
  Quero criar, editar e excluir tarefas
  Para organizar meu trabalho

  Contexto:
    Dado que estou autenticado e na página de tarefas

  Cenário: Criar uma tarefa com dados válidos
    Quando preencho uma nova tarefa com título "Revisar PR" e vencimento "2026-12-31"
    E clico em "salvar"
    Então a tarefa "Revisar PR" deve aparecer na lista

  Cenário: Tentativa de criar tarefa sem título
    Quando abro o formulário de nova tarefa
    E clico em "salvar" sem preencher o título
    Então o formulário de tarefa deve continuar aberto

  Cenário: Editar uma tarefa existente
    Dado que existe uma tarefa cadastrada com título "Tarefa original"
    Quando edito essa tarefa para o título "Tarefa atualizada"
    E clico em "salvar"
    Então a tarefa "Tarefa atualizada" deve aparecer na lista

  Cenário: Excluir uma tarefa existente
    Dado que existe uma tarefa cadastrada com título "Tarefa para excluir"
    Quando excluo essa tarefa e confirmo
    Então a tarefa "Tarefa para excluir" não deve mais aparecer na lista

  Cenário: Editar uma tarefa inexistente retorna 404
    Quando tento atualizar uma tarefa com id inexistente diretamente na API
    Então a API deve responder com 404

  Cenário: Excluir uma tarefa inexistente retorna 404
    Quando tento excluir uma tarefa com id inexistente diretamente na API
    Então a API deve responder com 404
