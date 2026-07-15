# Lições Aprendidas — Task Manager

Checklist de pontos de atenção identificados ao longo deste projeto, para
aplicar desde o início do próximo (não descobrir de novo na prática).

---

## Segurança

- **Nunca hardcodar segredos no código-fonte.** Neste projeto,
  `SECRET_KEY` ficou fixa em `auth_service.py` desde o início — funcionou
  porque é portfólio/local, mas o hábito certo é usar variável de ambiente
  desde a primeira linha:
  ```python
  import os
  SECRET_KEY = os.environ["SECRET_KEY"]
  ```
  com um arquivo `.env` (sempre no `.gitignore`, nunca commitado) e um
  `.env.example` versionado, mostrando quais variáveis existem sem expor
  valores reais.
- O mesmo vale para qualquer senha de banco, token de API externa, ou
  string de conexão — se o valor muda entre "sua máquina" e "produção",
  é variável de ambiente, não constante no código.

## Dados de teste

- Massa de dados manual (`"teste@teste.com"`, `"123456"` repetidos em
  toda fixture) funciona, mas é frágil e repetitivo. Para o próximo
  projeto, usar **Faker** desde o início:
  ```python
  from faker import Faker
  fake = Faker("pt_BR")
  email = fake.email()
  nome = fake.name()
  ```
  Isso também ajuda a pegar bugs de validação que dados fixos e "bonitos"
  escondem (acentos, nomes longos, formatos variados de e-mail).
- No front-end/Cypress, o mesmo princípio: e-mails gerados dinamicamente
  (`usuario_${Date.now()}@teste.com`) já foram necessários aqui porque o
  banco não reseta entre execuções — o Faker no back-end resolveria a
  raiz do mesmo problema de forma mais robusta.

## Git e versionamento

- **Arquivos que mudam sozinhos a cada execução não devem ser
  versionados**: banco de dados local (`.db`), relatórios gerados
  (`report.html`), `node_modules/`. Definir o `.gitignore` completo
  **antes** do primeiro commit, não corrigir depois — neste projeto isso
  gerou dois incidentes reais (ver `HISTORICO_INCIDENTE_GIT.md`).
- **Cuidado ao trocar de branch com um arquivo de banco de dados ainda
  rastreado em uma delas.** Se for parar de versionar um `.db`, fazer
  isso o quanto antes e em todas as branches relevantes — não deixar uma
  branch com o arquivo rastreado e outra sem.
- Script de setup do projeto (`start.sh` e similares) **deve** ser
  versionado — não tem segredo, e ajuda reprodutibilidade.

## Testes E2E (Cypress + Cucumber)

- **Windows + `[filepath]` do cucumber-preprocessor**: se o `.feature`
  tiver o mesmo nome da pasta que o contém (`login/login.feature`), o
  caminho de busca dos step_definitions pode duplicar
  (`login\login\step_definitions`). Solução: `.feature` direto em
  `cypress/e2e/`, sem repetir o nome como subpasta —
  `cypress/e2e/login.feature` + `cypress/e2e/login/step_definitions/`.
- **Electron headless tem flakiness conhecida** em `cy.type()` logo após
  navegação de página (`TypeError: Cannot read properties of undefined
  (reading 'KeyboardEvent')`). Mitigar com `retries: { runMode: 2,
  openMode: 0 }` no `cypress.config.js` — nunca aplicar retry no
  `openMode`, para não esconder falha real durante debug manual.
- **Não confiar só em `required` do HTML** para validação — neste
  projeto, um teste do Cypress provou que o envio passava mesmo com
  campo obrigatório vazio. Validar também em JS no front-end, **e** no
  back-end (Pydantic `Field(min_length=1)` ou equivalente) — nunca só
  uma camada.
- Cenários de erro "ID inexistente" (404) são mais confiáveis testados
  via `cy.request()` direto na API do que tentando forçar pela UI, que
  normalmente só permite agir sobre o que já está na tela.

## Arquitetura / integração front-end + back-end

- Login com **OAuth2PasswordRequestForm** (padrão FastAPI) espera
  `form-urlencoded` com campos `username`/`password` — não confundir com
  outros endpoints (cadastro) que usam JSON normal. Confirmar o formato
  esperado de cada rota lendo o teste automatizado correspondente antes
  de escrever a chamada no front-end.
- **CORS não é opcional** assim que front-end e back-end rodam em portas
  diferentes (mesmo em `127.0.0.1`) — configurar `CORSMiddleware` desde
  o início evita o `405` no preflight `OPTIONS` que só aparece na
  primeira tentativa real de integração.
- `Base.metadata.create_all()` **idempotente no startup** do `main.py`
  desde o início — evita depender de lembrar um comando manual toda vez
  que o banco precisar ser (re)criado.
