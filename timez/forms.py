from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, ValidationError, \
    TextAreaField, FloatField
from timez.models import Contact


class AddContactForm(FlaskForm):
    contact_name = StringField('Contact name', [validators.DataRequired(),
                               validators.Length(min=2, max=50)])
    platform = StringField('Platform', [validators.DataRequired()])
    comment = TextAreaField('Comment')
    location = StringField('Location')
    zone_name = StringField('Zone_name')
    utc_offset = FloatField('Utc_offset', [validators.Optional()])
    submit = SubmitField('Submit')

    def validate_contact_name(self, contact_name):
        contact = Contact.query.filter_by(contact_name=contact_name.data).first()
        if contact:
            raise ValidationError('That contact_name is taken. Please choose a different one.')


