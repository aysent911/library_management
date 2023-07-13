from db_config import db, app, Book, Member, Transaction, Stock, upload_folder
from form_classes import NameForm, NewBookForm, NewMemberForm
from flask import render_template, session, url_for, redirect, flash, request
from flask_bootstrap import Bootstrap
from datetime import datetime
from base64 import b64encode
import base64
from io import BytesIO
import os
@app.route('/', methods=['GET', 'POST'])
def index():
  #db.drop_all()
  #db.create_all()
  form = NameForm()
  if form.validate_on_submit():
    #POST/Redirect/GET request
    #With redirect, form data will be lost as soon as request ends
    #hence save data to session
    if (session.get('name') is not None and session.get('name') != form.name.data):
      flash('Looks like {} was here!'.format(session.get('name')))
    session['name'] = form.name.data
    form.name.data=''   
    return redirect(url_for('index'))
  return render_template('index.html', form = form, name = session.get('name'))

@app.route('/books', methods=['GET', 'POST'])
def books():
  #db.drop_all()
  #db.create_all()
  form = NameForm()
  new_book_form = NewBookForm()
  menu="all_books"
  if (request.form.get('add_book_menu')=="selected" or 
   request.form.get('clear_book_button')=="selected"):
      menu="add_book_menu"      
      flash("Welcome. To add a new book, complete the new book form below")
      new_book_form.ISBN.data="";
      new_book_form.title.data="";
      new_book_form.author.data="";
      new_book_form.edition.data="New";
      new_book_form.publisher.data="";
      new_book_form.subject.data="Law";
      return render_template('books.html', form = new_book_form, name = session.get('name'), menu=menu)
      
  if (request.form.get('add_book_button')=="selected"):
      menu="add_book_menu"
      try:
       new_book = Book(
	ISBN = new_book_form.ISBN.data,
	title = new_book_form.title.data,
	author = new_book_form.author.data,
	edition = new_book_form.edition.data,
	publisher = new_book_form.publisher.data,
	year_of_pub = new_book_form.year_of_publication.data,
	subject = new_book_form.subject.data)
       new_stock = Stock(
	book_ISBN = new_book_form.ISBN.data,
	copies = new_book_form.copies.data,
	lent = 0,
	available = new_book_form.copies.data)
       db.session.add_all([new_book, new_stock])
       db.session.commit()
       flash("{} sucessfully added".format(new_book_form.title.data))
      except Exception as e:
       db.session.rollback()
       flash("Oops! An exception occurred.{} not added.Try again later".format(
        new_book_form.title.data))
       print('AddBookException:'+e)
      finally:
       db.session.close()
       return render_template('books.html', form = new_book_form, name = session.get('name'), menu=menu)
  
  if(request.form.get('exit_button')=='selected'):
    return redirect(url_for('books'))
  
  return render_template('books.html', form = form, name = session.get('name'), menu=menu)

@app.route('/members', methods=['GET', 'POST'])
def members():
  menu = 'all_members'
  new_member_form = NewMemberForm()
  if (request.form.get('add_member_menu') == 'selected'):
    menu='add_member_menu'
    flash("Welcome. To add a new member, complete the new member form below")
    return render_template('members.html', form = new_member_form, menu=menu)
  if (request.form.get('add_member_button') == 'selected'):
    menu='add_member_menu'
    #print(new_member_form.photo.data)
    if "image_file" not in request.files:
      print("no image found")
      print(request.files)
    else:
      print("image found")
    #file1= request.files['image_file']
    print(upload_folder)
    uploaded_image = request.form['image_file']
    if  isinstance(uploaded_image, str):
      uploaded_image = bytes(uploaded_image, 'utf-8')
    elif uploaded_image is not None:
      uploaded_image = bytes(uploaded_image)
    try:
      new_member = Member(
       first_name = new_member_form.first_name.data,
       second_name = new_member_form.second_name.data,
       contact = new_member_form.contact.data,
       email = new_member_form.email.data,
       photo = uploaded_image)
      db.session.add(new_member)
      db.session.commit()
      flash("{} sucessfully admitted".format(new_member_form.first_name.data))
    except Exception as e:
      db.session.rollback()
      flash("Oops! An exception occurred.{} not added.Try again later".format(
      new_member_form.first_name.data))
      print('AddMemberException:'+e)
    finally:
      db.session.close()
    return render_template('members.html', form = new_member_form, name = session.get('name'), menu=menu)
    #file1=request.files['clear_member_button']
    #print(file1)
    #file2=file1.read()
    #print(file2)
  
  return render_template('members.html', form = new_member_form, menu=menu)

if __name__ =='__main__':
#create app_context()
	app.run()
