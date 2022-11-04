from . import app
from flask import render_template, request, flash, redirect, url_for, session, make_response
from src.libs.validation_file import allowed_file
from src.libs.validation_contact import contact_validation
from werkzeug.utils import secure_filename
import pathlib
import uuid
from datetime import datetime, timedelta
from src.repository import users, pics
from src.repository.contacts import create_contact, get_contacts_user, cont_delete, update_contact
from src.libs.validation_schemas import RegistrationSchema, LoginSchema,ContactSchema
from marshmallow import ValidationError


@app.before_request
def before_func():
    auth = True if 'username' in session else False
    if not auth:
        token_user = request.cookies.get('username')
        if token_user:
            user = users.login_in_cookie(token_user)
            if user:
                session['username'] = {'username': user.username, 'id': user.id}

@app.route('/healthcheck')
def healthcheck():
    return 'I`m working'


@app.route('/')
def index():
    auth = True if 'username' in session else False
    if auth:
        print(session['username']['id'])
        user = users.find_by_id(session['username']['id'])
        return render_template('pages/index.html', title='Assistant', auth=auth, username=user.username)
    return render_template('pages/index.html', title='Assistant', auth=auth)


@app.route('/pictures', strict_slashes=False)
def pictures():
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    pictures_user = pics.get_pictures_user(session['username']['id'])
    print(pictures_user)
    return render_template('pages/pictures.html', auth=auth, pictures=pictures_user) 


@app.route('/registration', methods=["GET", "POST"], strict_slashes=False)
def registration():
    auth = True if 'username' in session else False
    if request.method == 'POST':
        try:
            RegistrationSchema().load(request.form)
        except ValidationError as err:
            return render_template('pages/registration.html', messages=err.messages)
        email = request.form.get('email')
        password = request.form.get('password')
        nick = request.form.get('nick')
        user = users.create_user(email, password, nick)
        print(user)
        return redirect(url_for('login'))
    if auth:
        return redirect(url_for('index'))
    return render_template('pages/registration.html') 


@app.route('/login', methods=["GET", "POST"], strict_slashes=False)
def login():
    auth = True if 'username' in session else False
    if auth:
        return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            LoginSchema().load(request.form)
        except ValidationError as err:
            return render_template('pages/login.html', messages=err.messages)
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') == 'on' else False

        user = users.login(email, password)
        if user is None:
            return redirect(url_for('login'))
        session['username'] = {'username': user.username, 'id': user.id}
        response = make_response(redirect(url_for('index')))
        if remember:
            token = str(uuid.uuid4())
            expire_data = datetime.now() + timedelta(days=60)
            response.set_cookie('username', token, expires=expire_data)
            users.set_token(user, token)

        return response

    return render_template('pages/login.html')

@app.route('/logout', strict_slashes=False)
def logout():
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    session.pop('username')
    response = make_response(redirect(url_for('index')))
    response.set_cookie('username', '', expires=-1)
    return response


@app.route('/pictures/upload', methods=["GET", "POST"], strict_slashes=False)
def pictures_upload():
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    if request.method == 'POST':
        # print('POST')
        description = request.form.get('description')
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['photo']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = pathlib.Path(app.config['UPLOAD_FOLDER']) / filename
            file.save(file_path)
            pics.upload_file_for_user(session['username']['id'], file_path, description)
            flash('Uploaded successfully!')
            return redirect(url_for('pictures'))
    return render_template('pages/upload.html', auth=auth) 


    

@app.route('/pictures/edit/<pic_id>', methods=["GET", "POST"], strict_slashes=False)
def picture_edit(pic_id):
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
        
    picture = pics.get_picture_user(pic_id, session['username']['id'])
    if request.method == 'POST':
        description = request.form.get('description')
        pics.update_picture(id, session['username']['id'], description)
        return redirect(url_for('pictures'))
    return render_template('pages/edit.html', auth=auth, picture=picture) 


@app.route('/pictures/delete/<pic_id>', methods=["POST"], strict_slashes=False)
def delete(pic_id):
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    if request.method == 'POST':
        pics.delete(pic_id, session['username']['id'])
        flash('Operation successfully!')
    return redirect(url_for('pictures'))


@app.route('/contacts', methods=["GET", "POST"], strict_slashes=False)
def contacts():
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    contacts_user = get_contacts_user(session['username']['id'])
    print(contacts_user)
    return render_template('pages/contacts.html', auth=auth, contacts=contacts_user) 


@app.route('/add_contact', methods=["GET", "POST"], strict_slashes=False)
def add_contact():
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    if request.method == 'POST':
        try:
            ContactSchema().load(request.form)
        except ValidationError as err:
            return render_template('pages/add_contact.html', messages=err.messages,auth=auth)
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birthday = request.form.get('birthday')
        email = request.form.get('email')
        address = request.form.get('address')
        cell_phone = request.form.get('cell_phone')
        validation = contact_validation(first_name,last_name,birthday,email,address,cell_phone)
        if validation != None:
            flash(validation)
            return redirect(request.url)
        print(first_name, last_name,birthday,email,address,cell_phone)
        create_contact(first_name, last_name, birthday, email, address, cell_phone, session['username']['id'])
    return render_template('pages/add_contact.html', auth=auth) 


@app.route('/delete_contact/<contact_id>', methods=["POST"], strict_slashes=False)
def contact_delete(contact_id):
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    if request.method == 'POST':
        print(contact_id, session['username']['id'])
        cont_delete(contact_id, session['username']['id'])
        flash('Operation successfully!')
    return redirect(url_for('contacts'))


@app.route('/edit_contact/<contact_id>', methods=["POST"], strict_slashes=False)
def edit_contact(contact_id):
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    contact = get_contacts_user(contact_id)


    if request.method == 'POST':
        print("POST EDIT")
    return render_template('pages/edit_contact.html', auth=auth, contact_id=contact_id, contact=[contact]) 


@app.route('/edited_contact/<contact_id>', methods=["POST"], strict_slashes=False)
def edited_contact(contact_id):
    print("edited_contact")
    auth = True if 'username' in session else False
    if not auth:
        return redirect(request.url)
    if request.method == 'POST':
        print("POST EDITed")
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birthday = request.form.get('birthday')
        email = request.form.get('email')
        address = request.form.get('address')
        cell_phone = request.form.get('cell_phone')
        print(first_name, last_name,birthday,email,address,cell_phone)
        update_contact(contact_id, session['username']['id'], first_name, last_name, birthday, email, address, cell_phone)

    return redirect(url_for('contacts'))