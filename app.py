from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify, send_from_directory, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import random
import uuid
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
from sqlalchemy import desc
import uuid

SAVE_PATH = 'editable_content.html'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hardt_tennis_datenbank_user:VUlLWxv3Whg4vyT4K3galn9ppelR6YYp@dpg-d06djibuibrs73efs0rg-a.oregon-postgres.render.com/hardt_tennis_datenbank'
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
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'downloads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)





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

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    excerpt = db.Column(db.Text, nullable=False)
    full_text = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=False)
    archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    short_title = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)  # Renamed from date
    end_date = db.Column(db.Date, nullable=True)     # New field for multi-day events
    is_all_day = db.Column(db.Boolean, default=False)  # New field for all-day events
    start_time = db.Column(db.String(5), nullable=True)  # Now nullable
    end_time = db.Column(db.String(5), nullable=True)    # Now nullable
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(20), nullable=False)   # 'training', 'turnier', 'sonstiges'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'shortTitle': self.short_title,
            'startDate': self.start_date.strftime('%Y-%m-%d'),
            'endDate': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'isAllDay': self.is_all_day,
            'startTime': self.start_time,
            'endTime': self.end_time,
            'location': self.location,
            'description': self.description or '',
            'category': self.category
        }
    
class AboutSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    title_mitgliedschaft = db.Column(db.Text, nullable=False)
    title_location = db.Column(db.Text, nullable=False)
    title_termin = db.Column(db.Text, nullable=False)
    title_vorstand = db.Column(db.Text, nullable=False)
    title_news = db.Column(db.Text, nullable=False)
    title_kontakt = db.Column(db.Text, nullable=False)
    welcome_text = db.Column(db.Text, nullable=False)
    welcome_text_location = db.Column(db.Text, nullable=False)
    welcome_text_mitgliedschaft = db.Column(db.Text, nullable=False)
    welcome_text_termin = db.Column(db.Text, nullable=False)
    welcome_text_vorstand = db.Column(db.Text, nullable=False)
    welcome_text_news = db.Column(db.Text, nullable=False)
    welcome_text_kontakt = db.Column(db.Text, nullable=False)
    club_text = db.Column(db.Text, nullable=False)
    goals_text = db.Column(db.Text, nullable=False)
    membership_text = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    title_training = db.Column(db.Text, nullable=False)
    welcome_text_training = db.Column(db.Text, nullable=False)
    text_training_1 = db.Column(db.Text, nullable=False)
    text_training_2 = db.Column(db.Text, nullable=False)
    text_training_3 = db.Column(db.Text, nullable=False)
    text_training_4 = db.Column(db.Text, nullable=False)
    news_card1_date = db.Column(db.String(255), nullable=False, default="4. Oktober 2024")
    news_card1_title = db.Column(db.String(255), nullable=False, default="Saisonabschlussfest 2024")
    news_card1_excerpt = db.Column(db.Text, nullable=False, default="Am vergangenen Samstag haben wir in geselliger Runde die Sommersaison verabschiedet: Wir haben gemeinsam …")
    news_card1_full_text = db.Column(db.Text, nullable=False, default="Am vergangenen Samstag haben wir in geselliger Runde die Sommersaison verabschiedet: Wir haben gemeinsam auf die schönsten Momente angestoßen, die Tanzfläche unsicher gemacht und die Saison noch einmal Revue passieren lassen.")
    news_card1_image = db.Column(db.String(255), nullable=False, default="/static/images/tennis.jpg")
    
    # News card 2
    news_card2_date = db.Column(db.String(255), nullable=False, default="4. Oktober 2024")
    news_card2_title = db.Column(db.String(255), nullable=False, default="Jahresrückblick 2024")
    news_card2_excerpt = db.Column(db.Text, nullable=False, default="Jahresrückblick 2024 – Danke für eine unvergessliche Saison! Das Jahr 2024 neigt sich dem Ende zu, und wir blicken auf eine großartige Saison voller schöner Momente zurück! Von der …")
    news_card2_full_text = db.Column(db.Text, nullable=False, default="Jahresrückblick 2024 – Danke für eine unvergessliche Saison! Das Jahr 2024 neigt sich dem Ende zu, und wir blicken auf eine großartige Saison voller schöner Momente zurück! Von der Saisoneröffnung bis zum Abschlussfest – es war ein Jahr voller Tennis, Freundschaft und gemeinsamer Erfolge.")
    news_card2_image = db.Column(db.String(255), nullable=False, default="/static/images/wilson-2259352_960_720.jpg")
    
    # News card 3
    news_card3_date = db.Column(db.String(255), nullable=False, default="News")
    news_card3_title = db.Column(db.String(255), nullable=False, default="Saisonabschluss 2024 – ein Abend voller Highlights!")
    news_card3_excerpt = db.Column(db.Text, nullable=False, default="Am vergangenen Samstag haben wir in geselliger Runde die Sommersaison verabschiedet: Wir haben gemeinsam auf die schönsten Momente angestoßen, die Tanzfläche unsicher")
    news_card3_full_text = db.Column(db.Text, nullable=False, default="Am vergangenen Samstag haben wir in geselliger Runde die Sommersaison verabschiedet: Wir haben gemeinsam auf die schönsten Momente angestoßen, die Tanzfläche unsicher gemacht und die Saison noch einmal Revue passieren lassen. Ein besonderes Highlight des Abends war das fantastische Buffet, das unsere Küchenfee Petra für uns gezaubert hat – ein Genuss für alle! Ein perfekter Abschluss für eine großartige Saison! Auf viele weitere gemeinsame Erlebnisse und unvergessliche Tennis-Momente im nächsten Jahr!")
    news_card3_image = db.Column(db.String(255), nullable=False, default="/static/images/Sasionabschluss 2024.jpg")
    
    # News card 4
    news_card4_date = db.Column(db.String(255), nullable=False, default="News")
    news_card4_title = db.Column(db.String(255), nullable=False, default="Unsere eigene Vereinskollektion ist da!")
    news_card4_excerpt = db.Column(db.Text, nullable=False, default="Endlich ist es soweit – ab sofort könnt ihr unsere brandneue Vereinskleidung bekommen! Ob für …")
    news_card4_full_text = db.Column(db.Text, nullable=False, default="Endlich ist es soweit – ab sofort könnt ihr unsere brandneue Vereinskleidung bekommen! Ob für Training, Wettkampf oder Freizeit – mit unserer Vereinskleidung zeigt ihr, dass ihr Teil unserer Tennis-Familie seid!")
    news_card4_image = db.Column(db.String(255), nullable=False, default="/static/images/tennis-court-1671852_960_720.jpg")

    location_card1_title = db.Column(db.String(255), nullable=False, default="6 Ascheplätze")
    location_card1_subtitle = db.Column(db.Text, nullable=False, default="Zwei mit Flutlichtanlage")
    location_card1_address = db.Column(db.Text, nullable=False, default="Gahlener Str. 204\n46284 Dorsten")
    location_card1_image = db.Column(db.String(255), nullable=False, default="/static/images/image copy 4.png")
    
    # Location card 2
    location_card2_title = db.Column(db.String(255), nullable=False, default="Clubheim Hardt")
    location_card2_subtitle = db.Column(db.Text, nullable=False, default="Vermietung nur an Mitglieder\nGastronomie")
    location_card2_address = db.Column(db.Text, nullable=False, default="Gahlener Str. 204\n46284 Dorsten")
    location_card2_image = db.Column(db.String(255), nullable=False, default="/static/images/image copy 2.png")
    
    # Location card 3
    location_card3_title = db.Column(db.String(255), nullable=False, default="Kletter- und Spielgerüst")
    location_card3_subtitle = db.Column(db.Text, nullable=False, default="")
    location_card3_address = db.Column(db.Text, nullable=False, default="Gahlener Str. 204\n46284 Dorsten")
    location_card3_image = db.Column(db.String(255), nullable=False, default="/static/images/image copy 3.png")
    
    # Location card 4
    location_card4_title = db.Column(db.String(255), nullable=False, default="Kleinfeldplatz inkl. Tenniswand")
    location_card4_subtitle = db.Column(db.Text, nullable=False, default="")
    location_card4_address = db.Column(db.Text, nullable=False, default="Gahlener Str. 204\n46284 Dorsten")
    location_card4_image = db.Column(db.String(255), nullable=False, default="/static/images/image.png")


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'title_mitgliedschaft': self.title_mitgliedschaft,
            'title_location': self.title_location,
            'title_termin': self.title_termin,
            'title_vorstand': self.title_vorstand,
            'title_news': self.title_news,
            'title_kontakt': self.title_kontakt,
            'welcome_text': self.welcome_text,
            'welcome_text_mitgliedschaft': self.welcome_text_mitgliedschaft,
            'welcome_text_location': self.welcome_text_location,
            'welcome_text_termin': self.welcome_text_termin,
            'welcome_text_vorstand': self.welcome_text_vorstand,
            'welcome_text_news': self.welcome_text_news,
            'welcome_text_kontakt': self.welcome_text_kontakt,
            'club_text': self.club_text,
            'goals_text': self.goals_text,
            'membership_text': self.membership_text,
            'image_path': self.image_path,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'title_training': self.title_training,
            'welcome_text_training': self.welcome_text_training,
            'text_training_1': self.text_training_1,
            'text_training_2': self.text_training_2,
            'text_training_3': self.text_training_3,
            'text_training_4': self.text_training_4,
            'news_card1_date': self.news_card1_date,
            'news_card1_title': self.news_card1_title,
            'news_card1_excerpt': self.news_card1_excerpt,
            'news_card1_full_text': self.news_card1_full_text,
            'news_card1_image': self.news_card1_image,
            
            'news_card2_date': self.news_card2_date,
            'news_card2_title': self.news_card2_title,
            'news_card2_excerpt': self.news_card2_excerpt,
            'news_card2_full_text': self.news_card2_full_text,
            'news_card2_image': self.news_card2_image,
            
            'news_card3_date': self.news_card3_date,
            'news_card3_title': self.news_card3_title,
            'news_card3_excerpt': self.news_card3_excerpt,
            'news_card3_full_text': self.news_card3_full_text,
            'news_card3_image': self.news_card3_image,
            
            'news_card4_date': self.news_card4_date,
            'news_card4_title': self.news_card4_title,
            'news_card4_excerpt': self.news_card4_excerpt,
            'news_card4_full_text': self.news_card4_full_text,
            'news_card4_image': self.news_card4_image,

            'location_card1_title': self.location_card1_title,
            'location_card1_subtitle': self.location_card1_subtitle,
            'location_card1_address': self.location_card1_address,
            'location_card1_image': self.location_card1_image,
            
            'location_card2_title': self.location_card2_title,
            'location_card2_subtitle': self.location_card2_subtitle,
            'location_card2_address': self.location_card2_address,
            'location_card2_image': self.location_card2_image,
            
            'location_card3_title': self.location_card3_title,
            'location_card3_subtitle': self.location_card3_subtitle,
            'location_card3_address': self.location_card3_address,
            'location_card3_image': self.location_card3_image,
            
            'location_card4_title': self.location_card4_title,
            'location_card4_subtitle': self.location_card4_subtitle,
            'location_card4_address': self.location_card4_address,
            'location_card4_image': self.location_card4_image,

        }

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    cover_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Beziehung zu den Bildern
    images = db.relationship('GalleryImage', backref='gallery', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'slug': self.slug,
            'cover_image': self.cover_image,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'image_count': len(self.images) if self.images else 0
        }

class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'), nullable=True)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_path': self.image_path,
            'category': self.category,
            'display_order': self.display_order,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'gallery_id': self.gallery_id
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
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/damen-1')
def damen_1():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/damen-1.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/damen-2')
def damen_2():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/damen-2.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/herren-1')
def herren_1():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/herren-1.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/herren-2')
def herren_2():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/herren-2.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/herren-30')
def herren_30():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/herren-30.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/damen-40')
def damen_40():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/damen-40.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/herren-40-1')
def herren_40_1():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/herren-40-1.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/herren-40-2')
def herren_40_2():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/herren-40-2.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/damen-50')
def damen_50():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/damen-50.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/herren-55')
def herren_55():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/herren-55.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/herren-60')
def herren_60():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/herren-60.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/damen-doppel-40')
def damen_doppel_40():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/damen-doppel-40.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/herren-doppel-60')
def herren_doppel_60():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/herren-doppel-60.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/gemischt-1')
def gemischt_1():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/gemischt-1.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/gemischt-2')
def gemischt_2():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/gemischt-2.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mannschaften/mixed-50-doppel')
def mixed_50_doppel():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mannschaften/mixed-50-doppel.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route("/impressum")
def impressum():
    is_admin_active = session.get('is_admin_active', True)

    return render_template("design1/impressum.html",
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route("/vorstand")
def vorstand():
    is_admin_active = session.get('is_admin_active', True)

    return render_template("design1/vorstand.html",
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route("/training")
def training():
    is_admin_active = session.get('is_admin_active', True)

    return render_template("design1/training.html",
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/mitgliedschaft')
def mitgliedschaft():
    is_admin_active = session.get('is_admin_active', True)

    return render_template('design1/mitgliedschaft.html',
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/location1')
def location1():
    is_admin_active = session.get('is_admin_active', True)

    return render_template("design1/location1.html",
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)



@app.route('/sitemap')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')


@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

# You'll need to create these PDF files and place them in the static/downloads folder
# Example of how to create placeholder files:
def create_placeholder_files():
    files = ['vorteile_mitgliedschaft.pdf', 'beitraege.pdf', 'anmeldeformular.pdf']
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(f"This is a placeholder for {file}")

# Call this function when starting the app
create_placeholder_files()


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
    "Trainingsgruppen": {
        "url": "/#trainer",
        "description": "Jugend-, Erwachsenen- und Leistungstraining"
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
        "url": "/mitgliedschaft",
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

    
    # Events & Activities
    "Vereinsturniere": {
        "url": "/kalender",
        "description": "Interne Turniere und Wettkämpfe"
    },
    "Mannschaften": {
        "url": "/mannschaften",
        "description": "Unsere Mannschaften und Spielergebnisse"
    },
    "Veranstaltungen": {
        "url": "/#termine",
        "description": "Soziale Events und Clubveranstaltungen"
    },
    "Kalender": {
        "url": "/kalender",
        "description": "Im Kalender finden Sie alle Termine"
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
                    
def is_admin():
    return current_user.is_authenticated and current_user.role == 'admin' and session.get('is_admin_active', True)

# API route to get about section data
@app.route('/api/about', methods=['GET'])
def get_about_data():
    about_data = AboutSection.query.first()
    if not about_data:
        # Create default data if none exists
        about_data = AboutSection(
            title="Herzlich Willkommen!",
            title_mitgliedschaft="Werde Teil unserer Tennis-Community",
            title_location="Besuche unseren Verein",
            title_termin="Termine",
            title_vorstand="Unser Vorstand",
            title_news="Aktuelle Neuigkeiten",
            title_kontakt="Schreibe uns direkt",
            welcome_text="Herzlich willkommen auf der neu gestalteten Homepage des Hardter TV. Hier gibt es zukünftig alle wichtigen Infos und Termine rund um unseren Tennisverein.",
            welcome_text_mitgliedschaft="Erlebe die Freude am Tennis und die Kraft der Gemeinschaft. Verbinde dich mit Gleichgesinnten und wachse gemeinsam im Sport.",
            welcome_text_location="Besuche uns jeden Sonntag an einem unserer Standorte!",
            welcome_text_termin="Hier erfahren Sie alles über kommende Termine und Veranstaltungen",
            welcome_text_vorstand="Lernen Sie unsere erfahrenen und qualifizierten Tennistrainer kennen",
            welcome_text_news="Bleiben Sie auf dem Laufenden über die neuesten Entwicklungen in unserem Verein",
            welcome_text_kontakt="Nehme über usere Seite direkt Kontakt mit uns auf!",
            club_text="Und los geht es mit einer sehr erfreulichen Nachricht von der Stadt Dorsten. Der Antrag des HTV auf Mittel aus der Sportpauschale 2023 zur Anschaffung einer Flutlichtanlage für zwei Plätze wurde angenommen. Somit wird der HTV der erste Tennisverein in Dorsten sein, der über eine solche Anlage für zwei Tennisfelder verfügen wird.",
            goals_text="Neben der dann möglichen Ausweitung der Trainingszeiten auch in die späten Abendstunden (sehr wichtig aufgrund der veränderten Arbeitswelt) sieht der HTV aber auch Chancen mit Nachturnieren eine Bereicherung des Vereinslebens zu erzielen. Und letztendlich mussten in der Vergangenheit auch das ein oder andere Meisterschafts- oder Turnierspiel bei sehr diffusen Lichtverhältnisse zu Ende gespielt. Aber das hat ab der nächsten Saison beim HTV nun ein Ende. Realisiert werden soll die Flutlichtanlage auf unseren Plätzen 5 und 6.",
            membership_text=" ",
            image_path="/static/images/Tennisball an Linie groß.jpg",
            title_training="Tennisschule André Albert",
            welcome_text_training="Wir l(i)eben Tennis – das ist das Motto von André Albert und dem Team seiner Tennisschule, mit dem er seit 2005 unseren Verein betreut.",
            text_training_1="André, Jahrgang 1982, ist bereits seit 2005 als selbständiger Tennistrainer tätig und besitzt die B-Trainer-Lizenz des Deutschen Tennisbundes. Als Aktiver hat er einige Siege bei deutschen Ranglistenturnieren errungen, war national die Nummer 330 im Ranking, und konnte sich gegen den einen oder anderen ATP-Ranglistenspieler durchsetzen.",
            text_training_2="Ob jung oder alt, Anfänger oder Fortgeschrittener, in seiner Tennisschule bringt André jedem noch etwas bei. Dabei setzt er auf ein Team ebenfalls gut ausgebildeter und selbst als Spieler erfolgreicher Trainer, ein individuell auf jeden Spielertyp zugeschnittenes Training und vor allem eines: Motivation.",
            text_training_3="Langsames Heranführen, regelmäßiges Einzel-, Gruppen- oder Mannschaftstraining, ein spezielles Matchtraining oder Turnier-begleitung? André und sein Team haben für jeden das richtige Angebot. Natürlich ist auch ein unverbindlicher Schnupperkurs möglich.",
            text_training_4="Seit dem 01.10.2022 ist André der neue Pächter der Tennishalle Kirchhellen. Aktuell könnt ihr auf insgesamt vier Plätzen spielen. Dabei handelt es sich um drei Sandplätze und einen Platz mit Teppichbelag. Buchen könnt ihr die Plätze auf der neuen Website der Tennishalle www.tennishalle-kirchhellen.com oder auch direkt bei André."

        )
        db.session.add(about_data)
        db.session.commit()
    
    return jsonify(about_data.to_dict())

# API route to update about section data
@app.route('/api/about', methods=['PUT'])
def update_about_data():
    if not current_user.is_authenticated or current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
        
    about_data = AboutSection.query.first()
    if not about_data:
        return jsonify({'error': 'About section data not found'}), 404
    
    data = request.form
    
    # Update fields if provided
    if 'title' in data:
        about_data.title = data['title']
    if 'title_mitgliedschaft' in data:
        about_data.title_mitgliedschaft = data['title_mitgliedschaft']
    if 'title_location' in data:
        about_data.title_location = data['title_location']
    if 'title_termin' in data:
        about_data.title_termin = data['title_termin']
    if 'title_vorstand' in data:
        about_data.title_vorstand = data['title_vorstand']
    if 'title_news' in data:
        about_data.title_news = data['title_news']
    if 'title_kontakt' in data:
        about_data.title_kontakt = data['title_kontakt']
    if 'welcome_text' in data:
        about_data.welcome_text = data['welcome_text']
    if 'welcome_text_mitgliedschaft' in data:
        about_data.welcome_text_mitgliedschaft = data['welcome_text_mitgliedschaft']
    if 'welcome_text_location' in data:
        about_data.welcome_text_location = data['welcome_text_location']
    if 'welcome_text_termin' in data:
        about_data.welcome_text_termin = data['welcome_text_termin']
    if 'welcome_text_vorstand' in data:
        about_data.welcome_text_vorstand = data['welcome_text_vorstand']
    if 'welcome_text_news' in data:
        about_data.welcome_text_news = data['welcome_text_news']
    if 'welcome_text_kontakt' in data:
        about_data.welcome_text_kontakt = data['welcome_text_kontakt']
    if 'club_text' in data:
        about_data.club_text = data['club_text']
    if 'title_training' in data:
        about_data.title_training = data['title_training']
    if 'welcome_text_training' in data:
        about_data.welcome_text_training = data['welcome_text_training']
    if 'text_training_1' in data:
        about_data.text_training_1 = data['text_training_1']
    if 'text_training_2' in data:
        about_data.text_training_2 = data['text_training_2']
    if 'text_training_3' in data:
        about_data.text_training_3 = data['text_training_3']
    if 'text_training_4' in data:
        about_data.text_training_4 = data['text_training_4']
    if 'goals_text' in data:
        about_data.goals_text = data['goals_text']
    if 'membership_text' in data:
        about_data.membership_text = data['membership_text']
    if 'news_card1_date' in data:
        about_data.news_card1_date = data['news_card1_date']
    if 'news_card1_title' in data:
        about_data.news_card1_title = data['news_card1_title']
    if 'news_card1_excerpt' in data:
        about_data.news_card1_excerpt = data['news_card1_excerpt']
    if 'news_card1_full_text' in data:
        about_data.news_card1_full_text = data['news_card1_full_text']
    
    # News card 2
    if 'news_card2_date' in data:
        about_data.news_card2_date = data['news_card2_date']
    if 'news_card2_title' in data:
        about_data.news_card2_title = data['news_card2_title']
    if 'news_card2_excerpt' in data:
        about_data.news_card2_excerpt = data['news_card2_excerpt']
    if 'news_card2_full_text' in data:
        about_data.news_card2_full_text = data['news_card2_full_text']
    
    # News card 3
    if 'news_card3_date' in data:
        about_data.news_card3_date = data['news_card3_date']
    if 'news_card3_title' in data:
        about_data.news_card3_title = data['news_card3_title']
    if 'news_card3_excerpt' in data:
        about_data.news_card3_excerpt = data['news_card3_excerpt']
    if 'news_card3_full_text' in data:
        about_data.news_card3_full_text = data['news_card3_full_text']
    
    # News card 4
    if 'news_card4_date' in data:
        about_data.news_card4_date = data['news_card4_date']
    if 'news_card4_title' in data:
        about_data.news_card4_title = data['news_card4_title']
    if 'news_card4_excerpt' in data:
        about_data.news_card4_excerpt = data['news_card4_excerpt']
    if 'news_card4_full_text' in data:
        about_data.news_card4_full_text = data['news_card4_full_text']

    if 'news_card1_image_file' in request.files:
        image = request.files['news_card1_image_file']
        if image.filename:
            filename = secure_filename(image.filename)
            image_path = f"/static/images/{filename}"
            image.save(os.path.join(app.root_path, 'static/images', filename))
            about_data.news_card1_image = image_path
    
    if 'news_card2_image_file' in request.files:
        image = request.files['news_card2_image_file']
        if image.filename:
            filename = secure_filename(image.filename)
            image_path = f"/static/images/{filename}"
            image.save(os.path.join(app.root_path, 'static/images', filename))
            about_data.news_card2_image = image_path
    
    if 'news_card3_image_file' in request.files:
        image = request.files['news_card3_image_file']
        if image.filename:
            filename = secure_filename(image.filename)
            image_path = f"/static/images/{filename}"
            image.save(os.path.join(app.root_path, 'static/images', filename))
            about_data.news_card3_image = image_path
    
    if 'news_card4_image_file' in request.files:
        image = request.files['news_card4_image_file']
        if image.filename:
            filename = secure_filename(image.filename)
            image_path = f"/static/images/{filename}"
            image.save(os.path.join(app.root_path, 'static/images', filename))
            about_data.news_card4_image = image_path
    
    # Handle image upload if provided
    if 'image' in request.files:
        image = request.files['image']
        if image.filename:
            # Save the image to the static folder
            filename = secure_filename(image.filename)
            image_path = f"/static/images/{filename}"
            image.save(os.path.join(app.root_path, 'static/images', filename))
            about_data.image_path = image_path


    if 'location_card1_title' in data:
        about_data.location_card1_title = data['location_card1_title']
    if 'location_card1_subtitle' in data:
        about_data.location_card1_subtitle = data['location_card1_subtitle']
    if 'location_card1_address' in data:
        about_data.location_card1_address = data['location_card1_address']
    
    # Location card 2
    if 'location_card2_title' in data:
        about_data.location_card2_title = data['location_card2_title']
    if 'location_card2_subtitle' in data:
        about_data.location_card2_subtitle = data['location_card2_subtitle']
    if 'location_card2_address' in data:
        about_data.location_card2_address = data['location_card2_address']
    
    # Location card 3
    if 'location_card3_title' in data:
        about_data.location_card3_title = data['location_card3_title']
    if 'location_card3_subtitle' in data:
        about_data.location_card3_subtitle = data['location_card3_subtitle']
    if 'location_card3_address' in data:
        about_data.location_card3_address = data['location_card3_address']
    
    # Location card 4
    if 'location_card4_title' in data:
        about_data.location_card4_title = data['location_card4_title']
    if 'location_card4_subtitle' in data:
        about_data.location_card4_subtitle = data['location_card4_subtitle']
    if 'location_card4_address' in data:
        about_data.location_card4_address = data['location_card4_address']
    
    # Bildupload für Location-Karten
    if 'location_card1_image_file' in request.files:
        image = request.files['location_card1_image_file']
        if image.filename:
            filename = secure_filename(image.filename)
            image_path = f"/static/images/{filename}"
            image.save(os.path.join(app.root_path, 'static/images', filename))
            about_data.location_card1_image = image_path
    
    if 'location_card2_image_file' in request.files:
        image = request.files['location_card2_image_file']
        if image.filename:
            filename = secure_filename(image.filename)
            image_path = f"/static/images/{filename}"
            image.save(os.path.join(app.root_path, 'static/images', filename))
            about_data.location_card2_image = image_path
    
    if 'location_card3_image_file' in request.files:
        image = request.files['location_card3_image_file']
        if image.filename:
            filename = secure_filename(image.filename)
            image_path = f"/static/images/{filename}"
            image.save(os.path.join(app.root_path, 'static/images', filename))
            about_data.location_card3_image = image_path
    
    if 'location_card4_image_file' in request.files:
        image = request.files['location_card4_image_file']
        if image.filename:
            filename = secure_filename(image.filename)
            image_path = f"/static/images/{filename}"
            image.save(os.path.join(app.root_path, 'static/images', filename))
            about_data.location_card4_image = image_path
    
    db.session.commit()
    return jsonify(about_data.to_dict())








def create_default_gallery_images():
    if GalleryImage.query.count() == 0:
        # Standardbilder erstellen
        default_images = [
            {
                'title': 'Jahresrückblick 2024',
                'description': 'Rückblick auf ein erfolgreiches Tennisjahr',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_1.jpg',
                'category': 'Rückblick'
            },
            {
                'title': 'Flutlicht Spaß',
                'description': 'Abendliches Tennisspiel unter Flutlicht',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_10.jpg',
                'category': 'Rückblick'
            },
            {
                'title': 'Abend mit kulinarischen Genüssen',
                'description': 'Gemeinsames Essen nach dem Training',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_11.jpg',
                'category': 'Events'
            },
            {
                'title': 'Petras kulinarischen Überraschungen',
                'description': 'Köstlichkeiten von unserer Vereinsköchin',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_12.jpg',
                'category': 'Events'
            },
            {
                'title': 'HTV-Momente',
                'description': 'Besondere Momente im Vereinsleben',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_13.jpg',
                'category': 'Vereinsleben'
            },
            {
                'title': 'Herbstputz',
                'description': 'Gemeinsame Pflege unserer Anlage',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_14.jpg',
                'category': 'Vereinsleben'
            },
            {
                'title': 'Saisonabschluss',
                'description': 'Feier zum Ende der Sommersaison',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_15.jpg',
                'category': 'Events'
            },
            {
                'title': 'Winterfest Pestalozzi Park',
                'description': 'Gemeinsame Winteraktivitäten',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_16.jpg',
                'category': 'Events'
            },
            {
                'title': 'Weihnachtliches Frühstück der Senioren',
                'description': 'Gemütliches Beisammensein in der Weihnachtszeit',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_17.jpg',
                'category': 'Senioren'
            },
            {
                'title': 'HTV Eisstock WM',
                'description': 'Winterliche Aktivitäten abseits des Tennisplatzes',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_2.jpg',
                'category': 'Events'
            },
            {
                'title': 'Eisstock WM Teams',
                'description': 'Teamwettbewerb beim Eisstockschießen',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_3.jpg',
                'category': 'Events'
            },
            {
                'title': 'Frühjahrsputz',
                'description': 'Gemeinsame Vorbereitung der Anlage auf die neue Saison',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_4.jpg',
                'category': 'Vereinsleben'
            },
            {
                'title': 'Saisoneröffnung',
                'description': 'Start in die neue Tennissaison',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_5.jpg',
                'category': 'Events'
            },
            {
                'title': 'Mannschaften',
                'description': 'Unsere Mannschaften in der Saison 2024',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_6.jpg',
                'category': 'Mannschaften'
            },
            {
                'title': 'Hobbytreff jeden Montag',
                'description': 'Regelmäßiges Treffen für Hobbyspieler',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_7.jpg',
                'category': 'Training'
            },
            {
                'title': 'Hobbytreff',
                'description': 'Spaß am Tennis für alle Altersklassen',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_8.jpg',
                'category': 'Training'
            },
            {
                'title': 'Ladies Day',
                'description': 'Besonderer Tag für unsere Tennisdamen',
                'image_path': '/static/images/Rückblick 2024/Rückblick 2024_9.jpg',
                'category': 'Events'
            }
        ]
        
        for img_data in default_images:
            image = GalleryImage(
                title=img_data['title'],
                description=img_data['description'],
                image_path=img_data['image_path'],
                category=img_data['category'],
                display_order=0
            )
            db.session.add(image)
        
        db.session.commit()
        print("Standardbilder für die Galerie wurden erstellt.")

# Beim Starten der Anwendung Standarddaten erstellen
@app.before_first_request
def initialize_data():
    create_default_gallery_images()

@app.route('/galerien')
def galleries():
    is_admin_active = session.get('is_admin_active', True)
    
    # Get all galleries
    all_galleries = Gallery.query.order_by(Gallery.created_at.desc()).all()

    if GalleryImage.query.count() == 0:
        create_default_gallery_images()
    
    # Bilder aus der Datenbank abrufen
    gallery_images = GalleryImage.query.filter_by(gallery_id=None).order_by(
        GalleryImage.display_order, GalleryImage.created_at.desc()).all()
    
    return render_template('design1/galleries.html',
                           galleries=all_galleries,
                           gallery_images=gallery_images,
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)


# Galerie-Seite anzeigen
@app.route('/galerie/<slug>')
def view_gallery(slug):
    is_admin_active = session.get('is_admin_active', True)
    
    # Find the gallery by slug
    gallery = Gallery.query.filter_by(slug=slug).first_or_404()
    
    # Get images for this gallery
    gallery_images = GalleryImage.query.filter_by(gallery_id=gallery.id).order_by(
        GalleryImage.display_order, GalleryImage.created_at.desc()).all()
    
    return render_template('design1/gallery.html',
                           gallery=gallery,
                           gallery_images=gallery_images,
                           logged_in=current_user.is_authenticated,
                           username=current_user.get_id() if current_user.is_authenticated else None,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

# API-Route zum Abrufen aller Galeriebilder
@app.route('/api/gallery', methods=['GET'])
def get_gallery_images():
    category = request.args.get('category')
    
    if category:
        gallery_images = GalleryImage.query.filter_by(category=category).order_by(GalleryImage.display_order, GalleryImage.created_at.desc()).all()
    else:
        gallery_images = GalleryImage.query.order_by(GalleryImage.display_order, GalleryImage.created_at.desc()).all()
    
    return jsonify([image.to_dict() for image in gallery_images])

@app.route('/api/galleries/<int:gallery_id>', methods=['GET'])
def get_gallery(gallery_id):
    try:
        gallery = Gallery.query.get_or_404(gallery_id)
        return jsonify(gallery.to_dict())
    except Exception as e:
        print(f"Error fetching gallery: {str(e)}")
        return jsonify({'error': f'Fehler beim Abrufen der Galerie: {str(e)}'}), 500

# Korrigierte Version der create_gallery-Funktion

@app.route('/api/galleries', methods=['POST'])
@login_required
def create_gallery():
    if not current_user.role == 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get form data
    name = request.form.get('name')
    description = request.form.get('description', '')
    
    if not name:
        return jsonify({'error': 'Gallery name is required'}), 400
    
    # Create a slug from the name
    slug = secure_filename(name.lower().replace(' ', '-'))
    
    # Check if slug already exists
    existing_gallery = Gallery.query.filter_by(slug=slug).first()
    if existing_gallery:
        # Make slug unique by adding a timestamp
        slug = f"{slug}-{int(datetime.utcnow().timestamp())}"
    
    # Handle cover image if provided
    cover_image = None
    if 'cover_image' in request.files and request.files['cover_image'].filename:
        image = request.files['cover_image']
        filename = secure_filename(f"gallery-cover-{slug}-{uuid.uuid4()}.{image.filename.rsplit('.', 1)[1].lower()}")
        image_path = f"/static/images/gallery/{filename}"
        
        # Ensure directory exists
        os.makedirs(os.path.join(app.root_path, 'static/images/gallery'), exist_ok=True)
        
        # Save the image
        image.save(os.path.join(app.root_path, 'static/images/gallery', filename))
        cover_image = image_path
    
    # Create new gallery
    new_gallery = Gallery(
        name=name,
        description=description,
        slug=slug,
        cover_image=cover_image
    )
    
    try:
        db.session.add(new_gallery)
        db.session.commit()
        return jsonify(new_gallery.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating gallery: {str(e)}")
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/api/galleries/<int:gallery_id>', methods=['PUT'])
@login_required
def update_gallery(gallery_id):
    if not current_user.role == 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    gallery = Gallery.query.get_or_404(gallery_id)
    
    try:
        # Textfelder aktualisieren
        if 'name' in request.form:
            gallery.name = request.form['name']
        
        if 'description' in request.form:
            gallery.description = request.form['description']
        
        # Titelbild aktualisieren, falls vorhanden
        if 'cover_image' in request.files and request.files['cover_image'].filename != '':
            image = request.files['cover_image']
            
            # Altes Bild löschen (optional)
            if gallery.cover_image and gallery.cover_image.startswith('/static/images/gallery/'):
                old_image_path = os.path.join(app.root_path, gallery.cover_image.lstrip('/'))
                if os.path.exists(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except:
                        pass  # Fehler beim Löschen ignorieren
            
            # Neues Bild speichern
            filename = secure_filename(f"gallery-cover-{gallery.slug}-{uuid.uuid4()}.{image.filename.rsplit('.', 1)[1].lower()}")
            image_path = f"/static/images/gallery/{filename}"
            
            # Stellen Sie sicher, dass das Verzeichnis existiert
            os.makedirs(os.path.join(app.root_path, 'static/images/gallery'), exist_ok=True)
            
            image.save(os.path.join(app.root_path, 'static/images/gallery', filename))
            gallery.cover_image = image_path
        
        db.session.commit()
        
        return jsonify(gallery.to_dict())
    except Exception as e:
        db.session.rollback()
        print(f"Error updating gallery: {str(e)}")
        return jsonify({'error': f'Fehler beim Aktualisieren der Galerie: {str(e)}'}), 500

# API-Route zum Löschen einer Galerie
@app.route('/api/galleries/<int:gallery_id>', methods=['DELETE'])
@login_required
def delete_gallery(gallery_id):
    if not current_user.role == 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    gallery = Gallery.query.get_or_404(gallery_id)
    
    try:
        # Alle zugehörigen Bilder auf gallery_id = NULL setzen
        # oder alternativ löschen, je nach Anforderung
        gallery_images = GalleryImage.query.filter_by(gallery_id=gallery_id).all()
        for image in gallery_images:
            image.gallery_id = None  # Bilder behalten, aber von der Galerie trennen
            # Alternativ: db.session.delete(image)  # Bilder löschen
        
        # Titelbild löschen (optional)
        if gallery.cover_image and gallery.cover_image.startswith('/static/images/gallery/'):
            cover_path = os.path.join(app.root_path, gallery.cover_image.lstrip('/'))
            if os.path.exists(cover_path):
                try:
                    os.remove(cover_path)
                except:
                    pass  # Fehler beim Löschen ignorieren
        
        # Galerie löschen
        db.session.delete(gallery)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Galerie erfolgreich gelöscht'})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting gallery: {str(e)}")
        return jsonify({'error': f'Fehler beim Löschen der Galerie: {str(e)}'}), 500

# API-Route zum Abrufen eines einzelnen Galeriebildes
@app.route('/api/gallery/<int:image_id>', methods=['GET'])
def get_gallery_image(image_id):
    gallery_image = GalleryImage.query.get(image_id)
    
    if not gallery_image:
        return jsonify({'error': 'Bild nicht gefunden'}), 404
    
    return jsonify(gallery_image.to_dict())

# API-Route zum Hinzufügen eines neuen Galeriebildes
# Aktualisiere die bestehende add_gallery_image-Funktion
@app.route('/api/gallery', methods=['POST'])
@login_required
def add_gallery_image():
    if not current_user.role == 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    if 'image' not in request.files:
        return jsonify({'error': 'Kein Bild hochgeladen'}), 400
    
    image = request.files['image']
    
    if image.filename == '':
        return jsonify({'error': 'Kein Bild ausgewählt'}), 400
    
    if image:
        try:
            # Eindeutigen Dateinamen generieren
            filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
            image_path = f"/static/images/gallery/{filename}"
            
            # Stellen Sie sicher, dass das Verzeichnis existiert
            os.makedirs(os.path.join(app.root_path, 'static/images/gallery'), exist_ok=True)
            
            # Bild speichern
            image.save(os.path.join(app.root_path, 'static/images/gallery', filename))
            
            # Galerie-ID verarbeiten (kann None sein)
            gallery_id = request.form.get('gallery_id')
            if gallery_id == '':
                gallery_id = None
            elif gallery_id is not None:
                gallery_id = int(gallery_id)
            
            # Neues Galeriebild erstellen
            new_image = GalleryImage(
                title=request.form.get('title', 'Neues Bild'),
                description=request.form.get('description', ''),
                image_path=image_path,
                category=request.form.get('category', ''),
                display_order=int(request.form.get('display_order', 0)),
                gallery_id=gallery_id
            )
            
            db.session.add(new_image)
            db.session.commit()
            
            return jsonify(new_image.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            print(f"Error adding gallery image: {str(e)}")
            return jsonify({'error': f'Fehler beim Hochladen des Bildes: {str(e)}'}), 500
    
    return jsonify({'error': 'Fehler beim Hochladen des Bildes'}), 500

# API-Route zum Aktualisieren eines Galeriebildes
@app.route('/api/gallery/<int:image_id>', methods=['PUT'])
@login_required
def update_gallery_image(image_id):
    if not current_user.role == 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    gallery_image = GalleryImage.query.get_or_404(image_id)
    
    try:
        # Textfelder aktualisieren
        if 'title' in request.form:
            gallery_image.title = request.form['title']
        
        if 'description' in request.form:
            gallery_image.description = request.form['description']
        
        if 'category' in request.form:
            gallery_image.category = request.form['category']
        
        if 'display_order' in request.form:
            gallery_image.display_order = int(request.form['display_order'])
        
        # Galerie-ID verarbeiten (kann None sein)
        if 'gallery_id' in request.form:
            gallery_id = request.form.get('gallery_id')
            if gallery_id == '':
                gallery_image.gallery_id = None
            else:
                gallery_image.gallery_id = int(gallery_id)
        
        # Bild aktualisieren, falls vorhanden
        if 'image' in request.files and request.files['image'].filename != '':
            image = request.files['image']
            
            # Altes Bild löschen (optional)
            if gallery_image.image_path.startswith('/static/images/gallery/'):
                old_image_path = os.path.join(app.root_path, gallery_image.image_path.lstrip('/'))
                if os.path.exists(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except:
                        pass  # Fehler beim Löschen ignorieren
            
            # Neues Bild speichern
            filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
            image_path = f"/static/images/gallery/{filename}"
            
            # Stellen Sie sicher, dass das Verzeichnis existiert
            os.makedirs(os.path.join(app.root_path, 'static/images/gallery'), exist_ok=True)
            
            image.save(os.path.join(app.root_path, 'static/images/gallery', filename))
            gallery_image.image_path = image_path
        
        db.session.commit()
        
        return jsonify(gallery_image.to_dict())
    except Exception as e:
        db.session.rollback()
        print(f"Error updating gallery image: {str(e)}")
        return jsonify({'error': f'Fehler beim Aktualisieren des Bildes: {str(e)}'}), 500

# API-Route zum Löschen eines Galeriebildes
@app.route('/api/gallery/<int:image_id>', methods=['DELETE'])
@login_required
def delete_gallery_image(image_id):
    if not current_user.role == 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    gallery_image = GalleryImage.query.get(image_id)
    
    if not gallery_image:
        return jsonify({'error': 'Bild nicht gefunden'}), 404
    
    # Bild von der Festplatte löschen
    if gallery_image.image_path.startswith('/static/images/gallery/'):
        image_path = os.path.join(app.root_path, gallery_image.image_path.lstrip('/'))
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except:
                pass  # Fehler beim Löschen ignorieren
    
    # Bild aus der Datenbank löschen
    db.session.delete(gallery_image)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Bild erfolgreich gelöscht'})

# API-Route zum Verschieben von Bildern in eine Galerie

@app.route('/api/gallery/move', methods=['POST'])
@login_required
def move_images_to_gallery():
    if not current_user.role == 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.json
        image_ids = data.get('image_ids', [])
        gallery_id = data.get('gallery_id')
        
        # Überprüfen, ob die Galerie existiert (wenn eine Galerie angegeben wurde)
        if gallery_id is not None:
            gallery = Gallery.query.get(gallery_id)
            if not gallery:
                return jsonify({'error': 'Galerie nicht gefunden'}), 404
        
        # Bilder aktualisieren
        for image_id in image_ids:
            image = GalleryImage.query.get(image_id)
            if image:
                image.gallery_id = gallery_id
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'{len(image_ids)} Bilder wurden erfolgreich verschoben'
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error moving images: {str(e)}")
        return jsonify({'error': f'Fehler beim Verschieben der Bilder: {str(e)}'}), 500



# API-Route zum Hochladen mehrerer Bilder
@app.route('/api/gallery/bulk-upload', methods=['POST'])
@login_required
def bulk_upload_images():
    if not current_user.role == 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    if 'images[]' not in request.files:
        return jsonify({'error': 'Keine Bilder hochgeladen'}), 400
    
    images = request.files.getlist('images[]')
    category = request.form.get('category', '')
    
    # Galerie-ID verarbeiten (kann None sein)
    gallery_id = request.form.get('gallery_id')
    if gallery_id == '':
        gallery_id = None
    elif gallery_id is not None:
        gallery_id = int(gallery_id)
    
    if not images:
        return jsonify({'error': 'Keine Bilder ausgewählt'}), 400
    
    uploaded_images = []
    
    try:
        for image in images:
            if image.filename:
                # Eindeutigen Dateinamen generieren
                filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
                image_path = f"/static/images/gallery/{filename}"
                
                # Stellen Sie sicher, dass das Verzeichnis existiert
                os.makedirs(os.path.join(app.root_path, 'static/images/gallery'), exist_ok=True)
                
                # Bild speichern
                image.save(os.path.join(app.root_path, 'static/images/gallery', filename))
                
                # Neues Galeriebild erstellen
                new_image = GalleryImage(
                    title=os.path.splitext(image.filename)[0],  # Dateiname ohne Erweiterung als Titel
                    description='',
                    image_path=image_path,
                    category=category,
                    display_order=0,
                    gallery_id=gallery_id
                )
                
                db.session.add(new_image)
                uploaded_images.append(new_image)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(uploaded_images)} Bilder erfolgreich hochgeladen',
            'images': [image.to_dict() for image in uploaded_images]
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error in bulk upload: {str(e)}")
        return jsonify({'error': f'Fehler beim Hochladen der Bilder: {str(e)}'}), 500



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
    required_fields = ['title', 'short_title', 'start_date', 'location', 'category']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Field {field} is required'}), 400
    
    # Parse dates
    try:
        start_date_obj = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date_obj = None
        if 'end_date' in data and data['end_date']:
            end_date_obj = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Check if it's an all-day event
    is_all_day = 'is_all_day' in data and data['is_all_day'] == 'true'
    
    # Create new event
    new_event = Event(
        title=data['title'],
        short_title=data['short_title'],
        start_date=start_date_obj,
        end_date=end_date_obj,
        is_all_day=is_all_day,
        start_time=None if is_all_day else data.get('start_time'),
        end_time=None if is_all_day else data.get('end_time'),
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
    if 'start_date' in data:
        try:
            event.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid start date format. Use YYYY-MM-DD'}), 400
    if 'end_date' in data and data['end_date']:
        try:
            event.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid end date format. Use YYYY-MM-DD'}), 400
    elif 'end_date' in data:
        event.end_date = None
        
    # Update all-day status
    event.is_all_day = 'is_all_day' in data and data['is_all_day'] == 'true'
    
    # Update time fields based on all-day status
    if event.is_all_day:
        event.start_time = None
        event.end_time = None
    else:
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













@app.route('/api/news', methods=['GET'])
def get_news():
    # Get query parameters
    archived = request.args.get('archived', 'false').lower() == 'true'
    
    # Query news based on archived status
    news_items = News.query.filter_by(archived=archived).order_by(News.date.desc()).all()
    
    # Convert to JSON
    result = []
    for news in news_items:
        result.append({
            'id': news.id,
            'title': news.title,
            'date': news.date.strftime('%d.%m.%Y'),
            'excerpt': news.excerpt,
            'full_text': news.full_text,
            'image_url': news.image_url,
            'archived': news.archived,
            'created_at': news.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify(result)

@app.route('/add_news', methods=['POST'])
@login_required
def add_news():
    # Check if user is admin
    if current_user.role != 'admin':
        flash('Nur Administratoren können News hinzufügen.', 'error')
        return redirect(url_for('home'))
    
    # Get form data
    title = request.form.get('title')
    date_str = request.form.get('date')
    excerpt = request.form.get('excerpt')
    full_text = request.form.get('full_text')
    
    # Format date
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    except:
        date_obj = datetime.now()
    
    # Handle image upload
    if 'image' not in request.files:
        flash('Kein Bild ausgewählt', 'error')
        return redirect(url_for('home'))
    
    image = request.files['image']
    
    if image.filename == '':
        flash('Kein Bild ausgewählt', 'error')
        return redirect(url_for('home'))
    
    if image and allowed_file(image.filename):
        # Generate unique filename
        filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
        image_path = f"/static/images/news/{filename}"
        
        # Ensure directory exists
        os.makedirs(os.path.join(app.root_path, 'static/images/news'), exist_ok=True)
        
        # Save the image
        image.save(os.path.join(app.root_path, 'static/images/news', filename))
        
        # Create new news item
        new_news = News(
            title=title,
            date=date_obj,
            excerpt=excerpt,
            full_text=full_text,
            image_url=image_path,
            archived=False
        )
        
        db.session.add(new_news)
        db.session.commit()
        
        flash('News erfolgreich hinzugefügt!', 'success')
    else:
        flash('Ungültiger Dateityp', 'error')
    
    return redirect(url_for('home') + '#news')

@app.route('/delete_news/<int:news_id>', methods=['POST'])
@login_required
def delete_news(news_id):
    # Check if user is admin
    if current_user.role != 'admin':
        flash('Nur Administratoren können News löschen.', 'error')
        return redirect(url_for('home'))
    
    news = News.query.get_or_404(news_id)
    
    # Delete image file if it exists
    if news.image_url and news.image_url.startswith('/static/images/news/'):
        image_path = os.path.join(app.root_path, news.image_url.lstrip('/'))
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except:
                pass  # Ignore errors when deleting file
    
    # Delete news from database
    db.session.delete(news)
    db.session.commit()
    
    flash('News erfolgreich gelöscht!', 'success')
    return redirect(url_for('home') + '#news')

@app.route('/archive_news/<int:news_id>', methods=['POST'])
@login_required
def archive_news(news_id):
    # Check if user is admin
    if current_user.role != 'admin':
        flash('Nur Administratoren können News archivieren.', 'error')
        return redirect(url_for('home'))
    
    news = News.query.get_or_404(news_id)
    
    # Archive news
    news.archived = True
    db.session.commit()
    
    flash('News erfolgreich archiviert!', 'success')
    return redirect(url_for('home') + '#news')

@app.route('/news-archive')
def news_archive():
    # Get all archived news
    archived_news = News.query.filter_by(archived=True).order_by(News.date.desc()).all()
    
    # Extract years for filter
    years = set()
    for news in archived_news:
        years.add(news.date.year)
    
    years = sorted(list(years), reverse=True)
    
    is_admin_active = session.get('is_admin_active', True)
    
    return render_template('design1/news-archive.html',
                           archived_news=archived_news,
                           years=years,
                           logged_in=current_user.is_authenticated,
                           is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active,
                           is_verified=current_user.is_authenticated and current_user.is_verified)

@app.route('/edit_news/<int:news_id>', methods=['POST'])
@login_required
def edit_news(news_id):
    # Check if user is admin
    if current_user.role != 'admin':
        flash('Nur Administratoren können News bearbeiten.', 'error')
        return redirect(url_for('home'))
    
    news = News.query.get_or_404(news_id)
    
    # Get form data
    title = request.form.get('title')
    date_str = request.form.get('date')
    excerpt = request.form.get('excerpt')
    full_text = request.form.get('full_text')
    
    # Format date
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    except:
        date_obj = news.date  # Keep existing date if format is invalid
    
    # Update news data
    news.title = title
    news.date = date_obj
    news.excerpt = excerpt
    news.full_text = full_text
    
    # Handle image upload if a new image was provided
    if 'image' in request.files and request.files['image'].filename != '':
        image = request.files['image']
        
        if allowed_file(image.filename):
            # Delete old image if it exists
            if news.image_url and news.image_url.startswith('/static/images/news/'):
                old_image_path = os.path.join(app.root_path, news.image_url.lstrip('/'))
                if os.path.exists(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except:
                        pass  # Ignore errors when deleting file
            
            # Generate unique filename
            filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
            image_path = f"/static/images/news/{filename}"
            
            # Ensure directory exists
            os.makedirs(os.path.join(app.root_path, 'static/images/news'), exist_ok=True)
            
            # Save the image
            image.save(os.path.join(app.root_path, 'static/images/news', filename))
            
            # Update image URL
            news.image_url = image_path
        else:
            flash('Ungültiger Dateityp', 'error')
            return redirect(url_for('home') + '#news')
    
    # Save changes
    db.session.commit()
    
    flash('News erfolgreich aktualisiert!', 'success')
    return redirect(url_for('home') + '#news')


@app.route('/unarchive_news/<int:news_id>', methods=['POST'])
@login_required
def unarchive_news(news_id):
    # Check if user is admin
    if current_user.role != 'admin':
        flash('Nur Administratoren können News zurück auf die Hauptseite verschieben.', 'error')
        return redirect(url_for('news_archive'))
    
    news = News.query.get_or_404(news_id)
    
    # Unarchive news
    news.archived = False
    db.session.commit()
    
    flash('News erfolgreich zurück auf die Hauptseite verschoben!', 'success')
    return redirect(url_for('news_archive'))


# @app.route('/news', methods=['GET', 'POST'])
# def news():
#     design = session.get('design', 'design1')  # Default-Fallback falls nicht in der Session
    
#     if request.method == 'POST':
#         image = request.files['image']
#         date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
#         heading = request.form['heading']
#         info = request.form['info']
#         span = request.form['span']

#         if image and allowed_file(image.filename):
#             # Bild in Binärdaten umwandeln
#             image_data = image.read()

#         # Box in der Datenbank speichern
#         new_box = Box(
#             image_data=image_data,  # Binärdaten des Bildes
#             date=date,
#             heading=heading,
#             info=info, 
#             span=span
#         )
#         db.session.add(new_box)
#         db.session.commit()

#         return redirect(url_for('news'))
    
#     # Abrufen der Boxen
#     boxes = Box.query.all()
#     is_admin_active = session.get('is_admin_active', True)


#     # Base64-Umwandlung für jedes Bild
#     for box in boxes:
#         if box.image_data:
#             box.image_data_base64 = base64.b64encode(box.image_data).decode('utf-8')


#     return render_template(f'{design}/news.html', logged_in=current_user.is_authenticated, is_admin=current_user.is_authenticated and current_user.role == 'admin' and is_admin_active, boxes=boxes)


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

#     __     __    ___   __   ____   __    __   __ _ 
#    (  )   /  \  / __) / _\ (_  _) (  )  /  \ (  ( \
#    / (_/\(  O )( (__ /    \  )(    )(  (  O )/    /
#    \____/ \__/  \___)\_/\_/ (__)  (__)  \__/ \_)__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add_content', methods=['POST'])
def add_content():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
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
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return JSON response
            return jsonify({
                'success': True,
                'message': 'Inhalt erfolgreich hinzugefügt!',
                'item_id': new_item.id
            })
    
    # For non-AJAX requests, redirect as before
    return redirect(url_for('home') + "#one")

#     ____  ____  __    ____  ____  ____ 
#    (    \(  __)(  )  (  __)(_  _)(  __)
#     ) D ( ) _) / (_/\ ) _)   )(   ) _) 
#    (____/(____)\____/(____) (__) (____)

@app.route('/delete_content/<int:item_id>', methods=['GET', 'POST'])
def delete_content(item_id):
    item = ContentItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'message': 'Inhalt erfolgreich gelöscht!'
        })
    
    # For non-AJAX requests, redirect as before
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
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'message': 'Termin erfolgreich hinzugefügt!',
            'termin_id': neuer_termin.id,
            'datum': datum,
            'veranstaltung': veranstaltung,
            'uhrzeit': uhrzeit,
            'ort': ort
        })
    
    # For non-AJAX requests, redirect as before
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
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'message': 'Termin erfolgreich gelöscht!'
        })
    
    # For non-AJAX requests, redirect as before
    return redirect(url_for('home') + "#termine")





@app.route('/add_img', methods=["POST"])
def add_img():
    if 'image' not in request.files:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'No image provided'}), 400
        return redirect(url_for('home'))
    
    file = request.files['image']
    
    if file.filename == '':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'No selected file'}), 400
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
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return JSON response
            return jsonify({
                'success': True,
                'message': 'Bild erfolgreich hinzugefügt!',
                'item_id': new_item.id
            })
    
    # For non-AJAX requests, redirect as before
    return redirect(url_for('home') + "#img")


@app.route('/delete_img/<int:img_id>', methods=['GET', 'POST'])
def delete_img(img_id):
    image = Img.query.get_or_404(img_id)
    db.session.delete(image)
    db.session.commit()
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'message': 'Bild erfolgreich gelöscht!'
        })
    
    # For non-AJAX requests, redirect as before
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
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'No content provided'}), 400
        return redirect(url_for('home') + "#about")
    
    if text_type == "headline":
        new_text = AboutText(content=text_content, type="headline")
    else:
        new_text = AboutText(content=text_content, type="normal")

    db.session.add(new_text)
    db.session.commit()
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'message': 'Text erfolgreich hinzugefügt!',
            'text_id': new_text.id,
            'content': text_content,
            'type': text_type
        })
    
    # For non-AJAX requests, redirect as before
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
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': 'Text erfolgreich gelöscht!'
            })
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Text nicht gefunden'}), 404
        flash("Text nicht gefunden.", "error")
    
    # For non-AJAX requests, redirect as before
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
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Toggle the admin active state
    is_admin_active = not session.get('is_admin_active', True)
    session['is_admin_active'] = is_admin_active
    
    # Return JSON response
    return jsonify({
        'success': True, 
        'is_admin_active': is_admin_active
    })








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

    about_data = AboutSection.query.first()
    
    # Get the 4 most recent non-archived news items
    news_items = []
    try:
        news_items = News.query.filter_by(archived=False).order_by(News.date.desc()).limit(4).all()
    except:
        # If there's an error (e.g., table doesn't exist yet), just use an empty list
        pass

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
                           image=image,
                           about_data=about_data,
                           news_items=news_items)  # Pass news items to the template






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
    email = request.form['email']
    
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
        mail.send(msg)
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': 'E-Mail wurde erfolgreich versendet!'
            })
        
        flash('E-Mail wurde erfolgreich versendet!', 'success')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'error': f'Fehler beim Senden der E-Mail: {str(e)}'
            }), 500
        
        flash(f'Fehler beim Senden der E-Mail: {e}', 'error')
    
    return redirect(url_for('home'))





#     ____  ____  __ _  ____  ____  __ _ 
#    / ___)(  __)(  ( \(    \(  __)(  ( \
#    \___ \ ) _) /    / ) D ( ) _) /    /
#    (____/(____)\_)__)(____/(____)\_)__)



@app.route('/send_email', methods=['POST'])
def send_email():
    design = session.get('design', 'design1')
    name = request.form['name']
    user_email = request.form['email']
    message = request.form['message']

    # Nachricht erstellen
    msg = Message('Nachricht von ' + name,
                  sender=user_email,
                  recipients=['myandr180709@gmail.com'])
    msg.body = f"Nachricht von: {name} ({user_email})\n\n{message}"

    # E-Mail senden
    try:
        mail.send(msg)
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': 'Nachricht erfolgreich gesendet!'
            })
        
        return render_template(f'{design}/email-sent.html')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'error': f'Fehler beim Senden der E-Mail: {str(e)}'
            }), 500
        
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
    design = session.get('design', 'design1')  # Default design if not in session
    
    if request.method == 'POST':
        if request.form['password'] == DB_PASSWORD:
            # Fetch data from database based on your new models
            users = User.query.all()
            events = Event.query.all()
            about_sections = AboutSection.query.all()
            
            # Get current time for the footer
            now = datetime.now()
            
            # Render the database preview template with the data
            return render_template(
                f'{design}/db_preview.html',
                users=users,
                events=events,
                about_sections=about_sections,
                now=now
            )
        else:
            # If password is incorrect, show error
            return render_template(f'{design}/passwort.html', error="Falsches Passwort! Versuche es erneut.")

    # If it's a GET request, show the password form
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
