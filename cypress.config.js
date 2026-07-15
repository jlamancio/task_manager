const { defineConfig } = require("cypress");
const createBundler = require("@bahmutov/cypress-esbuild-preprocessor");
const { addCucumberPreprocessorPlugin } = require("@badeball/cypress-cucumber-preprocessor");
const { createEsbuildPlugin } = require("@badeball/cypress-cucumber-preprocessor/esbuild");

module.exports = defineConfig({
  // ADICIONADO: retry automático só no modo headless (runMode) — se um teste falhar,
  // tenta mais 1 vez antes de marcar como falho de vez. Não mascara bugs reais:
  // se falhar 2x seguidas, continua sendo reportado como falha. Ajuda com flakiness
  // de infraestrutura (ex: Electron perdendo foco entre specs), não com bugs de lógica.
  // openMode: 0 mantém o Cypress App (uso manual/debug) sem retry, para não esconder
  // um problema real enquanto você está olhando o teste rodar.
  retries: {
    runMode: 1,
    openMode: 0,
  },
  e2e: {
    baseUrl: "http://127.0.0.1:5500/frontend",
    specPattern: "cypress/e2e/**/*.feature",
    async setupNodeEvents(on, config) {
      await addCucumberPreprocessorPlugin(on, config);
      on("file:preprocessor", createBundler({ plugins: [createEsbuildPlugin(config)] }));
      return config;
    },
  },
});