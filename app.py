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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user_tuxj_user:n8Iy81pCRKYh0GCc1cbqYzbQhAseN3Fe@dpg-cutmst5ds78s7391hpe0-a.oregon-postgres.render.com/user_tuxj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP-Server
app.config['MAIL_PORT'] = 587  # Port für TLS
app.config['MAIL_USE_TLS'] = True  # TLS aktivieren
app.config['MAIL_USE_SSL'] = False  # SSL nicht verwenden
app.config['MAIL_USERNAME'] = 'myandr180709@gmail.com'  # Deine Gmail-Adresse
app.config['MAIL_DEFAULT_SENDER'] = 'myandr180709@gmail.com'
app.config['MAIL_PASSWORD'] = 'jcyx ozgy hjll hzyl'  # Dein App-Passwort
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['REMEMBER_COOKIE_DURATION'] = 2592000  # 30 days
app.config["SESSION_COOKIE_SECURE"] = True  # Nur über HTTPS senden
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Nicht per JavaScript zugänglich
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"  # Cross-Site-Angriffe verhindern
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {
        "sslmode": "require"
    }
}
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}






#  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____ 
# (____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)







#     __ __   ____  ____   ____   ____  ____   _        ___  ____  
#    |  |  | /    ||    \ |    | /    ||    \ | |      /  _]|    \ 
#    |  |  ||  o  ||  D  ) |  | |  o  ||  o  )| |     /  [_ |  _  |
#    |  |  ||     ||    /  |  | |     ||     || |___ |    _]|  |  |
#    |  :  ||  _  ||    \  |  | |  _  ||  O  ||     ||   [_ |  |  |
#     \   / |  |  ||  .  \ |  | |  |  ||     ||     ||     ||  |  |
#      \_/  |__|__||__|\_||____||__|__||_____||_____||_____||__|__|                                                    
                                                                                                                                            



db = SQLAlchemy(app)

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

login_manager.login_message = "Bitte melde dich an, um diese Seite zu sehen."
login_manager.login_message_category = "info"
login_manager.refresh_message = "Bitte authentifiziere dich erneut, um fortzufahren."
login_manager.refresh_message_category = "error"
login_manager.needs_refresh_message = "Deine Sitzung ist abgelaufen. Bitte melde dich erneut an."
login_manager.needs_refresh_message_category = "error"






#  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____ 
# (____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)






#    ___     ____  ______    ___  ____   ____    ____  ____   __  _ 
#    |   \   /    ||      |  /  _]|    \ |    \  /    ||    \ |  |/ ]
#    |    \ |  o  ||      | /  [_ |  _  ||  o  )|  o  ||  _  ||  ' / 
#    |  D  ||     ||_|  |_||    _]|  |  ||     ||     ||  |  ||    \ 
#    |     ||  _  |  |  |  |   [_ |  |  ||  O  ||  _  ||  |  ||     \
#    |     ||  |  |  |  |  |     ||  |  ||     ||  |  ||  |  ||  .  |
#    |_____||__|__|  |__|  |_____||__|__||_____||__|__||__|__||__|\_|




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
    uhrzeit = db.Column(db.String(100), nullable=False)
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
 
class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    short_title = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(5), nullable=False)  # Format: "HH:MM"
    end_time = db.Column(db.String(5), nullable=False)    # Format: "HH:MM"
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(20), nullable=False)   # 'training', 'turnier', 'sonstiges'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'shortTitle': self.short_title,
            'date': self.date.strftime('%Y-%m-%d'),
            'startTime': self.start_time,
            'endTime': self.end_time,
            'location': self.location,
            'description': self.description or '',
            'category': self.category
        }

# Erstellen Sie die Tabellen in der Datenbank
with app.app_context():
    db.create_all()


#  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____ 
# (____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)







#    ____    ___   __ __  ______    ___  ____  
#    |    \  /   \ |  |  ||      |  /  _]|    \ 
#    |  D  )|     ||  |  ||      | /  [_ |  _  |
#    |    / |  O  ||  |  ||_|  |_||    _]|  |  |
#    |    \ |     ||  :  |  |  |  |   [_ |  |  |
#    |  .  \|     ||     |  |  |  |     ||  |  |
#    |__|\_| \___/  \__,_|  |__|  |_____||__|__|




@app.route('/mannschaften')
def mannschaften():
    return render_template('design1/mannschaften.html')

@app.route('/mannschaften/damen-1')
def damen_1():
    return render_template('design1/mannschaften/damen-1.html')

@app.route('/mannschaften/damen-2')
def damen_2():
    return render_template('design1/mannschaften/damen-2.html')

@app.route('/mannschaften/herren-1')
def herren_1():
    return render_template('design1/mannschaften/herren-1.html')

@app.route('/mannschaften/herren-2')
def herren_2():
    return render_template('design1/mannschaften/herren-2.html')

@app.route('/mannschaften/herren-30')
def herren_30():
    return render_template('design1/mannschaften/herren-30.html')

@app.route('/mannschaften/damen-40')
def damen_40():
    return render_template('design1/mannschaften/damen-40.html')

@app.route('/mannschaften/herren-40-1')
def herren_40_1():
    return render_template('design1/mannschaften/herren-40-1.html')

@app.route('/mannschaften/herren-40-2')
def herren_40_2():
    return render_template('design1/mannschaften/herren-40-2.html')

@app.route('/mannschaften/damen-50')
def damen_50():
    return render_template('design1/mannschaften/damen-50.html')

@app.route('/mannschaften/herren-55')
def herren_55():
    return render_template('design1/mannschaften/herren-55.html')

@app.route('/mannschaften/herren-60')
def herren_60():
    return render_template('design1/mannschaften/herren-60.html')

@app.route('/mannschaften/damen-doppel-40')
def damen_doppel_40():
    return render_template('design1/mannschaften/damen-doppel-40.html')

@app.route('/mannschaften/herren-doppel-60')
def herren_doppel_60():
    return render_template('design1/mannschaften/herren-doppel-60.html')

@app.route('/mannschaften/gemischt-1')
def gemischt_1():
    return render_template('design1/mannschaften/gemischt-1.html')

@app.route('/mannschaften/gemischt-2')
def gemischt_2():
    return render_template('design1/mannschaften/gemischt-2.html')

@app.route('/mannschaften/mixed-50-doppel')
def mixed_50_doppel():
    return render_template('design1/mannschaften/mixed-50-doppel.html')

@app.route("/impressum")
def impressum():
    return render_template("design1/impressum.html")

@app.route("/vorstand")
def vorstand():
    return render_template("design1/vorstand.html")

@app.route("/training")
def training():
    return render_template("design1/training.html")

@app.route('/galerie')
def gallery():
    return render_template('design1/gallery.html')




website_content = {
    # Main Navigation & Home Sections
    "Startseite": {
        "url": "/#home",
        "description": "Willkommen beim Hardter Tennisverein"
    },
    "Standorte": {
        "url": "/#one",
        "description": "Unsere Tennisplätze und Trainingsstandorte"
    },
    "Über uns": {
        "url": "/#about",
        "description": "Geschichte und Information über den Hardter Tennisverein"
    },
    "Bilder": {
        "url": "/#img",
        "description": "Fotogalerie unserer Anlage und Veranstaltungen"
    },
    "Termine": {
        "url": "/#termine",
        "description": "Aktuelle Turniere und Veranstaltungstermine"
    },
    
    # Training Section
    "Trainer": {
        "url": "/#trainer",
        "description": "Unsere qualifizierten Tennistrainer"
    },
    "Tennistraining": {
        "url": "/#trainer",
        "description": "Professionelles Training für alle Altersgruppen"
    },
    "Trainingsgruppen": {
        "url": "/#trainer",
        "description": "Jugend-, Erwachsenen- und Leistungstraining"
    },
    "Trainingszeiten": {
        "url": "/#trainer",
        "description": "Aktuelle Trainingszeiten und Platzbelegung"
    },
    
    # News Section
    "Neuigkeiten": {
        "url": "/#news",
        "description": "Aktuelle Nachrichten und Ankündigungen"
    },
    "News": {
        "url": "/news",
        "description": "Vereinsnachrichten und Turnierberichte"
    },
    "Turnierberichte": {
        "url": "/news",
        "description": "Aktuelle Ergebnisse und Spielberichte"
    },
    "Vereinsnachrichten": {
        "url": "/news",
        "description": "Wichtige Informationen für Vereinsmitglieder"
    },
    
    # Contact & Support
    "Kontakt": {
        "url": "/#contact",
        "description": "Kontaktieren Sie uns - Hardter Tennisverein"
    },
    "Downloads": {
        "url": "/downloads",
        "description": "Formulare, Dokumente und Informationsmaterial"
    },
    "Blog": {
        "url": "/newsletter",
        "description": "Tennis-Blog und Newsletter"
    },
    
    # Account Management
    "Account": {
        "url": "/dashboard",
        "description": "Ihr persönlicher Mitgliederbereich"
    },
    "Login": {
        "url": "/login",
        "description": "Anmeldung für Mitglieder"
    },
    "Registrierung": {
        "url": "/signup",
        "description": "Neues Mitgliedskonto erstellen"
    },
    
    # Additional Club Information
    "Mitgliedschaft": {
        "url": "/#about",
        "description": "Informationen zur Vereinsmitgliedschaft"
    },
    "Platzreservierung": {
        "url": "/#termine",
        "description": "Online Tennisplatz buchen"
    },
    "Jugendförderung": {
        "url": "/#trainer",
        "description": "Jugendtraining und Nachwuchsförderung"
    },
    "Tenniskurse": {
        "url": "/#trainer",
        "description": "Anfänger- und Fortgeschrittenenkurse"
    },
    
    # Events & Activities
    "Vereinsturniere": {
        "url": "/#termine",
        "description": "Interne Turniere und Wettkämpfe"
    },
    "Mannschaften": {
        "url": "/news",
        "description": "Unsere Mannschaften und Spielergebnisse"
    },
    "Veranstaltungen": {
        "url": "/#termine",
        "description": "Soziale Events und Clubveranstaltungen"
    }
}                              

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify({})
    
    results = {}
    for key, data in website_content.items():
        if (query in key.lower() or 
            query in data['description'].lower()):
            results[key] = {
                'url': data['url'],
                'description': data['description']
            }
    return jsonify(results)


# Nur für die Testversion um zwei Design anzeigen lassen zu können

@app.route('/choose-design', methods=['GET', 'POST'])
def choose_design():
    if request.method == 'POST':
        # Ausgewähltes Design speichern
        session['design'] = request.form.get('design1', 'design2')

        return redirect(url_for('home'))  # Weiterleitung zur Anmeldeseite

    return render_template('choose_design.html')



@app.route('/sitemap')
def sitemap():
    return send_from_directory('.', 'sitemap.xml', mimetype='application/xml')

@app.route('/newsletter')
def newsletter():
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design
    return render_template(f'{design}/newsletter.html')



@app.before_request
def before_request():
    session.modified = True
    if current_user.is_authenticated and not current_user.is_verified and request.endpoint != 'verify' and request.endpoint != 'resend_verification':
        flash('Bitte verifizieren Sie zuerst Ihre E-Mail', 'error')
        return redirect(url_for('verify'))
    


@app.before_request
def before_request():
    session.modified = True


@app.before_request
def make_session_permanent():
    session.permanent = True




#  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____ 
# (____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)



#      ____  ___    ___   
#     /    ||   \  |   \  
#    |  o  ||    \ |    \ 
#    |     ||  D  ||  D  |
#    |  _  ||     ||     |
#    |  |  ||     ||     |
#    |__|__||_____||_____|
                    








#     __ _  ____  _  _  ____ 
#    (  ( \(  __)/ )( \/ ___)
#    /    / ) _) \ /\ /\___ \
#    \_)__)(____)(_/\_)(____/

@app.route('/news', methods=['GET', 'POST'])
def news():
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
    
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


    return render_template(f'{design}/news.html', logged_in=current_user.is_authenticated, is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active, boxes=boxes)


#     ____  ____  __    ____  ____  ____ 
#    (    \(  __)(  )  (  __)(_  _)(  __)
#     ) D ( ) _) / (_/\ ) _)   )(   ) _) 
#    (____/(____)\____/(____) (__) (____)

@app.route('/delete/<int:box_id>', methods=['POST'])
def delete_box(box_id):
    box = Box.query.get_or_404(box_id)
    

    if box.image_data:
        box.image_data = None  # Bild aus der Datenbank entfernen
    
    db.session.delete(box)
    db.session.commit()
    return redirect(url_for('news'))












#kalender



@app.route('/kalender')
def kalender():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/kalender.html',                            
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/api/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.form
    
    # Validate required fields
    required_fields = ['title', 'short_title', 'date', 'start_time', 'end_time', 'location', 'category']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Field {field} is required'}), 400
    
    # Parse date
    try:
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Create new event
    new_event = Event(
        title=data['title'],
        short_title=data['short_title'],
        date=date_obj,
        start_time=data['start_time'],
        end_time=data['end_time'],
        location=data['location'],
        description=data.get('description', ''),
        category=data['category']
    )
    
    db.session.add(new_event)
    db.session.commit()
    
    return jsonify(new_event.to_dict()), 201

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'}), 200

@app.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.form
    
    # Update fields if provided
    if 'title' in data:
        event.title = data['title']
    if 'short_title' in data:
        event.short_title = data['short_title']
    if 'date' in data:
        try:
            event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    if 'start_time' in data:
        event.start_time = data['start_time']
    if 'end_time' in data:
        event.end_time = data['end_time']
    if 'location' in data:
        event.location = data['location']
    if 'description' in data:
        event.description = data['description']
    if 'category' in data:
        event.category = data['category']
    
    db.session.commit()
    return jsonify(event.to_dict())


#     __     __    ___   __   ____   __    __   __ _ 
#    (  )   /  \  / __) / _\ (_  _) (  )  /  \ (  ( \
#    / (_/\(  O )( (__ /    \  )(    )(  (  O )/    /
#    \____/ \__/  \___)\_/\_/ (__)  (__)  \__/ \_)__)


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
    
    return redirect(url_for('home') + "#one")

#     ____  ____  __    ____  ____  ____ 
#    (    \(  __)(  )  (  __)(_  _)(  __)
#     ) D ( ) _) / (_/\ ) _)   )(   ) _) 
#    (____/(____)\____/(____) (__) (____)

@app.route('/delete/<int:item_id>')
def delete_content(item_id):
    item = ContentItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('home') + '#one')

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








#     ____  ____  ____  _  _   __   __ _  ____ 
#    (_  _)(  __)(  _ \( \/ ) (  ) (  ( \(  __)
#      )(   ) _)  )   // \/ \  )(  /    / ) _) 
#     (__) (____)(__\_)\_)(_/ (__) \_)__)(____)


@app.route('/add_termin', methods=['POST'])
def add_termin():
    datum = request.form['datum']
    veranstaltung = request.form['veranstaltung']
    uhrzeit = request.form['uhrzeit']
    ort = request.form['ort']

    neuer_termin = Termin(datum=datum, veranstaltung=veranstaltung, uhrzeit=uhrzeit, ort=ort)
    db.session.add(neuer_termin)
    db.session.commit()
    return redirect(url_for('home') + "#termine")


#     ____  ____  __    ____  ____  ____ 
#    (    \(  __)(  )  (  __)(_  _)(  __)
#     ) D ( ) _) / (_/\ ) _)   )(   ) _) 
#    (____/(____)\____/(____) (__) (____)

@app.route('/delete_termin/<int:termin_id>', methods=['POST'])
def delete_termin(termin_id):
    termin = Termin.query.get_or_404(termin_id)
    db.session.delete(termin)
    db.session.commit()
    return redirect(url_for('home') + "#termine")





@app.route('/add_img', methods=["POST"])
def add_img():
    if 'image' not in request.files:
        return redirect(url_for('home'))
    
    file = request.files['image']
    
    if file.filename == '':
        return redirect(url_for('home'))
    

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Bild in Binärdaten umwandeln
        image = file.read()
        new_item = Img(
            image=image,

        )
        db.session.add(new_item)
        db.session.commit()
    return redirect(url_for('home') + "#img")


@app.route('/delete_img/<int:img_id>')
def delete_img(img_id):
    image = Img.query.get_or_404(img_id)
    db.session.delete(image)
    db.session.commit()
    return redirect(url_for('home') + "#img")



#      __   ____   __   _  _  ____ 
#     / _\ (  _ \ /  \ / )( \(_  _)
#    /    \ ) _ ((  O )) \/ (  )(  
#    \_/\_/(____/ \__/ \____/ (__)


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

#     ____  ____  __    ____  ____  ____ 
#    (    \(  __)(  )  (  __)(_  _)(  __)
#     ) D ( ) _) / (_/\ ) _)   )(   ) _) 
#    (____/(____)\____/(____) (__) (____)

@app.route("/delete_about_text/<int:id>", methods=["POST"])
def delete_about_text(id):
    text_to_delete = AboutText.query.get(id)
    if text_to_delete:
        db.session.delete(text_to_delete)
        db.session.commit()
    else:
        flash("Text nicht gefunden.", "error")
    return redirect(url_for('home') + "#about")






#  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____ 
# (____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)









#     _       ___    ____  ____  ____  
#    | |     /   \  /    ||    ||    \ 
#    | |    |     ||   __| |  | |  _  |
#    | |___ |  O  ||  |  | |  | |  |  |
#    |     ||     ||  |_ | |  | |  |  |
#    |     ||     ||     | |  | |  |  |
#    |_____| \___/ |___,_||____||__|__|
                                  












@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def generate_verification_code():
    return ''.join(random.choices('0123456789', k=6))


def send_verification_email(email, code):
    msg = Message('Verify Your Email', sender='your_email@gmail.com', recipients=[email])
    msg.body = f'Your verification code is: {code}'
    mail.send(msg)






#     ____   __    ___  __ _  _  _  ____ 
#    / ___) (  )  / __)(  ( \/ )( \(  _ \
#    \___ \  )(  ( (_ \/    /) \/ ( ) __/
#    (____/ (__)  \___/\_)__)\____/(__) 


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design
    if current_user.is_authenticated:
        flash('Du bist bereits eingeloggt. Bitte melde dich ab, um einen neuen Account zu erstellen.', 'info')
        return redirect(url_for('dashboard'))
    
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
    
    return render_template(f'{design}/signup.html')






#    _  _  ____  ____   __   ____  _  _ 
#   / )( \(  __)(  _ \ (  ) (  __)( \/ )
#   \ \/ / ) _)  )   /  )(   ) _)  )  / 
#    \__/ (____)(__\_) (__) (__)  (__/



@app.route('/verify', methods=['GET', 'POST'])
def verify():
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design
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
    
    return render_template(f'{design}/verify.html', email=email)





#     __     __    ___   __   __ _ 
#    (  )   /  \  / __) (  ) (  ( \
#    / (_/\(  O )( (_ \  )(  /    /
#    \____/ \__/  \___/ (__) \_)__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design

    if current_user.is_authenticated:
        flash('Du bist bereits eingeloggt. Bitte melde dich ab, um mit einem neuen Account dich einzuloggen.', 'info')
        return redirect(url_for('dashboard'))
    
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
    
    return render_template(f'{design}/login.html')







#     ____   __   ____  _  _  ____   __    __   ____  ____ 
#    (    \ / _\ / ___)/ )( \(  _ \ /  \  / _\ (  _ \(    \
#     ) D (/    \\___ \) __ ( ) _ ((  O )/    \ )   / ) D (
#    (____/\_/\_/(____/\_)(_/(____/ \__/ \_/\_/(__\_)(____/


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
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design
    if not current_user.is_verified:
        flash('Bitte verifizieren Sie zuerst Ihre E-Mail', 'error')
        return redirect(url_for('verify'))
    
    users = User.query.all()
    return render_template(f'{design}/dashboard.html', 
                           is_admin=current_user.is_authenticated and current_user.role == 'admin', 
                           user=current_user, 
                           users=users)





#     __     __    ___   __   _  _  ____ 
#    (  )   /  \  / __) /  \ / )( \(_  _)
#    / (_/\(  O )( (_ \(  O )) \/ (  )(  
#    \____/ \__/  \___/ \__/ \____/ (__)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sie sind erfolgreich ausgeloggt', 'success')
    return redirect(url_for('login'))







#     ____  ____  ____  ____  __ _  ____     _   ____   __   ____   ___   __   ____ 
#    (  _ \(  __)/ ___)(  __)(  ( \(    \   / ) (  __) /  \ (  _ \ / __) /  \ (_  _)
#     )   / ) _) \___ \ ) _) /    / ) D (  / /   ) _) (  O ) )   /( (_ \(  O )  )(  
#    (__\_)(____)(____/(____)\_)__)(____/ (_/   (__)   \__/ (__\_) \___/ \__/  (__) 



@app.route('/resend_verification', methods=['GET', 'POST'])
def resend_verification():
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design
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
    return render_template(f'{design}/resend_verification.html')

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
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            send_password_reset_email(user.email)
            flash('Eine E-Mail zur Zurücksetzung des Passworts wurde gesendet', 'info')
        else:
            flash('E-Mail-Adresse nicht gefunden', 'error')
        return redirect(url_for('login'))
    return render_template(f'{design}/forgot_password.html')





@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design
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
            return render_template(f'{design}/reset_password.html', token=token)
        
        user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.commit()
        flash('Ihr Passwort wurde aktualisiert!', 'success')
        return redirect(url_for('login'))
    
    return render_template(f'{design}/reset_password.html', token=token)





#     ____  ____  __    ____  ____  ____     _   ____  ____   __   ____ 
#    (    \(  __)(  )  (  __)(_  _)(  __)   / ) (  __)(    \ (  ) (_  _)
#     ) D ( ) _) / (_/\ ) _)   )(   ) _)   / /   ) _)  ) D (  )(    )(  
#    (____/(____)\____/(____) (__) (____) (_/   (____)(____/ (__)  (__) 



@app.route('/delete_account', methods=['POST'])
def delete_account():
    if current_user.is_authenticated:
        user = current_user._get_current_object()  # Ensure you get the actual object
        db.session.delete(user)
        db.session.commit()
        flash('Account erfolgreich gelöscht', 'success')
        return redirect(url_for('signup'))
    return redirect(url_for('login'))




@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    # Überprüfen, ob der aktuelle Benutzer ein Admin ist
    if current_user.role != 'admin':
        flash('Nur Administratoren können Benutzer löschen.', 'error')
        return redirect(url_for('dashboard'))

    # Suche den Benutzer in der Datenbank
    user = User.query.get_or_404(user_id)
    
    # Stelle sicher, dass der Admin nicht sich selbst löscht
    if user.id == current_user.id:
        flash('Du kannst dein eigenes Konto nicht löschen.', 'error')
        return redirect(url_for('dashboard'))

    # Lösche den Benutzer
    db.session.delete(user)
    db.session.commit()

    flash('Benutzer erfolgreich gelöscht.', 'success')
    return redirect(url_for('dashboard'))





@app.route('/edit_account', methods=['GET', 'POST'])
@login_required
def edit_account():
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design
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

    return render_template(f'{design}/edit_account.html', user=current_user)








#      __   ____  _  _   __   __ _ 
#     / _\ (    \( \/ ) (  ) (  ( \
#    /    \ ) D (/ \/ \  )(  /    /
#    \_/\_/(____/\_)(_/ (__) \_)__)


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








#  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____ 
# (____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)









#     __ __   ___   ___ ___    ___ 
#    |  |  | /   \ |   |   |  /  _]
#    |  |  ||     || _   _ | /  [_ 
#    |  _  ||  O  ||  \_/  ||    _]
#    |  |  ||     ||   |   ||   [_ 
#    |  |  ||     ||   |   ||     |
#    |__|__| \___/ |___|___||_____|














@app.route('/')
def home():
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design
    images = Image.query.all()
    image = Img.query.all()
    about_texts = AboutText.query.all()
    content_items = ContentItem.query.all()
    for item in content_items:
        if item.image_data:
            item.image_data_base64 = base64.b64encode(item.image_data).decode('utf-8')
        else:
            item.image_data_base64 = None

    for img in image:
        if img.image:
            img.image_data_base64 = base64.b64encode(img.image).decode('utf-8')
        else:
            img.image_data_base64 = None

    termine = Termin.query.all()

    cookie_consent = request.cookies.get('necessary') == 'true'

    is_admin_active = session.get('is_admin_active', True)



    return render_template(f'{design}/index.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified,
                           termine=termine,
                           about_texts=about_texts,
                           images=images,
                           content_items=content_items,
                           cookie_consent=cookie_consent,
                           image=image)






#      ___   __    __   __ _   __   ____  ____ 
#     / __) /  \  /  \ (  / ) (  ) (  __)/ ___)
#    ( (__ (  O )(  O ) )  (   )(   ) _) \___ \
#     \___) \__/  \__/ (__\_) (__) (____)(____/



@app.route('/api/cookies/accept-all', methods=['POST'])
def accept_all_cookies():
    response = make_response(jsonify({'message': 'Alle Cookies akzeptiert'}))
    
    # Set cookies with 1 year expiration
    expires = datetime.now() + timedelta(days=365)
    
    response.set_cookie('necessary', 'true', expires=expires, secure=True, httponly=True)
    response.set_cookie('functional', 'true', expires=expires, secure=True)
    response.set_cookie('analytics', 'true', expires=expires, secure=True)
    
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








#  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____ 
# (____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)







#     ___ ___   ____  ____  _       _____
#    |   |   | /    ||    || |     / ___/
#    | _   _ ||  o  | |  | | |    (   \_ 
#    |  \_/  ||     | |  | | |___  \__  |
#    |   |   ||  _  | |  | |     | /  \ |
#    |   |   ||  |  | |  | |     | \    |
#    |___|___||__|__||____||_____|  \___|
                                   








#     __ _  ____  _  _  ____  __    ____  ____  ____  ____  ____ 
#    (  ( \(  __)/ )( \/ ___)(  )  (  __)(_  _)(_  _)(  __)(  _ \
#    /    / ) _) \ /\ /\___ \/ (_/\ ) _)   )(    )(   ) _)  )   /
#    \_)__)(____)(_/\_)(____/\____/(____) (__)  (__) (____)(__\_)




@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']  # E-Mail-Adresse vom Benutzer
    
    # Hier kannst du die E-Mail-Adresse in einer Datenbank speichern, wenn gewünscht
    
    # E-Mail senden
    msg = Message('Danke für deine Anmeldung zum Newsletter!',
                  recipients=[email])
    msg.html = '''
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <table style="width: 100%; max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">
                <tr>
                    <td style="text-align: center; padding-bottom: 20px;">
                        <h1 style="color: #4CAF50;">Willkommen bei unserem Newsletter!</h1>
                    </td>
                </tr>
                <tr>
                    <td>
                        <p style="font-size: 16px; line-height: 1.6;">
                            Vielen Dank, dass du dich für unseren Newsletter angemeldet hast! Du wirst nun regelmäßig mit den neuesten Updates, 
                            exklusiven Angeboten und spannenden Neuigkeiten versorgt. Wir freuen uns, dich auf dieser Reise dabei zu haben!
                        </p>
                        <p style="font-size: 16px; line-height: 1.6;">
                            In den kommenden Ausgaben erwarten dich unter anderem:
                        </p>
                        <ul style="font-size: 16px; line-height: 1.6;">
                            <li>Exklusive Einblicke in kommende Produkte und Angebote</li>
                            <li>Tipps und Tricks aus unserer Branche</li>
                            <li>Besondere Rabatte und Aktionen nur für Newsletter-Abonnenten</li>
                        </ul>
                        <p style="font-size: 16px; line-height: 1.6;">
                            Wir hoffen, dass du unsere Inhalte spannend findest und freuen uns auf dein Feedback. 
                            Falls du dich irgendwann vom Newsletter abmelden möchtest, findest du dafür immer einen Link am Ende jeder E-Mail.
                        </p>
                    </td>
                </tr>
                <tr>
                    <td style="text-align: center; padding-top: 20px;">
                        <p style="font-size: 14px; color: #999;">Mit freundlichen Grüßen,<br>
                        Dein Newsletter-Team</p>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    '''
    
    try:
        mail.send(msg)  # E-Mail versenden
        flash('E-Mail wurde erfolgreich versendet!', 'success')
    except Exception as e:
        flash(f'Fehler beim Senden der E-Mail: {e}', 'error')
    
    return redirect(url_for('home'))





#     ____  ____  __ _  ____  ____  __ _ 
#    / ___)(  __)(  ( \(    \(  __)(  ( \
#    \___ \ ) _) /    / ) D ( ) _) /    /
#    (____/(____)\_)__)(____/(____)\_)__)



@app.route('/send_email', methods=['POST'])
def send_email():
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design
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
        return render_template(f'{design}/email-sent.html')
    except Exception as e:
        return f'Fehler beim Senden der E-Mail: {str(e)}'






#  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____ 
# (____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)








#     _____  ___   ____    _____ ______  ____   ____    ___   _____
#    / ___/ /   \ |    \  / ___/|      ||    | /    |  /  _] / ___/
#   (   \_ |     ||  _  |(   \_ |      | |  | |   __| /  [_ (   \_ 
#    \__  ||  O  ||  |  | \__  ||_|  |_| |  | |  |  ||    _] \__  |
#    /  \ ||     ||  |  | /  \ |  |  |   |  | |  |_ ||   [_  /  \ |
#    \    ||     ||  |  | \    |  |  |   |  | |     ||     | \    |
#      \___| \___/ |__|__|  \___|  |__|  |____||___,_||_____|  \___|











@app.route('/downloads')
def downloads():
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design
    return render_template(f'{design}/downloads.html')

@app.route('/download-form')
def download_form():
    file_path = 'static/IMG_0001.jpeg' # Pfad zur Datei
    return send_file(file_path, as_attachment=True)






DB_PASSWORD = "1234"  # Ersetze dies durch ein starkes Passwort

@app.route('/db-preview', methods=['GET', 'POST'])
def db_preview():
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design
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


            return render_template(f'{design}/db_preview.html', users=users,
                                   termine=termine, about_texts=about_texts, content_item=content_items, box=box)
        else:
            return render_template(f'{design}/passwort.html', error="Falsches Passwort! Versuche es erneut.")

    return render_template(f'{design}/passwort.html', error=None)



@app.errorhandler(404)
def page_not_found(e):
    design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
#design
    return render_template(f'{design}/404.html'), 404




#  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____  ____ 
# (____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)(____)






if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
