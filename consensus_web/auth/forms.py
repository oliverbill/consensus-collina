from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError

from consensus_web.models import User, Role


class UserForm(Form):
    email = StringField(u'E-mail: ', validators=[DataRequired("campo obrigatório"), Length(1, 64),Email("e-mail inválido")])
    nome = StringField(u'Nome: ',validators=[DataRequired("campo obrigatório")])
    sobrenome = StringField(u'Sobrenome: ',validators=[DataRequired("campo obrigatório")])

    # dataNascimento criado manualmente
    # genero criado manualmente

    num_ap = StringField(u'Núm. do Apartamento: ',validators=[DataRequired("campo obrigatório")])
    bloco = StringField(u'Bloco: ',validators=[DataRequired("campo obrigatório")])

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


class RoleForm(Form):
    usuario = SelectField('Usuario:',validators=[DataRequired("campo obrigatório")])
    role = SelectField('Role:', validators=[DataRequired("campo obrigatório")])

    salvar = SubmitField(u'Salvar')

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.usuario.choices = [(u.id, u.nome) for u in User.query.all()]
        self.role.choices =  [(r.id,r.nome) for r in Role.query.all()]