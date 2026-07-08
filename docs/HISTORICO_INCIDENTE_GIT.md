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
