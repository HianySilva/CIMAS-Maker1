document.addEventListener("DOMContentLoaded", () => {
    preencherSelectInstituicoes("institution-select");
});

async function preencherSelectInstituicoes(selectId) {
    const url = "http://127.0.0.1:5000/institutions"; // Substitua pelo endpoint correto

    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                Accept: "application/json",
            },
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP! Status: ${response.status}`);
        }

        const result = await response.json();
        console.log(result); // Verifique o formato da resposta

        const instituicoes = result.institutions; // Acesse o array 'institutions'

        if (Array.isArray(instituicoes)) {
            renderInstituicoesSelect(instituicoes, selectId);
        } else {
            console.error("A resposta não contém um array 'institutions'");
        }

    } catch (error) {
        console.error("Erro ao preencher o select com instituições:", error);
    }
}

function renderInstituicoesSelect(instituicoes, selectId) {
    const selectElement = document.getElementById(selectId);

    if (!selectElement) {
        console.error("Elemento <select> não encontrado!");
        return;
    }

    selectElement.innerHTML = ""; // Limpa as opções anteriores

    const optionDefault = document.createElement("option");
    optionDefault.value = "";
    optionDefault.textContent = "Selecione uma instituição";
    selectElement.appendChild(optionDefault);

    // Itera sobre o array de instituições e cria as opções
    instituicoes.forEach((instituicao) => {
        const option = document.createElement("option");
        option.value = instituicao[0]; // Aqui usamos o primeiro item como valor (ID)
        option.textContent = instituicao[1]; // O segundo item será o nome da instituição
        selectElement.appendChild(option);
    });
}

document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault(); // Impede o envio padrão

    const form = e.target;
    const formData = new FormData(form);

    // Pega o valor selecionado do select de instituições
    const institutionSelect = document.getElementById("institution-select");
    const institutionId = institutionSelect.value;

    // Verifica se uma instituição foi selecionada
    if (!institutionId) {
        const messageElement = document.getElementById("message");
        messageElement.textContent = "Por favor, selecione uma instituição.";
        messageElement.style.color = "red";
        return;
    }

    // Pega o valor do e-mail inserido
    const email = formData.get("email");

    // Verifica se o e-mail e o domínio são válidos
    const emailValid = await verifyEmailDomain(email, institutionId);

    if (!emailValid) {
        const messageElement = document.getElementById("message");
        messageElement.textContent = "Domínio de e-mail não permitido para esta instituição.";
        messageElement.style.color = "red";
        return;
    }

    // Adiciona o id da instituição ao FormData
    formData.append("institution_id", institutionId);
    console.log("ID da Instituição Selecionada:", institutionId); // Ajustado para "institution_id" conforme esperado na rota do Flask

    try {
        const response = await fetch(form.action, {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        const messageElement = document.getElementById("message");

        if (response.ok) {
            messageElement.textContent = result.message;
            messageElement.style.color = "green";
        } else {
            messageElement.textContent = result.error || "Erro ao registrar.";
            messageElement.style.color = "red";
        }
    } catch (error) {
        console.error("Erro ao enviar formulário:", error);
    }
});

// Função para verificar o domínio do e-mail com a API
async function verifyEmailDomain(email, institutionId) {
    try {
        const response = await fetch("http://127.0.0.1:5000/email-domain/verify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, institution_id: institutionId }),
        });

        if (response.ok) {
            return true; // Domínio permitido
        } else {
            const result = await response.json();
            console.error(result.error || "Erro na verificação de domínio");
            return false; // Domínio não permitido
        }
    } catch (error) {
        console.error("Erro ao verificar domínio de e-mail:", error);
        return false; // Em caso de falha na requisição
    }
}
