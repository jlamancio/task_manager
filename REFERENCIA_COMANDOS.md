# Referência de Comandos — Task Manager

Arquivo de consulta rápida para os comandos usados ao longo do projeto,
organizados por categoria. Use `Ctrl+F` para encontrar o que precisa.

> Para o histórico narrativo do incidente de Git (25/06/2026), consulte
> `HISTORICO_INCIDENTE_GIT.md`.

---

## 1. Comandos Git

### 1.1 Diagnóstico

```bash
git status
```
Mostra mudanças não comitadas na branch atual: arquivos modificados,
novos (untracked), e se a branch está sincronizada com a remota.

```bash
git log --oneline -5
```
Lista os últimos 5 commits da branch atual — rápido para confirmar
"onde estou" antes de qualquer ação. **Sempre rodar antes de criar uma
branch nova**, para confirmar que o ponto de partida está atualizado.

```bash
git log --all --oneline
```
Lista commits de **todas** as branches locais, mesmo as inativas — útil
para confirmar se um trabalho "desaparecido" ainda existe em algum lugar.

```bash
git log --all --oneline --graph -10
```
Mesma ideia, mas com representação visual de como as branches se
relacionam (merges, divergências).

```bash
git show --stat HEAD
```
Lista os arquivos que fazem parte do commit mais recente (`HEAD`) e
quantas linhas cada um teve alteradas.

```bash
git fetch origin
```
Busca informações atualizadas do GitHub **sem alterar arquivos locais**.

### 1.2 Commit e push

```bash
git add .
git status
git commit -m "JLA - tipo: descrição curta e objetiva"
git push origin <branch>
```
Sequência padrão de commit. Rodar `git status` depois do `git add .`
para confirmar o que será commitado antes de confirmar.

**Prefixos de commit (Conventional Commits):**

| Prefixo | Quando usar |
|---|---|
| `feat:` | Nova funcionalidade |
| `fix:` | Correção de bug |
| `docs:` | Só documentação |
| `test:` | Adicionar ou ajustar testes |
| `refactor:` | Reorganizar código sem mudar comportamento |
| `chore:` | Tarefas de manutenção (instalar dependência, etc.) |

### 1.3 Branches

```bash
git checkout <branch>
```
Troca para uma branch já existente.

```bash
git checkout -b <nome_da_branch>
```
Cria uma branch nova e já troca para ela. ⚠️ Sempre confirmar com
`git log --oneline -5` que o ponto de partida está atualizado antes.

```bash
git branch -m <nome_novo>
```
Renomeia a branch **atual**.

```bash
git branch -m <nome_antigo> <nome_novo>
```
Renomeia especificando os dois nomes.

```bash
git branch -D <nome_da_branch>
```
Apaga uma branch local à força (seguro quando o conteúdo já foi
mergeado ou recuperado de outra forma).

```bash
git branch
```
Lista as branches locais, destacando em qual você está.

### 1.4 Sincronizar com o GitHub

```bash
git pull origin <branch>
```
Traz atualizações da branch remota e mescla na branch local atual.

```bash
git merge <branch>
```
Mescla outra branch local na branch atual.

### 1.5 Stash — guardar mudanças temporariamente

```bash
git stash
```
Guarda mudanças não comitadas, deixando a pasta limpa — permite trocar
de branch quando o Git bloqueia o checkout por mudanças não salvas.

```bash
git stash pop
```
Traz de volta o que estava no stash. Pode gerar conflito de merge.

```bash
git stash drop
```
Remove uma entrada do stash que não é mais necessária.

### 1.6 Resolvendo conflitos de merge

```bash
grep -E "<<<<<<<|=======|>>>>>>>" <arquivo>
```
Verifica se ainda restam marcadores de conflito. Não deve retornar nada
se a resolução estiver completa.

```bash
git add <arquivo>
```
Marca o arquivo com conflito como resolvido, depois de editar
manualmente.

---

## 2. Comandos Bash (terminal Git Bash / Linux)

### 2.1 Navegação e listagem

```bash
find . -path ./venv -prune -o -path ./.git -prune -o -print | sort
```
Lista todos os arquivos do projeto, ignorando `venv/` e `.git/` — mais
confiável que o Explorer do VS Code para confirmar o que existe no disco.

```bash
ls -la
```
Lista arquivos e pastas com detalhes (permissões, tamanho, data).

```bash
cat <arquivo>
```
Exibe o conteúdo de um arquivo no terminal.

### 2.2 Arquivos e pastas

```bash
mkdir -p app/routes app/services app/models tests
```
Cria pastas (e subpastas) de uma vez. `-p` evita erro se já existirem.

```bash
touch <arquivo>
```
Cria um arquivo vazio.

```bash
cat > <arquivo> << 'EOF'
conteúdo aqui
EOF
```
Cria (ou sobrescreve) um arquivo com conteúdo.
⚠️ Use `>>` em vez de `>` para **adicionar** ao final sem sobrescrever.

### 2.3 Permissões

```bash
chmod +x start.sh
```
Concede permissão de execução a um arquivo — necessário antes de rodar
scripts `.sh` com `./start.sh`.

### 2.4 Ambiente virtual Python

```bash
python -m venv venv
```
Cria o ambiente virtual na pasta `venv/`.

```bash
source venv/Scripts/activate
```
Ativa o ambiente virtual (Windows/Git Bash).
No Mac/Linux: `source venv/bin/activate`.
O prompt exibe `(venv)` quando ativo.

```bash
pip install <pacote>==<versão>
```
Instala uma dependência com versão travada. Sempre usar `==`, nunca `^`
ou `~`.

```bash
pip freeze > requirements.txt
```
Atualiza o `requirements.txt` com o estado atual do ambiente.
**Rodar toda vez que instalar ou remover uma dependência.**

```bash
pip show <pacote>
```
Mostra informações de um pacote instalado (versão, localização).

```bash
pip install -r requirements.txt
```
Instala todas as dependências listadas no `requirements.txt` — usado
para recriar o ambiente em outra máquina.

---

## 3. Comandos Python

### 3.1 Execução rápida (sem criar arquivo)

```bash
python -c 'código aqui'
```
Executa código Python diretamente no terminal, sem criar um arquivo `.py`.
Útil para testes rápidos e validações de import.

```bash
python -c 'from app.models.tarefa import Tarefa; print("OK")'
```
Exemplo: valida que um módulo carrega sem erro de sintaxe ou import.

> ⚠️ No Git Bash, use aspas simples por fora e duplas por dentro para
> evitar o erro `event not found` causado pelo `!` dentro de aspas duplas
> (history expansion do Bash).

### 3.2 Execução de módulos

```bash
python -m <modulo>
```
Executa um módulo instalado como script. Exemplos:

```bash
python -m pytest -v           # roda os testes
python -m json.tool           # formata JSON
python -m pip index versions <pacote>  # lista versões disponíveis
```

### 3.3 Verificação do ambiente

```bash
python --version
pip --version
```
Confirma as versões instaladas.

---

## 4. Comandos Pytest

### 4.1 Execução básica

```bash
python -m pytest
```
Roda todos os testes encontrados no projeto.

```bash
python -m pytest -v
```
Modo verbose — mostra o nome de cada teste e se passou/falhou.

```bash
python -m pytest -vv
```
Extra verbose — mostra detalhes do assert que falhou, com diff completo.

```bash
python -m pytest -v -s
```
Exibe `print()` dentro dos testes, mesmo quando passam (por padrão o
Pytest captura e esconde a saída de testes que passam).

### 4.2 Seleção de testes

```bash
python -m pytest tests/test_tarefas.py -v
```
Roda só os testes de um arquivo específico.

```bash
python -m pytest tests/test_tarefas.py::test_listar_tarefas_vazias -v
```
Roda um único teste específico pelo nome completo.

```bash
python -m pytest -k "put" -v
```
Roda todos os testes cujo nome contenha a palavra "put" — útil para
rodar um grupo de testes relacionados sem especificar cada nome.

### 4.3 Relatórios

```bash
python -m pytest -v --durations=0
```
Exibe o tempo de execução de todos os testes, do mais lento ao mais
rápido.

```bash
python -m pytest -v --html=report.html
```
Gera um relatório HTML completo (requer `pytest-html` instalado).
Abrir o arquivo `report.html` no navegador para visualizar.

> `report.html` e a pasta `assets/` gerada junto devem estar no
> `.gitignore` — são artefatos gerados, não código fonte.

### 4.4 Coleta sem executar

```bash
python -m pytest --collect-only
```
Lista todos os testes que o Pytest encontrou, sem executar nenhum —
útil para verificar se o arquivo de teste está sendo reconhecido
corretamente antes de rodar de verdade.
