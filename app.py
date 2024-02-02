from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)
    


    def __repr__(self) -> str:
        return f"{self.srno} - {self.title}"

@app.route('/contact')
def contact():
    return 'You can contact me on 8668862550'

@app.route('/delete/<int:srno>')
def delete(srno):
    todo_del = Todo.query.filter_by(srno=srno).first()
    db.session.delete(todo_del)
    db.session.commit()
    return redirect('/')



@app.route('/update/<int:srno>', methods = ["GET","POST"])
def update(srno):
    if request.method == 'POST':
        title=request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(srno=srno).first()
        todo.title = title 
        todo.desc = desc 
        db.session.add(todo)
        db.session.commit()
        return redirect('/')



    todo = Todo.query.filter_by(srno=srno).first()
    return render_template('update.html', todo = todo)


    


@app.route('/', methods = ["GET","POST"])
def hello_world():
    if request.method == "POST":
        title=request.form['title']
        desc = request.form['desc']
        
        todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodos = Todo.query.all()
    return render_template('index.html',allTodos = allTodos)

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#         app.run(debug=True)


# git push -u origin main