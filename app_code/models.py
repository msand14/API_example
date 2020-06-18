from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

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

@login_manager.user_loader
def load_user(u_id):
    return User.query.get(int(u_id))