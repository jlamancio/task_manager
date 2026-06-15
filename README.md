# Porjeto: Task Manager

Sistema de gerenciamento de tarefas com API back-end e front-end, com cobertura de testes em ambas as camadas.

GitHub: https://github.com/jlamancio/task_manager

---

## Tecnologias

| Camada | Tecnologia | Versão |
|---|---|---|
| Back-end | Python | Python: 3.12.9|
| Back-end | Python | Pip: 26.0.1|
| Back-end | FastApi |  |
| Banco de dados | SQLite | |
| Front-end | NodeJs | 22.22.3 |
| Front-end | Npm |10.9.8 |
| Front-end | HTML + CSS + JavaScript puro | - |
| Testes back-end | Pytest | A definir no setup (LTS) |
| Testes front-end | Cypress | A definir no setup (LTS) |
| Ambiente | Node.js + npm | A definir no setup (LTS) |
| Clientes de API | Postman / Insomnia | - |
| Versionamento | Git + GitHub |2.51.0 |

> Todas as versões serão travadas no setup inicial. O package.json não utilizará `^` ou `~`.

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
- [ ] Etapa 0 — Setup do ambiente
- [ ] Etapa 1 — Back-end: API + Banco de dados + Testes (Pytest)
- [ ] Etapa 2 — Front-end: Páginas + Testes (Cypress)

---

## Validação do ambiente

```bash
python --version
pip --version
node -v
npm -v
git --version
```

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
