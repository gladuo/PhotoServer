import os
import datetime, time

from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename

import config
from utils import allowed_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('upload.html')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'image_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image_file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            timestamp = str(int(time.time()))
            filename = timestamp + os.path.splitext(file.filename)[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(file.filename+' uploaded successfully !')
            return redirect(url_for('index'))


@app.route('/api/get', methods=['GET'])
def get_image():
    newest_file = os.listdir(config.UPLOAD_FOLDER)[-1]
    return jsonify({'file_name': newest_file, 'src': url_for('static', filename=os.path.join('upload', newest_file))})


if __name__ == '__main__':
    app.secret_key = 'some secret key'
    app.run()
