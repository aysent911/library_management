from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
db_user = 'flask';
db_pass = 'flask_234'
db_host = 'localhost'
db_port = 3306
db_name = 'library_management'
connection_string = \
'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(db_user,db_pass,db_host,db_port,db_name)
secret = 'odChja_jfgs#jkdl98763_!'
app=Flask(__name__)
#congigure SQLALCHEMY_DATABASE_URI key with the database application URL
app.config['SQLALCHEMY_DATABASE_URI']=connection_string
#enable automatic commits of database changes at the end of each request
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
#secret key for authenticating request form data in order to prent CSRF
app.config['SECRET_KEY']= secret
upload_folder = os.path.join(os.getcwd(),'photos')
app.config['UPLOAD_FOLDER']= upload_folder
# Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
from wtforms.fields import HiddenField
def is_hidden_field_filter(field):
  return isinstance(field, HiddenField)
  
app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter
#create instance of sqlalchemy
#to allow access to flask-sqlalchemy functionalities
db = SQLAlchemy(app)
#Model is equivalent of entity/table in RDBMS
class Book(db.Model):
#provide a tablename with the plurals convention
#if not provided a tablename will be created but without plurals
  __tablename__='books'
  ISBN = db.Column(db.String(20), primary_key=True)
  title = db.Column(db.String(100), index=True, nullable=False)
  author = db.Column(db.String(100), index=True, nullable=False)
  edition = db.Column(db.String(10), index=True, nullable=True)
  publisher = db.Column(db.String(20), index=True, nullable=True)
  year_of_pub = db.Column(db.SmallInteger, index=True, nullable = False)	
  subject = db.Column(db.String(30), index=True)
  transactions = db.relationship('Transaction', backref='book')
  stock = db.relationship('Stock', backref='book', uselist=False)
  def __repr__(self):
    return '<Title: %r>' % self.title

class Member(db.Model):
  __tablename__='members' 		
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(15), index=True, nullable=False)
  second_name = db.Column(db.String(15), index=True, nullable=False)
  contact = db.Column(db.String(15), nullable=False, unique=True)
  email = db.Column(db.String(64), nullable=False, unique=True)
  photo = db.Column(db.LargeBinary, nullable=False)
#db.relationship('model_pointed',backref='new_attribute')
#db.relationship() returns list of objects of model_pointed whereas
#object_of_model_pointed.new_attribute returns object of this model
  transactions = db.relationship('Transaction', backref='member')
  def __repr__(self):
    return '<Member: %r %r>'%self.first_name %self.second_name

class Transaction(db.Model):
  __tablename__ = 'transactions'
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date, index=True, nullable=False, default=datetime.now().date())
  time = db.Column(db.Time, nullable=False, default=datetime.now().time())
  member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
  book_ISBN = db.Column(db.String(20), db.ForeignKey('books.ISBN'))
  #transaction type = 'issue' or 'return'
  transaction_type = db.Column(db.String(7),index=True, nullable=False)
  lease = db.Column(db.SmallInteger, nullable=False, default='\0')
  charge = db.Column(db.SmallInteger, nullable=False)
  def __repr__(self):
    return '<Transaction: %r>'% self.id
  
class Stock(db.Model):
  __tablename__='stocks'
  id = db.Column(db.Integer, primary_key=True)
  book_ISBN = db.Column(db.String(20),db.ForeignKey('books.ISBN'),unique=True)
  copies = db.Column(db.SmallInteger, nullable=False)
  lent = db.Column(db.SmallInteger, nullable=False) 
  available = db.Column(db.SmallInteger, nullable=False)
  #book = db.relationship('Book', backref='stock',uselist=False)
  def __repr__(self):
    return '<Stock: %r>'% self.id

