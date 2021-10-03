from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/Python Projects/ToDo List/todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id_x = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    items = Todo.query.all()
    pending = [x for x in items if not x.complete]
    done = [x for x in items if x.complete]
    print(items)
    return render_template('index.html', pending=pending, done=done)

@app.route('/add', methods=['POST'])
def add():
    todo = Todo(item = request.form.get('item'), complete = False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/done', methods=['POST'])
def done():
    values = list(request.form.keys())
    print(values)
    for v in values:
        check = Todo.query.filter_by(id_x=int(v)).first()
        check.complete = True
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)