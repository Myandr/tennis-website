from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import random
import string
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
from flask_migrate import Migrate
import subprocess
from io import BytesIO
import base64
from functools import wraps
from flask_bcrypt import Bcrypt

SAVE_PATH = 'editable_content.html'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user_n8v5_user:cuxgdv9h0nXv6w0qVopJ36Q1AayExu5h@dpg-cu8dhv9opnds73d4tf00-a.oregon-postgres.render.com/user_n8v5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP-Server
app.config['MAIL_PORT'] = 587  # Port für TLS
app.config['MAIL_USE_TLS'] = True  # TLS aktivieren
app.config['MAIL_USE_SSL'] = False  # SSL nicht verwenden
app.config['MAIL_USERNAME'] = 'myandr180709@gmail.com'  # Deine Gmail-Adresse
app.config['MAIL_PASSWORD'] = 'tkkl szsh ybkj vprx'  # Dein App-Passwort
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['REMEMBER_COOKIE_DURATION'] = 2592000  # 30 days
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {
        "sslmode": "require"
    }
}


db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#datebank

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6))

class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('reset_tokens', lazy=True))

class Termin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datum = db.Column(db.String(10), nullable=False)
    veranstaltung = db.Column(db.String(100), nullable=False)
    uhrzeit = db.Column(db.String(5), nullable=False)
    ort = db.Column(db.String(50), nullable=False)

class AboutText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # Hinzugefügtes Feld für den Texttyp (Überschrift oder normal)

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)

class ContentItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_data = db.Column(db.LargeBinary)
    heading = db.Column(db.String(100), nullable=False)
    text1 = db.Column(db.Text, nullable=False)
    text2 = db.Column(db.Text, nullable=False)
    iframe = db.Column(db.Text, nullable=False)
    

class Box(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_data = db.Column(db.LargeBinary)
    date = db.Column(db.Date, nullable=False)
    heading = db.Column(db.String(100), nullable=False)
    info = db.Column(db.Text, nullable=False)
    span = db.Column(db.Text, nullable=False)

# Erstellen Sie die Tabellen in der Datenbank
with app.app_context():
    db.create_all()




#ADD

@app.route('/news', methods=['GET', 'POST'])
def news():
    if request.method == 'POST':
        image = request.files['image']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        heading = request.form['heading']
        info = request.form['info']
        span = request.form['span']

        if image and allowed_file(image.filename):
            # Bild in Binärdaten umwandeln
            image_data = image.read()

        # Box in der Datenbank speichern
        new_box = Box(
            image_data=image_data,  # Binärdaten des Bildes
            date=date,
            heading=heading,
            info=info, 
            span=span
        )
        db.session.add(new_box)
        db.session.commit()

        return redirect(url_for('news'))
    
    # Abrufen der Boxen
    boxes = Box.query.all()
    is_admin_active = session.get('is_admin_active', True)


    # Base64-Umwandlung für jedes Bild
    for box in boxes:
        if box.image_data:
            box.image_data_base64 = base64.b64encode(box.image_data).decode('utf-8')


    return render_template('news.html', logged_in=current_user.is_authenticated, is_admin=current_user.is_authenticated and current_user.role == 'admin', boxes=boxes, is_admin_active=is_admin_active)









    





@app.route('/delete/<int:box_id>', methods=['POST'])
def delete_box(box_id):
    box = Box.query.get_or_404(box_id)
    

    if box.image_data:
        box.image_data = None  # Bild aus der Datenbank entfernen
    
    db.session.delete(box)
    db.session.commit()
    return redirect(url_for('news'))





def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add', methods=['POST'])
def add_content():
    if 'image' not in request.files:
        return redirect(url_for('home'))
    
    file = request.files['image']
    
    if file.filename == '':
        return redirect(url_for('home'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Bild in Binärdaten umwandeln
        image_data = file.read()
        new_item = ContentItem(
            image_data=image_data,
            heading=request.form['heading'],
            text1=request.form['text1'],
            text2=request.form['text2'],
            iframe=request.form['iframe']
        )
        db.session.add(new_item)
        db.session.commit()
    
    return redirect(url_for('home'))

@app.route('/delete/<int:item_id>')
def delete_content(item_id):
    item = ContentItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No file part", 400
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_image = Image(filename=filename)
        db.session.add(new_image)
        db.session.commit()
    return redirect(url_for('home') + "#awards")



@app.route('/delete_image/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    # Löschen der Datei aus dem Upload-Ordner
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    # Löschen des Eintrags aus der Datenbank
    db.session.delete(image)
    db.session.commit()
    return redirect(url_for('home') + "#awards")




@app.route('/add_termin', methods=['POST'])
def add_termin():
    datum = request.form['datum']
    veranstaltung = request.form['veranstaltung']
    uhrzeit = request.form['uhrzeit']
    ort = request.form['ort']

    neuer_termin = Termin(datum=datum, veranstaltung=veranstaltung, uhrzeit=uhrzeit, ort=ort)
    db.session.add(neuer_termin)
    db.session.commit()
    return redirect(url_for('home') + "#work")



@app.route('/delete_termin/<int:termin_id>', methods=['POST'])
def delete_termin(termin_id):
    termin = Termin.query.get_or_404(termin_id)
    db.session.delete(termin)
    db.session.commit()
    return redirect(url_for('home') + "#work")






@app.route("/add_about_text", methods=["POST"])
def add_about_text():
    text_content = request.form["about_content"]
    text_type = request.form["text_type"]

    if not text_content:
        return redirect(url_for('home') + "#about")

    
    if text_type == "headline":
        new_text = AboutText(content=text_content, type="headline")
    else:
        new_text = AboutText(content=text_content, type="normal")

    db.session.add(new_text)
    db.session.commit()
    return redirect(url_for('home') + "#about")



@app.route("/delete_about_text/<int:id>", methods=["POST"])
def delete_about_text(id):
    text_to_delete = AboutText.query.get(id)
    if text_to_delete:
        db.session.delete(text_to_delete)
        db.session.commit()
    else:
        flash("Text nicht gefunden.", "error")
    return redirect(url_for('home') + "#about")










#login


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_verification_code():
    return ''.join(random.choices('0123456789', k=6))

def send_verification_email(email, code):
    msg = Message('Verify Your Email', sender='your_email@gmail.com', recipients=[email])
    msg.body = f'Your verification code is: {code}'
    mail.send(msg)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('E-Mail existiert bereits', 'error')
            return redirect(url_for('signup'))
        
        if role == 'admin':
            admin_password = request.form['admin_password']
            if admin_password != os.environ.get('ADMIN_PASSWORD', 'hardter-tennis-tv-dorsten-admin'):
                flash('Ungültiges Admin-Passwort', 'error')
                return redirect(url_for('signup'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        verification_code = generate_verification_code()
        new_user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password_hash=hashed_password,
            role=role,
            verification_code=verification_code
        )

        db.session.add(new_user)
        db.session.commit()

        send_verification_email(email, verification_code)
        
        # E-Mail in der Session speichern
        session['email'] = email

        flash('Bitte überprüfen Sie Ihre E-Mails auf den Bestätigungscode', 'info')
        return redirect(url_for('verify'))
    
    return render_template('signup.html')


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    # Stelle sicher, dass die E-Mail in der Session vorhanden ist
    email = session.get('email')
    if not email:
        flash('Es gibt kein Konto zur Verifizierung. Bitte melden Sie sich erneut an.', 'error')
        return redirect(url_for('signup'))

    if request.method == 'POST':
        code = request.form['code']
        
        # Suche den Benutzer basierend auf der Session-E-Mail
        user = User.query.filter_by(email=email).first()
        if user and user.verification_code == code:
            user.is_verified = True
            user.verification_code = None
            db.session.commit()

            # Entferne die E-Mail aus der Session nach erfolgreicher Verifizierung
            session.pop('email', None)

            flash('Ihr Konto wurde erfolgreich verifiziert!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Ungültiger Bestätigungscode.', 'error')
    
    return render_template('verify.html', email=email)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = 'remember' in request.form
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            if user.is_verified:
                login_user(user, remember=remember)
                flash('Sie sind erfolgreich eingeloggt', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Bitte verifizieren Sie zuerst Ihre E-Mail', 'error')
                return redirect(url_for('verify'))
        else:
            flash('Ungültige E-Mail oder Passwort', 'error')
    
    return render_template('login.html')

def mask_email(email):
    username, domain = email.split('@')
    if len(username) <= 4:
        visible_part = len(username) // 2
        masked_username = username[:visible_part] + '*' * (len(username) - visible_part)
    else:
        masked_username = username[:2] + '***' + username[-2:]
    return f"{masked_username}@{domain}"

@app.template_filter('mask_email')
def mask_email_filter(email):
    return mask_email(email)

@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_verified:
        flash('Bitte verifizieren Sie zuerst Ihre E-Mail', 'error')
        return redirect(url_for('verify'))
    
    users = User.query.all()
    return render_template('dashboard.html', 
                           is_admin=current_user.is_authenticated and current_user.role == 'admin', 
                           user=current_user, 
                           users=users)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sie sind erfolgreich ausgeloggt', 'success')
    return redirect(url_for('login'))

@app.route('/resend_verification', methods=['GET', 'POST'])
def resend_verification():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user and not user.is_verified:
            new_code = generate_verification_code()
            user.verification_code = new_code
            db.session.commit()
            send_verification_email(email, new_code)
            flash('Ein neuer Bestätigungscode wurde an Ihre E-Mail gesendet', 'info')
            return redirect(url_for('verify'))
        else:
            flash('Ungültige E-Mail oder Konto bereits verifiziert', 'error')
    return render_template('resend_verification.html')

def send_password_reset_email(user_email):
    token = serializer.dumps(user_email, salt='password-reset-salt')
    reset_url = url_for('reset_password', token=token, _external=True)
    msg = Message('Password Reset Request', 
                  sender='your_email@gmail.com', 
                  recipients=[user_email])
    msg.body = f'Um das Passwort zurück zu setzen, folge dem Link: {reset_url}'
    mail.send(msg)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            send_password_reset_email(user.email)
            flash('Eine E-Mail zur Zurücksetzung des Passworts wurde gesendet', 'info')
        else:
            flash('E-Mail-Adresse nicht gefunden', 'error')
        return redirect(url_for('login'))
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('Der Link zur Passwortzurücksetzung ist ungültig oder abgelaufen', 'error')
        return redirect(url_for('login'))
    
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Benutzer nicht gefunden', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash(' Passwörter stimmen nicht überein', 'error')
            return render_template('reset_password.html', token=token)
        
        user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.commit()
        flash('Ihr Passwort wurde aktualisiert!', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if current_user.is_authenticated:
        user = current_user._get_current_object()  # Ensure you get the actual object
        db.session.delete(user)
        db.session.commit()
        flash('Account erfolgreich gelöscht', 'success')
        return redirect(url_for('signup'))
    return redirect(url_for('login'))

@app.route('/edit_account', methods=['GET', 'POST'])
@login_required
def edit_account():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')

        if User.query.filter((User.email == email) & (User.id != current_user.id)).first():
            flash('Die E-Mail-Adresse ist bereits vergeben.', 'error')
            return redirect(url_for('edit_account'))

        current_user.firstname = firstname
        current_user.lastname = lastname
        current_user.email = email
        db.session.commit()

        flash('Ihr Konto wurde erfolgreich aktualisiert.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_account.html', user=current_user)



@app.before_request
def before_request():
    session.modified = True


# Admin-Rechte in der Session speichern
@app.route('/toggle_admin', methods=['POST'])
@login_required
def toggle_admin():
    if current_user.role == 'admin':  # Überprüfen, ob der Nutzer ein Admin ist
        session['is_admin_active'] = not session.get('is_admin_active', True)
        status = 'aktiviert' if session['is_admin_active'] else 'deaktiviert'
        flash(f'Admin-Rechte wurden {status}.', 'success')
    else:
        flash('Sie haben keine Berechtigung, diese Aktion auszuführen.', 'error')
    return redirect(url_for('dashboard'))


#home seite + cookies

@app.route('/')
def home():
    images = Image.query.all()
    about_texts = AboutText.query.all()
    content_items = ContentItem.query.all()
    for item in content_items:
        if item.image_data:
            item.image_data_base64 = base64.b64encode(item.image_data).decode('utf-8')
        else:
            item.image_data_base64 = None
    
    termine = Termin.query.all()

    cookie_consent = request.cookies.get('necessary') == 'true'

    is_admin_active = session.get('is_admin_active', True)

    return render_template('index2.html', 
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin',
                           is_verified=current_user.is_authenticated and current_user.is_verified,
                           termine=termine,
                           about_texts=about_texts,
                           images=images,
                           content_items=content_items,
                           cookie_consent=cookie_consent, 
                           is_admin_active=is_admin_active)



@app.route('/api/cookies/accept-all', methods=['POST'])
def accept_all_cookies():
    response = make_response(jsonify({'message': 'Alle Cookies akzeptiert'}))
    
    # Set cookies with 1 year expiration
    expires = datetime.now() + timedelta(days=365)
    
    response.set_cookie('necessary', 'true', expires=expires, secure=True, httponly=True)
    response.set_cookie('functional', 'true', expires=expires, secure=True)
    response.set_cookie('analytics', 'true', expires=expires, secure=True)
    response.set_cookie('marketing', 'true', expires=expires, secure=True)
    
    return response

@app.route('/api/cookies/save-settings', methods=['POST'])
def save_cookie_settings():
    settings = request.get_json()
    response = make_response(jsonify({'message': 'Cookie-Einstellungen gespeichert'}))
    
    expires = datetime.now() + timedelta(days=365)
    
    # Necessary cookies are always enabled
    response.set_cookie('necessary', 'true', expires=expires, secure=True, httponly=True)
    
    # Set other cookies based on user preferences
    for cookie_type in ['functional', 'analytics', 'marketing']:
        if cookie_type in settings and settings[cookie_type]:
            response.set_cookie(cookie_type, 'true', expires=expires, secure=True)
        else:
            response.delete_cookie(cookie_type)
    
    return response



@app.route('/newsletter')
def newsletter():
    return render_template('newsletter.html')










from datetime import timedelta


@app.before_request
def make_session_permanent():
    session.permanent = True




#mails




# Mail-Objekt erstellen


# Route für das Formular

# Route zum Senden der E-Mail
# Route zum Senden der E-Mail
@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']  # Name des Benutzers
    user_email = request.form['email']  # E-Mail des Benutzers
    message = request.form['message']  # Nachricht des Benutzers

    # Nachricht erstellen
    msg = Message('Nachricht von ' + name,  # Betreff: Name des Benutzers
                  sender=user_email,  # Absender ist die E-Mail-Adresse des Benutzers
                  recipients=['myandr180709@gmail.com'])  # E-Mail immer an deine Adresse
    msg.body = f"Nachricht von: {name} ({user_email})\n\n{message}"  # E-Mail-Inhalt

    # E-Mail senden
    try:
        mail.send(msg)
        return render_template("email-sent.html")
    except Exception as e:
        return f'Fehler beim Senden der E-Mail: {str(e)}'


@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

@app.route('/download-form')
def download_form():
    file_path = 'static/IMG_0001.jpeg' # Pfad zur Datei
    return send_file(file_path, as_attachment=True)



DB_PASSWORD = "1234"  # Ersetze dies durch ein starkes Passwort

@app.route('/db-preview', methods=['GET', 'POST'])
def db_preview():
    if request.method == 'POST':
        if request.form['password'] == DB_PASSWORD:
            # Daten aus der Datenbank holen
            users = User.query.all()
            termine = Termin.query.all()
            about_texts = AboutText.query.all()
            content_items = ContentItem.query.all()
            for item in content_items:
                if item.image_data:
                    item.image_data_base64 = base64.b64encode(item.image_data).decode('utf-8')
                else:
                    item.image_data_base64 = None

            box = Box.query.all()
            

            for item in box:
                if item.image_data:
                    item.image_data_base64 = base64.b64encode(item.image_data).decode('utf-8')
                else:
                    item.image_data_base64 = None


            return render_template('db_preview.html', users=users,
                                   termine=termine, about_texts=about_texts, content_item=content_items, box=box)
        else:
            return render_template('passwort.html', error="Falsches Passwort! Versuche es erneut.")

    return render_template('passwort.html', error=None)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/test')
def schule():
    return render_template('test.html')






if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
