(function () {
    if (getToken()) {
        window.location.href = "index.html";
        return;
    }

    const formEl = document.getElementById("form-login");
    const erroEl = document.getElementById("form-erro");
    const btnEntrar = document.getElementById("btn-entrar");

    formEl.addEventListener("submit", entrar);

    function textoDoErro(corpo) {
        // CORREÇÃO: corpo.detail do FastAPI pode ser uma string (erro de negócio,
        // ex: "Email ou senha inválidos") ou uma lista de objetos de validação (422)
        // — sem isso, a lista virava "[object Object],[object Object]" na tela
        if (!corpo || !corpo.detail) return null;
        if (typeof corpo.detail === "string") return corpo.detail;
        if (Array.isArray(corpo.detail)) {
            return corpo.detail.map((item) => item.msg || JSON.stringify(item)).join(" | ");
        }
        return null;
    }

    async function entrar(evento) {
        evento.preventDefault();
        erroEl.hidden = true;
        btnEntrar.disabled = true;

        const email = document.getElementById("email").value;
        const senha = document.getElementById("senha").value;

        try {
            const resposta = await login(email, senha);

            if (!resposta.ok) {
                const corpo = await resposta.json().catch(() => ({}));
                erroEl.textContent = textoDoErro(corpo) || "e-mail ou senha inválidos.";
                erroEl.hidden = false;
                return;
            }

            const dados = await resposta.json();
            salvarToken(dados.access_token);
            window.location.href = "index.html";
        } catch (erro) {
            erroEl.textContent = "não foi possível conectar ao servidor. verifique se a API está rodando.";
            erroEl.hidden = false;
        } finally {
            btnEntrar.disabled = false;
        }
    }
})();
