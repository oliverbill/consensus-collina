from flask import flash, redirect, render_template, url_for

from ..models import AnexoModel,OpcaoVoto, Voto, SugestaoItemPauta, ItemPauta


def incluir_anexos(session,db):
    anexos = []
    if session.get('paths_anexos'):
        for p in session['paths_anexos']:
            a = AnexoModel(p)
            db.session.add(a)
            db.session.commit()
            anexos.append(a)
    return anexos

def incluir_opcao_voto(form, db):
    valor = set()
    for o in form.votacao_outros:
        valor.add(o.data)
    for r in o.raw_data:
        valor.add(r)
    vl_formatado = '/ '.join(valor)
    nova_op = OpcaoVoto(vl_formatado)
    db.session.add(nova_op)
    db.session.commit()
    return nova_op

def get_op_voto_por_sugestao(sugestao):
    opcoes_voto = {}
    for s in sugestao:
        op_nomes = OpcaoVoto.query.get(s.op_voto).nome
        op_nomes_split = op_nomes.split('/')
        opcoes_voto[s.num] = op_nomes_split
    return opcoes_voto

def get_op_voto_por_itempauta(itens):
    opcoes_voto = {}
    for it in itens:
        sugestao = SugestaoItemPauta.query.get(it.sugestao_itempauta)
        op_nomes = OpcaoVoto.query.get(sugestao.op_voto).nome
        op_nomes_split = op_nomes.split('/')
        opcoes_voto[it.num] = op_nomes_split
    return opcoes_voto

def remover_itens_ja_votados(itens_pauta_sugeridos, current_user):
    itens_pauta_nao_votados = []
    for it in itens_pauta_sugeridos:
        voto_do_usuario_nesse_item = Voto.query\
            .filter(Voto.autor == current_user.id, Voto.itempauta == it.num).all()
        if not voto_do_usuario_nesse_item:
            itens_pauta_nao_votados.append(it)
    return itens_pauta_nao_votados

def nenhum_itempauta_ou_listar_com_op_voto(msg, itens_pauta, *template):
    if not itens_pauta:
        flash(msg)
        return redirect(url_for('main.index'))

    opcoes_voto = {}
    if isinstance(itens_pauta[0], SugestaoItemPauta):
        opcoes_voto = get_op_voto_por_sugestao(itens_pauta)
    elif isinstance(itens_pauta[0], ItemPauta):
        opcoes_voto = get_op_voto_por_itempauta(itens_pauta)

    return render_template(template or "itempauta/listar_itenspauta.html",
                           itens_de_pauta=itens_pauta,
                           opcoes_voto=opcoes_voto)