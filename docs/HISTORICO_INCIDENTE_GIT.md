# Histórico do Incidente — Branch Nascida Desatualizada

**Data:** 25/06/2026
**Contexto:** Sessão de implementação de testes (Pytest), antes de escrever
o primeiro teste de fato.

Este documento narra, em ordem, o que aconteceu, por que aconteceu, e como
foi resolvido — material de estudo sobre um cenário real de Git, não um
tutorial idealizado.

---

## 1. O sintoma

Durante a criação da branch `feature/tests`, o Explorer do VS Code mostrava
as pastas `app/models/`, `app/routes/`, `app/services/` e `database/`
contendo **apenas** `__init__.py` e `__pycache__` — sem os arquivos `.py`
com o código real (schemas, rotas, services, conexão com banco).

A reação inicial foi de preocupação: "o projeto está corrompido?".

---

## 2. Por que não era corrupção (o primeiro diagnóstico correto)

A pasta `__pycache__` continha arquivos `.pyc` (`tarefa.cpython-312.pyc`,
`tarefas.cpython-312.pyc`, etc.) — esses arquivos só são gerados quando o
Python **importa de fato** um módulo `.py` correspondente. A existência
deles era prova de que os arquivos fonte tinham existido e funcionado em
algum momento recente.

Isso eliminou a hipótese de "nunca existiu" e apontou para duas
possibilidades: (a) os arquivos foram apagados depois de existir, ou (b)
nunca foram comitados, e a branch atual simplesmente não tinha acesso a
eles.

---

## 3. Confirmando a causa raiz

```bash
git status
```
Não mostrou os arquivos como "deleted" — se tivessem sido removidos depois
de comitados, apareceriam aqui. Isso reduziu a hipótese a "nunca foram
incluídos nesta branch".

```bash
git show --stat HEAD
```
Revelou que o `HEAD` da branch (`feature/tests`, criada a partir de
`main`) apontava para o commit `692f3ec` — **o commit da Sessão 1**,
datado de 15/06/2026. Ou seja: a branch `feature/tests` tinha nascido de
um ponto do histórico muito anterior a todo o trabalho de CRUD,
SQLAlchemy e Services.

```bash
git log --all --oneline
```
Confirmou que **todo o trabalho existia**, em commits já mergeados via
Pull Requests (#1, #2, #3) dentro da branch `feature/backend` — só que o
`main` nunca tinha recebido esses merges de fato. `main` estava "preso" no
commit da Sessão 1 desde aquela época, apesar de PRs anteriores parecerem
ter sido concluídos.

**Causa raiz:** o `main` remoto e local estavam desatualizados em relação
ao trabalho real, feito e mergeado dentro de `feature/backend`. Qualquer
branch nova criada a partir de `main` nesse estado nasceria sem o código
recente — exatamente o que aconteceu com `feature/tests`.

---

## 4. A recuperação, passo a passo

### 4.1 Resgatar o ponto certo do histórico

```bash
git checkout feature/backend
```
Bloqueado na primeira tentativa: havia uma mudança não comitada em
`requirements.txt` (a instalação do `httpx`) que seria perdida na troca.

```bash
git stash
git checkout feature/backend
```
O `stash` guardou a mudança pendente sem comitá-la, liberando a troca de
branch. Confirmado com `find .` que todos os arquivos reais estavam
presentes em `feature/backend`.

### 4.2 Corrigir o `main`

```bash
git checkout main
git merge feature/backend
git push origin main
```
Como `main` estava atrás de `feature/backend` sem nenhum commit conflitante
entre os dois, o merge foi um **fast-forward** — o ponteiro de `main`
simplesmente avançou para o commit mais recente, sem necessidade de
resolver nada.

### 4.3 Recriar a branch de testes do ponto certo

```bash
git branch -D feature/tests
git checkout main
git checkout -b feature/tests
```
A branch antiga (nascida errada) foi apagada e recriada a partir do `main`
agora corrigido.

### 4.4 Recuperar o trabalho que estava no stash

```bash
git stash pop
```
Gerou um **conflito de merge** em `requirements.txt`: a versão "Updated
upstream" (já presente após o merge de `feature/backend`) e a versão
"Stashed changes" (com `httpx` e suas dependências) tinham conteúdo
diferente nas mesmas linhas. Resolvido manualmente, mantendo ambas as
linhas necessárias (`certifi`, `sniffio`) e removendo os marcadores de
conflito (`<<<<<<<`, `=======`, `>>>>>>>`).

```bash
git add requirements.txt
git add .
git commit -m "JLA - chore: adiciona httpx, recupera conftest.py e test_tarefas.py após reorganização de branches"
git push origin feature/tests
```

### 4.5 Abrir e mergear o Pull Request

PR aberto na interface do GitHub (`feature/tests` → `main`) e mergeado.
Verificado com `git pull origin main` localmente.

### 4.6 Repetir o ciclo limpo

Como a branch `feature/tests` original já tinha sido mergeada, ela foi
apagada e recriada mais uma vez — agora de forma limpa, a partir do `main`
já correto:
```bash
git branch -D feature/tests
git checkout -b feature/tests
```

**Resultado:** nenhum trabalho foi perdido. O incidente todo foi sobre
**branches apontando para o lugar errado**, nunca sobre arquivos
deletados de verdade.

---

## 5. Lições registradas

1. **Antes de criar qualquer branch nova, confirmar visualmente que o
   ponto de partida está atualizado** — `git log --oneline -5` na branch
   base, checando se o commit esperado aparece no topo.
2. **`__pycache__`/`.pyc` são evidência forense útil** — provam que um
   arquivo `.py` existiu e foi executado, mesmo que o `.py` não esteja mais
   visível naquele exato ponto do histórico.
3. **Um merge de PR no GitHub não garante automaticamente que `main`
   local/remoto está sincronizado** se houver desalinhamentos anteriores no
   histórico — vale conferir com `git log --all --oneline` quando algo
   parecer inconsistente.
4. **`git stash` é a ferramenta certa para "pausar" um trabalho no meio**
   sem precisar commitar algo incompleto, especialmente ao trocar de branch
   em cima de mudanças não finalizadas.
5. **Conflitos de merge em `requirements.txt` são normais e de baixo risco
   de resolver** — geralmente basta entender quais linhas pertencem a cada
   lado e manter as duas, sem perder dependências reais.

---

# Incidente 2 — Banco de dados local apagado durante operações de Git

**Data:** 14/07/2026
**Contexto:** Sessão de configuração do Cypress + Cucumber, logo após
corrigir o rastreamento do `database/task_manager.db` no `.gitignore`.

## 1. O sintoma

Ao rodar `find` na raiz do projeto, `database/task_manager.db` não aparecia
mais na listagem — só o `database/task_manager.sqbpro` (arquivo de
configuração do DB Browser). O arquivo do banco em si tinha sumido do
disco.

Apesar disso, a aplicação (`index.html`, com o servidor `uvicorn` já em
execução) continuava mostrando as tarefas normalmente, inclusive após um
`Ctrl+F5` (recarregamento forçado, sem cache).

## 2. Diagnóstico em andamento — a conexão "fantasma"

A explicação mais provável nesse ponto: o processo do `uvicorn`, já em
execução havia algum tempo, mantinha uma conexão aberta com o arquivo
antigo. Em sistemas do tipo Unix, um processo consegue continuar lendo um
arquivo já removido do sistema de arquivos até fechar a conexão — o que
explicaria os dados ainda aparecerem no navegador mesmo com o arquivo já
ausente no disco. (Esse comportamento é menos comum no Windows puro, mas o
ambiente aqui é Git Bash/MINGW64, que se aproxima mais da semântica Unix
nesse ponto — daí a suspeita, sem confirmação absoluta do mecanismo.)

## 3. Causa raiz — não totalmente confirmada

A sequência de comandos executada imediatamente antes do sintoma aparecer
foi:
```bash
git add docs/GUIDE.md
git commit -m "docs: atualiza GUIDE.md com Sessão 12"
echo "database/*.db" >> .gitignore
git rm --cached database/task_manager.db
git add .gitignore
git commit -m "chore: remove task_manager.db do controle de versão"
git checkout main
git pull origin main
git checkout feature/frontend
git merge main
```

A suspeita principal: no momento do `git checkout main`, o arquivo ainda
estava referenciado de alguma forma na árvore de `main` (que não tinha
recebido a remoção do rastreamento feita em `feature/frontend`) — o log do
merge seguinte mostrou explicitamente `database/task_manager.db | Bin
24576 -> 24576 bytes`, confirmando que o Git tocou no conteúdo do arquivo
durante essa troca de branch. O que exatamente levou da sobrescrita para o
desaparecimento total não foi isolado com certeza — diferente do Incidente
1, aqui a causa raiz **não foi 100% confirmada**, só a sequência de eventos
que precedeu o sintoma.

## 4. A perda de dados

Diferente do Incidente 1, aqui houve **perda de dados real**: antes de um
backup poder ser extraído (via `fetch()` direto no console do navegador,
enquanto a conexão fantasma ainda respondia), o servidor foi reiniciado
duas vezes para corrigir um erro de digitação no comando (`main:api` em vez
de `main:app`). Isso encerrou a conexão que ainda enxergava os dados
antigos. O próximo request contra o arquivo `.db` recriado do zero pelo
SQLite falhou com `sqlite3.OperationalError: no such table: usuarios` — o
arquivo novo não tinha nenhuma tabela, porque a criação de tabelas nunca
foi automática no `main.py`, só um comando manual rodado uma vez na
Sessão 3.5.

**Resultado:** usuário de teste e tarefas cadastradas foram perdidos (dados
de desenvolvimento, sem impacto real — recriados manualmente em seguida).

## 5. A recuperação

```bash
python -c "from database.db import Base, engine; from app.models.tarefa_db import TarefaDB; from app.models.usuario_db import UsuarioDB; Base.metadata.create_all(bind=engine); print('Tabelas recriadas com sucesso')"
```
(Primeira tentativa falhou com `bash: !': event not found` — o `!` dentro
de aspas duplas aciona expansão de histórico do Bash; aspas simples
protegeriam, mas o mais simples foi remover o `!` da mensagem.)

Tabelas recriadas, usuário e tarefas recadastrados manualmente pela
interface.

## 6. Correção estrutural — tornando o banco autossuficiente

Para que a ausência do arquivo `.db` deixe de ser um incidente e passe a
ser autocorrigível, `Base.metadata.create_all(bind=engine)` foi movido para
o carregamento do `main.py`, rodando toda vez que o servidor sobe:

```python
from database.db import Base, engine
from app.models import tarefa_db, usuario_db

Base.metadata.create_all(bind=engine)
```

Essa chamada é **idempotente** — se as tabelas já existem, não faz nada; só
cria as que faltarem. Isso significa que, se o arquivo `.db` desaparecer de
novo por qualquer motivo, o próximo `uvicorn --reload` recria a estrutura
sozinho, sem exigir o comando manual que atrasou a recuperação desta vez.

## 7. Lições registradas

1. **Um arquivo de banco de dados local não deveria ser tocado por
   operações de Git em andamento** — mesmo removido do rastreamento
   (`.gitignore` + `git rm --cached`), ele ainda pode ser afetado por
   `checkout`/`merge` se a remoção não estiver presente em todas as
   branches envolvidas na operação.
2. **Aplicações com servidor em hot-reload escondem problemas de arquivo
   temporariamente** — uma conexão já aberta pode continuar respondendo
   normalmente mesmo com o arquivo já ausente do disco, atrasando a
   percepção do problema até o próximo restart.
3. **Extrair um backup rápido (`fetch()` no console do navegador) é uma
   opção legítima quando se suspeita que um arquivo de dados sumiu, mas o
   processo que ainda o "enxerga" continua rodando** — mas essa janela
   fecha assim que o servidor reinicia, então não deve ser adiada.
4. **Erros de digitação em comandos de restart (`main:api` vs `main:app`)
   podem ter consequência maior que o esperado**, se coincidirem com uma
   janela de recuperação de dados em andamento.
5. **Tornar a criação de schema idempotente e automática no startup** é
   uma rede de segurança de baixo custo — transforma um incidente
   manual-dependente em algo autocorrigível.