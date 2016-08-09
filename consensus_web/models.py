from enum import Enum

from flask_login import UserMixin, current_app, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from consensus_web import db, login_manager


class StatusAssembleia(Enum):
    CRIADA = 'CRIADA'
    EM_ANDAMENTO = 'EM_ANDAMENTO'
    ENCERRADA = 'ENCERRADA'

    @classmethod
    def to_str(cls):
        return ",".join([p for p in cls.__members__])

class Assembleia(db.Model):
    __tablename__ = 'assembleias'

    __num = db.Column(db.BigInteger,primary_key=True,autoincrement=True,name="num")
#
#    no MySql, nao é permitido utilizar funções como valores DEFAULT. Com exceção da CURRENT_TIMESTAMP
#       somente para colunas TIMESTAMP(na versao 5.5) e tb para para DATETIME (na versao > 5.6)
#
#    http: // dev.mysql.com / doc / refman / 5.7 / en / data - type - defaults.html
#
    __dataHoraCriacao = db.Column(db.TIMESTAMP, name="dt_hora_criacao", nullable=False,
                            server_default=db.func.now()) ## invoca function "CURRENT_TIMESTAMP" especifica do mysql

    status = db.Column(db.String(20), server_default='CRIADA')
    __dataHoraInicio = db.Column(db.String(30),name="dt_hora_inicio", nullable=False)
    __dataHoraFim = db.Column(db.String(30), name="dt_hora_fim", nullable=False)

    itemsPautas = relationship("ItemPauta", backref="assembleias", cascade="all, delete-orphan")

    def __init__(self, dtinicio, dtfim):
        super(Assembleia, self).__init__()
        self.__dataHoraInicio = dtinicio
        self.__dataHoraFim = dtfim

    @property
    def sugestoesDosItensPauta(self):
        sugestoes = [(SugestaoItemPauta.query.get(it.sugestao_itempauta)) for it in self.itemsPautas]
        return sugestoes

    @property ## atributo "num" eh somente leitura
    def num(self):
        return self.__num

    @property ## recupera a data no formato 'DD-MM-YY hh:mm:ss' e retorna STRING
    def dataHoraCriacao(self):
        local_datetime = self.__dataHoraCriacao.strftime('%d-%m-%Y %H:%M:%S')
        return local_datetime

    @property
    def dataHoraCriacaoAsDate(self):
        return self.__dataHoraCriacao

    @property
    def dataHoraInicio(self):
        return self.__dataHoraInicio

    @property
    def dataHoraFim(self):
        return self.__dataHoraFim


class StatusItemPauta(Enum):
     CRIADO = 'CRIADO'  # apos aprovacao da sugestao pela sindica
     REPROVADO = 'REPROVADO'  # apos reprovação da sugestao pela sindica
     EM_VOTACAO = 'EM_VOTACAO' # apos atribuição de assembleia
     QUESTIONADO = 'QUESTIONADO'  # por suspeita de infringir o RI
     ANULADO = 'ANULADO'  # caso questionamento seja aceito
     EXCLUIDO = 'EXCLUIDO'  # caso seja criado por erro

     @classmethod
     def to_str(cls):
         return ",".join([p for p in cls.__members__])


class OpcaoVoto(db.Model):
    __tablename__ = 'opcoes_voto'

    __num = db.Column(db.Integer, primary_key=True, autoincrement=True, name="num")
    nome = db.Column(db.String(255), unique=True, nullable=False)

    sugestao_itempauta = db.relationship("SugestaoItemPauta", backref="opcoes_voto", cascade="all, delete-orphan")

    def __init__(self, nome):
        super(OpcaoVoto, self).__init__()
        self.nome = nome

    @property ## atributo "num" eh somente leitura
    def num(self):
        return self.__num


class ItemPauta(db.Model):
    __tablename__ = 'itemspautas'

    __num = db.Column(db.BigInteger,primary_key=True, autoincrement=True, name="num")
    status = db.Column(db.String(70), server_default='APROVADO')

    assembleia = db.Column(db.BigInteger, db.ForeignKey('assembleias.num'), nullable=False, name="num_assembleia")
    sugestao_itempauta = db.Column(db.BigInteger, db.ForeignKey('sugestoes_itempauta.num'),
                                   name="num_sugestao", nullable=False)

    def __init__(self, assembleia, sugestao):
        super(ItemPauta, self).__init__()
        self.assembleia = assembleia
        self.sugestao_itempauta = sugestao

    @property
    def get_obj_sugestao(self):
        return SugestaoItemPauta.query.get(self.sugestao_itempauta)

    @property
    def num(self):
        return self.__num


class SugestaoItemPauta(db.Model):
    __tablename__ = 'sugestoes_itempauta'

    __num = db.Column(db.BigInteger,primary_key=True, autoincrement=True, name="num")
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    status_aprovado = db.Column(db.String(1)) # S:sim, N:nao(reprovado), ' ':ainda nao avaliado
    justif_reprovacao = db.Column(db.String(255))

    autor = db.Column(db.String(70), db.ForeignKey('usuarios.id'), name="email_autor", nullable=False)
    op_voto = db.Column(db.Integer, db.ForeignKey('opcoes_voto.num'), name="opcao_voto", nullable=False)

    anexos = db.relationship("AnexoModel", backref="itemspautas", cascade="all, delete-orphan", lazy='subquery')

    def __init__(self, titulo, autor, desc, opcoes_voto = None, anexos = []):
        super(SugestaoItemPauta, self).__init__()
        self.titulo = titulo
        self.autor = autor
        self.descricao = desc
        self.op_voto = opcoes_voto
        self.anexos = anexos

    @property
    def num(self):
        return self.__num


class Voto(db.Model):
    __tablename__ = 'votos'

    __num = db.Column(db.BigInteger,primary_key=True, autoincrement=True, name="num")
    nome = db.Column(db.String(70), nullable = False)

    autor = db.Column(db.String(70), db.ForeignKey('usuarios.id'), name="email_autor", nullable=False)
    itempauta = db.Column(db.BigInteger, db.ForeignKey('itemspautas.num'), name="num_itempauta", nullable=False)

    @property
    def num(self):
        return self.__num

    def __init__(self, autor_email, itempauta_num, op_nome):
        self.autor = autor_email
        self.itempauta = itempauta_num
        self.nome = op_nome


class AnexoModel(db.Model):
    __tablename__ = 'anexos'

    __num = db.Column(db.BigInteger, name="num", autoincrement=True, primary_key=True)
    pathArquivo = db.Column(db.String(50), name="path", nullable=False)
## o usuario pode mudar o nome do arquivo depois no Google Drive e portanto, invalidar a URL
#     _urlsGoogleDrive = db.Column(db.String(255), name="url_google_drive")
    usuarioGoogleDrive = db.Column(db.String(70), name="usuario_google_drive")

# nao é atualizado pq na criacao da sug item pauta, ainda nao tem a PK
    sugestao_itempauta = db.Column(db.BigInteger, db.ForeignKey('sugestoes_itempauta.num'),nullable=False)

    def __init__(self, path, usuarioGoogleDrive=None):
        super(AnexoModel, self).__init__()
        self.pathArquivo = path
        self.usuarioGoogleDrive = usuarioGoogleDrive

    @property
    def path(self):
        return self.pathArquivo


class User(db.Model,UserMixin):
    __tablename__ = 'usuarios'

    __id = db.Column(db.String(50), name="id", primary_key=True) ## email do usuario

    nome =  db.Column(db.String(20), nullable=False)
    sobrenome = db.Column(db.String(20), nullable=False)
    idade = db.Column(db.String(3), nullable=False)
    genero = db.Column(db.String(1), nullable=False)

    hash_senha = db.Column(db.String(128), nullable=False)
    confirmado = db.Column(db.Boolean, default=False)

    __role = db.Column(db.Integer, db.ForeignKey('roles.id'), name="role_id", nullable=False)

    def __init__(self, email, password, nome, sobrenome, idade, genero, role=None):
        super(User, self).__init__()
        self.__id = email
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade
        self.genero = genero
        self.__role = role
        if self.__role is None:
            if self.__id == current_app.config['ADMIN_USER']:
                self.__role = Role.query.filter_by(_permissoes=ConsensusTask.ADMINISTRAR_SISTEMA).first()
        self.hash_senha = generate_password_hash(password)

    @property
    def role(self):
        return self.__role

    @property
    def id(self):
        return self.__id

    def pode(self, permissions):
        return self.__role is not None and \
               (self.__role._permissoes & permissions) == permissions

    def is_administrador(self):
        return self.can(Permissao.ADMINISTRAR_SISTEMA)

    def is_senha_correta(self, password):
        return check_password_hash(self.hash_senha, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    def gerar_token_confirmacao(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.__id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.__id:
            return False
        self.confirmado = True
        return True


permissoes_roles = db.Table('permissoes_roles', db.metadata,
                             db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
                             db.Column('permissao_id', db.Integer, db.ForeignKey('permissoes.id')) )

class Role(db.Model):
    __tablename__ = 'roles'

    __id = db.Column(db.Integer, primary_key=True, name="id")
    nome = db.Column(db.String(50), unique=True, nullable=False)

    permissoes_da_role = db.relationship("Permissao", backref="roles", cascade="all, delete-orphan",
                                  secondary=permissoes_roles, single_parent = True)

    usuarios = db.relationship("User", backref="roles", cascade="all, delete-orphan" )

    def __init__(self, nome):
        super(Role, self).__init__()
        self.nome = nome


class ConsensusTask(Enum):
    ADMINISTRAR_SISTEMA = 'ADMINISTRAR_SISTEMA'
    SUGERIR_ITEM_PAUTA = 'SUGERIR_ITEM_PAUTA'
    RESPONDER_SUGESTAO_ITEM_PAUTA = 'RESPONDER_SUGESTAO_ITEM_PAUTA'
    GERAR_ATA_ASSEMBLEIA = 'GERAR_ATA_ASSEMBLEIA'
    QUESTIONAR_ITEM_PAUTA = 'QUESTIONAR_ITEM_PAUTA'
    EXCLUIR_ITEM_PAUTA = 'EXCLUIR_ITEM_PAUTA'
    ANULAR_ITEM_PAUTA = 'ANULAR_ITEM_PAUTA'
    RESPONDER_QUESTIONAMENTO = 'RESPONDER_QUESTIONAMENTO'
    CONVOCAR_ASSEMBLEIA_ONLINE = 'CONVOCAR_ASSEMBLEIA_ONLINE'
    PESQUISAR_RI = 'PESQUISAR_RI',
    CRIAR_ENQUETE = 'CRIAR_ENQUETE'
    PUBLICAR_COMUNICADO = 'PUBLICAR_COMUNICADO'
    VOTAR_ITEM_PAUTA = 'VOTAR_ITEM_PAUTA'
    COMENTAR_ITEM_PAUTA = 'COMENTAR_ITEM_PAUTA'
    LISTAR_ASSEMBLEIAS = 'LISTAR_ASSEMBLEIAS'
    CRIAR_ASSEMBLEIA = 'CRIAR_ASSEMBLEIA'
    ALTERAR_ASSEMBLEIA = "ALTERAR_ASSEMBLEIA"
    ATRIBUIR_ASSEMBLEIA = "ATRIBUIR_ASSEMBLEIA"
    DESFAZER_REJEICAO = "DESFAZER_REJEICAO"
    LISTAR_ITEM_PAUTA = "LISTAR_ITEM_PAUTA"

    @classmethod
    def to_str(cls):
        return ",".join([p for p in cls.__members__])


class Permissao(db.Model):
    __tablename__ = 'permissoes'

    __id = db.Column(db.Integer, primary_key=True, name="id")
    nome = db.Column(db.String(30), nullable=False)

    roles_da_permissao = db.relationship("Role", backref="permissoes", cascade="all, delete-orphan",
                                        secondary=permissoes_roles, single_parent=True)

    def __init__(self, nome):
        super(Permissao, self).__init__()
        self.nome = nome


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False