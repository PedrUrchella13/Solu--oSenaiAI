from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from functools import wraps

import sqlite3
import os

# =========================================================
# CONFIGURAÇÕES INICIAIS
# =========================================================

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

app.secret_key = "SENAI_SECRET_KEY"

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# LIMITE DE UPLOAD
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

DEFAULT_IMAGE = "default.png"

# EXTENSÕES PERMITIDAS
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def allowed_file(filename):

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# CONEXÃO COM BANCO
def get_db_connection():

    conn = sqlite3.connect('database.db')

    conn.row_factory = sqlite3.Row

    return conn

# MIDDLEWARE DE LOGIN
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'usuario_id' not in session:

            flash("Faça login para acessar o sistema.")

            return redirect('/login')

        return f(*args, **kwargs)

    return decorated_function

# =========================================================
# ROTAS PÚBLICAS
# =========================================================

# HOME
@app.route('/')
def index():

    return render_template('index.html')

# =========================================================
# CADASTRO
# =========================================================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        tipo = request.form['tipo']

        conn = get_db_connection()

        # VERIFICA DUPLICIDADE
        usuario_existente = conn.execute(
            'SELECT * FROM usuarios WHERE email = ?',
            (email,)
        ).fetchone()

        if usuario_existente:

            conn.close()

            flash("E-mail já cadastrado.")

            return redirect('/register')

        senha_hash = generate_password_hash(senha)

        conn.execute('''
            INSERT INTO usuarios
            (
                nome,
                email,
                senha,
                tipo,
                foto
            )
            VALUES (?, ?, ?, ?, ?)
        ''', (
            nome,
            email,
            senha_hash,
            tipo,
            DEFAULT_IMAGE
        ))

        conn.commit()
        conn.close()

        flash("Usuário cadastrado com sucesso.")

        return redirect('/login')

    return render_template('register.html')

# =========================================================
# LOGIN
# =========================================================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        senha = request.form['senha']

        conn = get_db_connection()

        usuario = conn.execute(
            'SELECT * FROM usuarios WHERE email = ?',
            (email,)
        ).fetchone()

        conn.close()

        if usuario and check_password_hash(
            usuario['senha'],
            senha
        ):

            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            session['usuario_tipo'] = usuario['tipo']
            session['usuario_foto'] = usuario['foto']

            flash("Login realizado com sucesso.")

            return redirect('/dashboard')

        flash("Credenciais inválidas.")

    return render_template('login.html')

# =========================================================
# DASHBOARD
# =========================================================

@app.route('/dashboard')
@login_required
def dashboard():

    return render_template('dashboard.html')

# =========================================================
# PERFIL
# =========================================================

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():

    conn = get_db_connection()

    usuario = conn.execute(
        'SELECT * FROM usuarios WHERE id = ?',
        (session['usuario_id'],)
    ).fetchone()

    if request.method == 'POST':

        if 'foto' not in request.files:

            flash("Nenhuma imagem enviada.")

            return redirect('/perfil')

        file = request.files['foto']

        if file.filename == '':

            flash("Selecione uma imagem.")

            return redirect('/perfil')

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )

            file.save(path)

            conn.execute(
                '''
                UPDATE usuarios
                SET foto = ?
                WHERE id = ?
                ''',
                (
                    filename,
                    session['usuario_id']
                )
            )

            conn.commit()

            session['usuario_foto'] = filename

            flash("Foto atualizada com sucesso.")

        else:

            flash("Formato inválido.")

    conn.close()

    return render_template(
        'perfil.html',
        usuario=usuario
    )

# =========================================================
# CURSOS
# =========================================================

@app.route('/cursos')
def cursos():

    pesquisa = request.args.get('pesquisa', '')

    conn = get_db_connection()

    cursos = conn.execute(
        '''
        SELECT * FROM cursos
        WHERE nome LIKE ?
        ''',
        ('%' + pesquisa + '%',)
    ).fetchall()

    conn.close()

    return render_template(
        'cursos.html',
        cursos=cursos
    )

# =========================================================
# DETALHES DO CURSO
# =========================================================

@app.route('/curso/<int:id>')
def curso_detalhes(id):

    conn = get_db_connection()

    curso = conn.execute(
        'SELECT * FROM cursos WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if not curso:

        return render_template(
            'erro.html',
            mensagem='Curso não encontrado.'
        )

    return render_template(
        'curso_detalhes.html',
        curso=curso
    )

# =========================================================
# ADMINISTRAÇÃO
# =========================================================

@app.route('/admin')
@login_required
def admin():

    if session['usuario_tipo'] != 'gestor':

        flash("Acesso negado.")

        return redirect('/dashboard')

    conn = get_db_connection()

    cursos = conn.execute(
        'SELECT * FROM cursos'
    ).fetchall()

    conn.close()

    return render_template(
        'admin.html',
        cursos=cursos
    )

# =========================================================
# CRIAR CURSO
# =========================================================

@app.route('/criar-curso', methods=['GET', 'POST'])
@login_required
def criar_curso():

    if session['usuario_tipo'] != 'gestor':

        return redirect('/dashboard')

    if request.method == 'POST':

        nome = request.form['nome']
        descricao = request.form['descricao']
        carga_horaria = request.form['carga_horaria']
        duracao = request.form['duracao']
        vagas = request.form['vagas']

        conn = get_db_connection()

        conn.execute(
            '''
            INSERT INTO cursos
            (
                nome,
                descricao,
                carga_horaria,
                duracao,
                vagas
            )
            VALUES (?, ?, ?, ?, ?)
            ''',
            (
                nome,
                descricao,
                carga_horaria,
                duracao,
                vagas
            )
        )

        conn.commit()
        conn.close()

        flash("Curso criado com sucesso.")

        return redirect('/admin')

    return render_template('criar_curso.html')

# =========================================================
# EDITAR CURSO
# =========================================================

@app.route('/editar-curso/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_curso(id):

    if session['usuario_tipo'] != 'gestor':

        return redirect('/dashboard')

    conn = get_db_connection()

    curso = conn.execute(
        'SELECT * FROM cursos WHERE id = ?',
        (id,)
    ).fetchone()

    if not curso:

        conn.close()

        return render_template(
            'erro.html',
            mensagem='Curso não encontrado.'
        )

    if request.method == 'POST':

        nome = request.form['nome']
        descricao = request.form['descricao']
        carga_horaria = request.form['carga_horaria']
        duracao = request.form['duracao']
        vagas = request.form['vagas']

        conn.execute(
            '''
            UPDATE cursos
            SET
                nome = ?,
                descricao = ?,
                carga_horaria = ?,
                duracao = ?,
                vagas = ?
            WHERE id = ?
            ''',
            (
                nome,
                descricao,
                carga_horaria,
                duracao,
                vagas,
                id
            )
        )

        conn.commit()
        conn.close()

        flash("Curso atualizado.")

        return redirect('/admin')

    conn.close()

    return render_template(
        'editar_curso.html',
        curso=curso
    )

# =========================================================
# EXCLUIR CURSO
# =========================================================

@app.route('/deletar-curso/<int:id>')
@login_required
def deletar_curso(id):

    if session['usuario_tipo'] != 'gestor':

        return redirect('/dashboard')

    conn = get_db_connection()

    curso = conn.execute(
        'SELECT * FROM cursos WHERE id = ?',
        (id,)
    ).fetchone()

    if not curso:

        conn.close()

        return render_template(
            'erro.html',
            mensagem='Curso não encontrado.'
        )

    conn.execute(
        'DELETE FROM cursos WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Curso removido com sucesso.")

    return redirect('/admin')

# =========================================================
# LOGOUT
# =========================================================

@app.route('/logout')
def logout():

    session.clear()

    flash("Logout realizado com sucesso.")

    return redirect('/')

# =========================================================
# TRATAMENTO DE ERROS
# =========================================================

@app.errorhandler(404)
def not_found(error):

    return render_template(
        'erro.html',
        mensagem='Página não encontrada.'
    ), 404

@app.errorhandler(413)
def arquivo_muito_grande(error):

    return render_template(
        'erro.html',
        mensagem='Arquivo excede o limite permitido.'
    ), 413

# =========================================================
# EXECUÇÃO
# =========================================================

if __name__ == '__main__':

    # GARANTE EXISTÊNCIA DA PASTA DE UPLOADS
    os.makedirs(
        app.config['UPLOAD_FOLDER'],
        exist_ok=True
    )

    app.run(
        debug=True
    )