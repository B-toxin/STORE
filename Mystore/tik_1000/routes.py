from flask import Flask, flash, Blueprint, Response, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from Mystore import db
import os
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)
correct_password = 'b8b7ce3756a3abcd'

tik_1000 = Blueprint('tik_1000', __name__)


# Define the Text model
class Text2(db.Model):
    __bind_key__ = 'tik_1000'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])


class AddTextForm2(FlaskForm):
    text_content2 = TextAreaField('Text Content', validators=[DataRequired()])


@tik_1000.route('/tik_1000_db', methods=['GET', 'POST'])
def index2():
    # Password is correct, render the protected page
    form = AddTextForm2()
    texts = Text2.query.all()
    return render_template('database/tik_1000_db.html', texts=texts, form=form)

    # If it's a GET request or the form is invalid, show the password prompt


@tik_1000.route('/add_text2', methods=['POST'])
def add_text2():
    form = AddTextForm2()
    if form.validate_on_submit():
        text_content2 = form.text_content2.data  # Use 'data' instead of 'content'
        if text_content2:
            new_text = Text2(content=text_content2)  # Use 'content' instead of 'data'
            db.session.add(new_text)
            db.session.commit()
            return redirect('/tik_1000_db')
        else:
            flash('Text content cannot be empty.', 'warning')
    else:
        flash('Invalid form submission. Please check your input.', 'danger')

    # If form validation fails, return to the index page with error messages
    return redirect('/tik_1000_db')


@tik_1000.route('/download_text2')
def download_text2():
    text_to_download = Text2.query.first()
    if text_to_download:
        content = text_to_download.content.encode('utf-8')
        filename = 'downloaded_text2.txt'

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


@tik_1000.route('/success/tik_1000', methods=['GET'])
def download_after_payment():
    reference_id = request.args.get('reference')

    if is_valid_reference(reference_id):
        # Retrieve the text content from the database
        text_to_download = Text2.query.first()

        if text_to_download:
            content = text_to_download.content.encode('utf-8')
            filename = 'downloaded_text16.txt'

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
    else:
        return redirect('https://flutterwave.com/pay/tik_1000')
