from flask import request, redirect, render_template, url_for, flash
from flask_login import login_required, session, login_user,logout_user

from consensus_web.main.forms import LoginForm
from consensus_web.models import User
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