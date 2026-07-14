(function () {
    const formEl = document.getElementById("form-cadastro");
    const erroEl = document.getElementById("form-erro");
    const btnCadastrar = document.getElementById("btn-cadastrar");

    formEl.addEventListener("submit", cadastrarUsuario);

    function textoDoErro(corpo) {
        // CORREÇÃO: mesmo tratamento do login.js — corpo.detail pode vir como lista
        // de erros de validação (422), não só como string
        if (!corpo || !corpo.detail) return null;
        if (typeof corpo.detail === "string") return corpo.detail;
        if (Array.isArray(corpo.detail)) {
            return corpo.detail.map((item) => item.msg || JSON.stringify(item)).join(" | ");
        }
        return null;
    }

    async function cadastrarUsuario(evento) {
        evento.preventDefault();
        erroEl.hidden = true;

        const email = document.getElementById("email").value;
        const senha = document.getElementById("senha").value;
        const confirmarSenha = document.getElementById("confirmar-senha").value;

        if (senha !== confirmarSenha) {
            erroEl.textContent = "as senhas não coincidem.";
            erroEl.hidden = false;
            return;
        }

        btnCadastrar.disabled = true;

        try {
            const resposta = await cadastrar(email, senha);

            if (!resposta.ok) {
                const corpo = await resposta.json().catch(() => ({}));
                erroEl.textContent = textoDoErro(corpo) || "não foi possível criar a conta.";
                erroEl.hidden = false;
                return;
            }

            window.location.href = "login.html";
        } catch (erro) {
            erroEl.textContent = "não foi possível conectar ao servidor. verifique se a API está rodando.";
            erroEl.hidden = false;
        } finally {
            btnCadastrar.disabled = false;
        }
    }
})();
