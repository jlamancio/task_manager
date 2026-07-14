const API_URL = "http://127.0.0.1:8000";

function getToken() {
    return localStorage.getItem("token");
}

function salvarToken(token) {
    localStorage.setItem("token", token);
}

function removeToken() {
    localStorage.removeItem("token");
}

async function login(email, senha) {
    const resposta = await fetch(`${API_URL}/auth/login`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, senha })
        });
    return resposta;
}

async function cadastrar(email, senha) {
    const resposta = await fetch(`${API_URL}/auth/cadastro`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, senha })
        });
    return resposta;
}

async function listarTarefas() {
    const resposta = await fetch(`${API_URL}/v1/tarefas/`,
        {
            method: "GET",
            headers: { "Authorization": `Bearer ${getToken()}` },
        });
    return resposta;
}

async function criarTarefa(dados) {
    const resposta = await fetch(`${API_URL}/v1/tarefas/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify(dados)
    });
    return resposta;
}

async function deletarTarefa(id) {
    const resposta = await fetch(`${API_URL}/v1/tarefas/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${getToken()}` }
    });
    return resposta;
}

async function atualizartarefa(id, dados) {
    const resposta = await fetch(`${API_URL}/v1/tarefas/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify(dados)
    });
    return resposta;
}

async function logout() {
    removeToken();
    window.location.href = "login.html";
}







