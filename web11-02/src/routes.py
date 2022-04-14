import pathlib
from datetime import datetime, timedelta

from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
import uuid
from . import app
from flask import render_template, request, redirect, url_for, session, flash, make_response
from src.repository import users, pic
from .validation import RegistrationSchema, LoginSchema, ValidationError

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@app.before_request
def before_request():
    username = request.cookies.get('username')
    if username:
        user = users.login_in_cookie(username)
        if user:
            session['username'] = {"username": user.username, "id": user.id}


@app.route('/', strict_slashes=False)
def index():
    auth = True if 'username' in session else False
    return render_template('pages/index.html', title='Upload Service', auth=auth)


@app.route('/registration', methods=['GET', 'POST'], strict_slashes=False)
def registration():
    auth = True if 'username' in session else False
    if request.method == 'POST':
        try:
            RegistrationSchema().load(request.form)
        except ValidationError as err:
            return render_template('error.html', messages=err.messages)
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
        try:
            LoginSchema().load(request.form)
        except ValidationError as err:
            return render_template('error.html', messages=err.messages)
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') == 'on' else False

        user = users.login(email=email, password=password)
        if user is None:
            return redirect(url_for('login'))
        session['username'] = {"username": user.username, "id": user.id}
        response = make_response(redirect(url_for('index')))
        if remember:
            token = str(uuid.uuid4())
            expire_date = datetime.now()
            expire_date = expire_date + timedelta(days=90)
            response.set_cookie('username', token, expires=expire_date)
            users.set_token_to_db(user, token)
        return response
    if auth:
        return redirect(url_for('index'))
    else:
        return render_template('pages/login.html', title='Upload Service')


@app.route('/logout', strict_slashes=False)
def logout():
    session.pop('username')
    response = make_response(redirect(url_for('index')))
    response.set_cookie('username', '', expires=-1)
    return response


@app.route('/pictures', strict_slashes=False)
def pictures():
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    pictures_user = pic.get_pictures_user(session['username']["id"])
    return render_template('pages/pictures.html', title='Upload Service', auth=auth, pictures=pictures_user)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/pictures/upload', methods=['GET', 'POST'], strict_slashes=False)
def upload():
    auth = True if 'username' in session else False
    if request.method == 'POST' and auth:
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
            full_path = pathlib.Path(app.config['UPLOAD_FOLDER']) / filename
            file.save(full_path)
            pic.upload_file_to_user(session['username']["id"], full_path, description)
            flash('Picture uploaded successfully!')
            return redirect(url_for('upload'))
    return render_template('pages/upload.html', title='Upload Service', auth=auth)


@app.route('/pictures/edit/<id>', methods=['GET', 'POST'], strict_slashes=False)
def picture_edit(id):
    auth = True if 'username' in session else False
    picture = pic.get_picture_user(id, session['username']["id"])
    if request.method == 'POST' and auth:
        description = request.form.get('description')
        pic.update_picture(id, session['username']["id"], description)
        flash('Picture updated successfully!')
        return redirect(url_for('pictures'))

    return render_template('pages/edit.html', title='Upload Service', auth=auth, picture=picture)


@app.route('/pictures/delete/<id>', methods=['POST'], strict_slashes=False)
def picture_delete(id):
    auth = True if 'username' in session else False
    if request.method == 'POST' and auth:
        pic.delete_picture(id, session['username']["id"])
        flash('Picture deleted successfully!')

    return redirect(url_for('pictures'))


@app.errorhandler(Exception)
def handle_exception(e):
    return render_template("500.html", e=e)
