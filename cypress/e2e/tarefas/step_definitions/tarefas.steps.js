const { Given, When, Then } = require("@badeball/cypress-cucumber-preprocessor");

const API_URL = "http://127.0.0.1:8000";

let token;
let tituloAtual;

Given("que estou autenticado e na página de tarefas", () => {
    const email = `usuario_${Date.now()}@teste.com`;
    const senha = "123456";

    cy.request({
        method: "POST",
        url: `${API_URL}/auth/cadastro`,
        body: { email, senha },
        failOnStatusCode: false,
    });

    cy.request({
        method: "POST",
        url: `${API_URL}/auth/login`,
        form: true,
        body: { username: email, password: senha },
    }).then((resposta) => {
        token = resposta.body.access_token;
        cy.visit("/index.html", {
            onBeforeLoad(win) {
                win.localStorage.setItem("token", token);
            },
        });
    });
});

When("preencho uma nova tarefa com título {string} e vencimento {string}", (titulo, vencimento) => {
    cy.contains("button", "+ nova tarefa").click();
    cy.get("#titulo").type(titulo);
    cy.get("#data_vencimento").type(vencimento);
});

When("abro o formulário de nova tarefa", () => {
    cy.contains("button", "+ nova tarefa").click();
});

When("clico em {string}", (texto) => {
    cy.contains("button", texto).click();
});

When("clico em {string} sem preencher o título", (texto) => {
    // Intercepta a chamada real à API — evidência direta de que o envio
    // foi bloqueado, em vez de inferir só pelo estado visual do formulário
    cy.intercept("POST", `${API_URL}/v1/tarefas/`).as("criarTarefa");
    // Preenche só o vencimento, para isolar a validação do campo título
    // (sem isso, o required do data_vencimento também bloquearia o envio)
    cy.get("#data_vencimento").type("2026-12-31");
    cy.contains("button", texto).click();
});

Then("a tarefa {string} deve aparecer na lista", (titulo) => {
    cy.contains(".tarefa__titulo", titulo).should("be.visible");
});

Then("o formulário de tarefa deve continuar aberto", () => {
    cy.get("@criarTarefa.all").should("have.length", 0);
    cy.get("#form-tarefa").should("be.visible");
});

Given("que existe uma tarefa cadastrada com título {string}", (titulo) => {
    // Criação via API direta (não pela UI) — o cenário quer testar editar/excluir,
    // não testar de novo o fluxo de criação, que já tem cenário próprio
    tituloAtual = titulo;
    cy.request({
        method: "POST",
        url: `${API_URL}/v1/tarefas/`,
        headers: { Authorization: `Bearer ${token}` },
        body: {
            titulo,
            descricao: "",
            status: "pendente",
            prioridade: "media",
            data_vencimento: "2026-12-31",
        },
    });
    cy.reload();
});

When("edito essa tarefa para o título {string}", (novoTitulo) => {
    cy.contains(".tarefa", tituloAtual).within(() => {
        cy.contains("button", "editar").click();
    });
    cy.get("#titulo").clear().type(novoTitulo);
});

When("excluo essa tarefa e confirmo", () => {
    cy.on("window:confirm", () => true);
    cy.contains(".tarefa", tituloAtual).within(() => {
        cy.contains("button", "excluir").click();
    });
});

Then("a tarefa {string} não deve mais aparecer na lista", (titulo) => {
    cy.contains(".tarefa__titulo", titulo).should("not.exist");
});

When("tento atualizar uma tarefa com id inexistente diretamente na API", () => {
    cy.request({
        method: "PUT",
        url: `${API_URL}/v1/tarefas/999999`,
        headers: { Authorization: `Bearer ${token}` },
        failOnStatusCode: false,
        body: {
            titulo: "Não existe",
            descricao: "",
            status: "pendente",
            prioridade: "media",
            data_vencimento: "2026-12-31",
        },
    }).as("respostaApi");
});

When("tento excluir uma tarefa com id inexistente diretamente na API", () => {
    cy.request({
        method: "DELETE",
        url: `${API_URL}/v1/tarefas/999999`,
        headers: { Authorization: `Bearer ${token}` },
        failOnStatusCode: false,
    }).as("respostaApi");
});

Then("a API deve responder com 404", () => {
    cy.get("@respostaApi").its("status").should("eq", 404);
});