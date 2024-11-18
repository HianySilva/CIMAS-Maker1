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
        const messageElement = document.getElementById("message");

        if (response.ok) {
            // Exibe a mensagem de sucesso
            messageElement.textContent = result.message;
            messageElement.style.color = "green";  // Define a cor como verde para o sucesso

            // Redireciona para o dashboard adequado
            if (result.redirect === '/admin_dashboard') {
                window.location.href = '/admin_dashboard';
            } else if (result.redirect === '/user_dashboard') {
                window.location.href = '/user_dashboard';
            }
        } else {
            // Exibe a mensagem de erro
            messageElement.textContent = result.error || "Erro ao fazer login.";
            messageElement.style.color = "red";  // Define a cor como vermelha para o erro
        }
    } catch (error) {
        console.error("Erro ao enviar formulário:", error);
        const messageElement = document.getElementById("message");
        messageElement.textContent = "Erro inesperado. Tente novamente.";
        messageElement.style.color = "red";  // Em caso de erro inesperado, exibe a mensagem em vermelho
    }
});
