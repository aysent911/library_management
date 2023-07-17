#import flask-wtf extension classes
#flask-wtf makes working with web forms easier
from flask_wtf.form import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FileField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange
from datetime import datetime
from db_config import db, app, Book, Member, Transaction, Stock, upload_folder
class NameForm(FlaskForm):
  name = StringField("What is your name?", validators=[])
  submit = SubmitField("<i class=\"fas fa-filter\" ></i>")
 
class NewBookForm(FlaskForm):
  ISBN = StringField("ISBN: ", validators=[DataRequired(),Length(5,20,
   "Maximum allowed is 20 characters!")])
  title = StringField("Book Title: ", validators=[DataRequired(),Length(5,100,
   "Maximum allowed is 100 characters!")])
  author = StringField("Book Author(s): ", validators=[DataRequired(),
   Length(5,100,"Maximum allowed is 100 characters!")])
  edition = SelectField("Book Edition:", choices=[(0,"New"),(1,"First"),
   (2,"Second"),(3,"Third"),(4,"Fourth"),(5,"Fifth"),(6,"Sixth"),(7,"Seventh"),
   (8,"Eighth"),(9,"Ninth"),(10,"Tenth"),(11,"Eleventh"),(12,"Twelfth"),
   (13,"Other")])
  publisher = StringField("Publisher:", validators=[Length(5,20,
   "Maximum allowed is 20 characters!")])
  year_of_publication = IntegerField("Year of Publication: ",
   validators=[DataRequired(),NumberRange(1800,2023,
    "Input out of range 1800 - now!")])
  subject = SelectField("Subject:",choices=[(1,"Law"),(2,"Religion"),
   (3,"Business"),(4,"Biology"),(5,"Geography"),(6,"Physics"),
   (7, "Mathematics"), (8, "Engineering"),(9,"Language"),
   (10,"Information Technology")])
  copies = IntegerField("Copies: ", validators=[DataRequired()])
  add = SubmitField("Add")
  clear = SubmitField("Clear")

class NewMemberForm(FlaskForm):
  first_name = StringField("First Name:", validators=[])
  second_name = StringField("Second Name:", validators=[])
  contact = StringField("Phone:", validators=[])
  email = StringField("email:", validators=[])
  photo = FileField("Member Photo:", validators=[])

class NewTransactionForm(FlaskForm):
  member_id = SelectField("Member ID:", coerce = int)
  book_ISBN = SelectField("Book ISBN:", coerce = str)
  transaction_type = SelectField("Transaction Type:", choices=[("issue","Issue"),("return","Return")])
  lease = SelectField("Lease Period(weeks):", choices=[(1,1),(2,2),(3,3),(4,4)])
  charge = IntegerField("Charge (Kshs):", validators=[])
  def __init__(self, *args, **kwargs):
    super(NewTransactionForm,self).__init__(*args,**kwargs)
    i=0
    self.book_ISBN.choices = [(book.ISBN, book.ISBN)
     for book in Book.query.order_by(Book.ISBN).all()]
    self.member_id.choices = [(member.id, member.id)
     for member in Member.query.order_by(Member.id).all()]
  
  
