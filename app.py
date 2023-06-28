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

    @property
    def contact_time(self):
        if self.zone_name:
            return TimeKeeper.get_current_time(self.zone_name)
        elif self.utc_offset:
            return TimeKeeper.get_current_time(self.utc_offset)


# with app.app_context():
#     db.create_all()

new_contact = dict()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
    else:
        contacts = Contacts.query.order_by(Contacts.contact_name).all()
        tz_dict = TimeKeeper.tz_olson
        print(tz_dict)
        return render_template('index.html', contacts=contacts, tz_dict=tz_dict)


@app.route('/time_operations', methods=['POST', 'GET'])
def time_operations():
    if request.method == 'POST':
        if request.form.get('time_data'):
            data = list(map(int, request.form.get('time_data').split(':')))
            result = TimeKeeper.time_operation_0(data)
            return "In {} hours {} minutes it'll be: {}".format(data[0], data[1], result)
        elif request.form.get('time_data_1'):
            data = request.form.get('time_data_1')
            print(data)
            result = TimeKeeper().get_current_time(data)
            return f'current time in {data} time zone: {result}'
        elif request.form.get('time_data_2'):  # format "EST;00:00"
            data = request.form.get('time_data_2').split(';')
            print(data)
            result = TimeKeeper.time_operation_2(data, 'y')
            return result
        elif request.form.get('time_data_3'):  # format "EST;00:00"
            data = request.form.get('time_data_3').split(';')
            print(data)
            result = TimeKeeper.time_operation_2(data, 'n')
            return result

    return render_template('time_operations.html')


@app.route('/delete/<contact_name>')
def delete(contact_name):
    contact_to_delete = Contacts.query.get_or_404(contact_name)
    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return f'There was a problem deleting contact <{contact_to_delete.content}>'


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


@app.route('/update/<contact_name>', methods=['POST', 'GET'])
def update(contact_name):
    contact = Contacts.query.get_or_404(contact_name)
    if request.method == 'POST':
        info = (request.form.get('contact_name'), request.form.get('platform'),
                request.form.get('comment'), request.form.get('location'),
                request.form.get('zone_name'), request.form.get('utc_offset'))
        contact.contact_name = info[0]
        contact.platform = info[1]
        contact.comment = info[2]
        contact.location = info[3]
        contact.zone_name = info[4]
        contact.utc_offset = info[5]
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return f'There was an issue updating contact {contact_name}'
    else:
        return render_template('update.html', contact=contact)


if __name__ == '__main__':
    app.run()
