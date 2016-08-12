# !flask/bin/python

# Author: Ngo Duy Khanh
# Email: ngokhanhit@gmail.com
# Git repository: https://github.com/ngoduykhanh/flask-file-uploader
# This work based on jQuery-File-Upload which can be found at https://github.com/blueimp/jQuery-File-Upload/

import os
import traceback

import PIL
from PIL import Image
from werkzeug.utils import iteritems

from . import main


@main.record
def record_params(setup_state):
  app = setup_state.app
  main.config = dict([(key,value) for (key,value) in iteritems(app.config)])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in main.config['ALLOWED_EXTENSIONS']


def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """
    path = main.config['UPLOAD_FOLDER']
    i = 1
    while os.path.exists(os.path.join(path, filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i = i + 1

    return filename


def create_thumbnail(image):
    try:
        basewidth = 80
        img = Image.open(os.path.join(main.config['UPLOAD_FOLDER'], image))
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        img.save(os.path.join(main.config['THUMBNAIL_FOLDER'], image))

        return True

    except:
        print
        traceback.format_exc()
        return False