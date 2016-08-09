import os

import simplejson
from flask import request, redirect, url_for, current_app, send_from_directory, flash, render_template
from flask_login import login_required, session
from werkzeug.utils import secure_filename

from consensus_web.models import ConsensusTask
from . import main
from .upload_file import gen_file_name, allowed_file, create_thumbnail
from .upload_model import uploadfile
from ..decorators import permission_required


@permission_required(ConsensusTask.SUGERIR_ITEM_PAUTA)
@main.route("/sugerir-item-pauta/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # pprint (vars(objectvalue))
        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(filename)
            mimetype = file.content_type

            if not allowed_file(file.filename):
                result = uploadfile(name=filename, type=mimetype, size=0,
                                    not_allowed_msg="Tipo de arquivo nao permitido")
                flash('Tipo de arquivo nao permitido')
            else:
                # save file to disk
                uploaded_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(uploaded_file_path)

                # create thumbnail after saving
                if mimetype.startswith('image'):
                    create_thumbnail(filename)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(name=filename, type=mimetype, size=size)

                if session.get('paths_anexos') == None:
                    session['paths_anexos'] = [uploaded_file_path]
                else:
                    session.get('paths_anexos').append(uploaded_file_path)

    return redirect(url_for('main.sugerir_itempauta'))
#            return simplejson.dumps({"files": [result.get_file()]})
#     if request.method == 'GET':
#         # get all file in ./data directory
#         files = [f for f in os.listdir(current_app.config['UPLOAD_FOLDER']) if
#                  os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'], f))]
#         file_display = []
#         for f in files:
#             size = os.path.getsize(os.path.join(current_app.config['UPLOAD_FOLDER'], f))
#             file_saved = uploadfile(name=f, size=size)
#             file_display.append(file_saved.get_file())

#        return simplejson.dumps({"files": file_display})


@permission_required(ConsensusTask.SUGERIR_ITEM_PAUTA)
@main.route("/delete/<string:filename>", methods=['DELETE'])
@login_required
def delete(filename):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file_thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)
            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})


@permission_required(ConsensusTask.SUGERIR_ITEM_PAUTA)
@main.route("/uploads/thumbnail/<string:filename>", methods=['GET'])
@login_required
def get_thumbnail(filename):
    return send_from_directory(current_app.config['THUMBNAIL_FOLDER'], filename=filename)


@main.route("/uploads/<string:filename>", methods=['GET'])
@login_required
def get_file(filename):
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER']), filename=filename)


@main.route("/uploads/<anexos>", methods=['GET'])
@login_required
def get_files(anexos):
    paths = []
    for a in anexos:
        paths.append(a.path)
    return render_template("itempauta/listar_anexos.html", paths=paths)
