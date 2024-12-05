// Variável para armazenar o ID do administrador
let currentAdminId = null;

// Adicionar o evento de clique nos botões de editar
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const adminId = this.getAttribute('data-id');  // Pega o ID do administrador
            console.log('ID do administrador clicado:', adminId);  // Diagnóstico
            openEditModal(adminId); // Passa o ID para abrir o modal
        });
    });
});

// Função para abrir o modal e preencher os dados do administrador
function openEditModal(adminId) {
    // Exibir o modal
    const modal = document.getElementById('editAdminModal');
    modal.style.display = "block";
  
    // Armazenar o ID do administrador para ser usado na atualização
    currentAdminId = adminId;
    console.log('currentAdminId no modal:', currentAdminId);  // Diagnóstico

    // Fechar o modal ao clicar no "X"
    document.getElementById('closeEditModalBtn').addEventListener('click', () => {
        modal.style.display = "none";
    });
  
    // Fechar o modal se o usuário clicar fora dele
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };

    // Preencher o ID do administrador no formulário
    document.getElementById('editAdminId').value = adminId;
    
    // Não carregamos os dados aqui, vamos carregá-los quando o botão de "Atualizar" for clicado
}

// Enviar os dados editados para o backend quando o formulário for enviado
document.getElementById('editAdminForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio padrão do formulário
  
    // Verificar se o ID do administrador foi corretamente armazenado
    if (currentAdminId === null) {
        alert('ID do administrador não encontrado');
        console.error('currentAdminId não encontrado');  // Diagnóstico
        return;
    }

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
  
    const adminId = currentAdminId; // ID do administrador que será enviado
  
    // Carregar os dados do administrador antes de enviar para atualização
    fetch(`/admin/${adminId}`)
        .then(response => response.json())
        .then(admin => {
            // Preencher os campos com os dados do administrador antes de enviar a atualização
            data.username = data.username || admin.username;
            data.email = data.email || admin.email;
            data.password = data.password || admin.password; // Se o campo de senha não for modificado, mantém o valor atual
  
            // Enviar os dados via PUT para atualizar o administrador
            fetch(`/admin/${adminId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data) // Dados do formulário (incluindo ID)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    document.getElementById('editMessage').innerHTML = 'Administrador atualizado com sucesso!';
                    document.getElementById('editMessage').style.color = 'green';
                    document.getElementById('editMessage').style.display = 'block';
    
                    // Fechar o modal após a atualização
                    document.getElementById('editAdminModal').style.display = 'none';
    
                    // Atualizar a tabela de administradores
                    updateAdminList();
                } else {
                    document.getElementById('editMessage').innerHTML = 'Erro ao atualizar administrador!';
                    document.getElementById('editMessage').style.color = 'red';
                    document.getElementById('editMessage').style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Erro ao atualizar administrador:', error);
                document.getElementById('editMessage').innerHTML = 'Erro ao atualizar administrador!';
                document.getElementById('editMessage').style.color = 'red';
                document.getElementById('editMessage').style.display = 'block';
            });
        })
        .catch(error => {
            console.error('Erro ao carregar dados do administrador:', error);
            document.getElementById('editMessage').innerHTML = 'Erro ao carregar dados do administrador!';
            document.getElementById('editMessage').style.color = 'red';
            document.getElementById('editMessage').style.display = 'block';
        });
});

// Função para atualizar a lista de administradores na tabela
// Função para atualizar a lista de administradores na tabela
function updateAdminList() {
    fetch('/admin')
        .then(response => response.json())
        .then(admins => {
            const tableBody = document.querySelector('.management-table tbody');
            tableBody.innerHTML = ''; // Limpa a tabela

            admins.forEach(admin => {
                const row = document.createElement('tr');
                row.innerHTML = `
                  <!--  <td>${admin.id}</td> -->
                    <td>${admin.username}</td>
                    <td>${admin.email}</td>
                    <td>
                        <div class="actions-container">
                            <button class="btn-action edit-btn" data-id="${admin.id}">
                                <i class="fa-solid fa-pen-to-square"></i> 
                            </button>
                            <button class="btn-action delete-btn" data-id="${admin.id}">
                                <i class="fa-solid fa-trash"></i> 
                            </button>
                        </div>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            // Reaplica a funcionalidade de exclusão e edição
            addDeleteEventListeners();
            addEditEventListeners();
        })
        .catch(error => console.error('Erro ao atualizar a lista de administradores:', error));
}
