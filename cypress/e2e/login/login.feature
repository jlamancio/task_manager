# language: pt

Funcionalidade: Login
  Como usuário cadastrado
  Quero entrar no sistema task_manager
  Para acessar minhas tarefas

  Contexto:
    Dado que existe um usuário cadastrado com e-mail e senha válidos

  Cenário: Login com credenciais válidas
    Dado que estou na página de login
    Quando informo o e-mail e a senha corretos
    E clico em "entrar"
    Então devo ser redirecionado para a página de tarefas
    E o token de acesso deve estar salvo

  Cenário: Login com senha incorreta
    Dado que estou na página de login
    Quando informo o e-mail correto e uma senha incorreta
    E clico em "entrar"
    Então devo ver a mensagem de erro "Email ou senha inválidos"

  Cenário: Login com e-mail não cadastrado
    Dado que estou na página de login
    Quando informo um e-mail não cadastrado e qualquer senha
    E clico em "entrar"
    Então devo ver a mensagem de erro "Email ou senha inválidos"

  Cenário: Tentativa de login com campos vazios
    Dado que estou na página de login
    Quando clico em "entrar" sem preencher nenhum campo
    Então devo permanecer na página de login

  Cenário: Usuário já autenticado é redirecionado automaticamente
    Dado que já possuo um token de acesso válido salvo
    Então devo ser redirecionado para a página de tarefas
