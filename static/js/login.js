document.querySelector("#loginForm").addEventListener("submit", async (e) => {
    e.preventDefault(); // Impede o envio do formulário

    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(form.action, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",  // Envia os dados como JSON
            },
            body: JSON.stringify(data),  // Converte os dados para JSON
        });

        const result = await response.json();
        console.log("Resposta do servidor:", result); // Log para verificar a resposta

        const messageElement = document.getElementById("message");

        if (response.ok) {
            messageElement.textContent = result.message;
            messageElement.style.color = "green";  // Exibe mensagem de sucesso

            // Verifica se há redirecionamento na resposta e faz o redirecionamento
            if (result.redirect) {
                console.log("Redirecionando para:", result.redirect);  // Log de redirecionamento
                window.location.href = result.redirect;  // Redireciona para a página de destino
            } else {
                messageElement.textContent = "Redirecionamento ausente na resposta.";  // Se não houver redirecionamento
                messageElement.style.color = "red";  // Exibe mensagem de erro
            }
        } else {
            messageElement.textContent = result.error || "Erro ao fazer login.";  // Exibe erro
            messageElement.style.color = "red";  // Exibe mensagem de erro
        }
    } catch (error) {
        console.error("Erro ao enviar formulário:", error);  // Log de erro no console
        const messageElement = document.getElementById("message");
        messageElement.textContent = "Erro inesperado. Tente novamente.";  // Mensagem de erro geral
        messageElement.style.color = "red";  // Exibe mensagem de erro
    }
});
