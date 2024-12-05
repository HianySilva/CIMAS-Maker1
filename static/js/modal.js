document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("projectModal");
    const addProjectBtn = document.getElementById("addProjectBtn");
    const closeBtn = document.querySelector(".close-btn");

    // Abre o modal
    addProjectBtn.addEventListener("click", () => {
        modal.style.display = "flex";
    });

    // Fecha o modal
    closeBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // Fecha o modal ao clicar fora dele
    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});
