from flask import Blueprint

main = Blueprint('main', __name__)

# importado no final do arquivo para evitar dependencias ciclicas
from . import views, file_upload_views, errors

# @main.app_context_processor
# def inject_permissions():
#     return dict(Permission=Permission)
