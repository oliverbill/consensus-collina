## encoding: utf-8

from datetime import datetime

from flask import request, render_template, url_for, redirect, flash, jsonify, json
from flask_login import login_required, current_user

from . import main
from .utils import incluir_anexos, incluir_opcao_voto, get_op_voto_por_sugestao,\
    remover_itens_ja_votados, nenhum_itempauta_ou_listar_com_op_voto,get_op_voto_por_itempauta,gravatar
from .. import db
from ..decorators import permission_required
from ..main.forms import SugerirItemPautaForm, ReprovarSugestaoForm
from ..models import ItemPauta, ConsensusTask, Assembleia, OpcaoVoto, Voto, StatusItemPauta, \
    SugestaoItemPauta, ComentariosItemPauta, Morador


@main.route('/', methods = ['GET','POST'])
@login_required
def index():
    return render_template("index.html",is_home=True)


############################################
############## ITEM DE PAUTA ###############
############################################

@main.route('/listar-itenspauta/<status>', methods = ['GET'])
@login_required
@permission_required(ConsensusTask.LISTAR_ITEM_PAUTA)
def listar_itens_de_pauta_status(status):
    if status not in StatusItemPauta.__members__:
        flash(u"Status inexistente: " + status)
        return redirect(url_for('main.index'))
    # nao mostra sugestoes. Para isso, utilizar o metodo "listar_itenspautas_sugeridos"
    itens_pauta = ItemPauta.query \
        .filter(ItemPauta.status == status).all()
    return nenhum_itempauta_ou_listar_com_op_voto\
        (msg=u"Não há Itens de Pauta com situação " + status, itens_pauta=itens_pauta)


@main.route('/listar-itenspauta/<num_assembleia>/', methods = ['GET'])
@login_required
@permission_required(ConsensusTask.LISTAR_ITEM_PAUTA)
def listar_itens_de_pauta_da_assembleia(num_assembleia):
    itens_pauta = ItemPauta.query\
        .filter(ItemPauta.assembleia == num_assembleia).all()

    return nenhum_itempauta_ou_listar_com_op_voto\
         (msg=u"Não há Itens de Pauta para a Assembléia selecionada", itens_pauta=itens_pauta,
            num_assembleia=num_assembleia)


@main.route('/votar-item-pauta/', methods = ['GET','POST'])
@login_required
@permission_required(ConsensusTask.VOTAR_ITEM_PAUTA)
def votar_itempauta():
    if request.method == 'GET':
        itens_pauta_sugeridos = ItemPauta.query.filter(ItemPauta.status == 'EM_VOTACAO').all()
        if not itens_pauta_sugeridos:
            flash(u"Não há Itens de Pauta EM VOTAÇÃO")
            return redirect(url_for('main.index'))

        itens_pauta_nao_votados_pelo_usuario = remover_itens_ja_votados(itens_pauta_sugeridos, current_user)

        return nenhum_itempauta_ou_listar_com_op_voto\
            (msg=u"Não há Itens de Pauta PENDENTES de voto por você", itens_pauta=itens_pauta_nao_votados_pelo_usuario,
             template="itempauta/listar_itenspauta.html", is_votacao = True)
    else:
        if not request.form.get('link_op_voto'):
            return redirect(url_for('main.votar_itempauta'))

        voto_e_num_itempauta = request.form['link_op_voto']
        voto_e_num_item_split = voto_e_num_itempauta.split(";")
        nome_voto = voto_e_num_item_split[0]
        num_itempauta = voto_e_num_item_split[1]
        autor = current_user.id
        it = ItemPauta.query.get(num_itempauta)
        voto = Voto(autor_email=autor, itempauta_num = it.num, op_nome=nome_voto)

        if 'comentario' in request.form:
            comentario = request.form["comentario"]
            gravatar_src = gravatar(request, current_user.id or "aditil@gmail.com", size=40)
            morador = Morador.query.filter(Morador.usuario_id == autor).one() # somente morador pode comentar
            c = ComentariosItemPauta(texto=comentario,it=it.num,autor=morador.num,gravatar_src=gravatar_src)
            db.session.add(c)
        db.session.add(voto)
        db.session.commit()
        flash("Item de Pauta votado com sucesso")
        return redirect(url_for('main.index'))


@main.route('/detalhar-itenspauta/<num_it>/', methods = ['GET'])
@login_required
@permission_required(ConsensusTask.LISTAR_ITEM_PAUTA)
def detalhar_itempauta(num_it):
    itempauta = ItemPauta.query.get(num_it)
    opcoes_voto = get_op_voto_por_itempauta([itempauta])
    comentarios = ComentariosItemPauta.query.filter(ComentariosItemPauta.itempauta == itempauta.num).all()
    agora = datetime.now();
    return render_template("itempauta/detalhar_itempauta.html", it = itempauta, opcoes_voto = opcoes_voto,
                           comentarios = comentarios, agora = agora)

############################################
######## SUGESTÕES DE ITEM PAUTA ###########
############################################

## tem q permitir GET por causa do possivel refresh do usuario (post/redirect/get pattern)
@main.route('/sugerir-item-pauta/', methods = ['GET','POST'])
@login_required
@permission_required(ConsensusTask.SUGERIR_ITEM_PAUTA)
def sugerir_itempauta():
    form = SugerirItemPautaForm(request.form)
    form.autor.data = current_user.id
    display_div_erro = "display:none"
    if form.validate_on_submit():
        op = OpcaoVoto.query.get(form.votacao.data)
        sugestao = SugestaoItemPauta(titulo=form.titulo.data, autor=form.autor.data, desc=form.descricao.data)
        # se usuario selecionou 'outros' no combo 'opcoes de voto'
        if op.nome.__contains__("outras"):
            nova_op = incluir_opcao_voto(form.outra_opcao_voto.entries, db)
            sugestao.op_voto = nova_op.num
        else:
            sugestao.op_voto = op.num
        db.session.add(sugestao)
        db.session.commit()

        incluir_anexos(db, sugestao.num)

        flash(u"Sugestão de Item de Pauta incluída com sucesso")
        return redirect(url_for('main.index'))
    elif form.errors:
        display_div_erro = "display:inherit"
    return render_template("sugestao/sugerir_itempauta.html", form = form, display=display_div_erro)

# para validar as outras opcoes de voto no wtform
@main.route('/add-opcao-voto/', methods = ['POST'])
@login_required
@permission_required(ConsensusTask.SUGERIR_ITEM_PAUTA)
def add_opcao_voto():
    form = SugerirItemPautaForm(request.form)
    form.add_opcao_voto();
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@main.route('/listar-sugestoes-sem-avaliacao/', methods = ['GET','POST'])
@login_required
@permission_required(ConsensusTask.AVALIAR_SUGESTAO_ITEM_PAUTA)
def listar_sugestoes_sem_avaliacao():
    form = ReprovarSugestaoForm(request.form)
    return listar_sugestoes_nao_avaliadas(form=form)


def listar_sugestoes_nao_avaliadas(form):
    sugestoes = SugestaoItemPauta.query.filter(SugestaoItemPauta.status == 'NAO_AVALIADA').all()
    if not sugestoes:
        flash(u"Não há Sugestões de Item Pauta A AVALIAR")
        return redirect(url_for('main.index'))
    opcoes_voto = get_op_voto_por_sugestao(sugestoes)
    ids = [(it.num) for it in sugestoes]  # variavel utilizada na pag. "botoes_aprovar_reprovar.html"
    return render_template("sugestao/listar_sugestoes_itempauta.html",
                           itens_de_pauta=zip(sugestoes, ids), opcoes_voto=opcoes_voto, form = form)


@main.route('/listar-sugestoes-reprovadas/', methods = ['GET'])
@login_required
@permission_required(ConsensusTask.LISTAR_ITEM_PAUTA)
def listar_sugestoes_reprovadas():
    sugestoes_reprovadas = SugestaoItemPauta.query.filter(SugestaoItemPauta.status == 'REPROVADA').all()
    return nenhum_itempauta_ou_listar_com_op_voto\
        (msg=u"Não há Sugestões de Item Pauta REPROVADAS", itens_pauta=sugestoes_reprovadas,
               template="sugestao/listar_sugestoes_reprovadas.html")


@main.route('/aprovar-sugestao/<num_sugestao>/', methods = ['POST'])
@login_required
@permission_required(ConsensusTask.AVALIAR_SUGESTAO_ITEM_PAUTA)
def aprovar_sugestao(num_sugestao):
    sugestao = SugestaoItemPauta.query.get(num_sugestao)
    sugestao.status = 'APROVADA'
    flash(u"Sugestão de Item de Pauta APROVADA com sucesso")
    db.session.add(sugestao)
    db.session.commit()
    return "/"  # retorna a url em texto pq o sistema redireciona via javascript apos o confirm do modal


@main.route('/reprovar-sugestao/<num_itempauta>', methods = ['POST'])
@login_required
@permission_required(ConsensusTask.AVALIAR_SUGESTAO_ITEM_PAUTA)
def reprovar_sugestao(num_itempauta):
    form = ReprovarSugestaoForm(request.form)
    if form.validate_on_submit():
        justificativa = request.form["justificativa"]
        sugestao = SugestaoItemPauta.query.get(num_itempauta)
        sugestao.status = 'REPROVADA'
        sugestao.justif_reprovacao = justificativa
        db.session.add(sugestao)
        db.session.commit()
        flash(u"Sugestão de Item Pauta REPROVADA com sucesso")
        return redirect(url_for('main.index'))
    return listar_sugestoes_sem_avaliacao(form=form)


@main.route('/add-itempauta-a-assembleia/', methods = ['POST'])
@login_required
@permission_required(ConsensusTask.ATRIBUIR_ASSEMBLEIA)
def add_itempauta_a_assembleia():
    try:
        num_sugestao = request.form["sugestao_num"]
        if num_sugestao:
            sugestao = SugestaoItemPauta.query.get(num_sugestao)
            return jsonify(num=sugestao.num,titulo=sugestao.titulo,autor=sugestao.autor)
    except Exception as e:
        flash(u'Erro na Aplicação. Contate o Administrador do Sistema')
        return redirect(url_for('main.index'))


@main.route('/atribuir-a-assembleia/', methods = ['GET','POST'])
@login_required
@permission_required(ConsensusTask.ATRIBUIR_ASSEMBLEIA)
def atribuir_sugestoes_a_assembleia():
    if request.method == 'GET':
        assembleias = Assembleia.query.filter_by(status='CRIADA').order_by("num").all()
        sugestoes_aprovadas = SugestaoItemPauta.query.filter(SugestaoItemPauta.status == 'APROVADA').all()

        if not sugestoes_aprovadas:
            flash(u"Não há Sugestões de Item Pauta APROVADAS para atribuir à assembléias")
            return redirect(url_for('main.index'))

        return render_template("sugestao/atribuir_a_assembleia.html",
                    sugestoes=sugestoes_aprovadas, assembleias_combo=assembleias,
                               assembleias_heading=assembleias)
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

        flash(u"Item de Pauta atribuído com sucesso")
        return "/"  # retorna a url em texto pq o sistema redireciona via javascript apos o confirm do modal


############################################
############### ASSEMBLEIAS ###############
############################################

@main.route('/criar-assembleia/', methods = ['GET','POST'])
@login_required
@permission_required(ConsensusTask.CRIAR_ASSEMBLEIA)
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


## tem q permitir GET por causa do possivel refresh do usuario (post/redirect/get pattern)
@main.route('/listar-assembleias/<status>/', methods = ['GET','POST'])
@login_required
@permission_required(ConsensusTask.LISTAR_ASSEMBLEIAS)
def listar_assembleias(status):
    pag_destino = ""
    agora = datetime.now();

    if status == '1':
        # joinedload = eager loading dos itempautas
        assembleias_criadas = Assembleia.query.filter(Assembleia.status == 'CRIADA').order_by("dt_hora_criacao").all()

        # verifica se já tem alguma sugestao criada para cada assembleia CRIADA, para exibir o botao de detalhamento na tela
        busca_sugestoes = len(SugestaoItemPauta.query.filter(SugestaoItemPauta.status == 'APROVADA').all()) > 0
        pag_destino = "AGUARDANDO INÍCIO"
        if assembleias_criadas:
            return render_template("assembleia/listar_assembleias_criadas.html",
                                   assembleias=assembleias_criadas, agora=agora,
                                   ha_sugestoes_nao_atribuidas=busca_sugestoes)
    elif status == '2':
        ## 'em andamento' contendo itens de pauta
        lista = Assembleia.query.filter(Assembleia.status == 'EM_ANDAMENTO') \
                                .filter(Assembleia.itemsPautas) \
                            .order_by("dt_hora_inicio").all()
        if lista:
            datainicio = datetime.strptime(lista[0].dataHoraInicio, '%d/%m/%Y %H:%M')

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


@main.route('/iniciar-assembleia/<num>/', methods = ['GET','POST'])
@login_required
@permission_required(ConsensusTask.ALTERAR_ASSEMBLEIA)
def iniciar_assembleia_agora(num):
    # assembleia.itemsPautas vem vazio... eager loading n funciona
    itempautas = ItemPauta.query.filter(ItemPauta.assembleia == num).all()
    if not itempautas:
        flash("Assembleia nao pode ser iniciada pois nao possui nenhum Item de Pauta")
        return redirect(url_for('main.index'))
    assembleia = Assembleia.query.get(num)
    assembleia.status = 'EM_ANDAMENTO'
    formato = '%d/%m/%Y %H:%M'
    agora = datetime.strptime(datetime.now().strftime(formato), formato)
    assembleia.__dataHoraInicio = agora
    for it in itempautas:
        if it.status == "CRIADO":
            it.status = 'EM_VOTACAO'
            db.session.add(it)
            db.session.add(assembleia)
    db.session.commit()
    flash(u"Assembléia iniciada com sucesso")
    return redirect(url_for('main.index'))