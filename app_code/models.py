from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Permission:
    FOLLOW = 1 #Students, Teachers
    COMMENT = 2 #Students, Teachers
    MODERATE = 4 #Teachers
    ADMIN = 8 # Admin

class Role(db.Model):
    __tablename__ = 'roles'
    id    = db.Column(db.Integer, primary_key = True)
    rolename  = db.Column(db.String(64), unique= True)
    default = db.Column(db.Boolean, default=False, index = True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role')

    @staticmethod
    def insert_roles():
        roles = {
            'student' : [Permission.FOLLOW, Permission.COMMENT],
            'teacher' : [Permission.FOLLOW, Permission.COMMENT,
            Permission.MODERATE],
            'admin'   : [Permission.MODERATE, Permission.COMMENT,
             Permission.ADMIN]
        }
        default_role = 'Student'
        for r in roles:
            role = Role.query.filter_by(rolename = r).first()
            if role is None:
                role = Role(rolename = r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.rolename == default_role)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return 'Role %r' % self.rolename

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += permission
    
    def remove_permission(self, perm):
        if  self.has_permission(perm):
            self.permissions -= permission

    def reset_permission(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

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

    def __init__(self, **kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(rolename = 'admin').first()
            if self.role is None:
                self.role = Role.query.filter_by(default =True).first()
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.can(Permission.ADMIN)
        
    def is_teacher(self):
        return self.can(Permission.ADMIN)

@login_manager.user_loader
def load_user(u_id):
    return User.query.get(int(u_id))