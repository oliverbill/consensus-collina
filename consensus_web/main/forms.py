from flask_wtf import Form
from wtforms.fields import StringField, BooleanField, SubmitField, PasswordField, TextAreaField, \
    SelectField
from wtforms.validators import DataRequired, Email

from consensus_web.models import OpcaoVoto


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(message=u"por favor, informe seu e-mail"),
                                             Email(message=u"por favor, informe um e-mail válido")],
                        render_kw={"placeholder": "e-mail", "class" : "form-username form-control"})

    password = PasswordField('Senha', validators=[DataRequired(message="por favor, informe sua senha")],
                            render_kw = {"placeholder": "senha", "class" : "form-password form-control", "size" : "10" })

    remember_me = BooleanField(u'Lembre me')

    submit = SubmitField(u'Entrar', render_kw = {"class" : "btn btn-default"})

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


class SugerirItemPautaForm(Form):
    titulo = StringField(u'Título: ', validators=[DataRequired("campo obrigatório")])
    descricao = TextAreaField(u'Descrição: ', validators=[DataRequired("campo obrigatório")])
#    assembleia = SelectField(u'Assembléia: ', coerce=int)
    autor = StringField('Autor: ')
#    anexos = FileField('Anexo: ')
    votacao = SelectField(u'Opções de Voto: ', coerce=int)
    salvar = SubmitField(u'Salvar Sugestão',render_kw={"class":"btn btn-default"})
#    fazer_upload = SubmitField(u'Fazer Upload')

    def __init__(self, *args, **kwargs):
        super(SugerirItemPautaForm, self).__init__(*args, **kwargs)
#        assembleias = Assembleia.query.filter_by(_status='CRIADA').order_by("num").all()
#        self.assembleia.choices =  [(a.num,a.dataHoraCriacao) for a in assembleias]
        opcoes_votacao = OpcaoVoto.query.all()
        self.votacao.choices = [(o.num,o.nome) for o in opcoes_votacao]


# class CriarAssembleiaForm(Form):
#     data_inicio = DateTimeField(u'Data de Início: ',
#                                 validators=[DataRequired("Data de Início obrigatória")],
#                                 format="%Y-%m-%dT%H:%M") # passar o formato retornado pelo input html5
#
#     data_fim = DateTimeField(u'Data de Término: ',
#                                 validators=[DataRequired("Data de Término obrigatória")],
#                                 format="%Y-%m-%dT%H:%M")
#
#     salvar = SubmitField(u'Criar Assembléia', render_kw={"class": "btn btn-default"})
#
#     def __init__(self, *args, **kwargs):
#         super(CriarAssembleiaForm, self).__init__(*args, **kwargs)
