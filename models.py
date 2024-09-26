from app import db

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
    download_link = db.Column(db.String(200), nullable=False)

class ComboItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    download_link = db.Column(db.String(200), nullable=False)