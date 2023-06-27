import json
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tzr_utils import TimeKeeper


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


class Contacts(db.Model):
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

new_contact = dict()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        command = request.form.get('command')

    else:
        contacts = Contacts.query.order_by(Contacts.contact_name).all()
        return render_template('index.html', contacts=contacts)


@app.route('/delete/<contact_name>')
def delete(contact_name):
    contact_to_delete = Contacts.query.get_or_404(contact_name)
    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return f'There was a problem deleting contact {id}<{contact_to_delete.content}>'


@app.route('/add_contact', methods=['POST', 'GET'])
def add_contact():
    global new_contact
    if request.method == 'POST':
        info = (request.form.get('contact_name'), request.form.get('platform'),
                request.form.get('comment'), request.form.get('location'),
                request.form.get('time_zone'))
        print(info)
        zone_name, utc_offset = TimeKeeper.tz_from_input(info[4])
        print(zone_name, utc_offset)
        if zone_name:
            new_contact = Contacts(contact_name=info[0], platform=info[1],
                                   comment=info[2], location=info[3],
                                   zone_name=zone_name)
        elif utc_offset:
            new_contact = Contacts(contact_name=info[0], platform=info[1],
                                   comment=info[2], location=info[3],
                                   utc_offset=utc_offset)
        else:
            new_contact = Contacts(contact_name=info[0], platform=info[1],
                                   comment=info[2], location=info[3])
        db.session.add(new_contact)
        db.session.commit()
        new_contact = ()
        return render_template('index.html')
    return render_template('add_contact.html')


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Contacts.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form.get('content')

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return f'There was an issue updating task {id}'
    else:

        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run()
