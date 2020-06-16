from flask import Flask, request, render_template, url_for, session,redirect
from flask_sqlalchemy import SQLAlchemy
import datetime







app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.sqlite3'
app.config['SECRET_KEY'] = "PES84TEN"

db = SQLAlchemy(app)


class Tasks(db.Model):
   id = db.Column( db.Integer, primary_key = True)
   content = db.Column(db.String(100))
   date_created = db.Column(db.DateTime(), default=datetime.datetime.now() )  
  

def __init__(self, content):

   self.content = content
   
   




@app.route('/', methods=['POST', 'GET'])
def index():
 if request.method == 'POST':
  task_content = request.form['content']
  new_task = Tasks(content=task_content)

  try:
   db.session.add(new_task)
   db.session.commit()
   return redirect('/')
  except:
   return 'There was an issue adding your task'

 else:
  tasks = Tasks.query.order_by(Tasks.id).all()
  return render_template('index.html', tasks=tasks)





@app.route('/delete/<int:id>')
def delete(id):
 task_to_delete = Tasks.query.get_or_404(id)

 try:
  db.session.delete(task_to_delete)
  db.session.commit()
  return redirect('/')
 except:
  return 'There was a problem deleting that task'




@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
 task = Tasks.query.get_or_404(id)

 if request.method == 'POST':
  task.content = request.form['content']

  try:
   db.session.commit()
   return redirect('/')
  except:
   return 'There was an issue updating your task'

 else:
  return render_template('update.html', task=task)




# @app.route('/search/<searchbox>', methods=["POST","GET"])
# def search(searchbox):

#  if request.method == 'GET':
#   try:

#    searchterm = form.args('searchbox')
#    task_to_search = Tasks.query.get_or_404(content=searchbox).all()
#    return render_template('search.html', task=task_to_search)       

#   except:
#    return 'There was a problem with the search'
#  return render_template('search.html', task=task_to_search)
   


  
   
if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
