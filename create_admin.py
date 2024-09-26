from app import app, db, User
from werkzeug.security import generate_password_hash

def create_admin_user():
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', password=generate_password_hash('admin_password'))
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    create_admin_user()