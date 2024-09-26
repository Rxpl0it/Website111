from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def update_last_seen(self):
        self.last_seen = datetime.utcnow()
        db.session.commit()

class ShopItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(200), nullable=False)

class ToolItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    file = db.Column(db.String(100), nullable=False)

class ComboItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    file = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            user.update_last_seen()
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
        else:
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/shop')
def shop():
    items = ShopItem.query.all()
    return render_template('shop.html', items=items)

@app.route('/tools')
def tools():
    items = ToolItem.query.all()
    return render_template('tools.html', items=items)

@app.route('/tools/<int:item_id>')
@login_required
def tool_detail(item_id):
    item = ToolItem.query.get_or_404(item_id)
    return render_template('item_detail.html', item=item, type='tool')

@app.route('/combo')
def combo():
    items = ComboItem.query.all()
    return render_template('combo.html', items=items)

@app.route('/combo/<int:item_id>')
@login_required
def combo_detail(item_id):
    item = ComboItem.query.get_or_404(item_id)
    return render_template('item_detail.html', item=item, type='combo')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.username != 'admin':
        flash('You do not have permission to access the admin panel.')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        section = request.form['section']
        title = request.form['title']
        description = request.form['description']
        image = request.files['image']
        
        image_filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        if section == 'shop':
            price = request.form['price']
            link = request.form['link']
            new_item = ShopItem(title=title, image=image_filename, price=price, description=description, link=link)
        else:
            file = request.files['file']
            file_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_filename))
            if section == 'tools':
                new_item = ToolItem(title=title, image=image_filename, description=description, file=file_filename)
            elif section == 'combo':
                new_item = ComboItem(title=title, image=image_filename, description=description, file=file_filename)

        db.session.add(new_item)
        db.session.commit()
        flash('New item added successfully.')
        return redirect(url_for('admin'))

    return render_template('admin.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def create_upload_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

if __name__ == '__main__':
    with app.app_context():
        create_upload_folder()
        db.create_all()
    app.run(debug=True)