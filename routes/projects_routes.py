from flask import Blueprint, render_template, request, redirect, url_for,send_from_directory
from entities.project_crud import insert_project, get_all_projects
import os
from werkzeug.utils import secure_filename
projects_bp = Blueprint('projects_bp', __name__, template_folder='templates', static_folder='static')
# Rota para upload de projeto
@projects_bp.route('/upload', methods=['POST'])
def upload_file():
    title = request.form['title']
    description = request.form['description']
    file = request.files['file']
    image = request.files['image']

    # Salvando o arquivo enviado
    file_path = os.path.join('static', 'uploads', 'files', secure_filename(file.filename))
    image_path = os.path.join('static', 'uploads', 'images', secure_filename(image.filename))

    # Garantindo que os diretórios existem
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    # Salvando os arquivos nos locais apropriados
    file.save(file_path)
    image.save(image_path)

    # Salvando dados no banco
    insert_project(title, description, file.filename, image.filename)

    return redirect(url_for('projects_bp.display_projects'))


@projects_bp.route('/projects', methods=['GET'])
def display_projects():
    projects = get_all_projects()  # Busca todos os projetos no banco
    return render_template('projeto.html', projects=projects)

@projects_bp.route('/uploads/<path:filename>')
def serve_uploads(filename):
    """
    Serve arquivos armazenados na pasta uploads.
    """
    return send_from_directory('uploads', filename)

@projects_bp.route('/uploads/files/<filename>')
def download_file(filename):
    # Caminho completo para o diretório de arquivos
    uploads_dir = os.path.join(app.root_path, 'static', 'uploads', 'files')
    
    # Envia o arquivo para o cliente
    return send_from_directory(uploads_dir, filename, as_attachment=True)


@projects_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
def delete_project_route(project_id):
    """
    Remove um projeto.
    """
    project = get_project_by_id(project_id)
    if project:
        # Remove arquivos do sistema de arquivos
        file_path = os.path.join('static', 'uploads', 'files', project[3])
        image_path = os.path.join('static', 'uploads', 'images', project[4])
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(image_path):
            os.remove(image_path)

        # Remove do banco
        delete_project(project_id)
        return redirect(url_for('projects_bp.display_projects'))
    else:
        return "Projeto não encontrado", 404


@projects_bp.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    """
    Permite a edição de um projeto existente.
    """
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files.get('file')
        image = request.files.get('image')

        # Caminhos para salvar novos arquivos, se enviados
        file_path = None
        image_path = None

        if file:
            file_path = os.path.join('static', 'uploads', 'files', secure_filename(file.filename))
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)

        if image:
            image_path = os.path.join('static', 'uploads', 'images', secure_filename(image.filename))
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)

        # Atualiza o projeto no banco
        update_project(project_id, title, description, file_path, image_path)
        return redirect(url_for('projects_bp.display_projects'))

    # Método GET: exibe formulário com os dados atuais do projeto
    project = get_project_by_id(project_id)
    if project:
        return render_template('edit_project.html', project=project)
    else:
        return "Projeto não encontrado", 404