from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


class Todo(db.Model):
    contact_name = db.Column(db.String(255), primary_key=True)
    platform = db.Column(db.String(255), nullable=False)
    comment = db.Column(db.String(255))
    location = db.Column(db.String(255))
    zone_name = db.Column(db.String(255))
    utc_offset = db.Column(db.Float)

    def __repr__(self):
        return '<Contact {} from {}>'.format(self.contact_name, self.location)


# with app.app_context():
#     db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('content')
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return f'There was an issue adding new task <{task_content}>'
    else:
        # tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html')

#
# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)
#
#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return f'There was a problem deleting task {id}<{task_to_delete.content}>'
#
#

@app.route('/add_contact')
def add_contact():
    return render_template('add_contact.html')
# @app.route('/update/<int:id>', methods=['POST', 'GET'])
# def update(id):
#     task = Todo.query.get_or_404(id)
#     if request.method == 'POST':
#         task.content = request.form.get('content')
#
#         try:
#             db.session.commit()
#             return redirect('/')
#         except Exception as e:
#             print(e)
#             return f'There was an issue updating task {id}'
#     else:
#
#         return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run()
