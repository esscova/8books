from extensions import db, UserMixin, login_manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

class Users (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=True)
    sobrenome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True, unique=True)
    senha = db.Column(db.String, nullable=True)

class Books (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.String, nullable=True)
    titulo = db.Column(db.String, nullable=True)
    categoria = db.Column(db.String)
    descricao = db.Column(db.String)
    rate = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref = 'books')

    __table_args__ = (db.CheckConstraint('rate >= 1 AND <= 5', name = 'check_rate_range'),)