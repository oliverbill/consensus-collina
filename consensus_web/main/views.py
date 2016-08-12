# encoding: utf-8

from datetime import datetime

from flask import request, render_template, url_for, redirect, flash, jsonify, json
from flask_login import login_required, current_user

from . import main
from .utils import incluir_anexos, incluir_opcao_voto, get_op_voto_por_sugestao, \
    remover_itens_ja_votados, nenhum_itempauta_ou_listar_com_op_voto
from .. import db
from ..decorators import permission_required
from ..main.forms import SugerirItemPautaForm
from ..models import ItemPauta, ConsensusTask, Assembleia, OpcaoVoto, Voto, StatusItemPauta, \
    SugestaoItemPauta, ComentariosItemPauta


@main.route('/', methods = ['GET','POST'])
@login_required
def index():
    return render_template("index.html")


############################################
############## ITEM DE PAUTA ###############
############################################

@permission_required(ConsensusTask.LISTAR_ITEM_PAUTA)
@main.route('/listar-itenspauta/<status>', methods = ['GET'])
@login_required
def listar_itens_de_pauta_status(status):
    if status not in StatusItemPauta.__members__:
        flash(u"Status inexistente: " + status)
        return redirect(url_for('main.index'))
    # nao mostra sugestoes. Para isso, utilizar o metodo "listar_itenspautas_sugeridos"
    itens_pauta = ItemPauta.query \
        .filter(ItemPauta.status == status).all()
    return nenhum_itempauta_ou_listar_com_op_voto\
        (u"Não há Itens de Pauta com situação " + status, itens_pauta)


@permission_required(ConsensusTask.LISTAR_ITEM_PAUTA)
@main.route('/listar-itenspauta/<num_assembleia>/', methods = ['GET'])
@login_required
def listar_itens_de_pauta_da_assembleia(num_assembleia):
    itens_pauta = ItemPauta.query\
        .filter(ItemPauta.assembleia == num_assembleia).all()

    return nenhum_itempauta_ou_listar_com_op_voto\
         (u"Não há Itens de Pauta para a Assembléia selecionada", itens_pauta, num_assembleia)

#
# @permission_required(ConsensusTask.LISTAR_ITEM_PAUTA)
# @main.route('/listar-itempauta-em-votacao/', methods = ['GET'])
# @login_required
# def listar_item_pauta_em_votacao():
#     itens_pauta_sugeridos = ItemPauta.query.filter(ItemPauta.status == 'EM_VOTACAO').all()
#     if not itens_pauta_sugeridos:
#         flash(u"Não há Itens de Pauta EM VOTAÇÃO")
#         return redirect(url_for('main.index'))
#
#     itens_pauta_nao_votados_pelo_usuario = remover_itens_ja_votados(itens_pauta_sugeridos, current_user)
#
#     return nenhum_itempauta_ou_listar_com_op_voto \
#         (u"Não há Itens de Pauta PENDENTES de voto por você", itens_pauta_nao_votados_pelo_usuario,
#             is_consulta_em_votacao=True)


@permission_required(ConsensusTask.VOTAR_ITEM_PAUTA)
@main.route('/votar-item-pauta/', methods = ['GET','POST'])
@login_required
def votar_itempauta():
    if request.method == 'GET':
        itens_pauta_sugeridos = ItemPauta.query.filter(ItemPauta.status == 'EM_VOTACAO').all()
        if not itens_pauta_sugeridos:
            flash(u"Não há Itens de Pauta EM VOTAÇÃO")
            return redirect(url_for('main.index'))

        itens_pauta_nao_votados_pelo_usuario = remover_itens_ja_votados(itens_pauta_sugeridos, current_user)

        return nenhum_itempauta_ou_listar_com_op_voto \
            (u"Não há Itens de Pauta PENDENTES de voto por você", itens_pauta_nao_votados_pelo_usuario,
             template="itempauta/listar_itenspauta_em_votacao.html")
    else:
        voto_e_num_itempauta = request.form['link_op_voto']
        voto_e_num_item_split = voto_e_num_itempauta.split(";")
        nome_voto = voto_e_num_item_split[0]
        num_itempauta = voto_e_num_item_split[1]
        autor = current_user.id
        it = ItemPauta.query.get(num_itempauta)
        voto = Voto(autor_email=autor, itempauta_num = it.num, op_nome=nome_voto)

        comentario = request.form["comentario"]
        if comentario:
            c = ComentariosItemPauta(texto=comentario,it=it.num)

        db.session.add(voto)
        db.session.add(c)
        db.session.commit()
        flash("Item de Pauta votado com sucesso")
        return redirect(url_for('main.index'))


############################################
######## SUGESTÕES DE ITEM PAUTA ###########
############################################

@permission_required(ConsensusTask.SUGERIR_ITEM_PAUTA)
## tem q permitir GET por causa do possivel refresh do usuario (post/redirect/get pattern)
@main.route('/sugerir-item-pauta/', methods = ['GET','POST'])
@login_required
def sugerir_itempauta():
    form = SugerirItemPautaForm(request.form)
    form.autor.data = current_user.id
    if form.validate_on_submit():
        op = OpcaoVoto.query.get(form.votacao.data)
        desc_unicode = form.descricao.data.encode()
        sugestao = SugestaoItemPauta(titulo=form.titulo.data, autor=form.autor.data, desc=desc_unicode)
        # se usuario selecionou 'outros' no combo 'opcoes de voto'
        if op.nome.__contains__("outras"):
            combo_votacao_outros = request.form.getlist('txt_outra_opcao')
            if combo_votacao_outros:
                nova_op = incluir_opcao_voto(combo_votacao_outros, db)
                sugestao.op_voto = nova_op.num
        else:
            sugestao.op_voto = op.num
        db.session.add(sugestao)
        db.session.commit()

        incluir_anexos(db, sugestao.num)

        flash(u"Sugestão de Item de Pauta incluída com sucesso")
        return redirect(url_for('main.index'))
    return render_template("itempauta/sugerir_itempauta.html", form = form)


@permission_required(ConsensusTask.LISTAR_ITEM_PAUTA)
@main.route('/listar-sugestoes-sem-avaliacao/', methods = ['GET','POST'])
@login_required
def listar_sugestoes_sem_avaliacao():
    sugestoes = SugestaoItemPauta.query.filter(SugestaoItemPauta.status == 'NAO_AVALIADA').all()
    if not sugestoes:
        flash(u"Não há Sugestões de Item Pauta A AVALIAR")
        return redirect(url_for('main.index'))
    opcoes_voto = get_op_voto_por_sugestao(sugestoes)
    ids = [(it.num) for it in sugestoes] # variavel utilizada na pag. "botoes_aprovar_reprovar.html"
    return render_template("itempauta/listar_sugestoes_itempauta.html",
                           itens_de_pauta = zip(sugestoes,ids), opcoes_voto=opcoes_voto)


@permission_required(ConsensusTask.LISTAR_ITEM_PAUTA)
@main.route('/listar-sugestoes-reprovadas/', methods = ['GET'])
@login_required
def listar_sugestoes_reprovadas():
    sugestoes_reprovadas = SugestaoItemPauta.query.filter(SugestaoItemPauta.status == 'REPROVADA').all()
    return nenhum_itempauta_ou_listar_com_op_voto\
        (u"Não há Sugestões de Item Pauta REPROVADAS", sugestoes_reprovadas,
               "itempauta/listar_sugestoes_reprovadas.html")


@permission_required(ConsensusTask.AVALIAR_SUGESTAO_ITEM_PAUTA)
@main.route('/aprovar-sugestao/<num_sugestao>/', methods = ['POST'])
@login_required
def aprovar_sugestao(num_sugestao):
    sugestao = SugestaoItemPauta.query.get(num_sugestao)
    sugestao.status = 'APROVADA'
    flash(u"Sugestão de Item de Pauta APROVADA com sucesso")
    db.session.add(sugestao)
    db.session.commit()
    return "/"  # retorna a url em texto pq o sistema redireciona via javascript apos o confirm do modal


@permission_required(ConsensusTask.AVALIAR_SUGESTAO_ITEM_PAUTA)
@login_required
@main.route('/reprovar-sugestao/<num_itempauta>', methods = ['POST'])
def reprovar_sugestao(num_itempauta):
    justificativa = request.form["justificativa"]
    sugestao = SugestaoItemPauta.query.get(num_itempauta)
    sugestao.status = 'REPROVADA'
    sugestao.justif_reprovacao = justificativa
    db.session.add(sugestao)
    db.session.commit()
    flash(u"Sugestão de Item Pauta REPROVADA com sucesso")
    return redirect(url_for('main.index'))


@permission_required(ConsensusTask.DESFAZER_REJEICAO)
@login_required
@main.route('/desfazer-reprovacao/<num_sugestao>', methods = ['POST'])
def desfazer_reprovacao(num_sugestao):
    sugestao_reprovada = SugestaoItemPauta.query.get(num_sugestao)
    sugestao_reprovada.status = 'APROVADA'
    # mantendo a justificativa_reprovada para historico
    db.session.add(sugestao_reprovada)
    db.session.commit
    flash(u"Reprovação de Sugestão de Item Pauta DESFEITA com sucesso")
    return redirect(url_for('main.index'))


@permission_required(ConsensusTask.ATRIBUIR_ASSEMBLEIA)
@main.route('/add-itempauta-a-assembleia/', methods = ['POST'])
@login_required
def add_itempauta_a_assembleia():
    try:
        num_sugestao = request.form["sugestao_num"]
        if num_sugestao:
            sugestao = SugestaoItemPauta.query.get(num_sugestao)
            return jsonify(num=sugestao.num,titulo=sugestao.titulo,autor=sugestao.autor)
    except Exception as e:
        flash(u'Erro na Aplicação. Contate o Administrador do Sistema')
        return redirect(url_for('main.index'))


@permission_required(ConsensusTask.ATRIBUIR_ASSEMBLEIA)
@main.route('/atribuir-a-assembleia/', methods = ['GET','POST'])
@login_required
def atribuir_sugestoes_a_assembleia():
    if request.method == 'GET':
        assembleias = Assembleia.query.filter_by(status='CRIADA').order_by("num").all()
        # alimenta o combo
        sugestoes_aprovadas = SugestaoItemPauta.query\
                                .filter(SugestaoItemPauta.status == 'APROVADA').all()

        if not sugestoes_aprovadas:
            flash(u"Não há Sugestões de Item Pauta APROVADAS para atribuir à assembléias")
            return redirect(url_for('main.index'))

        return render_template("itempauta/atribuir_a_assembleia.html",
                    sugestoes=sugestoes_aprovadas, assembleias_combo=assembleias,
                               assembleias_heading=assembleias, )
    else:
        jsonString = request.form['mapa']
        assembleias_sugestoes = json.loads(jsonString)
        assembleias_atribuidas = []
        for num_assembleia in assembleias_sugestoes.keys():
            if assembleias_sugestoes[num_assembleia]:
                for sug_num in assembleias_sugestoes[num_assembleia]:
                    itempauta = ItemPauta(num_assembleia,sug_num)
                    sug = SugestaoItemPauta.query.get(sug_num)
                    if sug:
                        sug.status = 'ATRIBUIDA'
                        db.session.add(sug)
                    db.session.add(itempauta)
                assembleias_atribuidas.append(num_assembleia)
        db.session.commit()

        for n in assembleias_atribuidas:
            a = Assembleia.query.get(n)
            iniciar_assembleia(a) #verifica se a assembleia pode ser iniciada

        flash(u"Assembléias atribuídas com sucesso")
        return "/"  # retorna a url em texto pq o sistema redireciona via javascript apos o confirm do modal

############################################
############### ASSEMBLEIAS ###############
############################################

@permission_required(ConsensusTask.CRIAR_ASSEMBLEIA)
@main.route('/criar-assembleia/', methods = ['GET','POST'])
@login_required
def criar_assembleia():
    if request.method == 'GET':
        return render_template("assembleia/criar_assembleia.html")
    data_inicio = request.form['data_inicio_text']
    data_fim = request.form['data_fim_text']
    assembleia = Assembleia(dtinicio=data_inicio,dtfim=data_fim)
    db.session.add(assembleia)
    db.session.commit()
    flash(u"Assembléia criada com sucesso")
    return redirect(url_for('main.index'))


@permission_required(ConsensusTask.LISTAR_ASSEMBLEIAS)
## tem q permitir GET por causa do possivel refresh do usuario (post/redirect/get pattern)
@main.route('/listar-assembleias/<status>/', methods = ['GET','POST'])
@login_required
def listar_assembleias(status):
    pag_destino = ""
    agora = datetime.now();

    # joinedload = eager loading dos itempautas
    assembleias_criadas = Assembleia.query.filter(Assembleia.status == 'CRIADA').order_by("dt_hora_criacao").all()

    if status == '1':
        pag_destino = "CRIADAS"
        if assembleias_criadas:
            return render_template("assembleia/listar_assembleias_criadas.html",
                                   assembleias=assembleias_criadas, agora=agora)
    elif status == '2':
        for a in assembleias_criadas:
            datainicio = datetime.strptime(a.dataHoraInicio, '%d/%m/%Y %H:%M')

        ## 'em andamento' contendo itens de pauta
        lista = Assembleia.query.filter(Assembleia.status == 'EM_ANDAMENTO') \
                                .filter(Assembleia.itemsPautas) \
                            .order_by("dt_hora_inicio").all()

        pag_destino = "EM ANDAMENTO"
        if lista:
            return render_template("assembleia/listar_assembleias_em_andamento.html",
                                   assembleias=lista, agora=agora, dt_inicio=datainicio)

    elif status == '3':
        lista = Assembleia.query.filter(Assembleia.status == 'ENCERRADA').order_by("dt_hora_fim").all()
        pag_destino = "ENCERRADAS"
        if lista:
            return render_template("assembleia/listar_assembleias_encerradas.html",
                                   assembleias=lista, agora=agora)

    flash(u"Não há Assembléias "+pag_destino)
    return redirect(url_for('main.index'))


def is_datainicio_futura(assembleia):
    formato = '%d/%m/%Y %H:%M'
    agora = datetime.strptime(datetime.now().strftime(formato), formato)
    datainicio = datetime.strptime(assembleia.dataHoraInicio, formato)
    return datainicio > agora

### Verifica se a assembleia deve ser iniciada AGORA, verificando sua data-hora-inicio.
### Se não houver itens de pauta criados, NÃO INICIA a assembleia
def iniciar_assembleia(assembleia):
    if is_datainicio_futura(assembleia):
        return
    # assembleia.itemsPautas vem vazio... eager loading n funciona
    itempautas = ItemPauta.query.filter(ItemPauta.assembleia == assembleia.num).all()
    if not itempautas:
        return
    ## altera o status dos itens pauta de todas as assembleias com "dtInicio >= AGORA"
    assembleia.status = 'EM_ANDAMENTO'
    for it in itempautas:
        if it.status == "CRIADO":
            it.status = 'EM_VOTACAO'
            db.session.add(it)
            db.session.add(assembleia)
    db.session.commit()
