from db_config import db, app
from home import NameForm
from flask import render_template, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
@app.route('/', methods=['GET', 'POST'])
def hello():
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
    return redirect(url_for('hello'))
  return render_template('index.html', form = form, name = session.get('name'))

if __name__ =='__main__':
#create app_context()
	app.run()
