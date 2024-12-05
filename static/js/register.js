document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault(); // Impede o envio padrão

    const form = e.target;
    const formData = new FormData(form);

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