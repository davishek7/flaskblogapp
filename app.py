import os
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app=Flask(__name__)

app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db=SQLAlchemy(app)
admin=Admin(app, name="Avishek's Blog", template_mode='bootstrap4')

user_roles=db.Table('user_roles',
            db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
            db.Column('role_id',db.Integer,db.ForeignKey('roles.id')))

class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(100),unique=True)
    username=db.Column(db.String(100))
    password=db.Column(db.String(255))
    active=db.Column(db.Boolean)
    confirmed_at=db.Column(db.DateTime)
    roles = db.relationship('Role', secondary='user_roles')
    posts=db.relationship('BlogPost',backref='author',lazy=True)

    def __repr__(self):
        return f"Users('{self.username}')"

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class BlogPost(db.Model):
    __tablename__='blogpost'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def __repr__(self):
        return f"blogpost('{self.title}')"

admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(BlogPost, db.session))
admin.add_view(ModelView(Role, db.session))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts',methods=['GET','POST'])
def posts():

    all_posts=BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html',posts=all_posts)

if __name__=='__main__':
    app.run(debug=True)
