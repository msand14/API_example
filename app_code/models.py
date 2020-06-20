from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Role(db.Model):
    __tablename__ = 'roles'
    id    = db.Column(db.Integer, primary_key = True)
    rolename  = db.Column(db.String(64), unique= True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return 'Role %r' % self.rolename

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id           = db.Column(db.Integer, primary_key = True)
    role_id      = db.Column(db.Integer,db.ForeignKey('roles.id'))
    username     = db.Column(db.String(64), unique=True, index=True )
    class_number = db.Column(db.SmallInteger)
    pswd_hashed  = db.Column(db.String(128))
    email        = db.Column(db.String(35), unique = True, index = True)
    confirmed    = db.Column(db.Boolean, default = False)
    @property
    def password(self):
        raise AttributeError(' The Password´s attribute is not readable.')

    @password.setter
    def password(self, password):
        self.pswd_hashed = generate_password_hash(password)

    def verify_pswd(self, password):
        return check_password_hash(self.pswd_hashed, password)

    def __repr__(self):
        return 'User %r' % self.username

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')
    
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data =s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

@login_manager.user_loader
def load_user(u_id):
    return User.query.get(int(u_id))