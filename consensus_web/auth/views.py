from flask import request, redirect, render_template, url_for, flash
from flask_login import login_required, session, login_user,logout_user
from werkzeug.security import generate_password_hash

from consensus_web import db
from consensus_web.main.forms import LoginForm
from consensus_web.models import User, Role
from . import auth
from .forms import UserForm, RoleForm


@auth.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        session['proximo'] = request.values.get('next')
    if request.method == 'POST' and form.validate():
        user = User.query.get(form.email.data)
        if user is not None and user.is_senha_correta(form.password.data):
            if login_user(user, form.remember_me.data):
                if session.get('proximo') is None:
                    return redirect(url_for('main.index'))
                return redirect(session.get('proximo'))
        else:
            flash("Usuário ou senha inválida")
    return render_template('login.html', form=form)


@auth.route('/admin/users',methods = ['GET','POST'])
def exibir_usuarios():
    users = User.query.all()
    return render_template('exibir_usuarios.html', users=users)


@auth.route('/admin/add-user',methods = ['GET','POST'])
def add_user():
    form = UserForm(request.form)
    roles = Role.query.all()
    if form.validate_on_submit():
        email = form.email.data
        nome = form.nome.data
        sobrenome = form.sobrenome.data
        dt_nascimento = request.form['dt_nascimento_text']
        genero = request.form['genero'][:1] # substring (somente o caracter 1)
        num_ap = form.num_ap.data
        bloco = form.bloco.data
        senha = form.senha.data
        hash = generate_password_hash(senha)
        role_nome = request.form['role']
        role = Role.query.filter(Role.nome == role_nome).all()

        u = User(email=email,password=hash,nome=nome,sobrenome=sobrenome,dataNascimento=dt_nascimento,genero=genero,
                 num=num_ap,bloco=bloco, role = role.id)

        db.session.add(u)
        db.session.commit()
        flash(u"Sugestão de Item de Pauta incluída com sucesso")
        return redirect(url_for('main.index'))
    return render_template("admin/criar_usuario.html", form=form, roles=roles)


@auth.route('/get-permissoes/', methods = ['POST'])
def get_permissoes():
    try:
        role_id = request.form['role_id']
        if role_id:
            permissoes = [p.nome for p in Role.query.get(role_id).permissoes]
            lista = str(permissoes)
            return lista
        else:
            # gravar erro especifico na log
            return ""
    except Exception as e:
        # gravar erro especifico na log
        return ""


@auth.route('/admin/remove-user/<user_email>/', methods = ['GET','POST'])
def excluir_user(user_email):
    u = User.query.get(user_email)
    db.session.delete(u)
    flash(u"Usuário excluído com sucesso")
    return redirect(url_for('main.index'))


@auth.route('/admin/add-role-user', methods=['GET', 'POST'])
def atribuir_role_user():
    form = RoleForm(request.form)
    if form.validate_on_submit():
        u = form.usuario
        r = form.role
        user = User.query.get(u)
        role = Role.query.filter(Role.nome == r).all()
        user.role = role
        db.session.add(user)
        db.session.commit()
        flash(u"Permissões atribuídas com sucesso")
        return redirect(url_for('main.index'))
    return render_template("admin/atribuir_role_usuario.html", form=form)


@login_required
@auth.route('/logout')
def logout():
    logout_user()
    flash('Você foi desconectado do sistema')
    return redirect(url_for('auth.login'))


############################################################################################################
 ######################################### GERACAO DE TOKEN ##############################################
############################################################################################################
#
# @auth.route('/novo-token')
# def gerar_token():
#     s = JSONWebSignatureSerializer('secret-key')
#     db.find_by_name_and_password()
#     token = s.dumps({'username': JaneDoe, 'password' : 'secret'})
#
# @auth.route('/validar-token')
# def validar_token(token):
#     s = JSONWebSignatureSerializer('secret-key')
#     credential = s.loads(token)