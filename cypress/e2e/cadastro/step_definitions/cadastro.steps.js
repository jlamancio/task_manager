const { Given, When, Then } = require("@badeball/cypress-cucumber-preprocessor");

const API_URL = "http://127.0.0.1:8000";

let usuarioExistente;

Given("que estou na página de cadastro", () => {
    cy.visit("/cadastro.html");
});

Given("que já existe um usuário cadastrado com e-mail e senha válidos", () => {
    // Mesma estratégia do login.steps.js: cria o usuário direto na API,
    // sem passar pela UI, já que aqui o cenário quer testar a colisão de
    // e-mail, não o fluxo de cadastro em si
    usuarioExistente = {
        email: `usuario_${Date.now()}@teste.com`,
        senha: "123456",
    };
    cy.request({
        method: "POST",
        url: `${API_URL}/auth/cadastro`,
        body: { email: usuarioExistente.email, senha: usuarioExistente.senha },
        failOnStatusCode: false,
    });
});

When("informo um e-mail novo e uma senha válida com confirmação igual", () => {
    cy.get("#email").type(`novo_${Date.now()}@teste.com`);
    cy.get("#senha").type("123456");
    cy.get("#confirmar-senha").type("123456");
});

When("informo o mesmo e-mail já cadastrado e uma senha válida com confirmação igual", () => {
    cy.get("#email").type(usuarioExistente.email);
    cy.get("#senha").type("123456");
    cy.get("#confirmar-senha").type("123456");
});

When("informo um e-mail novo e uma senha com menos de 6 caracteres", () => {
    cy.get("#email").type(`curta_${Date.now()}@teste.com`);
    cy.get("#senha").type("123");
    cy.get("#confirmar-senha").type("123");
});

When("informo um e-mail novo, uma senha válida e uma confirmação diferente", () => {
    cy.get("#email").type(`difere_${Date.now()}@teste.com`);
    cy.get("#senha").type("123456");
    cy.get("#confirmar-senha").type("654321");
});

When("clico em {string}", (texto) => {
    cy.contains("button", texto).click();
});

When("clico em {string} sem preencher nenhum campo", (texto) => {
    cy.contains("button", texto).click();
});

Then("devo ser redirecionado para a página de login", () => {
    cy.url().should("include", "login.html");
});

Then("devo ver a mensagem de erro {string}", (mensagem) => {
    cy.get("#form-erro").should("be.visible").and("contain.text", mensagem);
});

Then("devo permanecer na página de cadastro", () => {
    cy.url().should("include", "cadastro.html");
});
