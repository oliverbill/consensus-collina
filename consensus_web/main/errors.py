from flask import render_template

from . import main


@main.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html', title='Página não encontrada'), 404

@main.errorhandler(405)
def erro_interno(e):
    return render_template('405.html', title='Erro interno do servidor'), 405