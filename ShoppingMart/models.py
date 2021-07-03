from datetime import datetime
from ShoppingMart import db, login_manager
# from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# database tables using sqlalchemy
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(60), unique = True, nullable = False)
    totalBudget = db.Column(db.Integer, default = 15000)
    password = db.Column(db.Integer, nullable = False)
    image_file = db.Column(db.String, nullable = False, default = 'default.png')
    items = db.relationship('UserItems', backref = 'customer', lazy = True)

    def __repr__(self):
        return f'User({self.username},{self.email}, {self.totalBudget})'

    # methods necessary to work with flask_login package
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False
    def is_active(self):
        return True
    def get_id(self):
        return self.id



class UserItems(db.Model):
    __tablename__ = 'userItems'
    id = db.Column(db.Integer, primary_key = True)
    itemname = db.Column(db.String, nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    date_bought = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def __repr__(self):
        return f'User({self.itemname},{self.amount}, {self.date_bought})'


class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.String, nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    info = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f'User({self.item},{self.amount}, {self.info})'
