(function () {
    const token = getToken();
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    const listaEl = document.getElementById("lista-tarefas");
    const vazioEl = document.getElementById("estado-vazio");
    const carregandoEl = document.getElementById("estado-carregando");
    const formEl = document.getElementById("form-tarefa");
    const btnNova = document.getElementById("btn-nova-tarefa");
    const btnCancelar = document.getElementById("btn-cancelar");
    const erroEl = document.getElementById("form-erro");
    const countPendente = document.getElementById("count-pendente");
    const countAndamento = document.getElementById("count-andamento");
    const countConcluida = document.getElementById("count-concluida");

    document.getElementById("usuario-email").textContent = decodificarEmailDoToken(token);
    document.getElementById("btn-logout").addEventListener("click", logout);
    btnNova.addEventListener("click", () => abrirFormulario());
    btnCancelar.addEventListener("click", () => fecharFormulario());
    formEl.addEventListener("submit", salvarTarefa);

    function decodificarEmailDoToken(tokenAtual) {
        try {
            const payloadBase64 = tokenAtual.split(".")[1];
            const payloadJson = atob(payloadBase64.replace(/-/g, "+").replace(/_/g, "/"));
            const payload = JSON.parse(payloadJson);
            return payload.sub || "";
        } catch (erro) {
            return "";
        }
    }

    function abrirFormulario(tarefa) {
        erroEl.hidden = true;
        if (tarefa) {
            document.getElementById("tarefa-id").value = tarefa.id;
            document.getElementById("titulo").value = tarefa.titulo;
            document.getElementById("descricao").value = tarefa.descricao || "";
            document.getElementById("status").value = tarefa.status;
            document.getElementById("prioridade").value = tarefa.prioridade;
            document.getElementById("data_vencimento").value = tarefa.data_vencimento;
        } else {
            formEl.reset();
            document.getElementById("tarefa-id").value = "";
        }
        formEl.hidden = false;
        document.getElementById("titulo").focus();
    }

    function fecharFormulario() {
        formEl.hidden = true;
        formEl.reset();
    }

    async function salvarTarefa(evento) {
        evento.preventDefault();
        erroEl.hidden = true;

        const id = document.getElementById("tarefa-id").value;
        const dados = {
            titulo: document.getElementById("titulo").value,
            descricao: document.getElementById("descricao").value,
            status: document.getElementById("status").value,
            prioridade: document.getElementById("prioridade").value,
            data_vencimento: document.getElementById("data_vencimento").value
        };

        const resposta = id
            ? await atualizartarefa(id, dados)
            : await criarTarefa(dados);

        if (resposta.status === 401) {
            redirecionarParaLogin();
            return;
        }

        if (!resposta.ok) {
            erroEl.textContent = "não foi possível salvar. confira os campos e tente novamente.";
            erroEl.hidden = false;
            return;
        }

        fecharFormulario();
        await carregarTarefas();
    }

    async function excluirTarefa(id) {
        const confirmado = window.confirm("excluir esta tarefa?");
        if (!confirmado) return;

        const resposta = await deletarTarefa(id);
        if (resposta.status === 401) {
            redirecionarParaLogin();
            return;
        }
        await carregarTarefas();
    }

    function redirecionarParaLogin() {
        removeToken();
        window.location.href = "login.html";
    }

    function classeStatus(status) {
        if (status === "em_andamento") return "andamento";
        if (status === "concluida") return "concluida";
        return "pendente";
    }

    function renderTarefas(tarefas) {
        listaEl.innerHTML = "";

        if (tarefas.length === 0) {
            vazioEl.hidden = false;
            countPendente.textContent = "00";
            countAndamento.textContent = "00";
            countConcluida.textContent = "00";
            return;
        }
        vazioEl.hidden = true;

        const contagem = { pendente: 0, em_andamento: 0, concluida: 0 };

        tarefas.forEach((tarefa, indice) => {
            contagem[tarefa.status] = (contagem[tarefa.status] || 0) + 1;

            const li = document.createElement("li");
            li.className = "tarefa tarefa--" + classeStatus(tarefa.status);

            li.innerHTML =
                '<span class="tarefa__num">#' + String(indice + 1).padStart(3, "0") + '</span>' +
                '<div class="tarefa__corpo">' +
                    '<p class="tarefa__titulo"></p>' +
                    '<p class="tarefa__desc"></p>' +
                    '<div class="tarefa__meta">' +
                        '<span class="tarefa__venc"></span>' +
                        '<span class="tarefa__badge"></span>' +
                        '<span class="tarefa__status"></span>' +
                    '</div>' +
                '</div>' +
                '<div class="tarefa__acoes">' +
                    '<button type="button" class="btn-editar">editar</button>' +
                    '<button type="button" class="btn-excluir">excluir</button>' +
                '</div>';

            li.querySelector(".tarefa__titulo").textContent = tarefa.titulo;
            li.querySelector(".tarefa__desc").textContent = tarefa.descricao || "";
            li.querySelector(".tarefa__venc").textContent = "venc: " + (tarefa.data_vencimento || "—");
            li.querySelector(".tarefa__status").textContent = tarefa.status;

            const badgeEl = li.querySelector(".tarefa__badge");
            badgeEl.textContent = tarefa.prioridade;
            badgeEl.classList.add("badge--" + tarefa.prioridade);

            li.querySelector(".btn-editar").addEventListener("click", () => abrirFormulario(tarefa));
            li.querySelector(".btn-excluir").addEventListener("click", () => excluirTarefa(tarefa.id));

            listaEl.appendChild(li);
        });

        countPendente.textContent = String(contagem.pendente || 0).padStart(2, "0");
        countAndamento.textContent = String(contagem.em_andamento || 0).padStart(2, "0");
        countConcluida.textContent = String(contagem.concluida || 0).padStart(2, "0");
    }

    async function carregarTarefas() {
        carregandoEl.hidden = false;
        vazioEl.hidden = true;
        listaEl.innerHTML = "";

        const resposta = await listarTarefas();

        if (resposta.status === 401) {
            redirecionarParaLogin();
            return;
        }

        const tarefas = await resposta.json();
        carregandoEl.hidden = true;
        renderTarefas(tarefas);
    }

    carregarTarefas();
})();
