from flask import request, redirect, render_template, url_for, flash, session
from flask_login import login_required, login_user,logout_user
from werkzeug.security import generate_password_hash

from consensus_web import db
from .forms import UserEditForm, UserForm, RoleForm, LoginForm

from consensus_web.models import User, Role, ConsensusTask

from consensus_web.decorators import permission_required

from wtforms.validators import Regexp
from . import auth

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
@login_required
@permission_required(ConsensusTask.EXIBIR_USUARIOS)
def exibir_usuarios():
    users = User.query.all()
    return render_template('admin/exibir_usuarios.html', users=users)

@login_required
@auth.route('/admin/add-user',methods = ['GET','POST'])
@permission_required(ConsensusTask.ADMINISTRAR_SISTEMA)
def add_user():
    form = UserForm(request.form)
    roles = Role.query.all()
    if form.validate_on_submit():
        email = form.email.data
        nome = form.nome.data
        sobrenome = form.sobrenome.data
        dt_nascimento = request.form['dt_nascimento_text']
        genero = request.form['genero']
        num_ap = form.num_ap.data
        bloco = form.bloco.data
        senha = form.senha.data
        hash = generate_password_hash(senha)
        role_id = request.form['roles']

        u = User(email=email,password=hash,nome=nome,sobrenome=sobrenome,dataNascimento=dt_nascimento,genero=genero,
                 num=num_ap,bloco=bloco, role = role_id)

        db.session.add(u)
        db.session.commit()
        flash(u"Usuário incluído com sucesso")
        return redirect(url_for('main.index'))
    return render_template("admin/criar_usuario.html", form=form, roles=roles)

@login_required
@auth.route('/admin/edit-user/<user_email>/',methods = ['GET','POST'])
@auth.route('/admin/edit-user/',methods = ['GET','POST'])
@permission_required(ConsensusTask.ADMINISTRAR_SISTEMA)
def edit_user(user_email=None):
    form = UserEditForm(request.form)
    roles = Role.query.all()
    ## se passar o email, recupera user por email e preenche o form c/ seus dados
    if user_email:
        user_preenchido = User.query.get(user_email)
        preencher_form(form,user_preenchido,roles)
    if form.validate_on_submit():
        u = User.query.get(form.email.data)
        nome = form.nome.data
        sobrenome = form.sobrenome.data
        dt_nascimento = request.form['dt_nascimento_text']
        role_id = request.form['roles']
        genero = request.form['alterar_genero']
        num_ap = form.num_ap.data
        bloco = form.bloco.data
        #if request.form['alterar_senha']:
            #TODO:enviar email
        # altera somente o q for diferente do existente
        u.alterar(nome=nome,sobrenome=sobrenome,dt_nascimento=dt_nascimento,role=role_id,genero=genero,num_ap=num_ap,bloco=bloco)

        flash(u"Usuário Alterado com sucesso")
        return redirect(url_for('main.index'))
    return render_template("admin/editar_usuario.html", form=form, roles=roles, user=user_preenchido)


def preencher_form(form,user_preenchido,roles):
    form.email.data = user_preenchido.id
    form.nome.data = user_preenchido.nome
    form.sobrenome.data = user_preenchido.sobrenome
    ## dt_nascimento preenchido manualmente
    ## genero preenchido manualmente
    ## role preenchido manualmente
    if user_preenchido.morador:
        form.num_ap.data = user_preenchido.morador[0].num_ap
        form.bloco.data = user_preenchido.morador[0].bloco
    else:
        del form.num_ap
        del form.bloco
    ## sem alteracao de senha. Para alterá-la, o user recebe um email que direciona p uma tela especifica

    render_template("admin/editar_usuario.html", form=form, roles=roles, user=user_preenchido)

@login_required
@auth.route('/get-permissoes/', methods = ['POST'])
@permission_required(ConsensusTask.ADMINISTRAR_SISTEMA)
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

@login_required
@auth.route('/admin/remove-user/<user_email>/', methods = ['GET','POST'])
@permission_required(ConsensusTask.ADMINISTRAR_SISTEMA)
def excluir_user(user_email):
    u = User.query.get(user_email)
    db.session.delete(u)
    flash(u"Usuário excluído com sucesso")
    return "/"


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