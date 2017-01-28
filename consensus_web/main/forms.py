from flask_wtf import Form
from wtforms.fields import StringField, BooleanField, SubmitField, PasswordField, TextAreaField, \
    SelectField, FieldList
from wtforms.validators import DataRequired, Email

from consensus_web.models import OpcaoVoto


class SugerirItemPautaForm(Form):
    titulo = StringField(u'Título: ', validators=[DataRequired("campo obrigatório")])
    descricao = TextAreaField(u'Descrição: ', validators=[DataRequired("campo obrigatório")])
#    assembleia = SelectField(u'Assembléia: ', coerce=int)
    autor = StringField('Autor: ')
#    anexos = FileField('Anexo: ')
    votacao = SelectField(u'Opções de Voto: ', coerce=int)
    outra_opcao_voto = FieldList(StringField(u' '), min_entries=2)

    def __init__(self, *args, **kwargs):
        super(SugerirItemPautaForm, self).__init__(*args, **kwargs)
        opcoes_votacao = OpcaoVoto.query.all()
        self.votacao.choices = [(o.num,o.nome) for o in opcoes_votacao]

    def add_opcao_voto(self):
        self.outra_opcao_voto.append_entry(StringField(u' '))

    def validate(self):
        if not Form.validate(self):
            return False
        result = True

        if self.votacao.data == 3:
            for e in self.outra_opcao_voto.entries:
                if not e.data:
                    self.outra_opcao_voto.errors.append('campo obrigatorio')
                    result = False
        return result


class ReprovarSugestaoForm(Form):
    justificativa = TextAreaField(u'Justificativa: ', validators=[DataRequired("campo obrigatório")])

    def __init__(self, *args, **kwargs):
        super(ReprovarSugestaoForm, self).__init__(*args, **kwargs)


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
