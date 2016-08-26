import os

import simplejson
from flask import request, current_app, send_from_directory
from flask_login import current_user
from flask_login import login_required
from werkzeug.utils import secure_filename

from consensus_web.models import ConsensusTask, AnexoTemp
from . import main
from .upload_file_utils import gen_file_name, allowed_file, create_thumbnail
from .upload_model import uploadfile
from .. import db
from ..decorators import permission_required


@permission_required(ConsensusTask.SUGERIR_ITEM_PAUTA)
@main.route("/sugerir-item-pauta/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['files']
        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(filename)
            mimetype = file.content_type

            if not allowed_file(file.filename):
                result = uploadfile(name=filename, type=mimetype, size=0, not_allowed_msg="Extensão de arquivo não permitida")
            else:
                # salva o arquivo no S.O. Se não existir, cria o diretorio
                pasta = current_app.config['UPLOAD_FOLDER']
                uploaded_file_path = os.path.join(pasta, filename)

                if not os.path.exists(pasta):
                    os.makedirs(pasta, exist_ok=True) # cria diretorio. Se existir, sobrescreve sem lancar excecao

                file.save(uploaded_file_path)

                # create thumbnail after saving
                if mimetype.startswith('image'):
                    create_thumbnail(filename)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(name=filename, type=mimetype, size=size)

                # salva o arquivo adicionado temporariamente no BD, para poder recuperá-lo posteriormente em outro request.
                # a session do Flask não funciona direito, além de ser salva localmente num cookie(não seguro).
                anexo_no_bd = AnexoTemp(nome_arquivo=filename,url=result.url,usuario=current_user.id)
                db.session.add(anexo_no_bd)
                db.session.commit()

        return simplejson.dumps({"files": [result.get_file()]})
    if request.method == 'GET':
# nao mostra os arquivos presentes no diretorio
        # files = [f for f in os.listdir(current_app.config['UPLOAD_FOLDER']) if
        #          os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'], f))]
        file_display = []
        # for f in files:
        #     size = os.path.getsize(os.path.join(current_app.config['UPLOAD_FOLDER'], f))
        #     file_saved = uploadfile(name=f, size=size)
        #     file_display.append(file_saved.get_file())
        return simplejson.dumps({"files": file_display})
#    return redirect(url_for('main.sugerir_itempauta'))


@permission_required(ConsensusTask.SUGERIR_ITEM_PAUTA)
@main.route("/data/delete/<string:filename>", methods=['DELETE'])
@login_required
def delete(filename):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)

            # remove o arquivo temporario do BD
            f = AnexoTemp.query.filter(AnexoTemp.nome == filename)
            if f:
                f.delete()
                db.session.commit()

            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})


@permission_required(ConsensusTask.SUGERIR_ITEM_PAUTA)
@main.route("/data/thumbnail/<string:filename>", methods=['GET'])
@login_required
def get_thumbnail(filename):
    return send_from_directory(current_app.config['THUMBNAIL_FOLDER'], filename=filename)


@main.route("/data/<string:filename>", methods=['GET'])
@login_required
def get_file(filename):
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER']), filename=filename)