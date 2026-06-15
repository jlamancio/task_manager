# GUIDE — Diário Técnico do Projeto Task Manager

Este arquivo registra as atividades desenvolvidas em cada sessão do projeto,
servindo como material de referência e estudo.

---

## Sessão 1 — Setup do Ambiente
**Data:** 15/06/2025
**Branch:** feature/setup_do_projeto
**Objetivo:** Configurar o ambiente de desenvolvimento e estruturar o projeto.

---

### 1.1 Mapeamento do Ambiente

Antes de qualquer instalação, verificamos o que já estava disponível na máquina:

```bash
python --version   # Python 3.12.9
pip --version      # pip 26.0.1
node -v            # v22.22.3
npm -v             # 10.9.8
git --version      # git version 2.51.0.windows.1
```

**Resultado:** Python, Node.js, npm e Git já estavam instalados e prontos para uso.

---

### 1.2 Versões Escolhidas

Antes de instalar qualquer biblioteca, consultamos as versões disponíveis:

```bash
python -m pip index versions fastapi
python -m pip index versions pytest
python -m pip index versions uvicorn
```

**Critério de escolha:** versões LTS estáveis, com maior número de patches aplicados,
compatíveis entre si e com Python 3.12.9.

| Biblioteca | Versão escolhida | Motivo |
|---|---|---|
| FastAPI | 0.115.14 | Série mais longa e testada |
| Uvicorn | 0.34.3 | Última da série 0.34.x |
| Pytest | 8.3.5 | Última da série 8.3.x |

---

### 1.3 Ambiente Virtual (venv)

**O que é:** uma pasta isolada com uma instalação independente do Python e suas
bibliotecas, separada do Python instalado no sistema.

**Por que usar:** evita conflitos entre projetos diferentes que usam versões
distintas das mesmas bibliotecas.

**Comandos utilizados:**

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual (Windows / Git Bash)
source venv/Scripts/activate
```

> Quando ativo, o terminal exibe `(venv)` no início da linha.

---

### 1.4 Instalação das Dependências

Com o ambiente virtual ativo, instalamos as bibliotecas com versões exatas:

```bash
pip install fastapi==0.115.14 uvicorn==0.34.3 pytest==8.3.5
```

O FastAPI trouxe automaticamente as seguintes dependências:

| Biblioteca | Função |
|---|---|
| starlette | base sobre a qual o FastAPI é construído |
| pydantic | valida os dados que a API recebe e envia |
| anyio | gerencia operações assíncronas |
| click | permite rodar o uvicorn pela linha de comando |
| h11 | protocolo HTTP em Python puro |
| colorama | colore a saída do terminal no Windows |

---

### 1.5 Geração do requirements.txt

O `requirements.txt` registra todas as dependências com versões exatas,
permitindo que qualquer pessoa recrie o ambiente idêntico.

```bash
pip freeze > requirements.txt
```

**Conteúdo gerado:**

```
annotated-types==0.7.0
anyio==4.13.0
click==8.4.1
colorama==0.4.6
fastapi==0.115.14
h11==0.16.0
idna==3.18
iniconfig==2.3.0
packaging==26.2
pluggy==1.6.0
pydantic==2.13.4
pydantic_core==2.46.4
pytest==8.3.5
starlette==0.46.2
typing-inspection==0.4.2
typing_extensions==4.15.0
uvicorn==0.34.3
```

> Para instalar em outra máquina: `pip install -r requirements.txt`

---

### 1.6 Estrutura de Pastas

Criamos a estrutura seguindo a Arquitetura em Camadas definida no guia do projeto:

```bash
mkdir -p app/routes app/services app/models tests
```

**Estrutura criada:**

```
task_manager/
├── app/
│   ├── models/     → representação dos dados
│   ├── routes/     → endpoints da API
│   └── services/   → regras de negócio
└── tests/          → testes automatizados
```

---

### 1.7 Arquivos __init__.py

**O que são:** arquivos vazios que dizem ao Python que aquela pasta é um módulo
e pode ser importado por outros arquivos do projeto.

```bash
touch app/__init__.py
touch app/models/__init__.py
touch app/routes/__init__.py
touch app/services/__init__.py
touch tests/__init__.py
```

---

### 1.8 Configuração do .gitignore

**O que é:** arquivo que instrui o Git a ignorar determinados arquivos e pastas,
evitando que sejam enviados ao GitHub.

```bash
echo "venv/
__pycache__/
*.pyc
.env" > .gitignore
```

**O que ignoramos e por quê:**

| Entrada | Motivo |
|---|---|
| `venv/` | Pesado e cada desenvolvedor cria o seu próprio |
| `__pycache__/` | Arquivos temporários gerados automaticamente pelo Python |
| `*.pyc` | Arquivos compilados do Python, também temporários |
| `.env` | Guardará futuramente informações sensíveis |

---

### 1.9 Primeiro Commit e Push

Verificamos o que seria enviado antes de commitar:

```bash
git add .
git status
```

Realizamos o commit e enviamos para o GitHub:

```bash
git commit -m "JLA - feat: setup inicial do projeto - estrutura de pastas, dependências e gitignore"
git push origin feature/setup_do_projeto
```

**Resultado:** branch `feature/setup_do_projeto` criada no GitHub com 8 arquivos,
101 inserções.

---

### Resumo da Sessão 1

| Atividade | Status |
|---|---|
| Mapeamento do ambiente | ✅ |
| Definição e escolha de versões | ✅ |
| Criação do ambiente virtual | ✅ |
| Instalação das dependências | ✅ |
| Geração do requirements.txt | ✅ |
| Estrutura de pastas criada | ✅ |
| Arquivos __init__.py criados | ✅ |
| .gitignore configurado | ✅ |
| Primeiro commit e push | ✅ |

---

## Sessão 2 — A definir

**Objetivo:** Criar o `main.py` e a primeira rota da API.

