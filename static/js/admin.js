// Evento para submissão do formulário de criação de administrador
document.querySelector('#adminForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // Impede o envio tradicional do formulário

    const form = event.target;
    const formData = new FormData(form);

    // Converte o FormData para um objeto simples
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    try {
        // Envia a requisição POST para o backend
        const response = await fetch('/admin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // Enviando como JSON
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();  // Obtém a resposta em formato JSON

        // Verifica o que está sendo retornado pelo backend
        console.log('Resposta do backend:', result);

        // Seleciona o elemento para exibir a mensagem
        const messageElement = document.getElementById('message');
        
        if (response.ok) {
            // Exibe mensagem de sucesso
            messageElement.textContent = typeof result.message === 'string' 
                ? result.message 
                : 'Administrador criado com sucesso!';
            messageElement.style.color = "green";  // Mensagem verde
        } else {
            // Exibe mensagem de erro
            messageElement.textContent = typeof result.error === 'string' 
                ? result.error 
                : 'Erro ao criar administrador.';
            messageElement.style.color = "red";  // Mensagem vermelha
        }

        // Exibe a mensagem
        messageElement.style.display = 'block';

        // Atualiza a lista de administradores
        if (response.ok) {
            updateAdminList();  // Chama a função para atualizar a lista de administradores
            form.reset();  // Reseta os campos do formulário
        }

    } catch (error) {
        console.error('Erro ao criar administrador:', error);
        alert('Erro ao enviar a requisição.');
    }
});

// Função para atualizar a lista de administradores na tabela
async function updateAdminList() {
    try {
        const response = await fetch('/admin');  // Fazendo uma requisição para pegar todos os administradores
        const admins = await response.json();   // Obter a resposta JSON com a lista de administradores

        const tableBody = document.querySelector('.management-table tbody');
        tableBody.innerHTML = '';  // Limpa o corpo da tabela antes de preencher

        // Preenche a tabela com os dados dos administradores
        admins.forEach(admin => {
            const row = document.createElement('tr');
            row.innerHTML = `
               <!-- <td>${admin.id}</td> -->
                <td>${admin.username}</td>
                <td>${admin.email}</td>
                <td>
                    <div class="actions-container">
                        <button class="btn-action edit-btn" data-id="${admin.id}">
                            <i class="fa-solid fa-pen-to-square"></i> Editar
                        </button>
                        <button class="btn-action delete-btn" data-id="${admin.id}">
                            <i class="fa-solid fa-trash"></i> Excluir
                        </button>
                    </div>
                </td>
            `;
            tableBody.appendChild(row);
        });

        // Reaplica a funcionalidade de exclusão (deletar)
        addDeleteEventListeners();
        addEditEventListeners();

    } catch (error) {
        console.error('Erro ao atualizar a lista de administradores:', error);
    }
}

// Função para adicionar os event listeners aos botões de editar
function addEditEventListeners() {
    const editButtons = document.querySelectorAll('.edit-btn');
    
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const adminId = this.getAttribute('data-id');
            console.log("Editando administrador com ID: " + adminId);
            // Aqui você pode adicionar o código para editar o administrador
            alert(`Editar administrador com ID: ${adminId}`);
        });
    });
}

// Função para adicionar os event listeners aos botões de excluir
function addDeleteEventListeners() {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const adminId = this.getAttribute('data-id');
            console.log("Tentando excluir o admin com ID: " + adminId);  // Log para debugar
            
            // Mostra um alerta antes de confirmar a exclusão
            const confirmDelete = confirm(`Você tem certeza que deseja excluir o administrador com ID: ${adminId}?`);

            if (!confirmDelete) {
                console.log("Exclusão cancelada.");
                return;  // Se o usuário cancelar, não faz nada
            }

            try {
                // Requisição para excluir o administrador
                const response = await fetch(`/admin/${adminId}`, {
                    method: 'DELETE',
                });

                const result = await response.json();
                
                if (response.ok) {
                    console.log('Administrador excluído com sucesso!');  // Log para sucesso
                    // Atualiza a lista após a exclusão
                    updateAdminList();
                    alert('Administrador excluído com sucesso!');  // Alerta de sucesso
                } else {
                    console.log('Erro ao excluir administrador: ' + result.message);  // Log de erro
                    alert(result.message || 'Erro ao excluir administrador');  // Alerta de erro
                }

            } catch (error) {
                console.error('Erro ao excluir administrador:', error);  // Log de erro de rede
                alert('Erro ao excluir administrador');
            }
        });
    });
}

// Chama a função para carregar a lista de administradores ao carregar a página
document.addEventListener('DOMContentLoaded', function() {
    updateAdminList();
});
