// Ação para abrir a modal quando clicar no botão "Adicionar Administrador"
document.querySelector('.add-btn').addEventListener('click', function() {
    document.getElementById('adminModal').style.display = 'block'; // Exibe a modal
    document.querySelector('.dashboard').classList.add('blur'); // Aplica o desfoque no fundo
});

// Ação para fechar a modal
document.getElementById('closeModalBtn').addEventListener('click', function() {
    document.getElementById('adminModal').style.display = 'none'; // Esconde a modal
    document.querySelector('.dashboard').classList.remove('blur'); // Remove o desfoque do fundo
});

// Fechar a modal ao clicar fora dela
window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('adminModal')) {
        document.getElementById('adminModal').style.display = 'none'; // Esconde a modal
        document.querySelector('.dashboard').classList.remove('blur'); // Remove o desfoque
    }
});
