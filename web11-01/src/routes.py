import pathlib

from werkzeug.utils import secure_filename

from . import app
from flask import render_template, request, redirect, url_for, session, flash
from src.repository import users
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/', strict_slashes=False)
def index():
    auth = True if 'username' in session else False
    return render_template('pages/index.html', title='Upload Service', auth=auth)


@app.route('/registration', methods=['GET', 'POST'], strict_slashes=False)
def registration():
    auth = True if 'username' in session else False
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        nick = request.form.get('nick')
        users.create_user(username=nick, email=email, password=password)
        return redirect(url_for('login'))
    if auth:
        return redirect(url_for('index'))
    else:
        return render_template('pages/reg.html', title='Upload Service')


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    auth = True if 'username' in session else False
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = users.login(email=email, password=password)
        if user is None:
            return redirect(url_for('login'))
        session['username'] = {"username": user.username, "id": user.id}
        return redirect(url_for('index'))
    if auth:
        return redirect(url_for('index'))
    else:
        return render_template('pages/login.html', title='Upload Service')


@app.route('/logout', strict_slashes=False)
def logout():
    session.pop('username')
    return redirect(url_for('index'))


@app.route('/pictures', strict_slashes=False)
def pictures():
    auth = True if 'username' in session else False
    return render_template('pages/pictures.html', title='Upload Service', auth=auth)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/pictures/upload', methods=['GET', 'POST'], strict_slashes=False)
def upload():
    auth = True if 'username' in session else False
    if request.method == 'POST':
        # check if the post request has the file part
        description = request.form.get('description')
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['photo']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(pathlib.Path(app.config['UPLOAD_FOLDER']) / filename)
            return redirect(url_for('upload'))
    return render_template('pages/upload.html', title='Upload Service', auth=auth)
