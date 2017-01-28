from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, PasswordField, SelectField, BooleanField
from wtforms.validators import Optional, DataRequired, Email, Length, Regexp, EqualTo, ValidationError

from consensus_web.models import User, Role


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(message=u"por favor, informe seu e-mail"),
                                             Email(message=u"por favor, informe um e-mail válido")],
                        render_kw={"placeholder": "e-mail", "class" : "form-username form-control"})

    password = PasswordField('Senha', validators=[DataRequired(message="por favor, informe sua senha")],
                            render_kw = {"placeholder": "senha", "class" : "form-password form-control", "size" : "10" })

    remember_me = BooleanField(u'Lembre-me')

    submit = SubmitField(u'Entrar', render_kw = {"class" : "btn btn-default"})

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


class UserForm(Form):
    email = StringField(u'E-mail: ', validators=[DataRequired("campo obrigatório"), Length(1, 64),Email("e-mail inválido")])
    nome = StringField(u'Nome: ',validators=[DataRequired("campo obrigatório")])
    sobrenome = StringField(u'Sobrenome: ',validators=[DataRequired("campo obrigatório")])

    ## dataNascimento criado manualmente
    ## genero criado manualmente

    num_ap = StringField(u'Núm. do Apartamento: ') # n eh "required" pq usuario sendo cadastrado pode nao ser morador
    bloco = StringField(u'Bloco: ') # n eh "required" pq usuario sendo cadastrado pode nao ser morador

    senha = PasswordField(u'Senha: ',validators=[DataRequired("campo obrigatório"),
                                                 Regexp(regex='[A-Za-z0-9@#$%^&+=]{8,10}',
                                                        message="senha deve ter de 8 a 10 caracteres e conter letras, "
                                                                "números e caracteres especiais, e "),
                                                 EqualTo('confirma_senha', message='Senhas não conferem.')])

    confirma_senha = PasswordField(u'Confirme a senha: ', validators=[DataRequired()])

    criar = SubmitField(u'Criar Usuário')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def validate_email(self, field):
        if User.query.get(field.data):
            raise ValidationError(u'Email já cadastrado')

## nenhum campo pode ser obrigatorio ja q o usuario pode alterar qq campo
class UserEditForm(Form):
    email = StringField(u'E-mail: ', validators=[Optional(strip_whitespace=False),Length(1, 64),Email("e-mail inválido")])
    nome = StringField(u'Nome: ', validators=[Optional(strip_whitespace=False)])
    sobrenome = StringField(u'Sobrenome: ', validators=[Optional(strip_whitespace=False)])

    ## dataNascimento criado manualmente
    ## genero criado manualmente

    num_ap = StringField(u'Núm. do Apartamento: ', validators=[Optional(strip_whitespace=False)])
    bloco = StringField(u'Bloco: ', validators=[Optional(strip_whitespace=False)])

    criar = SubmitField(u'Criar Usuário')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        if super(UserEditForm, self).validate():
            if self.num_ap.data != "":
                if self.bloco.data == "":
                    self.bloco.errors.append(u'Informe o bloco do apartamento')
                    return False
            return True;


class RoleForm(Form):
    usuario = SelectField('Usuario:',validators=[DataRequired("campo obrigatório")])
    role = SelectField('Role:', validators=[DataRequired("campo obrigatório")])

    salvar = SubmitField(u'Salvar')

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.usuario.choices = [(u.id, u.nome) for u in User.query.all()]
        self.role.choices =  [(r.id,r.nome) for r in Role.query.all()]