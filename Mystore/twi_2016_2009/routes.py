from flask import Flask, flash, Blueprint, Response, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from Mystore import db
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)
correct_password = 'b8b7ce3756a3abcd'

twi_2016_2009 = Blueprint('twi_2016_2009', __name__)


# Define the Text model
class Text4(db.Model):
    __bind_key__ = 'twi_2016_2009'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])


class AddTextForm4(FlaskForm):
    text_content4 = TextAreaField('Text Content', validators=[DataRequired()])


@twi_2016_2009.route('/twi_2016_2009_db', methods=['GET', 'POST'])
def index4():
    # Password is correct, render the protected page
    form = AddTextForm4()
    texts = Text4.query.all()
    return render_template('database/twi_2016_2009_db.html', texts=texts, form=form)

    # If it's a GET request or the form is invalid, show the password prompt


@twi_2016_2009.route('/add_text4', methods=['POST'])
def add_text4():
    form = AddTextForm4()
    if form.validate_on_submit():
        text_content4 = form.text_content4.data  # Use 'data' instead of 'content'
        if text_content4:
            new_text = Text4(content=text_content4)  # Use 'content' instead of 'data'
            db.session.add(new_text)
            db.session.commit()
            return redirect('/twi_2016_2009_db')
        else:
            flash('Text content cannot be empty.', 'warning')
    else:
        flash('Invalid form submission. Please check your input.', 'danger')

    # If form validation fails, return to the index page with error messages
    return redirect('/twi_2016_2009_db')


@twi_2016_2009.route('/download_text4')
def download_text4():
    text_to_download = Text4.query.first()
    if text_to_download:
        content = text_to_download.content.encode('utf-8')
        filename = 'downloaded_text4.txt'

        db.session.delete(text_to_download)
        db.session.commit()

        return Response(
            content,
            mimetype='text/plain',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Length': len(content)
            }
        )
    else:
        return "No more texts to download."


# Function to check if the reference ID is valid (e.g., in a database)
def is_valid_reference(reference_id):
    return reference_id is None


@twi_2016_2009.route('/success/twi_2016_2009', methods=['GET'])
def download_after_payment():
    reference_id = request.args.get('reference')

    if is_valid_reference(reference_id):
        # Retrieve the text content from the database
        text_to_download = Text4.query.first()

        if text_to_download:
            content = text_to_download.content.encode('utf-8')
            filename = 'downloaded_text4.txt'

            db.session.delete(text_to_download)
            db.session.commit()

            return Response(
                content,
                mimetype='text/plain',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                    'Content-Length': len(content)
                }
            )
        else:
            return "No more texts to download."
