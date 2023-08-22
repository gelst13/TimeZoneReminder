from flask import flash, redirect, render_template, request, url_for, abort
from timez import app, db
from timez.forms import AddContactForm
from timez.models import Contact
from timez.tzr_utils import TimeKeeper


@app.route('/', methods=['POST', 'GET'])
def index():
    contacts = Contact.query.order_by(Contact.contact_name).all()
    return render_template('index.html', contacts=contacts)


@app.route('/time_operations', methods=['POST', 'GET'])
def time_operations():
    if request.method == 'POST':
        if request.form.get('time_data_1'):
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


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddContactForm()
    if form.validate_on_submit():
        contact = Contact(contact_name=form.contact_name.data, 
                          platform=form.platform.data, 
                          comment=form.comment.data, 
                          location=form.location.data, 
                          zone_name=form.zone_name.data, 
                          utc_offset=form.utc_offset.data)
        db.session.add(contact)
        db.session.commit()
        flash(f"New contact has been added!", 'success')
        return redirect(url_for('index'))
    return render_template('add.html', title='Add new contact', form=form)


@app.route('/delete/<contact_name>')
def delete(contact_name):
    contact_to_delete = Contact.query.get_or_404(contact_name)
    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return f'There was a problem deleting contact <{contact_to_delete.content}>'

#
# @app.route('/add_contact', methods=['POST', 'GET'])
# def add_contact():
#     global new_contact
#     if request.method == 'POST':
#         info = (request.form.get('contact_name'), request.form.get('platform'),
#                 request.form.get('comment'), request.form.get('location'),
#                 request.form.get('time_zone'))
#         print(info)
#         zone_name, utc_offset = TimeKeeper.tz_from_input(info[4])
#         print(zone_name, utc_offset)
#         if zone_name:
#             new_contact = Contact(contact_name=info[0], platform=info[1],
#                                   comment=info[2], location=info[3],
#                                   zone_name=zone_name)
#         elif utc_offset:
#             new_contact = Contact(contact_name=info[0], platform=info[1],
#                                   comment=info[2], location=info[3],
#                                   utc_offset=utc_offset)
#         else:
#             new_contact = Contact(contact_name=info[0], platform=info[1],
#                                   comment=info[2], location=info[3])
#         db.session.add(new_contact)
#         db.session.commit()
#         new_contact = ()
#         return redirect(url_for('index'))
#     return render_template('add_contact.html')


@app.route('/update/<int:post_id>', methods=['POST', 'GET'])
def update(id):
    contact = Contact.query.get_or_404(id)
    form = AddContactForm()
    if form.validate_on_submit():
        contact.contact_name = form.contact_name.data
        contact.platform = form.platform.data
        contact.comment = form.comment.data
        contact.location = form.location.data
        contact.zone_name = form.zone_name.data
        if form.utc_offset.data == '':
            contact.utc_offset = None
        else:
            contact.utc_offset = form.utc_offset.data
        try:
            db.session.commit()
            flash('Contact has been updated!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            return f'There was an issue updating contact {contact_name}'
    elif request.method == 'GET':
        contact.contact_name = form.contact_name.data
        contact.platform = form.platform.data
        contact.comment = form.comment.data
        contact.location = form.location.data
        contact.zone_name = form.zone_name.data
        return render_template('update.html', contact=contact)
