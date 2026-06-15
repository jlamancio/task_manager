# Task Manager

Sistema de gerenciamento de tarefas com API back-end e front-end, com cobertura de testes em ambas as camadas.

GitHub: https://github.com/jlamancio/task_manager

---

## Tecnologias

| Camada | Tecnologia | Versão |
|---|---|---|
| Back-end | Python + FastAPI | Python 3.12.9 / FastAPI 0.115.14 |
| Banco de dados | SQLite | A definir |
| Front-end | HTML + CSS + JavaScript puro | - |
| Testes back-end | Pytest | 8.3.5 |
| Testes front-end | Cypress | A definir no setup front-end |
| Servidor | Uvicorn | 0.34.3 |
| Ambiente | Node.js + npm | Node 22.22.3 / npm 10.9.8 |
| Clientes de API | Postman / Insomnia | - |
| Versionamento | Git + GitHub | Git 2.51.0 |

> Todas as versões estão travadas com `==` no requirements.txt. O package.json não utilizará `^` ou `~`.

---

## Pré-requisitos

Antes de rodar o projeto, certifique-se de ter instalado:

- Python 3.12+: https://www.python.org/downloads
- Node.js LTS: https://nodejs.org/en/download
- Git: https://git-scm.com/downloads
- Postman: https://www.postman.com/downloads
- Insomnia: https://insomnia.rest/download

### Validação do ambiente

```bash
python --version
pip --version
node -v
npm -v
git --version
```

---

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/jlamancio/task_manager.git
cd task_manager
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
source venv/Scripts/activate
```

> No Windows com Git Bash use `source venv/Scripts/activate`.
> No Mac/Linux use `source venv/bin/activate`.
>
> Quando ativo, o terminal exibirá `(venv)` no início da linha.

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Verificar as instalações

```bash
pip show fastapi
pip show uvicorn
pip show pytest
```

---

## Estrutura do Projeto

```
task_manager/
├── app/
│   ├── __init__.py
│   ├── models/         → representação dos dados (o "almoxarifado")
│   ├── routes/         → endpoints da API (o "porteiro")
│   └── services/       → regras de negócio (o "cérebro")
├── tests/              → testes automatizados com Pytest
├── venv/               → ambiente virtual (não vai para o GitHub)
├── .gitignore
├── requirements.txt    → dependências com versões travadas
├── README.md
└── GUIDE.md            → diário técnico do projeto
```

---

## Arquitetura

**Back-end — Arquitetura em Camadas:**

| Camada | Responsabilidade |
|---|---|
| Routes | Recebe as requisições |
| Services | Contém as regras de negócio |
| Models | Representa e manipula os dados |

**Front-end:** testes seguem o padrão Page Object Model (POM) com Cypress.

---

## Etapas

- [x] Definição de escopo e stack
- [x] Criação do repositório e README
- [x] Etapa 0 — Setup do ambiente
- [ ] Etapa 1 — Back-end: API + Banco de dados + Testes (Pytest)
- [ ] Etapa 2 — Front-end: Páginas + Testes (Cypress)

---

## Referências

- Python: https://www.python.org
- FastAPI: https://fastapi.tiangolo.com
- SQLite: https://sqlite.org
- JavaScript: https://developer.mozilla.org/pt-BR/docs/Web/JavaScript
- Node.js: https://nodejs.org
- npm: https://www.npmjs.com
- ECMAScript: https://ecma-international.org
- Cypress: https://www.cypress.io
- Pytest: https://docs.pytest.org
- Postman: https://www.postman.com
- Insomnia: https://insomnia.rest
- Git: https://git-scm.com
- GitHub: https://github.com
