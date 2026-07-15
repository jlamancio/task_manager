# language: pt

Funcionalidade: Cadastro
  Como visitante sem conta
  Quero me cadastrar no sistema
  Para poder fazer login e gerenciar minhas tarefas

  Cenário: Cadastro com dados válidos
    Dado que estou na página de cadastro
    Quando informo um e-mail novo e uma senha válida com confirmação igual
    E clico em "criar conta"
    Então devo ser redirecionado para a página de login

  Cenário: Cadastro com e-mail já existente
    Dado que já existe um usuário cadastrado com e-mail e senha válidos
    E que estou na página de cadastro
    Quando informo o mesmo e-mail já cadastrado e uma senha válida com confirmação igual
    E clico em "criar conta"
    Então devo ver a mensagem de erro "Email já cadastrado"

  Cenário: Senha menor que o mínimo permitido
    Dado que estou na página de cadastro
    Quando informo um e-mail novo e uma senha com menos de 6 caracteres
    E clico em "criar conta"
    Então devo permanecer na página de cadastro

  Cenário: Senha e confirmação diferentes
    Dado que estou na página de cadastro
    Quando informo um e-mail novo, uma senha válida e uma confirmação diferente
    E clico em "criar conta"
    Então devo ver a mensagem de erro "as senhas não coincidem"

  Cenário: Tentativa de cadastro com campos vazios
    Dado que estou na página de cadastro
    Quando clico em "criar conta" sem preencher nenhum campo
    Então devo permanecer na página de cadastro
