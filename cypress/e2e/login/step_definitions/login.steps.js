const { Given, When, Then, Before } = require("@badeball/cypress-cucumber-preprocessor");

const API_URL = "http://127.0.0.1:8000";

let usuarioTeste;

Before(() => {
    // Gera um e-mail único a cada execução, evitando colidir com "Email já
    // cadastrado" em execuções repetidas contra o banco real (não há reset
    // de banco entre execuções do Cypress, diferente do Pytest com SQLite em memória)
    usuarioTeste = {
        email: `usuario_${Date.now()}@teste.com`,
        senha: "123456",
    };
});

Given("que existe um usuário cadastrado com e-mail e senha válidos", () => {
    cy.request({
        method: "POST",
        url: `${API_URL}/auth/cadastro`,
        body: { email: usuarioTeste.email, senha: usuarioTeste.senha },
        failOnStatusCode: false,
    });
});

Given("que estou na página de login", () => {
    cy.visit("/login.html");
});

When("informo o e-mail e a senha corretos", () => {
    cy.get("#email").type(usuarioTeste.email);
    cy.get("#senha").type(usuarioTeste.senha);
});

When("informo o e-mail correto e uma senha incorreta", () => {
    cy.get("#email").type(usuarioTeste.email);
    cy.get("#senha").type("senha-errada");
});

When("informo um e-mail não cadastrado e qualquer senha", () => {
    cy.get("#email").type(`inexistente_${Date.now()}@teste.com`);
    cy.get("#senha").type("qualquercoisa");
});

When("clico em {string}", (texto) => {
    cy.contains("button", texto).click();
});

When("clico em {string} sem preencher nenhum campo", (texto) => {
    cy.contains("button", texto).click();
});

Then("devo ser redirecionado para a página de tarefas", () => {
    cy.url().should("include", "index.html");
});

Then("o token de acesso deve estar salvo", () => {
    cy.window().then((win) => {
        expect(win.localStorage.getItem("token")).to.exist;
    });
});

Then("devo ver a mensagem de erro {string}", (mensagem) => {
    cy.get("#form-erro").should("be.visible").and("contain.text", mensagem);
});

Then("devo permanecer na página de login", () => {
    cy.url().should("include", "login.html");
});

Given("que já possuo um token de acesso válido salvo", () => {
    cy.request({
        method: "POST",
        url: `${API_URL}/auth/cadastro`,
        body: { email: usuarioTeste.email, senha: usuarioTeste.senha },
        failOnStatusCode: false,
    });

    cy.request({
        method: "POST",
        url: `${API_URL}/auth/login`,
        form: true,
        body: { username: usuarioTeste.email, password: usuarioTeste.senha },
    }).then((resposta) => {
        cy.visit("/login.html", {
            onBeforeLoad(win) {
                win.localStorage.setItem("token", resposta.body.access_token);
            },
        });
    });
});
